**NOTREADY — authorized repairs complete; another retained caller defect blocks readiness.**

Changed only `app ap2-P3-gate5-h6-0348` in `suites.conf`:

- Rebound all six stale metadata guards to actual HEAD `6c33025b…`, tree `80addcc5…`, parent `9cb841ed…`, harness blob `793f49af…`, and selected test SHA.
- Grouped the outer tail behind capture/eval success; made the four P1 diagnostic guards terminal on failure.
- Preserved the complete inner payload, native/history checks, all guards, mounted leaf, and original final selector.
- Atomic current-read replacement preserved all 246 outside-row lines, including concurrent P2 changes. App worktree remains clean.

Validation with `TMPDIR=/tmp/w-733c600671`:

| Command/control | Result |
|---|---|
| `/bin/bash -n "$TMPDIR/after.outer"` and `intended.inner` | PASS |
| `/bin/bash "$TMPDIR/guards"` | 58/58 PASS |
| `/bin/bash "$TMPDIR/static.prefix"` | Exit 0; authentic source, receipts, origins, integrity and toolchain checks; stopped before setup |
| Six bad App/Agent/tree/body/receipt/path prefixes | All exit 2, body-NOTRUN |
| `python3 "$TMPDIR/qualify.py" > "$TMPDIR/qualification.log" 2>&1` | Exact whole-outer argv: argc 2, payload byte-exact |
| Capture exit 17 / inner parse / eval parse | Exits 17/2/1; **zero tail, graph, setup, leaf or body attempts** |
| 58 individually failed guard controls | All exit 2 before graph attempts |
| Intercepted success | Tail stages execute once, in order |
| `git diff --check` | PASS |

**Remaining defect:** the real inner exporter emits `ASTRID_CHECKOUT` and `ASTRID_RUNTIME_CHECKOUT`, but the retained tail assigns `AG="$P3AG"` and `RT="$P3RT"`. Neither alias is exported. `/bin/bash "$TMPDIR/alias.roundtrip"` produced `AG=<> RT=<>`, exit 1. I preserved these assignments because changing command content exceeds the specified six rebindings and connector repair. Next step is a mechanical alias-binding repair, then repeat the static caller qualification.

Final SHA256 records:

| Artifact | SHA256 |
|---|---|
| Row, 44,238 bytes | `01c4a3140f7cd666c049a6daba46b79d28c1d5c6d4a5d08132e55c7131207c05` |
| Unchanged inner, 28,941 bytes | `23111506eaa17ce3e11c3db71aa71a93245bad7ac89b95aaaf0cfa51ece97880` |
| Captured NUL-separated argv | `c573197ffcc1fcbd7802a59532aac27ee581a57d1f1d66d35c8da6e888a683cb` |
| Outside-row bytes, 471,612 bytes | `92bd8b9ebe26f6c37676c51c0b4d0a3be91ad48f3b75030d8d562cba7ab6a12e` |
| Complete resulting config, 515,850 bytes | `9f81196850d0abe4885c9526fa2727f7540fc729a3382bc471fb723cc04d8d74` |

The actual tree differs from `2107e187…` only in the seven harness paths; original body blob remains `37caf285…`. Result **5262 remains FAIL**, unchanged and unrepeated. No dependency mutation, setup, backend, service request, leaf, body, browser, or Git write occurred.

Wrote the P3 commit message and `BLOCKED`; no `DONE`.