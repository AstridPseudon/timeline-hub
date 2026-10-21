# Run-on-main result: App automatic current

Status: **REFUSED-PREFLIGHT**

The one authorized actual was not run. The packet ends with a HOME dispatch
hold dated 2026-10-21 10:40 UTC, and the current custody review at
`design/auto-main-command-custody-1040.md` still says:
`HOLD — necessary literal corrections remain.` The hold explicitly prohibits
consuming the one actual until the literal packet corrections and HOME’s
clearance are present.

## Exact source tuple

No source fetch, checkout, preflight, or source verification was performed
because the packet was still under the explicit HOME hold. Therefore no
commit/tree pair is verified by this run. The required, unverified tuple is:

| purpose | commit | tree |
|---|---|---|
| App under test | `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf` | `8e242d1497841f391b6152ecd8d204143fa03b52` |
| approved R51 admission fix | `02ac224cd3c0d376f08b6129f58ded624f3e400d` | `aed5248fada10bdd2c74da4d3b3c2515671cc1ed` |
| current readiness fix | `da5d6d564af58ad06f126188c25e9a47f4e45be4` | `1a3489722e87faa38d843a650fd668637363e934` |
| Agent pin | `6efc81500a0e0688c2bb41e736503f0fc3e04abb` | `2ed2b8a12b5b3391ca221ba6ff05390f71a73556` |
| Runtime pin | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` | `d3a290b407fa61e6ab2d476f50c068073f70df00` |

## Command and counts

The exact preflight command in
`design/run-on-main-app-automatic-current.md` was not run. The exact
Playwright command in that packet was not run.

- preflight: 0 started, 0 passed, 0 failed
- Playwright collection: 0
- Playwright passed: 0
- Playwright failed: 0
- duplicate actuals: 0
- retained HTTP failures: unavailable; no evidence tree was created

Expected main evidence paths were not created because no process started:

- `/home/user/work/tl-auto-current-1490fbfe9/evidence/automatic-current/playwright.log`
- `/home/user/work/tl-auto-current-1490fbfe9/evidence/automatic-current/trace.zip`
- `/home/user/work/tl-auto-current-1490fbfe9/evidence/automatic-current/error-context.md`

Failure classification: **missing authorization / stale packet corrections**,
not a product, harness, or environment failure. The custody review requires
the packet to add and correct literal executable checks before HOME clears the
hold. Nothing was run, and no product code, test, config, branch, or shared
dependency was modified.

Not run: `git fetch hub`, exact-ref/tree verification, keeper setup, all
preflight checks, Playwright `--list`, browser/Runtime/Vite startup, and the
one mandatory browser actual.
