"""Stage 5 — Verify: a result is recovered only when it *passes checks*.

"Verification must evaluate the intended outcome, not simply whether the
operation stopped throwing an exception." A candidate that returns without error
but fails a check is a *false recovery* and must be rejected.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Sequence, TypeVar

T = TypeVar("T")

Check = tuple[str, Callable[[T], bool]]


@dataclass(frozen=True)
class VerificationResult:
    passed: bool
    reason: str


class Verifier(Generic[T]):
    """Runs an ordered list of named checks against a candidate value."""

    def __init__(self, checks: Sequence[Check[T]]):
        self._checks = list(checks)

    def verify(self, value: T) -> VerificationResult:
        for name, predicate in self._checks:
            try:
                ok = predicate(value)
            except Exception as exc:  # a check that errors is a failed check
                return VerificationResult(False, f"check {name!r} raised: {exc}")
            if not ok:
                return VerificationResult(False, f"failed check: {name}")
        return VerificationResult(True, "all checks passed")


def non_empty(value: object) -> bool:
    """A common first check: result exists and is not blank."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True
