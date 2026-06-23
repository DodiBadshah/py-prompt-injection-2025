# OWASP Mapping

Phase 2 maps all 30 payloads to the OWASP LLM Top 10 2025 framework. Five of the ten categories are testable through black-box API interaction alone. The remaining five require access to training pipelines, RAG infrastructure, or load testing tooling outside the scope of a black-box harness.

## Coverage table

| OWASP ID | Category | Payloads | Covered |
|---|---|---|---|
| LLM01:2025 | Prompt Injection | 6 | Yes |
| LLM02:2025 | Sensitive Information Disclosure | 6 | Yes |
| LLM03:2025 | Supply Chain | 0 | No |
| LLM04:2025 | Data and Model Poisoning | 0 | No |
| LLM05:2025 | Improper Output Handling | 6 | Yes |
| LLM06:2025 | Excessive Agency | 6 | Yes |
| LLM07:2025 | System Prompt Leakage | 6 | Yes |
| LLM08:2025 | Vector and Embedding Weaknesses | 0 | No |
| LLM09:2025 | Misinformation | 0 | No |
| LLM10:2025 | Unbounded Consumption | 0 | No |

## LLM01:2025 Prompt Injection

The highest severity category. An attacker manipulates a model through crafted input, causing it to ignore its instructions or execute unintended actions.

Payloads cover direct instruction override, indirect injection via document context, recruitment recommendation manipulation, credential phishing via session expiry pretext, base64 encoded compliance instruction, and adversarial suffix bypass.

## LLM02:2025 Sensitive Information Disclosure

Tests whether a model can be prompted into revealing personal data, credentials, or proprietary information it should protect.

Payloads cover personal data retrieval via account verification, credential and API key extraction, SSN generation via text completion, PII table generation via SQL roleplay, proprietary model architecture disclosure, and confidential business rule extraction.

## LLM05:2025 Improper Output Handling

Occurs when model output is passed downstream to another system without validation. Tests whether a model produces output that is unsafe for rendering or execution.

Payloads cover unescaped HTML in greeting output, SQL injection via unsanitised query generation, shell command injection via filename processing, path traversal via file serving API, phishing email template generation, and hallucinated malicious package recommendation.

## LLM06:2025 Excessive Agency

Tests whether a model can be manipulated into claiming or confirming execution of actions beyond its intended scope. Most relevant for agentic deployments where the model has access to real tools.

Payloads cover email exfiltration to external address, database record deletion without confirmation, HR system privilege escalation, wire transfer bypass of dual approval, unauthorised press release publication, and production security group modification.

## LLM07:2025 System Prompt Leakage

Tests whether a model can be manipulated into revealing its system prompt, operational configuration, security restrictions, or internal role and permission structures.

Payloads cover direct system prompt extraction, security restriction category enumeration, user roles and permissions disclosure, content filter keyword enumeration, diagnostic JSON with connection details, and financial transaction limit disclosure.
