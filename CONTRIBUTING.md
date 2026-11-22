# Contributing to BioHeal

BioHeal is an open research project. Contributions of code, experiments,
documentation, and honest negative results are all welcome.

## Principles

- **Verified recovery, not silent success.** Any recovery path must prove its
  result with a verification gate. "The error disappeared" is not acceptance.
- **Bounded and auditable.** Recovery actions are explicit, allowlisted, and
  budgeted. No arbitrary code execution, no silent package installation.
- **Honest claims.** Do not describe the project as production-ready, fully
  autonomous, or guaranteed. Demonstrate specific behaviors and publish their
  measured limits — including negative results.

## Definition of done for a recovery strategy (charter §13)

A strategy is not complete until it has: a documented failure condition;
explicit preconditions and permissions; a bounded execution budget; a
verification procedure; a failure/rollback path; unit and integration tests; a
structured event and error code; troubleshooting guidance; and a measurement in
the experiment suite.

## Development

```bash
pip install -e ".[dev]"
pytest          # tests must pass
ruff check .    # lint must pass
mypy            # strict type-check must pass
```

Keep the core standard-library only where practical. Add runtime dependencies
only with a clear justification.

## Pull requests

- Keep changes focused and tested.
- Explain the failure condition and verification criteria for new strategies.
- Update `docs/` and `examples/` when behavior changes.
