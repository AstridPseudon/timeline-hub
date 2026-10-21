# App2 normal014 required-case verdict guard

## Result

Patched the existing normal014 App runner at
`design/normal014-app-central.sh`.

The runner now:

- selects only the exact bootstrap case title, so the already-passed current95
  neighbor is not rerun;
- reads the existing Playwright `three-products-summary.json` reporter output;
- requires exactly one matching case with status `passed`;
- turns a child exit of zero into exit 1 when the required case is missing or
  has any other status; and
- preserves a genuine nonzero child exit while still reporting a missing or
  failed required case.

The check runs before the existing common-helper EXIT trap removes the private
run root. No new DTO, result format, store, log-regex verdict, test-service
finalizer, historical status, or `bin/test-run` change was made.

## Exact hashes

The 0125 source-binding/profile state was present before this edit and remains
unchanged:

| File | Before | After |
| --- | --- | --- |
| `design/normal014-app-central.sh` | `65ea14c97c8bafccb53ae3ccc7054c380f409f211281ca46afbcaeed23e7f30f` | `c18d79205ca3b6af4a679ecef9cba0c11a1c3afee23b1daa56d95f109bedbf20` |
| `design/normal014-source-common.sh` | `3b2018de1fbc123135590c37d4b17e995fd194fc39089b793e3f1b82e742bd56` | `3b2018de1fbc123135590c37d4b17e995fd194fc39089b793e3f1b82e742bd56` |

The first hash is the reviewed 0125 after-hash. The unchanged common-helper
hash is the current 0125 source-binding state. The earlier 0108 profile
after-hash for the app runner was
`766e0b6a38a5d450a92aee8424d181041c54d523a8ea1427316cf02f3809d68c`.

## Evidence

Offline syntax and source checks:

- `sh -n design/normal014-app-central.sh` — PASS.
- `sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh` — PASS.
- `git diff --check` — PASS; the assigned App worktree is clean.

The actual patched wrapper was exercised through its `flock` child path with a
private synthetic reporter and private fake service commands. The fixture
produced the existing summary schema and used the exact required case name:

- required case status `passed`, child exit 0 — wrapper exit 0;
- required case status `failed`, child exit 0 — wrapper exit 1;
- required case missing, child exit 0 — wrapper exit 1.

The probe also verified the exact `--grep` title argument and that each
disposable run root was absent after the wrapper's EXIT cleanup. No browser,
localhost, live socket, install, dependency mutation, full suite, or gate was
run.

The retained 4657 evidence remains contradictory: its status/exit files say
`pass`/`0`, while its structured summary and log say `1 failed 1 passed` and
contain the Playwright timeout. The retained child-RC swallow point is still
unproven; this guard addresses the false-pass outcome without claiming to
identify that root cause.

## Test limitation and review

`node --test tests/e2e/local/support/current013-native-none.test.mjs` could not
collect under the available Node 22 because `node:vm` does not export
`SourceTextModule`; the qualified Node 20 toolchain was unavailable. This is a
pre-existing environment/test-runtime limitation, not a changed-test result.

Independent custody review is required before any real normal014 gate. The
first passed current95 neighbor was not rerun, and result 4657 was not edited
or relabeled.
