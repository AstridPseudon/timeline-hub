## PASS — P3/D53 caller review

Changed only [caller-publication.py](/home/user/work/wt/app-P3-D53-caller-cumulative-1206/caller-publication.py).

- Fixed caller-supplied final-manifest refusal.
- Authenticated final HOME `602f8b1f…`, tree `a3884497…`, parents `2e3c8f65…` + `2357df92…`.
- Authenticated P2/P3 rows and 248 outside rows (`6a45d056…`, `23226c27…`, `b9c97fbb…`).
- Compared all five final D53 source bodies against reviewed hashes.
- Replaced authentication `assert`s with explicit refusals; verified under `python -O`.
- Preserved full wire-field contract and honest PREPARED limits.

Tests/checks:

- AST/JSON parse: PASS.
- `git diff --check`: PASS.
- Private full PREPARED generation: PASS; 5 source paths, 117 guards.
- Optimized private PREPARED generation: PASS.
- Forged final/pure manifests: REFUSED.
- Synthetic P2/P3 row mutations: REFUSED in normal and optimized modes.
- Generated caller wrappers passed `bash -n`.
- Diff scope: exactly one allowed file.

Remaining real inputs: live integrated P3 execution and daemon identity. No install, browser, daemon, or full suite was run.

Commit message written and `DONE` marker created.