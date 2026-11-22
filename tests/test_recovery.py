import pytest

from bioheal import (
    KnownGoodStore,
    Policy,
    RecoveryEngine,
    RecoveryOutcome,
    Verifier,
    diagnose,
    non_empty,
)
from bioheal.diagnosis import FailureKind
from bioheal.errors import BioHealError, ErrorCode


def engine(**policy_kwargs):
    return RecoveryEngine(
        verifier=Verifier([("non-empty", non_empty)]),
        policy=Policy.allowing("cache", "replica", **policy_kwargs),
    )


def test_healthy_when_primary_verifies():
    r = engine().run(lambda: "ok", operation_id="op", component="svc")
    assert r.outcome is RecoveryOutcome.HEALTHY
    assert r.recovered and r.value == "ok"


def test_recovers_via_allowed_fallback():
    def primary():
        raise ConnectionError("down")

    r = engine().run(
        primary,
        fallbacks=[("cache", lambda: "from-cache")],
        operation_id="op", component="svc",
    )
    assert r.outcome is RecoveryOutcome.RECOVERED
    assert r.strategy == "cache" and r.value == "from-cache"


def test_false_recovery_is_rejected():
    # Primary returns without error but an empty value fails verification.
    def primary():
        return ""

    r = engine().run(
        primary,
        fallbacks=[("cache", lambda: "real")],
        operation_id="op", component="svc",
    )
    assert r.outcome is RecoveryOutcome.RECOVERED
    assert r.value == "real"  # the empty primary result was NOT accepted


def test_escalates_when_nothing_verifies():
    def boom():
        raise TimeoutError("slow")

    r = engine().run(
        boom,
        fallbacks=[("cache", lambda: "")],  # fallback also fails verification
        operation_id="op", component="svc",
    )
    assert r.outcome is RecoveryOutcome.ESCALATED
    assert r.value is None
    assert r.diagnosis is not None


def test_deny_by_default_skips_unlisted_strategy():
    def boom():
        raise ConnectionError("down")

    # "cache" is NOT in the allowlist, so it must be skipped -> escalate.
    eng = RecoveryEngine(Verifier([("non-empty", non_empty)]), Policy.allowing("replica"))
    r = eng.run(boom, fallbacks=[("cache", lambda: "x")], operation_id="op", component="svc")
    assert r.outcome is RecoveryOutcome.ESCALATED


def test_promotion_can_require_human_approval():
    def boom():
        raise ConnectionError("down")

    eng = RecoveryEngine(
        Verifier([("non-empty", non_empty)]),
        Policy.allowing("cache", allow_promotion=False),
    )
    r = eng.run(boom, fallbacks=[("cache", lambda: "x")], operation_id="op", component="svc")
    assert r.outcome is RecoveryOutcome.ESCALATED
    assert "approval" in r.reason


def test_event_is_recorded():
    seen = []
    eng = RecoveryEngine(
        Verifier([("non-empty", non_empty)]), Policy.allowing("cache"), on_event=seen.append
    )
    eng.run(lambda: "ok", operation_id="op-7", component="svc")
    assert seen and seen[0].operation_id == "op-7"
    assert seen[0].outcome == "healthy"


# -- diagnosis & errors ----------------------------------------------------
@pytest.mark.parametrize(
    "exc,kind,retryable",
    [
        (TimeoutError(), FailureKind.TIMEOUT, True),
        (ConnectionError(), FailureKind.CONNECTION, True),
        (ValueError("bad"), FailureKind.INVALID_INPUT, False),
        (RuntimeError("mystery"), FailureKind.UNKNOWN, False),
    ],
)
def test_diagnose(exc, kind, retryable):
    d = diagnose(exc)
    assert d.kind is kind
    assert d.retryable is retryable


def test_error_contract_shape():
    err = BioHealError(
        ErrorCode.DEPENDENCY_TIMEOUT, "primary did not respond", retryable=True,
        request_id="req_1", action="try the approved secondary",
    )
    payload = err.to_dict()["error"]
    assert payload["code"] == "DEPENDENCY_TIMEOUT"
    assert payload["retryable"] is True
    assert payload["request_id"] == "req_1"


# -- rollback --------------------------------------------------------------
def test_known_good_store_rolls_back_bad_candidate():
    store = KnownGoodStore({"timeout": 1.0})
    ok = store.promote({"timeout": 99.0}, verify=lambda c: c["timeout"] <= 10)
    assert ok is False
    assert store.current == {"timeout": 1.0}  # restored to known-good

    ok = store.promote({"timeout": 5.0}, verify=lambda c: c["timeout"] <= 10)
    assert ok is True
    assert store.known_good == {"timeout": 5.0}
