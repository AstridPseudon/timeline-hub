# AP2-M2 parent gate bounded follow-through

## Result

Worker 0138's single parent gate is complete and failed before any test case
ran. I did not rerun it, run a browser/full/socket suite, change the frozen
source, activate public14, adopt a pin, or prepare a deletion cut.

Retained result:

- Suite: `normal014-integration-parent-media-accepted`
- Request: `ap2-m2-parent-frozen-source-single-gate-0138-normal014-integration-parent-media-accepted-1021014332-27865`
- Result: `fail`, exit `1`, in `1s`
- App tree: `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`
- `log.txt` and `runner.log`: empty
- Test counts and structured case verdict: absent

## First failure classification

This is a central-wrapper source guard failure, not a parent-media product
assertion. The central test service creates a synthetic test commit from the
worker tree before running the suite (`orch/bin/test-run`, lines 5165-5167).
The parent wrapper then calls `verify_app_source` before source preparation or
pytest (`normal014-parent-media-central.sh`, lines 17-18). Its final95 guard
requires the synthetic checkout's `HEAD` to equal the frozen App commit
`25155ccb22728780a3ecd6379a929cad75cc1400`
(`normal014-source-common.sh`, line 182). That cannot be true after the
central service creates its `test snapshot` commit, even when the source tree
is exact. The next tree assertion and pin checks therefore never run.

Independent read-only source checks confirm the approved source itself is
intact:

- App commit tree is exactly `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`.
- The four expected App pin SHA-256 values match the wrapper constants:
  `runtime.lock.json` (`770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e`),
  generated metadata (`4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044`),
  generated client (`c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d`),
  and timeline types (`f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564`).
- The approved Agent and Runtime commits and trees exist and match the
  custody report; Runtime artifact and schema hashes also match.

## Exact HOME request

In the HOME-owned central wrapper, remove the commit-identity assertion at
`normal014-source-common.sh:182`:

```sh
test "$(git -C "$app_root" rev-parse HEAD)" = "$APP_ROOT_SHA"
```

Keep the existing exact `HEAD^{tree}` assertion immediately below it, the
clean-worktree assertion, and all four pin-byte assertions. Those checks bind
the synthetic central snapshot to the approved App source without requiring a
commit object that the central runner necessarily replaces. After that
one-line harness fix, HOME should submit the already-approved parent gate once
against the same final95/parent tuple. No App source, Runtime/Agent source,
wire field, timing policy, fallback, or `afterClipId` shape should change.

## Scope boundary

Because the gate never reached its required case, no physically remaining
legacy parent writer is proven dead and no App deletion is prepared here.
Duplicate-generation callers and the rest of the parent row remain open and
unqualified. The requested harness correction is the smallest next action;
the parent writer cut must wait for an actual passing parent result and its
focused neighbor evidence.

## Verification

- Read-only source/hash and retained-result inspection: completed; the exact
  commands and outputs are recorded above.
- Parent gate rerun: deliberately not run, per task instruction.
- App worktree diff: clean; no product files changed.
