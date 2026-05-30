# Required Agent Roles

Krypton can run in a single-agent harness, but it is designed for operators who
can assign narrow roles. Use these roles when the platform supports them.

## explorer

Read-only mapper. Answers one bounded question before planning or execution:
source of truth, read path, write path, contract boundary, unsafe files,
displaced path, cutover risk, and evidence gate.

Do not let explorers edit files or write implementation plans.

## plan-reviewer

Alignment gate. In `MODE: PRE`, checks whether the plan is ready to execute. In
`MODE: POST`, checks whether the final implementation still matches the plan's
intent, ownership, contract, cutover, displaced path, and evidence gate.

## reviewer

Runtime correctness gate. Checks user-visible behavior, security, data
integrity, trust boundaries, source freshness, and missing acceptance evidence.

## maintainer

Codebase-shape gate. Checks duplicate paths, stale artifacts, unclear ownership,
oversized files, unnecessary abstractions, coupling, migration hygiene, and
future operator confusion.

## verifier

Reality gate. Runs or inspects the smallest proof from the real path: browser
state, API payload, persisted record, trace, rendered artifact, CLI output, or
other target-perspective evidence.

## Default Operating Limits

- Use explorers before broad source reading.
- Keep implementation in the main agent by default.
- Use agents for exploration, review, maintenance, and verification gates.
- The main agent owns integration and final coherence.
- Tests, diffs, and agent claims are supporting evidence, not completion proof.
