# P2 D102 native-seed caller/retention report

## Finding

The App product caller is not implicated. The actionable App-owned defect is a pre-readiness diagnostic-retention gap in the D66 launcher/harness.

Both ADD12031 and ELEMENT4757 failed at `native-seed`, before readiness or original assertions:

- First failed boundary: `scripts/testing/d66-plain-stack.mjs:747-749`.
- Native path: `seedThreeProducts()` → `commitNativeSeed()` → `AstridClient.timelines.commit()`.
- Python seed script returned `not_ready` with `runtime_unavailable`; process exited `1`.
- Durations were 94s and 109s, below the 120s `execFileSync` timeout.
- No HTTP status/body, readiness XML, original XML, or assertions were retained.

The passing control `e96be/5fae/0c62/635f` reached native-seed and readiness successfully. App source was unchanged between passing App `e96be` and failed App `0244`; only pins/manifests differed. Runtime `0c62→689` changed exactly `service.py`, `timeline_commit_execution.py`, and one diagnostics test.

## Source/import attribution

Failed tuple, per retained manifest:

- App: `0244db2c…`, tree `126c5569…`
- Agent: `bde57850…`, tree `1df31228…`
- Runtime: `68935201…`, tree `a8217bdb…`
- Composition: `635f4de0…`, tree `5ab5191a…`

Import readback confirms `astrid` came from the selected Agent checkout, while `astrid_runtime` and `runtime_protocol` came from selected Runtime checkout. Harness `PYTHONPATH` construction is in [harness.ts](/home/user/work/wt/app-P2-D102-seed-caller-retention-0553/tests/e2e/local/support/harness.ts:651).

## Retention result

Runtime stdout/stderr is buffered by `spawnGroup`, but persisted only when `D66_RUNTIME_LOG_DIR` exists at teardown ([harness.ts](/home/user/work/wt/app-P2-D102-seed-caller-retention-0553/tests/e2e/local/support/harness.ts:1409)). The launcher injects that directory only into the later Playwright stage ([d66-plain-stack.mjs](/home/user/work/wt/app-P2-D102-seed-caller-retention-0553/scripts/testing/d66-plain-stack.mjs:247)); native seed runs earlier ([d66-plain-stack.mjs](/home/user/work/wt/app-P2-D102-seed-caller-retention-0553/scripts/testing/d66-plain-stack.mjs:737)).

Therefore:

- Agent/Python failure text was retained in the central run log/manifest.
- Runtime stderr was not retained for either setup failure.
- No bounded redacted diagnostic line was retained.
- The harness temporary directory was removed after teardown.

## Runtime exception-path conclusion

Published Runtime `689` contains bounded redacted diagnostics:

- `_lookup()` emits a diagnostic then raises `CommitOutcomeUnknown`.
- The service’s `except RuntimeErrorBase` path re-raises before the generic catchall.
- Ordinary unexpected exceptions reach the service generic catchall, which emits diagnostics and raises `CommitUnavailable`.

The public `not_ready/runtime_unavailable` result is proven; the exact internal lookup/provider/catchall branch is UNKNOWN because its diagnostic was not retained. No shared cause or Runtime source repair is justified from this evidence.

## Recommendation

Separate App author should fix only the launcher retention seam: make bounded, privacy-safe Runtime diagnostics available before native seed starts. Runtime/Agent owners should investigate handler/provider behavior only after such a retained diagnostic exists.

No product files were edited. No tests were run because this task was explicitly read-only and prohibited new test/build execution.

Commit message written and `DONE` marker created.