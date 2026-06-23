"""
Custom exceptions for py-prompt-injection-2025.
"""


class LLMProbeError(Exception):
    """Base exception for all llm-probe-2025 errors."""


class AdapterError(LLMProbeError):
    """Raised when a model adapter fails to get a response."""


class PayloadLoadError(LLMProbeError):
    """Raised when a payload catalog file cannot be loaded or validated."""


class ScoringError(LLMProbeError):
    """Raised when scoring fails for a response."""


class ReportError(LLMProbeError):
    """Raised when report generation fails."""


class ConfigError(LLMProbeError):
    """Raised when required configuration is missing or invalid."""
