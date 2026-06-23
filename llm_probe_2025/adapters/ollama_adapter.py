"""
Ollama adapter for py-prompt-injection-2025.
Uses LangChain ChatOllama as the model backend for local inference.
"""

from __future__ import annotations

from functools import cached_property

from langchain_ollama import ChatOllama
from langchain_core.language_models import BaseChatModel

from llm_probe_2025.adapters.base import BaseAdapter
from llm_probe_2025.config import config


class OllamaAdapter(BaseAdapter):
    """LangChain-backed adapter for local Ollama models."""

    def __init__(self, model: str = "mistral:7b") -> None:
        self._model_name = model

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def adapter_name(self) -> str:
        return "ollama"

    @cached_property
    def llm(self) -> BaseChatModel:
        return ChatOllama(
            model=self._model_name,
            base_url=config.ollama_base_url,
            timeout=config.default_timeout,
            num_predict=2048,
        )
