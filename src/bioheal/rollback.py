"""Stage 6 — Rollback: keep a known-good state and make promotion explicit.

Generalises Example F: a candidate becomes the new known-good only if it passes
verification; otherwise the store is restored to the last known-good value.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class KnownGoodStore(Generic[T]):
    """Holds a current value and the last value that passed verification."""

    def __init__(self, initial: T):
        self._current = deepcopy(initial)
        self._known_good = deepcopy(initial)

    @property
    def current(self) -> T:
        return deepcopy(self._current)

    @property
    def known_good(self) -> T:
        return deepcopy(self._known_good)

    def promote(self, candidate: T, verify: Callable[[T], bool]) -> bool:
        """Adopt ``candidate`` only if ``verify`` passes; else roll back."""
        if not verify(candidate):
            self._current = deepcopy(self._known_good)
            return False
        self._current = deepcopy(candidate)
        self._known_good = deepcopy(candidate)
        return True

    def rollback(self) -> None:
        self._current = deepcopy(self._known_good)
