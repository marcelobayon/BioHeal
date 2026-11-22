# Research hypotheses and open questions

These guide BioHeal's experiments. Treat every item as a hypothesis to test, not
a settled result. Publish negative results.

## Primary research question

Does a test-verified recovery loop outperform ordinary error handling under
controlled dependency failures?

## Hypotheses

1. A verification gate meaningfully reduces the **false recovery rate** versus a
   static fallback (System B), at an acceptable overhead cost.
2. Classifying failures (timeout vs. connection vs. stale output) and choosing a
   strategy per class recovers more correctly than a single blanket retry.
3. Bounded candidate generation + verification improves recovery without
   increasing security risk beyond an acceptable threshold.
4. Most of the reliability gain comes from a small number of strategies (retry,
   approved fallback, rollback) rather than from elaborate repair.

## Open questions (charter §15)

1. Which first use case has the clearest measurable pain: API failover, workflow
   recovery, queue/worker recovery, or configuration rollback?
2. Which recovery actions are safe to run without human approval?
3. What evidence is required before a recovery can be called successful?
4. Can a system distinguish an unavailable dependency from one returning
   plausible but incorrect data?
5. What is the operational cost of continuous verification?
6. How should a self-adaptive system explain its decisions to operators and
   downstream agents?

## Method

Compare at least three implementations (A baseline, B static fallback, C
BioHeal) across the scenarios in `BIOHEAL_PROJECT.md` §12. Define the failure
injection method, record versions and environment, repeat runs, and report:
recovery rate, time to recovery, correctness, false recovery rate, rejection
rate, overhead, human intervention rate, and cost per successful recovery.

## Evidence boundaries

Biological analogies generate hypotheses; they do not prove a mechanism works.
Tests are incomplete models of correctness — use layered verification and
conservative deployment. Verify all bibliographic details before citing them.
