# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example E — Candidate configuration mutation with verification."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    timeout_seconds: float
    max_retries: int


def verify(config: Config) -> bool:
    # Replace with real tests and policy checks.
    return 0.5 <= config.timeout_seconds <= 10.0 and 0 <= config.max_retries <= 3


def candidates(current: Config) -> list[Config]:
    return [
        Config(timeout_seconds=2.0, max_retries=current.max_retries),
        Config(timeout_seconds=current.timeout_seconds, max_retries=1),
    ]


def select_candidate(current: Config) -> Config:
    for candidate in candidates(current):
        if verify(candidate):
            return candidate
    return current  # retain known configuration if none pass


if __name__ == "__main__":
    original = Config(timeout_seconds=1.0, max_retries=2)
    print(select_candidate(original))
