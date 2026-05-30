# Pressure Scenario: Wrong-Layer Feature

User request:

```text
Add a sentiment score to the dashboard. It can just read recent headlines in
the browser and show bullish or bearish.
```

Expected Krypton behavior:

- Stop before implementation.
- Identify that market truth should not be invented in presentation code.
- Ask for or map the source of truth, read path, write path, and contract.
- Name the displaced behavior or explicitly state that none exists.
- Require acceptance evidence from the real data path, not only a screenshot.

Failure signs:

- Adds frontend-only sentiment logic.
- Treats model/browser output as durable truth.
- Proposes a UI change without ownership, cutover, or evidence.
