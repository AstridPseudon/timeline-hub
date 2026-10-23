R2 c271 config-root mirror repair — PASS for bounded offline authoring; DRAFT / P1 NO-GO remains.

Changed only `astrid/sdk/timeline/_step_undo.py` and new `tests/editing_conformance/test_captured_config_root_mirror.py`. No original test body, fixture, Runtime, schema, generated artifact, pin, checkout/sheet source, shared dependency, Git ref or integration worktree was changed. Existing ownership, binding, range, digest, ABA, order/membership and no-write guards are retained. `inverse.py` and `_root_inverse.py` were not needed.

Causal evidence and repair:

- Read PLAN §3 R2/G5, Runtime contract §§2–5, 1924 report and complete packet manifest. Verified archive SHA-256 `502266a70f0d1a3cb21d354e9cce01245acb39ea014649fe528039e997de1e8c` before extraction.
- Actual source forward publication `txn-dca405e7f44942b0a5818dd683a3a009`: `timeline.restructure`, 10 native writes, no derived writes. Accepted whole undo `txn-d59a7caf610544b5a747c99cc8a67d58`: `timeline.inverse`, 10 native writes, no derived writes, 9 effects. Its inherited native/effect ranges are exactly `[0,10]` / `[0,9]`, source step `restructure-0`, source ordinals `[0]`. All accepted command/step/receipt/binding/dependency structures were inspected and retained, without flattening the source ranges.
- The first undo native write restores the whole parent `config` (input has no `clips`; output has `clips: []`). Native write 2 then changes top-level `clips` from `cross, bed` to empty. The real recorder disables mirror compilation on that config assignment because the arrays differ at that moment. The old partition replay ignored the config write, invented a synchronized starting mirror, and demanded a nonexistent compiler observation at `_step_undo.py:157`.
- Replay now seeds an earlier whole-config input from its captured native before value, guards/replays the actual config write, and updates mirror eligibility at the same point as `Recording.assign`. Every actual derived observation is still consumed exactly, in order, with its cause and image checked. No blanket inverse exemption or derived-observation omission was added.
- The accepted parent-root effect at effect index 2 is checked through its exact clip/config projection before and after native replay. Other physical roots stay under the existing resolver/ownership/digest guards. Stage order images use the actual primary clip array, including when the config has no mirror. All native/effect range and inherited identity checks remain in place.
- The regression replays the exact captured request through `inverse_address_resolver` → existing selected records → `execute`, then checks the exact forward canonical document, native reversal, complete inverse step patch, no derived writes, original stage identity/ranges and input immutability. Nineteen strict tamper probes cover config inputs/outputs/site, native images/order, parent-root effect images, extra derived observation, ranges, source/step/ordinal, landing ownership, source digest/scope. Partition tampering must raise `history_unavailable`; sources and landing bundles remain unchanged.

Source identities:

- Base Agent `89c38c9355f5d4bcc68597ec74e4729435a7a07a`, tree `b050d29ec63cad9aaaf536427451d8079293f24c`.
- `_step_undo.py` before blob `db1dd6cc09a6f9b7cf59f8af9e49cdb9d682eb74`; after blob `0bdefdb813c9ffcbe94c7a627512784e60da3532`, SHA-256 `9214ee554507c21d70b76d81de251a2d9a04f972223cd3d42befca6e024ac9a2`.
- Other seven reviewed core paths match their original blobs exactly; complete before/after identities and loaded origins are in `evidence/source-identities.json`.
- Captured old source origin: `/home/user/work/wt/agt-G5-restructure-qualified-1924/astrid/sdk/timeline/_step_undo.py`. Repaired loaded origin: `/home/user/work/wt/agt-R2-c271-mirror-sol-1933/astrid/sdk/timeline/_step_undo.py`. `inverse.py`/`_root_inverse.py` load from this worker unchanged.
- Runtime remains `/home/user/work/wt/rt-pin-2a9e347f`, commit `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree `f79a2355cfb39d9ada7721978bd20d5702105778`. Actual `runtime_protocol.auth` and `timeline_commit_auth` origins/hash observations are in the identity file.

Capture retention:

- Lossless complete archive copied to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-c271-mirror-sol-1933/evidence/g5-c271-complete-packets.tar.gz` with the same SHA above (9,182,178 bytes). Source packet `058-provider-entry.json` SHA-256 `9056bdaa7926863a3c44d24a0303a6b3c790067623842f13e7f85bb2357974cd` matches the manifest.
- Only minimum deterministic captured inputs are embedded losslessly in the new test: the two actual complete source/target history entries, their two canonical documents, complete original context/request/idempotency, and expected captured forward result. No IDs, accepted records or source images were invented, relabelled or rehashed. Decoded fixture SHA-256 `16d87e20b1dc37be2246c8f9db0e61d3af12069c42acd03a980a9cd68a94c970`, 200,912 bytes; compressed 10,368 bytes. Scratch extraction and baseline code remain under `$TMPDIR/c271`, not the repository or worker evidence.

