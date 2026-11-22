# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example F — Rollback to known-good configuration (repair + reversibility)."""
from copy import deepcopy


class ConfigStore:
    def __init__(self, initial: dict):
        self.current = deepcopy(initial)
        self.known_good = deepcopy(initial)

    def promote(self, candidate: dict, test) -> bool:
        if not test(candidate):
            self.current = deepcopy(self.known_good)
            return False
        self.current = deepcopy(candidate)
        self.known_good = deepcopy(candidate)
        return True

    def rollback(self) -> None:
        self.current = deepcopy(self.known_good)


if __name__ == "__main__":
    store = ConfigStore({"timeout": 1.0})
    ok = store.promote({"timeout": 99.0}, test=lambda c: c["timeout"] <= 10)
    print("promoted:", ok, "current:", store.current)
