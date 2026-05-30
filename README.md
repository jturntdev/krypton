# Krypton

Krypton is a planning and execution discipline for AI coding agents.

It exists to stop plausible wrong work: the feature that compiles but lives on
the wrong layer, invents a second source of truth, skips cutover, or declares
success without evidence from the real path.

## Why

Coding agents are fast enough to create architectural debt before anyone notices.
Krypton slows the first decision down so the rest of the work can move faster.

A Krypton plan must answer:

- what outcome the work serves
- what current behavior is replaced, redirected, deleted, or demoted
- who owns the truth
- what contract crosses the boundary
- what acceptance evidence proves the result
- what kill criteria prevent duplicate paths from living forever

## Install

Early public package:

```bash
git clone https://github.com/Eluticz/krypton.git
cp -R krypton/skills/* ~/.codex/skills/
```

For Claude Code-style skill folders, copy the same `skills/*` directories into
the local skills directory used by your harness.

## Skills

- `krypton-planning`: turn a request into an outcome contract, architecture
  slice, task plan, and evidence gate.
- `krypton-execution`: execute an approved plan without drifting from ownership,
  cutover, or proof requirements.

## Basic Workflow

1. Use Krypton Planning before implementation.
2. Write the outcome contract.
3. Map source of truth, read path, write path, contract boundary, and unsafe files.
4. Choose the cutover: delete, redirect, demote, shim, or explicitly keep.
5. Define acceptance evidence from the target perspective.
6. Execute with Krypton Execution.
7. Finish only when the evidence gate is satisfied.

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

This is the first public cut. It is intentionally small: two skills, a reviewer
prompt, examples, pressure scenarios, and a validation script.

## Development

Run:

```bash
./scripts/validate.sh
```

The validator checks required files, skill metadata, JSON plugin metadata, and
public-safety issues such as placeholders or private project references.

## License

MIT
