## FAIL — app-P3-solo-caller-0955

Reviewed commit `1d92503b4c`; only the two permitted caller artifacts differ. No product files changed.

Findings:

1. P3-only custody is not implemented. `SUITES` still selects P2 and P3, computes 248 outsiders, and rewrites P2’s source/tree/parent. P3-alone requires 249 outsiders including byte-preserved P2.

2. `mechanical_controls()` claims `argv: argc=2`, but the decoded commands contain no argc/`$#`/`process.argv` guard. Supported `bash -c "$CMD"` invocation supplies zero positional arguments. This is an unverified/fabricated control.

3. Source custody is circular and unsupported. `final_source_input()` requires a pre-existing hashed `source_receipt` before any service request, but `test-run` creates the recycled worktree/snapshot only after request. Existing dispatcher metadata/report and queue markers exist; no generic `source_receipt` format exists. The authentic source `82cb…` has two parents, while the caller also requires a single-parent source.

4. C0 reply inventory omits `dependencies`.

Checks:

- `python3 -m py_compile caller-publication.py` — PASS
- `python3 -m json.tool caller-custody.json` — PASS
- `git diff --check 1d92503b4c^ HEAD` — PASS
- Actual decoded rows: P2 = 60 fingerprints, P3 = 106 — PASS
- Both decoded rows `bash -n` — PASS
- P3 source/tree/parent/body rebind model — PASS
- Existing custody: 4 clients, 78 backend files, 80 graph files — PASS
- Forced decoded P3 preflight — exit 2 with `original-body-NOTRUN`; no browser/backend stage reached — PASS
- Missing-manifest and pre-request manifest-without-receipt refusals — PASS

Minimal repair: select/rebind only P3 and count 249 outsiders; leave P2 outside unchanged. Replace the false argc claim with an executable check matching the supported invocation. Use existing dispatcher metadata/report and normal `test-run` snapshot identity after request; do not require or invent a pre-request generic receipt. Add `dependencies` to the reply inventory.

No row installation, service request, browser/backend run, build, provision, or full suite was performed.