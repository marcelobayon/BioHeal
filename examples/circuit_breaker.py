# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example D — Circuit breaker (homeostasis + protection)."""
from time import monotonic


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_after: float = 10.0):
        self.failure_threshold = failure_threshold
        self.reset_after = reset_after
        self.failures = 0
        self.opened_at = None

    def allow_request(self) -> bool:
        if self.opened_at is None:
            return True
        if monotonic() - self.opened_at >= self.reset_after:
            return True  # permit a trial request (half-open behavior)
        return False

    def record_success(self) -> None:
        self.failures = 0
        self.opened_at = None

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold and self.opened_at is None:
            self.opened_at = monotonic()


if __name__ == "__main__":
    cb = CircuitBreaker(failure_threshold=2, reset_after=5)
    cb.record_failure()
    cb.record_failure()
    print("allow_request after 2 failures:", cb.allow_request())
