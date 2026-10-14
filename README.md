# BioHeal
An experimental framework for biology-inspired self-healing software, combining adaptive recovery strategies, automated testing, controlled repair, and reproducible resilience experiments.

Research question: Does a test-verified recovery loop outperform ordinary error handling under controlled dependency failures?

System A — Baseline
A program with standard error handling that reports a failure when its primary service is unavailable.

System B — Static fallback
A program that switches to a predefined backup without automatically verifying its correctness.

System C — BioHeal
A program that detects the failure, selects a fallback, runs verification tests, and rolls back or reports failure if verification fails.

Measure:
- Recovery rate: Percentage of injected failures followed by successful recovery.
- Recovery time: Time from failure detection to restored service.
- Correctness: Percentage of recovered operations that return valid results.
- False recovery rate: Percentage of cases incorrectly reported as recovered.
- Overhead: Additional CPU time and memory consumption.
- Repair safety: Percentage of attempted changes rejected when they fail verification.
