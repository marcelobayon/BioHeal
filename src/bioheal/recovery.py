"""The recovery control loop (charter §6): the core of BioHeal.

Try the primary; if it fails or its result fails verification, try each
policy-approved fallback in order, verifying every candidate. Declare success
only on a *verified* result. If nothing verifies, escalate and keep the safe
state — never report a false recovery.

This is an experimental, Milestone-0-level reference implementation: bounded,
synchronous, standard-library only. It is not production resilience.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, Sequence, TypeVar

from .diagnosis import Diagnosis, FailureKind, diagnose
from .events import RecoveryEvent
from .policy import Policy
from .verification import VerificationResult, Verifier

T = TypeVar("T")

NamedStrategy = tuple[str, Callable[[], T]]


class RecoveryOutcome(str, Enum):
    HEALTHY = "healthy"        # primary worked and verified
    RECOVERED = "recovered"    # a fallback worked and verified
    ESCALATED = "escalated"    # nothing verified, or promotion needs approval


@dataclass
class RecoveryResult(Generic[T]):
    outcome: RecoveryOutcome
    strategy: str
    value: T | None
    reason: str
    event: RecoveryEvent
    diagnosis: Diagnosis | None = None

    @property
    def recovered(self) -> bool:
        return self.outcome in (RecoveryOutcome.HEALTHY, RecoveryOutcome.RECOVERED)


class RecoveryEngine(Generic[T]):
    """Runs the bounded detect → diagnose → select → verify → promote loop."""

    def __init__(
        self,
        verifier: Verifier[T],
        policy: Policy,
        on_event: Callable[[RecoveryEvent], None] | None = None,
        clock: Callable[[], float] = time.monotonic,
    ):
        self._verifier = verifier
        self._policy = policy
        self._on_event = on_event
        self._clock = clock

    def run(
        self,
        primary: Callable[[], T],
        fallbacks: Sequence[NamedStrategy[T]] = (),
        *,
        operation_id: str,
        component: str,
        correlation_id: str | None = None,
    ) -> RecoveryResult[T]:
        start = self._clock()
        last_diag: Diagnosis | None = None

        # --- Primary ---
        value, vr, exc = self._attempt(primary)
        if exc is None and vr is not None and vr.passed:
            return self._finish(
                RecoveryOutcome.HEALTHY, "primary", value, "primary result verified",
                operation_id, component, correlation_id, start, None,
            )
        last_diag = self._diag_from(exc, vr)

        # --- Fallbacks (policy-approved, in order) ---
        attempts = 0
        for name, fn in fallbacks:
            if attempts >= max(0, self._policy.max_attempts - 1):
                break
            if self._clock() - start >= self._policy.time_budget_s:
                break
            if not self._policy.permits(name):
                continue  # deny-by-default: skip strategies not on the allowlist
            attempts += 1

            value, vr, exc = self._attempt(fn)
            if exc is None and vr is not None and vr.passed:
                if not self._policy.allow_promotion:
                    return self._finish(
                        RecoveryOutcome.ESCALATED, name, value,
                        "verified, but policy requires human approval to promote",
                        operation_id, component, correlation_id, start, last_diag,
                    )
                return self._finish(
                    RecoveryOutcome.RECOVERED, name, value,
                    f"fallback {name!r} verified", operation_id, component,
                    correlation_id, start, last_diag,
                )
            last_diag = self._diag_from(exc, vr) or last_diag

        return self._finish(
            RecoveryOutcome.ESCALATED, "none", None,
            "no strategy produced a verified result; retain safe state and escalate",
            operation_id, component, correlation_id, start, last_diag,
        )

    # -- helpers ----------------------------------------------------------
    def _attempt(
        self, fn: Callable[[], T]
    ) -> tuple[T | None, VerificationResult | None, BaseException | None]:
        try:
            value = fn()
        except Exception as exc:  # expected failure classes in a real system
            return None, None, exc
        return value, self._verifier.verify(value), None

    @staticmethod
    def _diag_from(
        exc: BaseException | None, vr: VerificationResult | None
    ) -> Diagnosis | None:
        if exc is not None:
            return diagnose(exc)
        if vr is not None and not vr.passed:
            # Returned without error but failed verification = false recovery.
            return Diagnosis(FailureKind.STALE_OUTPUT, 0.6, False, vr.reason)
        return None

    def _finish(
        self,
        outcome: RecoveryOutcome,
        strategy: str,
        value: T | None,
        reason: str,
        operation_id: str,
        component: str,
        correlation_id: str | None,
        start: float,
        diag: Diagnosis | None,
    ) -> RecoveryResult[T]:
        event = RecoveryEvent(
            operation_id=operation_id,
            component=component,
            outcome=outcome.value,
            strategy=strategy,
            reason=reason,
            correlation_id=correlation_id,
            failure_kind=diag.kind.value if diag else None,
            duration_ms=round((self._clock() - start) * 1000, 3),
        )
        if self._on_event is not None:
            self._on_event(event)
        return RecoveryResult(outcome, strategy, value, reason, event, diag)
