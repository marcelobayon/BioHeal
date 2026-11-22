# BioHeal

An experimental, open-source framework for **verified** software recovery —
biology-inspired self-healing that combines adaptive recovery strategies,
automated verification, controlled repair, and reproducible resilience
experiments.

> **Detect. Adapt. Verify. Recover.**
>
> Self-healing here means *verified recovery* — never arbitrary
> self-modification, and never reporting success just because an error stopped
> appearing.

**Status: experimental / research.** This repository is the open-source core
and the research behind it. The `bioheal` package is a Milestone-0-level
reference implementation (bounded, synchronous, standard-library only) — useful
to read, run, and build on, but **not production resilience**. See
[`BIOHEAL_PROJECT.md`](BIOHEAL_PROJECT.md) for the full charter, roadmap, and
honest limitations. BioHeal does not prevent all failures, guarantee uptime, or
autonomously repair arbitrary software.

## The research question

Does a test-verified recovery loop outperform ordinary error handling under
controlled dependency failures? Three systems are compared:

- **System A — Baseline.** Standard error handling; reports failure when the
  primary service is unavailable.
- **System B — Static fallback.** Switches to a predefined backup without
  verifying its correctness.
- **System C — BioHeal.** Detects the failure, selects an approved fallback,
  runs verification, and rolls back or reports failure if verification fails.

Measured:
- **Recovery rate** — injected failures followed by a successful recovery.
- **Recovery time** — from detection to restored service.
- **Correctness** — recovered operations that return valid results.
- **False recovery rate** — cases incorrectly reported as recovered.
- **Overhead** — additional CPU time and memory.
- **Repair safety** — attempted changes rejected when they fail verification.

## Install

```bash
pip install "git+https://github.com/marcelobayon/BioHeal.git"
```

Python 3.10+. No runtime dependencies.

## Quick start

```python
from bioheal import RecoveryEngine, Verifier, Policy, non_empty

# A verifier decides what "recovered" actually means — not just "no exception".
engine = RecoveryEngine(
    verifier=Verifier([("non-empty", non_empty)]),
    policy=Policy.allowing("cache"),   # deny-by-default: only listed strategies run
)

def call_primary_api():
    raise ConnectionError("primary provider down")

result = engine.run(
    primary=call_primary_api,
    fallbacks=[("cache", lambda: "last-known-good value")],
    operation_id="op-1",
    component="weather",
)

print(result.outcome)    # RecoveryOutcome.RECOVERED
print(result.recovered)  # True — only because the cache result passed verification
print(result.event.to_dict())  # structured audit record
```

A fallback that returns an *empty or invalid* result is rejected as a **false
recovery**, and the engine moves on or escalates — it never declares victory on
an unverified result.

## What's in here

```text
BioHeal/
├── README.md
├── BIOHEAL_PROJECT.md              # the full product charter + roadmap
├── LICENSE                         # MIT
├── CONTRIBUTING.md
├── SECURITY.md
├── pyproject.toml
├── docs/
│   └── biological-computing-theory.md   # the biology → software theory + mappings
├── src/bioheal/
│   ├── errors.py          # stable, machine-readable error contract
│   ├── diagnosis.py       # classify a failure (timeout, connection, rate-limit…)
│   ├── policy.py          # deny-by-default allowlist + budgets
│   ├── verification.py    # verification gates — "verified, not just quiet"
│   ├── rollback.py        # known-good store + explicit promotion
│   ├── events.py          # structured audit events
│   └── recovery.py        # the detect → diagnose → verify → promote/rollback loop
├── examples/              # 10 runnable teaching examples (standard library only)
├── tests/
└── research/
    └── hypotheses.md
```

- **[`docs/biological-computing-theory.md`](docs/biological-computing-theory.md)**
  — the research: how biological principles (homeostasis, redundancy,
  opportunism, natural selection, repair) translate into bounded, verifiable
  software mechanisms, with their limits.
- **[`examples/`](examples/)** — each pattern as a standalone file you can run:
  `python examples/recovery_loop.py`.

## Develop

```bash
pip install -e ".[dev]"
pytest          # run the tests
ruff check .    # lint
mypy            # type-check (strict)
```

## Safety stance

BioHeal is designed to be bounded and auditable (charter §7): deny-by-default
permissions, explicit allowlists, no arbitrary package installation, no
arbitrary shell commands from model output, no self-overwriting of production
source, verification before promotion, rollback, and durable audit events. A
language model may *propose* a diagnosis or candidate repair, but deterministic
policy and verification decide whether anything is allowed.

## Related

The reusable, non-BioHeal-specific patterns (logging, config, generic
resilience) live in the
[Personal Engineering Kit](https://github.com/marcelobayon/personal_engineering_kit).
BioHeal builds the recovery *framework* on top of ideas like those.

## License

MIT © 2026 Marcelo Bayon. Free and open source — use it, learn from it, build on it.
