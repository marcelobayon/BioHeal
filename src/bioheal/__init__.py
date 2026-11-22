"""BioHeal — an experimental, open-source framework for *verified* recovery.

Detect a failure, diagnose it, select a policy-approved strategy, **verify the
result**, and promote it or roll back. Self-healing here means verified
recovery, never arbitrary self-modification.

Status: experimental reference implementation (Milestone-0 level). Bounded,
synchronous, standard-library only. Not production resilience — see
BIOHEAL_PROJECT.md for the roadmap and honest limitations.

    from bioheal import RecoveryEngine, Verifier, Policy, non_empty

    engine = RecoveryEngine(
        verifier=Verifier([("non-empty", non_empty)]),
        policy=Policy.allowing("cache"),
    )
    result = engine.run(
        primary=call_api,
        fallbacks=[("cache", read_cache)],
        operation_id="op-1", component="weather",
    )
    result.recovered  # True only if a result actually verified
"""

from __future__ import annotations

from .diagnosis import Diagnosis, FailureKind, diagnose
from .errors import BioHealError, ErrorCode
from .events import RecoveryEvent
from .policy import Policy
from .recovery import RecoveryEngine, RecoveryOutcome, RecoveryResult
from .rollback import KnownGoodStore
from .verification import VerificationResult, Verifier, non_empty

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "RecoveryEngine",
    "RecoveryResult",
    "RecoveryOutcome",
    "Verifier",
    "VerificationResult",
    "non_empty",
    "Policy",
    "KnownGoodStore",
    "Diagnosis",
    "FailureKind",
    "diagnose",
    "RecoveryEvent",
    "BioHealError",
    "ErrorCode",
]
