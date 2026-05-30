---
name: krypton-execution
description: Use when executing an approved Krypton plan, GOAL.md, or implementation plan that already defines intent, ownership, contract, cutover, task boundaries, and acceptance evidence. Use for coordinated coding-agent execution with explorer, worker, reviewer, maintainer, or proof gates.
---

# Krypton Execution

Krypton Execution runs an approved plan without drifting from its ownership, cutover, and evidence contract.

## Entry Rule

Do not invent the plan inside this workflow. If no approved plan, goal document, or clear task board exists, ask for one direct input or use Krypton Planning first.

Before work starts, restate:

```text
Goal:
Plan path:
Intent:
Truth owner:
Contract boundary:
Cutover:
Displaced path:
Acceptance evidence:
Kill criteria:
Forbidden moves:
```

## Task Board

Turn the plan into an ordered board:

```text
Task:
Owner:
Input:
Files allowed:
Files forbidden:
Output:
Evidence:
Depends on:
Parallel safe:
```

Run tasks in parallel only when inputs and write scopes are independent. Keep at most two active workers at once when the harness supports agents.

## Execution Loop

For each task:

1. Confirm the task still matches the plan contract.
2. Gather only the context needed for the task.
3. Dispatch a bounded worker when useful, or edit directly when the change is small.
4. Review every worker result before integration.
5. Check for wrong owner, duplicate path, missing cutover, contract drift, and weak proof.
6. Commit or checkpoint only the current task files when the local workflow expects commits.
7. Update the task board.

The main orchestrator owns final coherence. Do not blindly merge worker output.

## Evidence Gate

Do not call the goal complete because tests, lint, typecheck, or diffs passed. Those are supporting checks.

Completion requires target-perspective evidence, such as:

- UI or visual change: browser state, screenshot, or rendered output.
- API or data flow: request/response, fixture, trace, or persisted record.
- CLI or workflow: command plus important output proving the behavior.
- Migration or cutover: old path deleted, redirected, demoted, or shimmed with a removal trigger.
- Hidden logic: deterministic artifact showing the intended result.

If evidence cannot be captured, report the blocker and say `implemented but unproven`.

## Final Gates

Before final response:

1. Run POST plan review when the plan had a review gate.
2. Run correctness review for behavior, data integrity, trust, and missing evidence.
3. Run maintainability review for duplicate paths, stale artifacts, coupling, and unclear ownership.
4. Fix important findings or record why they remain.
5. Summarize changed artifacts, acceptance evidence, review result, and blockers.
