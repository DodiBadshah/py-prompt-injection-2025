# py-prompt-injection-2025

[![CI](https://github.com/DodiBadshah/py-prompt-injection-2025/actions/workflows/ci.yml/badge.svg)](https://github.com/DodiBadshah/py-prompt-injection-2025/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-live-green.svg)](https://dodibadshah.github.io/py-prompt-injection-2025)

A black-box LLM security evaluation harness mapped to the OWASP LLM Top 10 2025. Phase 2 of a four-phase suite. Extends Phase 1 with LangChain orchestration, five updated OWASP 2025 categories, and 30 structured attack payloads tested across seven models and five architecture families.

**Live docs:** https://dodibadshah.github.io/py-prompt-injection-2025

**Phase 2 findings paper:** https://dodibadshah.github.io/py-prompt-injection-2025/phase2-findings.html

**Phase 1 repo:** https://github.com/DodiBadshah/py-prompt-injection

---

## What it does

py-prompt-injection-2025 fires structured attack payloads at any LLM API and scores the responses automatically using a Generation 2 payload-aware scorer. It tells you whether a model is vulnerable to prompt injection, sensitive information disclosure, improper output handling, excessive agency, and system prompt leakage.

Think of it as Nessus for LLMs, updated for the 2025 OWASP threat landscape.

---

## Architecture

```
YAML Payload Catalogs
        ↓
Payload Loader + Schema Validation (pydantic v2)
        ↓
LangChain Orchestration Layer
        ↓
Model Adapters (Anthropic SDK / Ollama)
        ↓
LLM APIs (cloud or local)
        ↓
Raw Response
        ↓
Generation 2 Payload-Aware Scoring Engine
        ↓
Result Objects + MLflow Logging
        ↓
HTML Reporter + CLI Output
```

---

## OWASP LLM Top 10 2025 coverage

| OWASP ID | Category | Payloads |
|---|---|---|
| LLM01:2025 | Prompt Injection | 6 |
| LLM02:2025 | Sensitive Information Disclosure | 6 |
| LLM05:2025 | Improper Output Handling | 6 |
| LLM06:2025 | Excessive Agency | 6 |
| LLM07:2025 | System Prompt Leakage | 6 |
| **Total** | | **30** |

---

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

---

## Quick start

```bash
git clone https://github.com/DodiBadshah/py-prompt-injection-2025
cd py-prompt-injection-2025
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
python -m llm_probe_2025.cli.main --model claude-haiku-4-5
```

For local Ollama models, start Ollama first:

```bash
ollama serve
ollama pull mistral:7b
python -m llm_probe_2025.cli.main --model mistral:7b
```

---

## Running tests

```bash
python -m pytest tests/ --no-cov -v
```

All 50 tests should pass.

---

## Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| pydantic v2 | Payload schema validation |
| LangChain | Model orchestration layer |
| Anthropic SDK | Claude API adapter |
| Ollama | Local model inference |
| MLflow | Experiment tracking |
| Typer | CLI |
| Jinja2 | HTML report templating |
| pytest | Test suite |
| MkDocs Material | Documentation site |
| GitHub Actions | CI/CD and docs deployment |

---

## Project structure

```
py-prompt-injection-2025/
├── llm_probe_2025/
│   ├── adapters/          LangChain model adapters
│   ├── cli/               Typer CLI entry point
│   ├── payloads/
│   │   └── catalog/       YAML payload files (one per OWASP category)
│   ├── reporting/         Jinja2 HTML reporter
│   ├── runner/            Orchestration and MLflow logging
│   ├── scoring/           Generation 2 payload-aware scoring engine
│   ├── config.py          Environment and settings
│   ├── exceptions.py      Custom exception classes
│   └── schemas.py         Pydantic v2 data contracts
├── tests/
│   └── test_suite.py      Full test suite (50 tests)
├── docs/                  MkDocs documentation source
├── .env.example           Environment variable template
├── mkdocs.yml             MkDocs configuration
└── pyproject.toml         Package metadata and dependencies
```

---

## Suite roadmap

| Phase | Repo | Status | Coverage |
|---|---|---|---|
| Phase 1 | py-prompt-injection | Complete | OWASP LLM Top 10 2023-24 (4 categories) |
| Phase 2 | py-prompt-injection-2025 | Complete | OWASP LLM Top 10 2025 (5 categories) |
| Phase 3 | py-rag-security | Planned | RAG security, LLM-as-judge, OWASP LLM03 and LLM09 |
| Phase 4 | py-llm-load | Planned | Load testing, token consumption, OWASP LLM04 and LLM10 |

---

## License

MIT
