# Composition conflicts

Base: ORCH-owned bounded-reference scanner v1.0.1, not the active
preserve-clears v1.0.2 candidate. The patch targets exactly:

```text
owner_film_cliplook_scan.py
tests/test_owner_film_cliplook_scan.py
```

The final manager composition must apply these semantic hunks to the
preserve-clears source after retaining its required-field/optional-clear
changes. Both units edit the scanner source and synthetic tests, so a blind
whole-file replacement is unsafe. Preserve-clears owns closure validation and
version/package/archive handling; this proposal must not overwrite those
hunks or published archives.

No changes are proposed for Agent product paths, `VERSION`, README/package
metadata, ref-sanitizer logic, closure validation, or release packaging. The
final package owner should document `not_covered` and the new inventories in
the package README when composing the reviewed units.

The `not_covered` values in this proposal are intentionally bounded policy
labels: transition conversion, media look overlap, and renderer
presence/alpha/pixel coverage remain unclaimed. The transition inventory
reports canonical incoming declarations only; it does not pretend to compile
or evaluate them.
