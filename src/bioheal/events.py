"""Structured recovery events for the audit trail (charter §6 Stage 1, §7).

Every recovery outcome is recorded with a reason. Keep secrets and full payloads
out of events — identifiers and safe diagnostic details only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class RecoveryEvent:
    operation_id: str
    component: str
    outcome: str
    strategy: str
    reason: str
    correlation_id: str | None = None
    failure_kind: str | None = None
    duration_ms: float | None = None
    timestamp: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}
