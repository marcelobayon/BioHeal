# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example A — Approved fallback provider (opportunism + redundancy)."""
from dataclasses import dataclass
from typing import Callable


@dataclass
class Provider:
    name: str
    fetch: Callable[[], str]


def primary_provider() -> str:
    raise ConnectionError("Primary provider unavailable")


def secondary_provider() -> str:
    return "result from approved secondary provider"


APPROVED_PROVIDERS = [
    Provider("primary", primary_provider),
    Provider("secondary", secondary_provider),
]


def fetch_with_fallback() -> tuple[str, str]:
    failures = []
    for provider in APPROVED_PROVIDERS:
        try:
            result = provider.fetch()
            if not isinstance(result, str) or not result.strip():
                raise ValueError("Provider returned an invalid result")
            return result, provider.name
        except (ConnectionError, TimeoutError, ValueError) as exc:
            failures.append(f"{provider.name}: {exc}")
    raise RuntimeError("All approved providers failed: " + "; ".join(failures))


if __name__ == "__main__":
    result, provider_name = fetch_with_fallback()
    print({"result": result, "provider": provider_name})
