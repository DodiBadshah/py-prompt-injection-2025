"""
Anthropic adapter for py-prompt-injection-2025.
Uses LangChain ChatAnthropic as the model backend.
"""

from __future__ import annotations

from functools import cached_property

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel

from llm_probe_2025.adapters.base import BaseAdapter
from llm_probe_2025.config import config


class AnthropicAdapter(BaseAdapter):
    """LangChain-backed adapter for Anthropic Claude models."""

    def __init__(self, model: str = "claude-haiku-4-5") -> None:
        self._model_name = model

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def adapter_name(self) -> str:
        return "anthropic"

    @cached_property
    def llm(self) -> BaseChatModel:
        return ChatAnthropic(
            model=self._model_name,
            api_key=config.anthropic_api_key,
            timeout=config.default_timeout,
            max_tokens=2048,
        )
