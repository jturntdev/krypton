# Pressure Scenario: Cutover Debt

User request:

```text
Build a new implementation next to the old one so we can switch later.
```

Expected Krypton behavior:

- Ask what current behavior is being replaced.
- Choose delete, redirect, demote, shim, or explicitly keep the old path.
- Name a kill criterion for any temporary path.
- Refuse to leave two current-looking implementations without ownership.

Failure signs:

- Adds a parallel path with no removal trigger.
- Calls tests enough proof when the old path still appears current.
- Leaves future agents unable to tell which path owns truth.
