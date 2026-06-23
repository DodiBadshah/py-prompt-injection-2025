"""
Adapter factory for py-prompt-injection-2025.
Returns the correct LangChain adapter based on model name.
"""

from __future__ import annotations

from llm_probe_2025.adapters.anthropic_adapter import AnthropicAdapter
from llm_probe_2025.adapters.base import BaseAdapter
from llm_probe_2025.adapters.ollama_adapter import OllamaAdapter

ANTHROPIC_MODELS = {
    "claude-haiku-4-5",
    "claude-sonnet-4-6",
    "claude-opus-4-6",
}

OLLAMA_MODELS = {
    "mistral:7b",
    "phi3:mini",
    "gemma2:2b",
    "gemma2:9b",
    "llama3.1:8b",
    "llama3.2:3b",
}

ALL_SUPPORTED_MODELS = ANTHROPIC_MODELS | OLLAMA_MODELS


def get_adapter(model: str) -> BaseAdapter:
    """
    Return the correct adapter for the given model name.
    Raises ValueError for unsupported models.
    """
    if model in ANTHROPIC_MODELS:
        return AnthropicAdapter(model=model)
    if model in OLLAMA_MODELS:
        return OllamaAdapter(model=model)
    raise ValueError(
        f"Unsupported model: {model!r}. "
        f"Supported models: {sorted(ALL_SUPPORTED_MODELS)}"
    )


def sanitize_model_name(model: str) -> str:
    """
    Sanitize model name for use in filenames.
    Replaces colons and slashes with hyphens.
    Examples:
        phi3:mini       -> phi3-mini
        mistral:7b      -> mistral-7b
        llama3.1:8b     -> llama3.1-8b
        claude-haiku-4-5 -> claude-haiku-4-5
    """
    return model.replace(":", "-").replace("/", "-")
