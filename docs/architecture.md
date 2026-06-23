# Architecture

py-prompt-injection-2025 is built as a layered Python package. Each layer has a single responsibility and depends only on the layers below it.

## Layer overview

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

## Components

### Payload catalog
Five YAML files, one per OWASP category. Each payload defines an ID, category, severity, prompt text, expected behavior, and scoring method. The loader validates each payload against the pydantic schema on load.

### LangChain orchestration
Phase 2 replaces the raw API calls of Phase 1 with LangChain chain components. Model adapters for Anthropic and Ollama are implemented as LangChain runnables. This provides a uniform interface across cloud and local inference backends and positions the harness for agentic evaluation in future phases.

### Model adapters

| Adapter | Provider | API Key Required |
|---|---|---|
| AnthropicAdapter | Anthropic cloud | Yes |
| OllamaAdapter | Local Ollama instance | No |

The correct adapter is selected automatically based on the model name passed to the CLI.

### Generation 2 scoring engine
The scoring engine reads the `expected_behavior` field from each payload and routes to the appropriate detection check. It does not run all checks blindly against every response.

| Expected Behavior | Detection Check |
|---|---|
| refusal | detect_refusal() |
| no_exfiltration | detect_exfiltration() |
| no_code_execution | detect_code_execution() |
| no_sensitive_data | detect_sensitive_data() |
| no_agency | detect_excessive_agency() |

### Runner
Orchestrates the full evaluation loop. Iterates over payloads, calls the adapter via LangChain, routes responses to the scoring engine, logs results to MLflow, and collects the final list of Result objects.

### CLI
Built with Typer. Supports model selection, OWASP category filtering, single or multi-run mode, and interactive menu. Reports are saved as HTML files in the reports/ directory.

### Reporter
Generates self-contained HTML reports using Jinja2 templates. Reports include a summary header, per-payload results table with flags, and an UNSTABLE badge when single-run mode is used.

## Data flow

```
YAML catalogs -> Payload objects -> LangChain Runner -> Adapter -> LLM API
                                          |
                                    Raw response
                                          |
                               Generation 2 Scoring Engine -> Result objects
                                          |
                                     MLflow log + HTML Report
```
