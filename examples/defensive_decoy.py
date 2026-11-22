# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example G — Defensive decoy / honeypot event (defensive deception)."""
from datetime import datetime, timezone


def record_decoy_access(resource_name: str, source_label: str) -> dict:
    # This records an event only; it does not retaliate or access the source.
    return {
        "event": "decoy_resource_accessed",
        "resource": resource_name,
        "source_label": source_label,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    print(record_decoy_access("fake-admin-token", "internal-test"))
