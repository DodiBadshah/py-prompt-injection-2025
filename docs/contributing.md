# Contributing

Contributions to py-prompt-injection-2025 are welcome. This page covers how to set up the development environment, run the test suite, and submit changes.

## Development setup

```bash
git clone https://github.com/DodiBadshah/py-prompt-injection-2025
cd py-prompt-injection-2025
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e ".[dev]"
cp .env.example .env
```

Add your Anthropic API key to .env before running any cloud model evaluations.

## Running the tests

```bash
python -m pytest tests/ --no-cov -v
```

All 50 tests should pass. The test suite covers payload schema validation, loader, scoring engine, adapters (mocked), and CLI.

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

## Adding a payload

1. Open the relevant YAML file in `llm_probe_2025/payloads/catalog/`
2. Add a new entry following the existing structure:

```yaml
- id: llm01-007
  category: "LLM01:2025"
  severity: HIGH
  prompt: "Your attack prompt here"
  expected_behavior: refusal
  scoring_method: refusal_detection
```

3. Run the tests to confirm the loader picks up the new payload without schema errors
4. Run a model sweep to verify the scoring engine handles the new payload correctly

## Adding a model

1. If the model runs on Ollama, no adapter changes are needed. Pass the model name directly to the CLI.
2. If the model requires a new API, create a new adapter in `llm_probe_2025/adapters/` following the base adapter interface.
3. Register the new adapter in `llm_probe_2025/adapters/factory.py`.
4. Add tests for the new adapter in `tests/test_suite.py`.

## Pull request checklist

- All 50 existing tests pass
- New code has corresponding tests
- No secrets or API keys committed
- mlflow.db not committed (it is in .gitignore)
- HTML report files not committed
- Commit messages follow the format: `type: description` for example `feat: add gemma3 adapter` or `fix: refusal gate on agency payloads`
