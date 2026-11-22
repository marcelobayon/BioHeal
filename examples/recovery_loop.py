# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example H — Recovery control loop (monitor -> diagnose -> verify -> rollback)."""
from dataclasses import dataclass


@dataclass
class RecoveryResult:
    status: str
    strategy: str
    explanation: str


def recover(primary, fallback, verify) -> RecoveryResult:
    try:
        result = primary()
        if verify(result):
            return RecoveryResult("healthy", "primary", "Primary result verified")
    except Exception:
        pass  # In production, catch only expected failure classes and log details.

    try:
        result = fallback()
        if verify(result):
            return RecoveryResult("recovered", "fallback", "Fallback result verified")
    except Exception:
        pass

    return RecoveryResult(
        "unrecovered",
        "none",
        "No strategy produced a verified result; retain safe state and escalate",
    )


if __name__ == "__main__":
    def primary():
        raise ConnectionError("down")

    print(recover(primary, lambda: "backup", verify=lambda r: bool(r)))
