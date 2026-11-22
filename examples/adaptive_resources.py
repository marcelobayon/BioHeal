# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example B — Resource-aware operating mode (homeostasis + efficiency)."""
from dataclasses import dataclass


@dataclass
class ResourceSnapshot:
    memory_pressure: float  # 0.0 to 1.0
    cpu_pressure: float     # 0.0 to 1.0


def choose_mode(snapshot: ResourceSnapshot) -> str:
    if not (0 <= snapshot.memory_pressure <= 1):
        raise ValueError("memory_pressure must be between 0 and 1")
    if not (0 <= snapshot.cpu_pressure <= 1):
        raise ValueError("cpu_pressure must be between 0 and 1")

    if snapshot.memory_pressure > 0.90:
        return "minimal"
    if snapshot.cpu_pressure > 0.85 or snapshot.memory_pressure > 0.75:
        return "reduced"
    return "normal"


if __name__ == "__main__":
    current = ResourceSnapshot(memory_pressure=0.82, cpu_pressure=0.60)
    print(choose_mode(current))  # reduced
