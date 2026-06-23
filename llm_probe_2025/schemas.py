"""
Pydantic v2 schemas for py-prompt-injection-2025.
Payload and Result are the core data contracts used across all layers.
"""
 
from __future__ import annotations
 
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
 
from pydantic import BaseModel, Field
 
 
class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
 
 
class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
 
 
class ExpectedBehavior(str, Enum):
    REFUSAL = "refusal"
    NO_EXFILTRATION = "no_exfiltration"
    NO_CODE_EXECUTION = "no_code_execution"
    NO_SENSITIVE_DATA = "no_sensitive_data"
    NO_AGENCY = "no_agency"
    NO_HALLUCINATION = "no_hallucination"
    GENERIC = "generic"
 
 
class Payload(BaseModel):
    id: str
    name: str
    scenario: str
    technique: str
    prompt: str
    expected_behavior: ExpectedBehavior
    scoring_method: str
    severity: Severity
    tags: list[str] = Field(default_factory=list)
    category: str = ""
 
 
class Result(BaseModel):
    payload_id: str
    category: str
    model: str
    prompt: str
    response: str
    score: float = Field(ge=0.0, le=1.0)
    verdict: Verdict
    flags: list[str] = Field(default_factory=list)
    expected_behavior: ExpectedBehavior
    severity: Severity
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error: Optional[str] = None
    adapter: str = ""
    run_count: int = 1
    score_variance: Optional[float] = None
    score_min: Optional[float] = None
    score_max: Optional[float] = None
    verdict_stable: Optional[bool] = None