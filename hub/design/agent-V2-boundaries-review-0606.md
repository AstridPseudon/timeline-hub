# agt-V2-boundaries-review-0606

Readonly independent review of `b42b7d72a` on `bfa799284`.

## Decision

- **Boundedfix: FAIL.** `astrid/sdk/timeline/validation.py:241-243` permits an unchanged clip whose track is absent from both candidate and baseline tracks; `:255-258` similarly permits an unchanged clip whose referenced asset is absent from both registries. Direct reproduction with `validate_final_candidate(candidate, baseline=baseline)` accepted both malformed inherited baselines. This is inherited unrelated invalidity laundering, outside the narrow D12a exemption.
- **Outstanding scope case: FAIL.** Per the author report and independent Viewing0545 handoff, the original-three result remains 2 PASS / 1 FAIL. The stale-window case changes the legacy source search basis and is correctly retained as a refusal. The known-failed stale case was not rerun.

## Evidence

- Required validation matrix: **133 passed**.
- Fork/provider/recipe controls: **93 passed**.
- Scoped Ruff and mypy: **PASS**.
- Normal Ruff: **2150/2150**.
- Mypy ratchet: **1915/1915**.
- Vendor lock, artifact manifest, and `git diff --check`: **PASS**.
- Production caller remains at `astrid/sdk/timeline/commit.py:1117-1125`.
- No source, fixture, generated file, pin, shared dependency, or test expectation was changed by this review. No full/heavy/browser/socket/native14/farm suite was run.

Do not make an all-green or 52/54 claim. Remove the two unrelated invalidity exemptions and resolve the protected stale-window contract/fixture question before merge.
