# Example: Cutover Plan

Weak request:

```text
Build the new adapter next to the old adapter and we will switch later.
```

Krypton correction:

```text
Current behavior: Old adapter owns the payload.
Expected outcome: New adapter owns the payload after proof.
Cutover: Add compatibility shim for one release, redirect reads to the new adapter,
and mark the old adapter legacy with a removal issue and date.
Displaced path: Old adapter.
Kill criteria: If the new adapter cannot match fixture output and live trace,
delete the new path instead of keeping both current.
Acceptance evidence: Fixture parity, live trace, and one inspected downstream response.
```

The point is not to avoid temporary shims. The point is to make the temporary
state honest, owned, and removable.
