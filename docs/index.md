# py-prompt-injection-2025

A black-box prompt injection test harness for LLMs, mapped to the OWASP LLM Top 10 2025.

> **Status:** Phase 2 complete. Phase 2 findings and false positive analysis published. Phase 3 (py-rag-security) in development.

## What it does

py-prompt-injection-2025 fires structured attack payloads at any LLM API and scores the responses automatically. It tells you whether a model is vulnerable to prompt injection, sensitive information disclosure, improper output handling, excessive agency, and system prompt leakage.

Think of it as Nessus for LLMs, updated for the 2025 OWASP threat landscape.

## Key features

- 30 attack payloads across 5 OWASP LLM Top 10 2025 categories
- LangChain orchestration replacing raw API calls
- Generation 2 payload-aware scorer carried forward from Phase 1
- Support for Anthropic cloud API and local Ollama models
- MLflow experiment tracking
- Interactive CLI with category filtering
- HTML report generation with UNSTABLE badge for single-run verdicts

## Project status

Phase 1 (py-prompt-injection) complete. OWASP LLM Top 10 2023-24 payload catalog, 7 models, 168 scored runs, responsible disclosure advisory published.

[View Phase 1 on GitHub](https://github.com/DodiBadshah/py-prompt-injection) · [View Phase 1 Docs](https://dodibadshah.github.io/py-prompt-injection)

Phase 2: 30 payloads across 5 OWASP LLM Top 10 2025 categories. 7 models tested across 5 architecture families. 210 scored runs. CI passing on GitHub Actions.

[View Phase 2 Findings](phase2-findings.html)

Phase 3 (py-rag-security) in development. Production RAG pipeline over compliance document corpora with hybrid retrieval, Cohere reranking, and LLM-as-judge scoring.

[View Phase 3 on GitHub](https://github.com/DodiBadshah/py-rag-security)