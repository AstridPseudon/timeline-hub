# D134 map-check validation

## Read-only checks

- `git rev-parse HEAD` and `HEAD^{tree}` — PASS: `a30e74e901a28b39c28facba3deb00d76f186e23` / `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`.
- Current source SHA-256, byte-count, AST-function, and assertion-count comparison against the author `source-manifest.json` — PASS for the original helper and all six cohort files.
- Predicate-map JSON parse, exact selector count, distinctness, and partition sum — PASS: 30 declared, 30 distinct, 30 partitioned.
- Held-source hash via `git show 42040a9c05ae7105cf88459cad5f0b8b9bf56fd1:astrid/sdk/timeline/_command_state.py | sha256sum` — PASS: `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`.
- Static source anchors for current `shot_item_map`, `_item_ids`, `project_shot_items`, closure validation, and `occurrence.create` empty `items` — PASS.
- `git diff --quiet a30e74e901a28b39c28facba3deb00d76f186e23 --` — PASS; no source delta.
- JSON parsing of the author verdict, source manifest, predicate map, and this packet — PASS.

## Applicability conclusion

All six callers share the common first physical birth boundary described in
`findings.md`. The held 42040 product source has the exact positive physical
birth branch and preserves strict copied/remapped guards. No distinct
unsupported first seam or missing record was found in any of the 30 selectors.
The correction is therefore finite and source-only.

## Explicitly not run

No pytest, provider execution, Runtime service, socket, browser, setup/body,
all-tail, normal-home, P2/P4, native, profile, full suite, or current joined
original9 run was performed. No skipped, filtered, wrapper-only, historical,
or refused event was counted as a pass. No source, fixture, shared dependency,
pin, Runtime, App, schema, generated file, Git ref, or hub file was changed.
