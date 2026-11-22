# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example J — Provider strategy selection (specialization + adaptation)."""


def choose_storage_strategy(capabilities: dict) -> str:
    if capabilities.get("primary_region_writable"):
        return "primary-region"
    if capabilities.get("replica_writable"):
        return "replica-region"
    if capabilities.get("local_queue_available"):
        return "queue-for-later"
    return "read-only"


def describe_tradeoff(strategy: str) -> str:
    return {
        "primary-region": "Normal operation",
        "replica-region": "Failover; verify replication lag",
        "queue-for-later": "Writes delayed; do not claim persistence until confirmed",
        "read-only": "Preserve reads while disabling writes",
    }[strategy]


if __name__ == "__main__":
    s = choose_storage_strategy({"replica_writable": True})
    print(s, "-", describe_tradeoff(s))