Exact tests and results (cwd this worker):

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_config_root_mirror.py
```

Before source repair: **1 failed**, the original `compile_mirror` / `history_unavailable` at line 157. After repair and final assertion strengthening: **20 passed in 1.07s**. The final minimum capture also reproduces the same old refusal using only the baseline partition function from `git show HEAD:astrid/sdk/timeline/_step_undo.py`, loaded by a private `$TMPDIR/c271/c271_baseline_probe.py` pytest plugin:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH="$TMPDIR/c271":.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p c271_baseline_probe tests/editing_conformance/test_captured_config_root_mirror.py::test_captured_config_root_redo_preserves_exact_history
```

Expected RED: **1 failed in 0.32s**, baseline line 157; durable log `evidence/baseline-red.log`. This probe changes only the loaded old function for that subprocess, never source or accepted evidence.

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f PYTHONPATH=.:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_captured_config_root_mirror.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_parent_mirror_ranges.py tests/editing_conformance/test_captured_nested_redo.py
```

**143 passed in 70.25s**, log `evidence/targeted.log`. The final 20-test command above followed addition of stronger native-reversal, error-code and bundle-immutability assertions; the seven untouched core paths had no subsequent edit. An earlier combined run was **142 passed, 1 failed** because the newly authored ownership probe selected a nonexistent singular `owner` key. A subsequent plural-metadata-only probe was outside the compiler's landing-ownership guard; the final probe changes the actual landing occurrence identity and verifies refusal. No passing original expectation was changed or weakened.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_nested_parent_mirror_ranges.py astrid/sdk/timeline/_root_inverse.py tests/editing_conformance/test_transient_root_baseline.py tests/editing_conformance/test_captured_config_root_mirror.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --config-file pyproject.toml --follow-imports=skip --ignore-missing-imports --namespace-packages --explicit-package-bases --cache-dir="$TMPDIR/c271/mypy" astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_nested_parent_mirror_ranges.py astrid/sdk/timeline/_root_inverse.py tests/editing_conformance/test_transient_root_baseline.py tests/editing_conformance/test_captured_config_root_mirror.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

All PASS: Ruff clean, private mypy **no issues in 9 source files**, vendor lock `ok runtime.lock.json`, artifact manifest current, clean whitespace diff. Baseline/current scoped diagnostic identity sets are empty: original changed production source checked with Ruff stdin using its production filename; original eight-path mypy command used the same options with `--shadow-file astrid/sdk/timeline/_step_undo.py "$TMPDIR/c271/baseline-step.py"` and omitted the new file (**no issues in 8 source files**). Seven other blobs are identical. Baseline/current logs are retained in evidence. This is scoped evidence; no whole-repository ratchet totals are claimed.

Decisions, limits and next step:

- No plan decision was changed. Only the causal mirror observer was repaired; whole config input and root effect projection are necessary for this actual packet.
- Offline compiler evidence does not requalify Runtime acceptance/authentication, HTTP/public `tl.undo`/`redo`, preview envelopes or the full c271 journey. No original c271/FOUR/P1/P4/9/14/40/281/58 body, full suite, browser, daemon or live socket was run. Native/effect source histories and production public request/reply paths are unchanged.
- No authoring blocker. Keep DRAFT / P1 NO-GO pending independent source review and manager-owned original qualification. Recommend independent PASS on this source and exact captured packet, then manager qualification of the unchanged original body; no retry was performed by this worker.
