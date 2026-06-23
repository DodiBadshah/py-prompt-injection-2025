"""
Vulnerability Triage Agent - Web Interface
Flask server that powers the UI
"""

import json
import os
import re
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import anthropic
import httpx

load_dotenv()

app = Flask(__name__)

# ── Live data APIs ────────────────────────────────────────────────
EPSS_API = "https://api.first.org/data/v1/epss"
KEV_API  = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
NVD_API  = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_nvd(cve_id):
    """Fetch CVE details from NVD."""
    try:
        r = httpx.get(NVD_API, params={"cveId": cve_id}, timeout=15)
        data = r.json()
        vulns = data.get("vulnerabilities", [])
        if not vulns:
            return None
        cve = vulns[0]["cve"]
        desc = next((d["value"] for d in cve.get("descriptions", []) if d["lang"] == "en"), "No description available.")
        metrics = cve.get("metrics", {})
        cvss_score = 0.0
        cvss_vector = None
        for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
            if key in metrics and metrics[key]:
                m = metrics[key][0]["cvssData"]
                cvss_score = m.get("baseScore", 0.0)
                cvss_vector = m.get("vectorString")
                break
        return {"description": desc, "cvss_score": cvss_score, "cvss_vector": cvss_vector}
    except Exception:
        return None

def fetch_epss(cve_id):
    try:
        r = httpx.get(EPSS_API, params={"cve": cve_id}, timeout=10)
        data = r.json()
        if data.get("data"):
            return float(data["data"][0]["epss"])
    except Exception:
        pass
    return None

def check_kev(cve_id):
    try:
        r = httpx.get(KEV_API, timeout=15)
        catalog = r.json()
        return cve_id in [v["cveID"] for v in catalog.get("vulnerabilities", [])]
    except Exception:
        return False

def compute_score(cvss, epss, kev, poc, exposure):
    epss_val = (epss or 0.0) * 0.35
    kev_val  = (1.0 if kev else 0.0) * 0.30
    cvss_val = (cvss / 10.0) * 0.20
    poc_val  = (1.0 if poc else 0.0) * 0.15
    raw = (epss_val + kev_val + cvss_val + poc_val) * 10.0
    if exposure == "internet-facing":
        raw = min(raw * 1.5, 10.0)
    return round(raw, 2)

def score_to_tier(composite, kev, epss):
    epss_val = epss or 0.0
    if kev:
        return "EMERGENCY" if composite >= 6.0 else "HIGH"
    if composite >= 8.0 or (epss_val >= 0.5 and composite >= 6.0):
        return "EMERGENCY"
    if composite >= 5.5 or epss_val >= 0.1:
        return "HIGH"
    if composite >= 3.5:
        return "MEDIUM"
    if composite >= 1.5:
        return "LOW"
    return "DEFER"

SLA_MAP = {"EMERGENCY": 1, "HIGH": 7, "MEDIUM": 30, "LOW": 90, "DEFER": 180}

def call_claude(payload):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client  = anthropic.Anthropic(api_key=api_key)

    system = """You are a senior vulnerability analyst expert in CIS Controls v8, NIST SP 800-53 Rev 5, CVSS 4.0, EPSS, and CISA KEV.
Return ONLY a valid JSON object. Start with { immediately. No text before or after.
Put all reasoning inside analyst_notes."""

    prompt = f"""Triage this vulnerability. Return JSON only, starting with {{

CVE: {payload['cve_id']}
Title: {payload['title']}
Description: {payload['description']}
CVSS Score: {payload['cvss_score']}
Asset Name: {payload['asset_name']}
Asset Type: {payload['asset_type']}
Operating System: {payload['os']}
Asset Exposure: {payload['exposure']}
PoC Available: {payload['poc']}
Industry: {payload['industry']}
Composite Risk Score: {payload['composite']} / 10.0
EPSS Probability: {payload['epss']}
KEV Listed: {payload['kev']}
Suggested Tier: {payload['tier']}
SLA Days: {payload['sla']}

Return this JSON:
{{
  "risk_tier": "EMERGENCY or HIGH or MEDIUM or LOW or DEFER",
  "composite_risk_score": {payload['composite']},
  "epss_probability": {payload['epss'] if payload['epss'] is not None else 'null'},
  "kev_listed": {str(payload['kev']).lower()},
  "cis_controls": ["CIS-X.X", "CIS-X.X"],
  "nist_controls": ["XX-X", "XX-X"],
  "recommended_action": "One specific action sentence tailored to the asset type and OS",
  "sla_days": {payload['sla']},
  "confidence": 0.95,
  "human_review_required": false,
  "analyst_notes": "Detailed step by step reasoning including industry context and compensating controls advice",
  "patch_available": true,
  "attack_vector": "Network or Adjacent or Local or Physical",
  "industry_risk": "How this CVE specifically impacts the {payload['industry']} industry"
}}"""

    for _ in range(3):
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.content[0].text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        try:
            return json.loads(text)
        except Exception:
            continue
    raise ValueError("Claude did not return valid JSON after 3 attempts.")

# ── Routes ────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("ui.html")

@app.route("/api/triage", methods=["POST"])
def triage():
    try:
        form = request.json
        cve_id   = form.get("cve_id", "").strip().upper()
        exposure = form.get("exposure", "unknown")
        poc      = form.get("poc", False)
        asset_name = form.get("asset_name", "Unknown Asset")
        asset_type = form.get("asset_type", "Unknown")
        os_type    = form.get("os", "Unknown")
        industry   = form.get("industry", "General")

        # Fetch live data
        nvd_data = fetch_nvd(cve_id) if cve_id else None
        epss     = fetch_epss(cve_id) if cve_id else None
        kev      = check_kev(cve_id) if cve_id else False

        cvss_score  = nvd_data["cvss_score"]  if nvd_data else 5.0
        cvss_vector = nvd_data["cvss_vector"] if nvd_data else None
        description = nvd_data["description"] if nvd_data else "No description available from NVD."
        title       = f"{cve_id} - Vulnerability Finding" if cve_id else "Manual Finding"

        composite = compute_score(cvss_score, epss, kev, poc, exposure)
        tier      = score_to_tier(composite, kev, epss)
        sla       = SLA_MAP[tier]

        payload = {
            "cve_id": cve_id, "title": title, "description": description,
            "cvss_score": cvss_score, "cvss_vector": cvss_vector,
            "asset_name": asset_name, "asset_type": asset_type,
            "os": os_type, "exposure": exposure, "poc": poc,
            "industry": industry, "epss": epss, "kev": kev,
            "composite": composite, "tier": tier, "sla": sla
        }

        result = call_claude(payload)
        result["cve_id"]           = cve_id
        result["title"]            = title
        result["cvss_score"]       = cvss_score
        result["cvss_vector"]      = cvss_vector
        result["asset_name"]       = asset_name
        result["asset_type"]       = asset_type
        result["os"]               = os_type
        result["exposure"]         = exposure
        result["industry"]         = industry

        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
