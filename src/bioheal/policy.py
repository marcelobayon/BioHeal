"""Stage 3 policy: a deny-by-default allowlist of what recovery may do.

The charter's safety model is deny-by-default with explicit allowlists and
bounded budgets. A strategy that is not named is not permitted.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Policy:
    """Bounds and permissions for a recovery attempt."""

    allowed_strategies: frozenset[str] = field(default_factory=frozenset)
    max_attempts: int = 3
    time_budget_s: float = 10.0
    allow_promotion: bool = True

    def permits(self, strategy: str) -> bool:
        """Deny by default: only explicitly allowlisted strategies pass."""
        return strategy in self.allowed_strategies

    @classmethod
    def allowing(cls, *strategies: str, **kwargs: object) -> "Policy":
        """Convenience constructor: ``Policy.allowing("cache", "replica")``."""
        return cls(allowed_strategies=frozenset(strategies), **kwargs)  # type: ignore[arg-type]
