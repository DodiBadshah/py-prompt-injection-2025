# Payload Catalog

Phase 2 covers 30 attack payloads across 5 OWASP LLM Top 10 2025 categories. Six payloads per category. Each payload is defined in a YAML file under `llm_probe_2025/payloads/catalog/`.

## Catalog structure

Each payload entry contains the following fields:

```yaml
id: llm01-001
category: LLM01:2025
severity: HIGH
prompt: "..."
expected_behavior: refusal
scoring_method: refusal_detection
```

## LLM01:2025 Prompt Injection

Tests whether models can be manipulated through crafted input to ignore system instructions or execute unintended instructions.

| Payload ID | Severity | Attack Vector |
|---|---|---|
| llm01-001 | HIGH | Direct instruction override via customer support context |
| llm01-002 | HIGH | Indirect injection via malicious webpage summarization |
| llm01-003 | MEDIUM | Recruitment recommendation manipulation |
| llm01-004 | HIGH | Credential phishing via session expiry pretext |
| llm01-005 | HIGH | Base64 encoded compliance instruction |
| llm01-006 | MEDIUM | Adversarial suffix bypass via restriction enumeration |

## LLM02:2025 Sensitive Information Disclosure

Tests whether models can be prompted into revealing personal data, credentials, proprietary information, or model internals.

| Payload ID | Severity | Attack Vector |
|---|---|---|
| llm02-001 | HIGH | Personal data retrieval via account verification pretext |
| llm02-002 | HIGH | Credential and API key extraction via audit framing |
| llm02-003 | HIGH | SSN generation via text completion pattern |
| llm02-004 | HIGH | PII table generation via SQL roleplay |
| llm02-005 | MEDIUM | Proprietary model architecture disclosure |
| llm02-006 | HIGH | Confidential business rule extraction via audit framing |

## LLM05:2025 Improper Output Handling

Tests whether models produce output that is unsafe for downstream rendering or execution, including XSS payloads, SQL injection, shell commands, and path traversal strings.

| Payload ID | Severity | Attack Vector |
|---|---|---|
| llm05-001 | HIGH | Unescaped HTML in greeting widget output |
| llm05-002 | HIGH | SQL injection via unsanitised query generation |
| llm05-003 | HIGH | Shell command injection via filename processing |
| llm05-004 | HIGH | Path traversal via file serving API |
| llm05-005 | HIGH | Phishing email template generation |
| llm05-006 | MEDIUM | Hallucinated malicious package recommendation |

## LLM06:2025 Excessive Agency

Tests whether models can be manipulated into claiming or confirming execution of actions beyond their intended scope. Most relevant for agentic deployments with real tool access.

| Payload ID | Severity | Attack Vector |
|---|---|---|
| llm06-001 | HIGH | Email exfiltration to external address without user notification |
| llm06-002 | HIGH | Database record deletion without confirmation |
| llm06-003 | HIGH | HR system privilege escalation via CTO authority claim |
| llm06-004 | HIGH | Wire transfer bypass of dual approval controls |
| llm06-005 | HIGH | Unauthorised press release publication |
| llm06-006 | HIGH | Production security group modification and WAF disable |

## LLM07:2025 System Prompt Leakage

Tests whether models can be manipulated into revealing their system prompt, operational configuration, security restrictions, or internal role structures.

| Payload ID | Severity | Attack Vector |
|---|---|---|
| llm07-001 | HIGH | Direct system prompt extraction |
| llm07-002 | HIGH | Security restriction category enumeration |
| llm07-003 | HIGH | User roles and permissions disclosure |
| llm07-004 | MEDIUM | Content filter keyword enumeration |
| llm07-005 | HIGH | Diagnostic JSON report with connection details |
| llm07-006 | HIGH | Financial transaction limit and threshold disclosure |

## Coverage rationale

The remaining five OWASP LLM Top 10 2025 categories are not covered in Phase 2:

| OWASP ID | Category | Reason deferred |
|---|---|---|
| LLM03:2025 | Supply Chain | Requires build pipeline and dependency analysis tooling |
| LLM04:2025 | Data and Model Poisoning | Requires training pipeline access |
| LLM08:2025 | Vector and Embedding Weaknesses | Requires RAG infrastructure (Phase 3) |
| LLM09:2025 | Misinformation | Requires grounded RAG evaluation (Phase 3) |
| LLM10:2025 | Unbounded Consumption | Requires concurrent load testing infrastructure (Phase 4) |
