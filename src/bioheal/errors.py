"""Structured, machine-readable errors (BIOHEAL_PROJECT.md §8.2–8.3).

Stable error codes, a retryable flag, and a next-action hint — so callers (and
AI agents) never have to parse prose. Never put secrets or stack traces here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    DEPENDENCY_TIMEOUT = "DEPENDENCY_TIMEOUT"
    CONNECTION_FAILED = "CONNECTION_FAILED"
    RATE_LIMITED = "RATE_LIMITED"
    AUTH_FAILED = "AUTH_FAILED"
    INVALID_INPUT = "INVALID_INPUT"
    SCHEMA_MISMATCH = "SCHEMA_MISMATCH"
    DEPENDENCY_UNAVAILABLE = "DEPENDENCY_UNAVAILABLE"
    STALE_OUTPUT = "STALE_OUTPUT"
    RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class BioHealError:
    """A public, machine-readable error contract."""

    code: ErrorCode
    message: str
    retryable: bool = False
    request_id: str | None = None
    action: str | None = None
    documentation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code.value,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.request_id:
            payload["request_id"] = self.request_id
        if self.action:
            payload["action"] = self.action
        if self.documentation:
            payload["documentation"] = self.documentation
        return {"error": payload}
