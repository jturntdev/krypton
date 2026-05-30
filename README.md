# Krypton

Krypton is an operator discipline for running AI coding agents against serious
codebases.

It keeps production-grade codebases maintainable while agents move fast. The
failure mode Krypton is built for is not bad syntax. It is the plausible feature
that compiles while living on the wrong layer, inventing a second source of
truth, skipping cutover, or claiming success without proof from the real path.

## Why Operators Need It

Modern agents can create weeks of architectural debt in one enthusiastic
session. Krypton turns "build this" into an operational contract before the
agent touches code:

- what product or engineering outcome the work serves
- what current behavior is replaced, redirected, deleted, or demoted
- who owns the truth
- what contract crosses the boundary
- what evidence proves the result from the target person's perspective
- what kill criteria prevent duplicate paths from living forever

That contract is what lets an operator keep using agents on production systems
without letting the codebase become a pile of current-looking alternatives.

## Install

Early public package:

```bash
git clone https://github.com/jturntdev/krypton.git
cp -R krypton/skills/* ~/.codex/skills/
```

For Claude Code-style skill folders, copy the same `skills/*` directories into
the local skills directory used by your harness.

## Skills

- `krypton-planning`: turn a request into an outcome contract, architecture
  slice, task plan, evidence gate, and `/goal` handoff prompt.
- `krypton-execution`: execute an approved plan without drifting from ownership,
  cutover, or proof requirements.

## How It Works

1. Load `krypton-planning` with a feature request, bug, refactor, migration, or
   architecture goal.
2. The agent produces a goal package:

```text
docs/goals/<goal-slug>/PLAN.md
docs/goals/<goal-slug>/GOAL.md
```

3. `PLAN.md` is the full implementation plan. `GOAL.md` is the short `/goal`
   prompt or handoff prompt for the next session.
4. Paste or run the `GOAL.md` prompt in Codex or Claude.
5. Pair it with `krypton-execution` when you want the main agent to use the same
   ownership, cutover, review, and evidence discipline.
6. Finish only when the acceptance evidence is captured from the real route,
   artifact, payload, trace, browser state, or operator-visible output.

The workflow is intentionally two-stage:

```text
rough request
  -> krypton-planning
  -> PLAN.md + GOAL.md
  -> /goal handoff
  -> krypton-execution
  -> main-agent implementation + review gates + acceptance evidence
```

## Agent Roles

Krypton works best when the harness supports named agents:

- `explorer`: read-only source-of-truth and architecture mapping
- `plan-reviewer`: PRE and POST alignment checks
- `reviewer`: runtime correctness, security, and evidence check
- `maintainer`: codebase-shape, duplication, and cutover-debt check
- `verifier`: focused proof from the real path

See `agents/required-roles.md` for the role expectations. If your harness does
not support named agents, the main agent can still follow the same gates, but
independent exploration and review will be weaker.

## Prompt Files

Krypton keeps prompt templates individual instead of centralizing them into one
large prompt file. Each skill owns the prompts it actually uses:

- `skills/krypton-planning/plan-reviewer-prompt.md`
- `skills/krypton-execution/post-plan-reviewer-prompt.md`
- `skills/krypton-execution/reviewer-prompt.md`
- `skills/krypton-execution/maintainer-prompt.md`

## Example

Bad agent path:

```text
"Add sentiment to the dashboard."
```

The agent adds frontend-only sentiment logic and calls it done.

Krypton path:

```text
Truth owner: market intelligence producer
Contract boundary: typed sentiment payload
Cutover: dashboard reads producer output only
Evidence: API response plus browser state showing the real payload
```

See `examples/` and `tests/pressure-scenarios/` for more.

## Status

This is the first public cut. It is intentionally small: two skills, individual
prompt templates, agent role expectations, examples, pressure scenarios, and a
validation script.

## Development

Run:

```bash
./scripts/validate.sh
```

The validator checks required files, skill metadata, JSON plugin metadata, and
public-safety issues such as placeholders or private project references.

## License

MIT
