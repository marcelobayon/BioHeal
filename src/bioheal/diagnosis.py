"""Stage 2 — Diagnose: classify a failure into a known kind with confidence.

Unknown cases default to *safe* behavior (not retryable), per the charter:
"Unknown cases should default to safe behavior, not aggressive repair."
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .errors import ErrorCode


class FailureKind(str, Enum):
    TIMEOUT = "timeout"
    CONNECTION = "connection"
    RATE_LIMIT = "rate_limit"
    AUTH = "auth"
    INVALID_INPUT = "invalid_input"
    SCHEMA_MISMATCH = "schema_mismatch"
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    STALE_OUTPUT = "stale_output"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Diagnosis:
    kind: FailureKind
    confidence: float  # 0.0–1.0
    retryable: bool
    evidence: str

    @property
    def error_code(self) -> ErrorCode:
        return _KIND_TO_CODE.get(self.kind, ErrorCode.UNKNOWN)


_KIND_TO_CODE = {
    FailureKind.TIMEOUT: ErrorCode.DEPENDENCY_TIMEOUT,
    FailureKind.CONNECTION: ErrorCode.CONNECTION_FAILED,
    FailureKind.RATE_LIMIT: ErrorCode.RATE_LIMITED,
    FailureKind.AUTH: ErrorCode.AUTH_FAILED,
    FailureKind.INVALID_INPUT: ErrorCode.INVALID_INPUT,
    FailureKind.SCHEMA_MISMATCH: ErrorCode.SCHEMA_MISMATCH,
    FailureKind.DEPENDENCY_UNAVAILABLE: ErrorCode.DEPENDENCY_UNAVAILABLE,
    FailureKind.STALE_OUTPUT: ErrorCode.STALE_OUTPUT,
    FailureKind.RESOURCE_EXHAUSTED: ErrorCode.RESOURCE_EXHAUSTED,
    FailureKind.UNKNOWN: ErrorCode.UNKNOWN,
}

# Transient kinds are the only ones marked retryable by default.
_RETRYABLE = {FailureKind.TIMEOUT, FailureKind.CONNECTION, FailureKind.RATE_LIMIT}


def diagnose(exc: BaseException) -> Diagnosis:
    """Classify a Python exception into a :class:`Diagnosis`.

    This is intentionally conservative: anything it does not recognise is
    ``UNKNOWN`` and *not* retryable, so an unclassified failure never triggers
    aggressive recovery.
    """
    if isinstance(exc, TimeoutError):
        kind = FailureKind.TIMEOUT
    elif isinstance(exc, ConnectionError):
        kind = FailureKind.CONNECTION
    elif isinstance(exc, (ValueError, TypeError)):
        kind = FailureKind.INVALID_INPUT
    elif isinstance(exc, PermissionError):
        kind = FailureKind.AUTH
    elif isinstance(exc, MemoryError):
        kind = FailureKind.RESOURCE_EXHAUSTED
    else:
        # Light heuristic on the message for things without a dedicated type.
        text = str(exc).lower()
        if "rate limit" in text or "429" in text or "too many requests" in text:
            kind = FailureKind.RATE_LIMIT
        elif "unavailable" in text or "503" in text:
            kind = FailureKind.DEPENDENCY_UNAVAILABLE
        elif "schema" in text:
            kind = FailureKind.SCHEMA_MISMATCH
        else:
            kind = FailureKind.UNKNOWN

    retryable = kind in _RETRYABLE
    confidence = 0.85 if kind is not FailureKind.UNKNOWN else 0.3
    return Diagnosis(
        kind=kind,
        confidence=confidence,
        retryable=retryable,
        evidence=f"{type(exc).__name__}: {exc}",
    )
