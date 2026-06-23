# CLI Reference

py-prompt-injection-2025 provides an interactive command-line interface built with Typer.

## Starting the CLI

```bash
python -m llm_probe_2025.cli.main --model <model-name>
```

## Supported models

| Model | Provider | Adapter | API Key Required |
|---|---|---|---|
| claude-haiku-4-5 | Anthropic | AnthropicAdapter | Yes |
| mistral:7b | Ollama | OllamaAdapter | No |
| phi3:mini | Ollama | OllamaAdapter | No |
| gemma2:9b | Ollama | OllamaAdapter | No |
| gemma2:2b | Ollama | OllamaAdapter | No |
| llama3.1:8b | Ollama | OllamaAdapter | No |
| llama3.2:3b | Ollama | OllamaAdapter | No |

## Interactive menu

When you run the CLI it presents an interactive menu with the following options:

**Step 1: Select payload source**
```
1. Load from catalog (YAML files)
```

**Step 2: Select OWASP category**
```
1. LLM01:2025 - Prompt Injection
2. LLM02:2025 - Sensitive Information Disclosure
3. LLM05:2025 - Improper Output Handling
4. LLM06:2025 - Excessive Agency
5. LLM07:2025 - System Prompt Leakage
Enter category number (or press Enter for all):
```

**Step 3: Select run mode**
```
1. Single run
2. Multi-run (3 runs with averaging)
```

## Example: Run all categories against claude-haiku-4-5

```bash
python -m llm_probe_2025.cli.main --model claude-haiku-4-5
```

Then at the menu: select 1 for catalog, press Enter for all categories, select 1 for single run, confirm y.

## Example: Run LLM07 only against mistral:7b

```bash
python -m llm_probe_2025.cli.main --model mistral:7b
```

Then at the menu: select 1 for catalog, enter 5 for LLM07:2025, select 1 for single run, confirm y.

## Example: Multi-run with averaging against llama3.1:8b

```bash
python -m llm_probe_2025.cli.main --model llama3.1:8b
```

Then at the menu: select 1 for catalog, press Enter for all categories, select 2 for multi-run, confirm y.

## Output

Reports are saved to the reports/ directory as HTML files. The filename includes the model name and timestamp.

```
reports/
  claude-haiku-4-5_20260623_040400.html
  mistral-7b_20260622_233500.html
```

Reports generated from single-run mode include an UNSTABLE badge in the header indicating that results may vary across runs at default temperature.

## Environment setup

```bash
cp .env.example .env
```

Add your Anthropic API key to .env:

```
ANTHROPIC_API_KEY=your-key-here
```

Ollama models require Ollama to be running locally on port 11434. Start Ollama before running the CLI:

```bash
ollama serve
ollama pull mistral:7b
```

## MLflow tracking

All runs are logged to MLflow automatically. To view the MLflow UI:

```bash
mlflow ui
```

Then open http://localhost:5000 in your browser.
