# Krypton Distribution Growth Implementation Plan

**Intent:** Make Krypton spread through install surfaces, committed goal artifacts, and an enforceable PR gate instead of manual promotion.
**Current Behavior:** Krypton has skills and plugin metadata, but the public path still reads mostly as a prompt pack and does not give teams a reusable gate.
**Expected Outcome:** The repo presents Krypton as the goal-based planning and proof gate, installs through `skills`, exposes a Codex repo marketplace, ships goal package templates, and provides a GitHub Action for PR enforcement.
**Target-Perspective Output:** A maintainer can install Krypton, copy a workflow, and see code changes fail without `PLAN.md`, `GOAL.md`, and `EVIDENCE.md`.
**Truth Owner:** The Krypton repo owns its install docs, skill prompts, plugin manifests, goal templates, and PR gate script.
**Contract Boundary:** The public contract is the goal package shape under `docs/goals/<slug>/` plus the `scripts/check-krypton-goal.py` CLI and `action.yml` composite action.
**Cutover:** The documented workflow moves from `PLAN.md + GOAL.md` to `PLAN.md + GOAL.md + EVIDENCE.md`.
**Displaced Path:** Manual-only promotion is demoted; installed skills, marketplaces, and PR gates become the dominant growth path.
**Value Density:** One small gate script, templates, and install docs turn the repo into infrastructure teams can adopt.
**Evidence Gate:** Unit tests, repo validation, scanner output, and install smoke tests must pass from the final implementation state.
**Acceptance Evidence:** Local unit tests, repo validation, scanner output, and an install smoke test must pass.
**Evidence Lane:** CLI tests, validator output, scanner output, and skills CLI smoke test.
**Kill Criteria:** If the gate blocks normal docs-only work or cannot be explained in one workflow snippet, simplify or remove it.
**Architecture Slice:** Modify README, manifests, skills, templates, validation, scripts, and GitHub Action files only.
**Plan Review Gate:** Requires self-review before final handoff.

## Tasks

1. Task: Add a PR gate CLI with tests.
   Files allowed: `scripts/check-krypton-goal.py`, `tests/test_check_krypton_goal.py`
   Files forbidden: unrelated skills or package metadata
   Output: A local CLI that fails code changes without a goal package.
   Verification: `python3 -m unittest tests.test_check_krypton_goal`
   Acceptance evidence: Test output showing all focused gate tests pass.
   Parallel safe: no

2. Task: Add public goal package artifacts.
   Files allowed: `templates/goal-package/*`, `docs/goals/krypton-distribution-growth/*`, skill prompt files
   Files forbidden: demo repos or demo PRs
   Output: `PLAN.md`, `GOAL.md`, and `EVIDENCE.md` are the documented workflow.
   Verification: `./scripts/validate.sh`
   Acceptance evidence: Validator output and this committed goal package.
   Parallel safe: no

3. Task: Add marketplace and install surfaces.
   Files allowed: `README.md`, `.agents/plugins/marketplace.json`, `.codex-plugin/plugin.json`, `.claude-plugin/*`
   Files forbidden: unrelated generated marketplace repos
   Output: skills.sh install command, Codex repo marketplace, and clearer goal-based positioning.
   Verification: JSON validation plus skills CLI smoke test.
   Acceptance evidence: `npx skills add jturntdev/krypton --all --copy` succeeds in a temp directory.
   Parallel safe: no

4. Task: Add reusable GitHub Action gate.
   Files allowed: `action.yml`, `.github/workflows/krypton-goal-gate.yml`
   Files forbidden: unpinned third-party GitHub Actions
   Output: Other repos can add `uses: jturntdev/krypton@main` after checkout.
   Verification: Local gate CLI and repo validator.
   Acceptance evidence: Gate validates this change's goal package.
   Parallel safe: no
