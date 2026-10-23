**FULLFINALREADY — caller qualification only.**

Changed only P3 row 245 in `tests/suites.conf`, binding both donor files and rejecting abbreviated HEAD identities while preserving the authorized synthetic single-parent route.

| Binding | Exact value |
|---|---|
| Source | `82de83a0b2be5d92e4943c18ff1cbf9aeeca753e` |
| Tree | `7871e4d2e3d9efaf093a7274c2b0662fa74536f6` |
| Parent | `42c195769678e96b913af899436a555ee70c04a5` |
| Row SHA256 | `0d356b4fe2182d76dbab9962572c398334df1a2da64f3ea9b5a70737d27e5cb0` |
| Outside SHA256 | `2593c4c0db5352674274d2e27cf487493f0a0288838d7a0b1d2ff8365746da7c` |

All 246 outside rows remained byte-exact.

Commands passed with `TMPDIR=/tmp/w-85e10e5512`:

- `python3 "$TMPDIR/qualify.py"` — 58 guards, 58 closed faults, real argc2/byte-exact payload, carrier failures and ordered success.
- `python3 "$TMPDIR/controls.py"` — 12 caller controls, including exact and synthetic positives.
- `python3 "$TMPDIR/additional.py"` — seven additional controls, including authorized-parent/39hex rejection and build/leaf failure stopping.
- `python3 "$TMPDIR/audit.py"` — 19 exact carrier/tail values.
- `python3 "$TMPDIR/structure.py"` — original stages/tail preserved; inner/outer Bash syntax passed.
- `python3 "$TMPDIR/install-row.py"` — atomic fresh-read replacement and exact readback.
- `git diff --check`; `git status --short` — passed; App worktree clean.

Original native/history assertions, Gate-5 body/selector, pins, private graph, diagnostics export and limits remain unchanged. Failure-control files remain in TMPDIR.

**NOT RUN:** actual build/setup/native/list/readiness/browser/backend/service or full suite. No product-readiness claim. No blockers; commit message and `DONE` written.

Next: manager submits one changed P3 run targeting this worker, parallel with P2.