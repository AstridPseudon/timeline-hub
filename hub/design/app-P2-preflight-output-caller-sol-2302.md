**READY_CALLER.** Changed only the existing P2 row in `tests/suites.conf`:

- Export the validated actual-run `PLAYWRIGHT_OUTPUT_DIR` before the leaf.
- Clear inherited Node/dist overrides before preflight and body.
- Preserve `fa702ec…`, private graph, Node20/npm10, heap6144, native/history checks and original eight-test tail.

Validation:

- `python "$TMPDIR/qualify_p2.py"` — **15 scenarios passed**: exact `bash -c` payload, clean-environment export/eval, leaf/body environment, stage order and failure stops.
- `python "$TMPDIR/audit_p2.py"` — **passed** source/tree/parent, original eight tests and byte-preservation checks.
- `bash -n "$TMPDIR/outer-after.sh"` and `bash -n "$TMPDIR/inner-after.sh"` — **passed**.
- `git diff --check` — **passed**; worktree clean.

Outside-row bytes matched exactly at the atomic write. Final comparison found only the concurrent P3 worker’s separate row change.

Row SHA256: `e612d9a8ab0562d699b64a4178336ec02db3f4fff4d1b57fb19eb74bd61c25ac`

No actual service, build, browser journey or full suite ran. **Source leaf remains pending worker 2258**; manager must qualify and rebind it before the actual run. Commit message and `DONE` created.