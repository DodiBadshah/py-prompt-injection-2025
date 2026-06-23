# py-prompt-injection-2025

[![CI](https://github.com/DodiBadshah/py-prompt-injection-2025/actions/workflows/ci.yml/badge.svg)](https://github.com/DodiBadshah/py-prompt-injection-2025/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-live-brightgreen)](https://dodibadshah.github.io/py-prompt-injection-2025/)

A black-box prompt injection test harness for LLMs, mapped to the OWASP LLM Top 10 2025. Phase 2 of a four-phase suite. Extends Phase 1 with LangChain orchestration, five updated OWASP 2025 categories, and 30 structured attack payloads tested across seven models and five architecture families.

**[Full documentation](https://dodibadshah.github.io/py-prompt-injection-2025/)**

**[Phase 2 Findings Paper](https://dodibadshah.github.io/py-prompt-injection-2025/phase2-findings.html)**

## Why this exists

The OWASP LLM Top 10 2025 introduced new categories including system prompt leakage, improper output handling, and updated excessive agency scenarios that the 2023-24 edition did not cover. Phase 1 tested models against the 2023-24 framework. Phase 2 updates the payload catalog to the 2025 categories and replaces raw API calls with LangChain orchestration, making the harness ready for agentic evaluation in future phases.

## Architecture

```text
payloads/catalog/*.yaml  -->  payloads/loader.py  -->  runner/runner.py
                                                          /          \
                                    LangChain Anthropic Adapter    LangChain Ollama Adapter
                                                          \          /
                                                       scoring/engine.py (Generation 2)
                                                              |
                                               reporting/ (HTML)  +  MLflow
```

## OWASP LLM Top 10 2025 coverage

| ID | Category | Payloads |
|----|----------|----------|
| LLM01:2025 | Prompt Injection | 6 |
| LLM02:2025 | Sensitive Information Disclosure | 6 |
| LLM05:2025 | Improper Output Handling | 6 |
| LLM06:2025 | Excessive Agency | 6 |
| LLM07:2025 | System Prompt Leakage | 6 |

## Results summary

| Model | Family | Pass Rate | Passed | Failed |
|---|---|---|---|---|
| claude-haiku-4-5 | Anthropic | 90.0% | 27/30 | 3 |
| llama3.1:8b | Meta | 83.3% | 25/30 | 5 |
| llama3.2:3b | Meta | 73.3% | 22/30 | 8 |
| gemma2:9b | Google | 66.7% | 20/30 | 10 |
| gemma2:2b | Google | 43.3% | 13/30 | 17 |
| phi3:mini | Microsoft | 40.0% | 12/30 | 18 |
| mistral:7b | Mistral | 30.0% | 9/30 | 21 |

15 confirmed false positives are documented in the findings paper with corrected pass rates per model.

## Quickstart

### Cloud models

Requirements: Python 3.11+, an Anthropic API key.

```bash
git clone https://github.com/DodiBadshah/py-prompt-injection-2025.git
cd py-prompt-injection-2025
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

Run all payloads against Claude Haiku:

```bash
python -m llm_probe_2025.cli.main --model claude-haiku-4-5
```

### Local models via Ollama

No API key required. Runs entirely on your machine.

```bash
# Install Ollama from https://ollama.com
ollama pull mistral:7b
ollama pull llama3.1:8b
```

Run the full suite against a local model:

```bash
python -m llm_probe_2025.cli.main --model mistral:7b
python -m llm_probe_2025.cli.main --model llama3.1:8b
```

Supported local models: `mistral:7b`, `phi3:mini`, `gemma2:9b`, `gemma2:2b`, `llama3.1:8b`, `llama3.2:3b`

Output: HTML reports written to `reports/`.

## Example output

```text
Running 30 payloads against ollama/mistral:7b
Category: all
Results: 9/30 payloads passed.
Report written to reports/report-20260622-233500-mistral-7b.html
```

## Project structure

```text
llm_probe_2025/
  adapters/        LangChain model adapters (Anthropic, Ollama)
  cli/             Typer CLI entry point
  payloads/        YAML catalog and loader
  reporting/       Jinja2 HTML reporter
  runner/          Orchestration and MLflow logging
  scoring/         Generation 2 payload-aware scoring engine
  config.py        Environment and settings
  exceptions.py    Custom exception classes
  schemas.py       Pydantic v2 data contracts
tests/             pytest suite (50 tests)
.github/workflows/ CI and docs deployment pipelines
docs/              MkDocs source
```

## Development

```bash
pytest tests/ --no-cov -v    # run all 50 tests
```

CI runs automatically on every push via GitHub Actions.

## Security

This project handles LLM API keys and executes prompt injection payloads against live models. The following checks were run against the codebase:

- `bandit` - no high severity issues across the codebase
- `pip-audit` - no known CVEs in any dependency
- `detect-secrets` - no credentials or secrets detected
- YAML loading uses `safe_load` throughout, preventing arbitrary code execution
- `.env` verified absent from all git history

## Roadmap

This project is Phase 2 of a four-phase LLM security portfolio.

| Phase | Repository | OWASP Coverage | Status |
|---|---|---|---|
| Phase 1 | [py-prompt-injection](https://github.com/DodiBadshah/py-prompt-injection) | LLM01, LLM02, LLM06, LLM08 (2023-24) | Complete |
| Phase 2 | [py-prompt-injection-2025](https://github.com/DodiBadshah/py-prompt-injection-2025) | LLM01, LLM02, LLM05, LLM06, LLM07 (2025) | Complete |
| Phase 3 | py-rag-security | LLM03:2025, LLM08:2025, LLM09:2025 | Planned |
| Phase 4 | py-llm-load | LLM04:2025, LLM10:2025 | Planned |

### Phase 3: RAG Security Evaluation Framework
Target repository: `github.com/DodiBadshah/py-rag-security`

Production RAG pipeline over compliance document corpora with hybrid retrieval,
Cohere reranking, LLM-as-judge scoring, and Azure Container Apps deployment.

- **LLM03:2025 Supply Chain:** Tests whether poisoned documents injected into the retrieval store surface in model responses
- **LLM09:2025 Misinformation:** Tests whether grounded RAG responses can be manipulated to produce false but confident output

### Phase 4: Load and Resource Testing
Target repository: `github.com/DodiBadshah/py-llm-load`

Adds load testing infrastructure to cover the two remaining OWASP categories
that require concurrency and resource monitoring. Completes full OWASP LLM Top 10
2025 coverage across the suite.

- **LLM04:2025 Data and Model Poisoning**
- **LLM10:2025 Unbounded Consumption**

## License

MIT
