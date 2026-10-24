## Result: PASS — cumulative security authority

Reviewed joined source `94204351a976b483fa712316d6637cb7f548d24c` (tree `51f5b942700027037773a9610df24081bce086fb`).

- Component `234eeb443` and exact component test blobs retained.
- Normal create, staging, relocation, final verification, Store keying, and reuse bind Farm plus bootstrap authority.
- Source archive/blob/mode custody, test2 partition, ownership, links, races, inventory, lock/client/source mismatches, and forged inputs fail closed.
- No installer runs before valid Farm input authentication.
- Trusted OS/interpreter/Git and same-UID limitations remain explicit.
- Authentic schema commit remains unavailable; no live installation or real child qualification is claimed.

Required suite:

```text
267 passed, 1 failed, 1 warning
```

The sole failure is the inherited baseline assertion: joined candidate remains `e4c0a9…`, while the reviewed installed maker is `c1197e…`. This is an acceptance reconciliation issue, not a new security failure.

Independent baseline branch `62cac4dcb` was tested in a private snapshot with the exact original selector:

```text
1 passed
```

Its diff from `ab6d49bfb` is limited to `make-child-venv.baseline` and the two permitted manifest hashes; required SHA is `c1197e1a3407e970c02ff50519f800296905b89ad113ad32b9a41516a50fa3b6`.

Other checks passed: Ruff, bash syntax, source mypy, normalized parent/candidate mypy (9/9 identical, zero new), in-memory compilation, helper/component pins, manifest hashes, original test equality, lock `236d5be9…`, reserve check, and `git diff --check`.

No production source was changed. No broad acceptance PASS or live Farm/child qualification is claimed until the separate mechanical baseline join makes the actual joined tree green. DONE marker and commit message were written.