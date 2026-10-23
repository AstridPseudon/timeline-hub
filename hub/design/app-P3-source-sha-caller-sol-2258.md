**READY_CALLER.** Corrected only P3 row 245 in `tests/suites.conf`: both source gates now bind the full source and matching guard data. Source variables and `PLAYWRIGHT_OUTPUT_DIR` are exported before prefix stages and through eval into the mounted leaf and final body.

- Source: `4a7b45df4f77d2b7a1a50233f1d83dfed0e419b8`
- Tree: `370ada18715b387a3987d7829f9ee4e2a2492bb5`
- Row SHA256: `79d66301690dfcc12b22cca653d1f33d55de71053f80781d5c80041f0b78f70c`
- Preserved outside-row SHA256, 246 rows: `44c049291d0114499c0122d8e8accc75fc9f5b79b6dd307b7a1301335e00f386`

Commands run with `TMPDIR=/tmp/w-7d121eb2af`:

| Command | Result |
|---|---|
| `python3 "$TMPDIR/qualify.py"` | PASS: 58 guards, 58 closed faults, capture17/innerparse/evalparse stop following stages |
| `python3 "$TMPDIR/controls.py"` | PASS: 12 caller controls; exact and synthetic positives; required negatives stop before setup |
| `python3 "$TMPDIR/additional.py"` | PASS: truncated P3APP reproduces the original closed failure |
| `python3 "$TMPDIR/audit.py"` | PASS: 19 exact carrier/tail values |
| `python3 "$TMPDIR/structure.py"` | PASS: seven replacements only; bodies and complete tail unchanged |
| `python3 "$TMPDIR/install-row.py"` | PASS: fresh-read atomic replacement and readback |
| `/bin/bash -n "$TMPDIR/after.inner"` and `after.outer` | PASS |
| `git diff --check`; `git status --short` | PASS; App worktree clean |

Actual invocation is argc 2: `-c` plus the byte-exact **40,564-byte payload**. Both positives execute intercepted stages once in order. Eleven exported values match at all six stage boundaries.

Preserved original body `37caf285…`, native21/history, private80/`819acf…`, pins, toolchain, guards and limits. Prefix heap remains 6144 MiB; inherited mounted/body heap remains 4096 MiB; native timeout remains 300s.

One probe temporarily changed the local dependency link; it was restored. Shared package contents were untouched.

No service/browser/backend journey ran. Actual17178 remains original-body-NOTRUN. Pending: manager accepts the meaningful shared-leaf exact source before requesting P3 execution. Commit message and `DONE` created.