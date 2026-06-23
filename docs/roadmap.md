# Roadmap

The LLM Security Evaluation Suite is a four-phase project covering the full OWASP LLM Top 10 2025 framework across black-box evaluation, RAG security, and load testing.

## Phase 1: py-prompt-injection (Complete)

Black-box prompt injection evaluation harness covering OWASP LLM Top 10 2023-24.

- 24 payloads across 4 OWASP LLM Top 10 2023-24 categories
- 7 models across 5 architecture families
- Two scoring generations (keyword heuristic and payload-aware corrected scorer)
- 168 scored runs
- MLflow experiment tracking
- GitHub Actions CI/CD
- MkDocs documentation site
- Published research paper with responsible disclosure findings

Live site: [dodibadshah.github.io/py-prompt-injection](https://dodibadshah.github.io/py-prompt-injection)

## Phase 2: py-prompt-injection-2025 (Complete)

Updated evaluation harness covering OWASP LLM Top 10 2025 with LangChain orchestration.

- 30 payloads across 5 OWASP LLM Top 10 2025 categories
- 7 models across 5 architecture families
- LangChain orchestration replacing raw API calls
- Generation 2 payload-aware scorer carried forward from Phase 1
- 210 scored runs
- 15 confirmed false positives documented
- Published research paper with key findings and false positive analysis

Live site: [dodibadshah.github.io/py-prompt-injection-2025](https://dodibadshah.github.io/py-prompt-injection-2025)

## Phase 3: py-rag-security (Planned)

Production RAG pipeline over compliance document corpora with LLM-as-judge evaluation.

- Document corpora: HIPAA, NIST SP 800-53, CIS Controls v8
- Hybrid retrieval: BM25 sparse vectors and dense embeddings via Pinecone
- Cohere reranking of top 20 results to final top 5
- LLM-as-judge scoring replacing keyword heuristics
- RAGAS evaluation metrics
- FastAPI backend with vanilla HTML and JS frontend
- Docker containerization
- Azure Container Apps deployment via GitHub Actions
- Covers OWASP LLM03:2025 and LLM09:2025
- Golden evaluation dataset of 20 to 30 question-answer pairs from public compliance documents

## Phase 4: py-llm-load (Planned)

Load and resource testing harness completing full OWASP LLM Top 10 2025 coverage.

- asyncio-based concurrent request engine
- Token consumption monitoring per model and per request
- FastAPI backend with live deployed endpoint
- Token consumption dashboard
- Covers OWASP LLM04:2025 and LLM10:2025
- Cross-phase research question: do models start complying with injection payloads under resource pressure?

## OWASP LLM Top 10 2025 coverage across all phases

| OWASP ID | Category | Phase |
|---|---|---|
| LLM01:2025 | Prompt Injection | Phase 2 |
| LLM02:2025 | Sensitive Information Disclosure | Phase 2 |
| LLM03:2025 | Supply Chain | Phase 3 |
| LLM04:2025 | Data and Model Poisoning | Phase 4 |
| LLM05:2025 | Improper Output Handling | Phase 2 |
| LLM06:2025 | Excessive Agency | Phase 2 |
| LLM07:2025 | System Prompt Leakage | Phase 2 |
| LLM08:2025 | Vector and Embedding Weaknesses | Phase 3 |
| LLM09:2025 | Misinformation | Phase 3 |
| LLM10:2025 | Unbounded Consumption | Phase 4 |
