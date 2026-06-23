"""
Base adapter interface for py-prompt-injection-2025.
All model adapters implement this interface using LangChain.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage

from llm_probe_2025.exceptions import AdapterError


class BaseAdapter(ABC):
    """Abstract base for all LangChain-backed model adapters."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the canonical model name string."""

    @property
    @abstractmethod
    def adapter_name(self) -> str:
        """Return a short identifier for this adapter family."""

    @property
    @abstractmethod
    def llm(self) -> BaseChatModel:
        """Return the LangChain chat model instance."""

    def invoke(self, prompt: str) -> str:
        """
        Send a single prompt to the model and return the response text.
        Raises AdapterError on failure.
        """
        try:
            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as exc:
            raise AdapterError(
                f"{self.adapter_name} adapter failed for model "
                f"{self.model_name}: {exc}"
            ) from exc
