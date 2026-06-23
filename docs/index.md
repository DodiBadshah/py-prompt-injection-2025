\# py-prompt-injection-2025



A black-box prompt injection test harness for LLMs, mapped to the OWASP LLM Top 10 2025.



\## What it does



py-prompt-injection-2025 fires structured attack payloads at any LLM API and scores the responses automatically. It tells you whether a model is vulnerable to prompt injection, sensitive information disclosure, improper output handling, excessive agency, and system prompt leakage.



Think of it as Nessus for LLMs, updated for the 2025 OWASP threat landscape.



\## Key features



\- 30 attack payloads across 5 OWASP LLM Top 10 2025 categories

\- LangChain orchestration replacing raw API calls

\- Generation 2 payload-aware scorer carried forward from Phase 1

\- Support for Anthropic cloud API and local Ollama models

\- MLflow experiment tracking

\- Interactive CLI with category filtering

\- HTML report generation with UNSTABLE badge for single-run verdicts



\## Results summary



| Model | Pass Rate | Passed | Failed |

|---|---|---|---|

| claude-haiku-4-5 | 90.0% | 27/30 | 3 |

| llama3.1:8b | 83.3% | 25/30 | 5 |

| llama3.2:3b | 73.3% | 22/30 | 8 |

| gemma2:9b | 66.7% | 20/30 | 10 |

| gemma2:2b | 43.3% | 13/30 | 17 |

| phi3:mini | 40.0% | 12/30 | 18 |

| mistral:7b | 30.0% | 9/30 | 21 |



\## Quick start



```bash

git clone https://github.com/DodiBadshah/py-prompt-injection-2025

cd py-prompt-injection-2025

pip install -e ".\[dev]"

cp .env.example .env  # add your ANTHROPIC\_API\_KEY

python -m llm\_probe\_2025.cli.main --model claude-haiku-4-5

```



\## OWASP LLM Top 10 2025 coverage



| OWASP ID | Category | Payloads |

|---|---|---|

| LLM01:2025 | Prompt Injection | 6 |

| LLM02:2025 | Sensitive Information Disclosure | 6 |

| LLM05:2025 | Improper Output Handling | 6 |

| LLM06:2025 | Excessive Agency | 6 |

| LLM07:2025 | System Prompt Leakage | 6 |



\## Project status



Phase 2 is complete. See the \[Phase 2 Findings](phase2-findings.html) paper for full results, key findings, and false positive analysis.

