# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example C — Lazy loading (resource efficiency)."""


def create_report(data: list[dict], include_visuals: bool = False) -> dict:
    report = {"row_count": len(data), "data": data}

    if include_visuals:
        # Import optional dependency only when needed.
        try:
            import matplotlib.pyplot  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "Visual reports require the optional 'matplotlib' dependency"
            ) from exc
        report["visuals_available"] = True

    return report


if __name__ == "__main__":
    print(create_report([{"a": 1}, {"a": 2}]))
