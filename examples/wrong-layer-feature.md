# Example: Wrong-Layer Feature

User request:

```text
Add a sentiment score to the dashboard. It can read recent headlines and show
bullish or bearish.
```

## Krypton Outcome Contract

```text
Plan title: Dashboard sentiment from owned intelligence
Intent: Let users see sentiment without making presentation code invent market truth.
Current behavior: No sentiment score exists.
Expected outcome: Dashboard renders a sentiment score produced by the intelligence layer.
Target-perspective output: User sees sentiment, label, timestamp, and source references.
Truth owner: Market intelligence producer.
Contract boundary: Typed sentiment payload exposed through the existing API.
Cutover: Dashboard reads only the producer payload.
Displaced path: No old sentiment path; explicitly forbid frontend-only derivation.
Value density: One producer payload unlocks web, CLI, and future alerts.
Acceptance evidence: API response plus browser state showing the real payload.
Evidence lane: integration + browser.
Kill criteria: Remove the score if source references or freshness cannot be proven.
```

## Architecture Slice

```text
Files to create: producer test and sentiment payload builder.
Files to modify: API route, shared schema, dashboard renderer.
Files to avoid: local browser-only scoring utilities.
Source of truth: intelligence producer.
Read path: producer -> API -> dashboard.
Write path: producer creates sentiment payload.
Contract boundary: shared sentiment schema.
Migration/cutover: no duplicate scoring path.
Acceptance evidence gate: real response and rendered state match the schema.
```
