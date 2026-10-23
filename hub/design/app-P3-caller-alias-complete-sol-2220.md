**READY — caller qualification passes.**

Changed only `app ap2-P3-gate5-h6-0348`, row 245 of `suites.conf`:

- Bound `AG` and `RT` to verified `ASTRID_CHECKOUT` and `ASTRID_RUNTIME_CHECKOUT`.
- Moved the unchanged source guards and private graph selection before setup. Inspection proved setup previously used shared Composition `0.0.10` before selecting private `0.0.14`.
- Atomic current-read replacement preserved all 246 other rows, including concurrent P2 changes.

With `TMPDIR=/tmp/w-f85e2ea634`, exact validation commands were:

| Command | Result |
|---|---|
| `python3 "$TMPDIR/qualify.py" > "$TMPDIR/qualification.final.log" 2>&1` | PASS |
| `python3 "$TMPDIR/structure.py" > "$TMPDIR/structure.log" 2>&1` | PASS |
| `/bin/bash -n "$TMPDIR/after.inner"` | PASS |
| `/bin/bash -n "$TMPDIR/after.outer"` | PASS |
| `python3 "$TMPDIR/install-row.py"` | Atomic replacement/readback PASS |
| `git diff --check` | PASS |
| `git status --short` | Empty; App worktree clean |

Qualification proves:

- **58/58 guards PASS; 58 individually injected faults closed before graph/setup.**
- Six bad App/Agent/tree/body/receipt/path prefixes exit 2.
- Capture exit 17, inner-parse and eval-parse failures produce **zero tail or stage attempts**.
- Real inner exporter → capture → eval → entire intercepted tail resolves all **19 audited values** correctly in a clean environment.
- Actual argv is exactly two arguments: `-c` plus the byte-exact **40,062-byte** payload.
- Success stages execute once, in order: graph selection → setup → availability → native/history → collection → mounted leaf → original selector.
- Original native21 assertions, history commands, locked body `37caf285…`, and final exact grep remain unchanged. Product projection differs from `2107e187…` only in the seven harness paths.

Final SHA256 records:

| Artifact | Bytes | SHA256 |
|---|---:|---|
| Row | 44,756 | `0948f6d660ce296bc64e321ebf92c6654927bb9ececda4c3d91cab4df6986810` |
| Complete outer | 44,730 | `87555b9fabdbba50ee7a24876f089415eaa3eed65bead71c7eecf35ed6f4fc22` |
| Inner payload | 40,062 | `59a7f318f4ffb4315b826acbe7c101d322002a248d016b61ba8d68e5d0e915f8` |
| NUL-separated argv | 40,066 | `ea8f2865029cb123ee04915e582171c20425999158fd2274e0518e7fdb87649d` |
| Complete post-payload tail | 3,872 | `0ec3e4aeecc2dc574006b4a7769c9e700ade1370309fdeef147bf53b982e83dd` |
| Preserved outside-row bytes | 472,776 | `0e8beff8d563d432a8462fa4d5890506f7f451ad39de5633f1a5d4cfdd8d67be` |
| Complete config | 517,532 | `70bc854b59d8d1b1726086b927aef45f7e23d9cfb3f2446ee8f3d06f5043fe95` |

No product, source, test, pin, dependency or assertion changes. No external stages or test-service requests ran. Original result **5262 remains FAIL**, unchanged.

No blockers. Wrote the conventional P3 commit message and `DONE`. Next step: manager submits the **one changed managed request**; actual journey execution remains unverified.