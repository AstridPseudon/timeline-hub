**FAIL — U2-freeze is not ready for integration.**

Reviewed exact `cb6ce42cc2c0a071554353032a95073f04f72832` against `1f15f27482` and upstream `25359ed6877b9e13e07799bb2c9600fd143fde88`: all 77 cumulative files and all three conflict resolutions. Product/test files remain unchanged; worktree is clean. Wrote the required `U2-freeze-review` commit message and `DONE`.

The blockers are the duck fixture failure, 12 new type diagnostics, removed/changed behavioral coverage, and two whitespace errors.

**Checks and results**

Ran the required targeted command once:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= \
-pno:cacheprovider \
tests/packs/music/test_duck.py \
tests/packs/music/test_duck_overlap.py \
tests/packs/music/test_duck_runtime.py \
tests/core/rendering/test_remotion_registry_corpus_churn.py \
tests/sdk/test_host_bootstrap_source_identity.py \
tests/test_lane_registry.py tests/test_lanes.py tests/test_skip_guard.py
```

Result: **135 passed, 1 failed in 39.57s**, exit 1.

| Command | Result |
|---|---|
| `git merge-base --is-ancestor 25359ed6877b9e13e07799bb2c9600fd143fde88 HEAD` | PASS |
| `git diff --check 1f15f27482 HEAD` | FAIL: trailing blank lines at `position-keys.ts:39` and `test_duck.py:252` |
| `PYTHONDONTWRITEBYTECODE=1 make ruff PY=/home/user/work/venv-agent/bin/python` | PASS: 2145 / 2145 |
| `PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR="$TMPDIR/mypy-head-cache" make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python` | FAIL: 1914 / 1902 |
| `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-45c3a7f4` | PASS |
| `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` | PASS |

The producer path resolves to the existing checkout at exact `45c3a7f476e1c5f74fafc15956a58b9871eee21f`. No adoption occurred. An initial Ruff invocation using the typecheck venv failed because that venv lacks Ruff; the corrected normal Agent-venv invocation passed.

**Failure ownership and required repair**

`test_managed_duck_outputs_and_tagged_rerun_leave_the_input_revision_unchanged` fails at `tests/packs/music/test_duck_runtime.py:104`, during `create_empty`, before duck execution.

Its fixture calls `real_runtime()` without `authoring_profile="astrid"`. Runtime’s default neutral profile loads no commit provider. The retained failed database contains `duck-main` and its `timeline.create` receipt, but **no parent head and no commit history**. Agent’s `_native_empty_replay()` requests history and receives the correct fail-closed `history_unavailable`.

The repair belongs to the **Agent duck test fixture**: select the Astrid authoring profile when creating its daemon. Do not relax Runtime history checks. Subsequent seed, invocation, adoption and rerun assertions remain unverified.

**All new diagnostic identities**

Compared HEAD and a source-only archive of the first parent using `/home/user/work/venv-agent-typecheck-v2/bin/python`, identical mypy flags and separate temporary caches:

```bash
python -m mypy astrid scripts/reshape \
  --hide-error-context --no-color-output --no-pretty --show-error-codes
```

The parent invocation used its archived `pyproject.toml`, `astrid` and `scripts/reshape` paths. Parent: **1902 errors / 251 files / 961 checked**. HEAD: **1914 / 252 / 967**. Comparing path/message/code identities and multiplicities gives **12 additions, zero removals**.

Every addition is in `astrid/packs/music/actions/duck/core.py`:

| Line | Diagnostic |
|---|---|
| 212, 238 | `object` is not iterable `[attr-defined]` — two |
| 219 | `inside` needs annotation `[var-annotated]` |
| 222 | ndarray assigned to previously inferred `float` variable `bed` `[assignment]` |
| 224 | `voiced_mask` needs annotation `[var-annotated]` |
| 231 | `object` is not indexable `[index]` |
| 263 | Slice indices are not proven integer `[misc]` |
| 265 | `object - float` `[operator]` |
| 267 | `object - int` `[operator]` |
| 281 | `min(object)` and `max(object)` `[type-var]` — two |
| 282 | `min(object)` `[type-var]` |

Repair the heterogeneous line-record typing, scalar/array `bed` reuse and mask annotations. **No baseline increase is justified.**

**Conflict resolutions and production preservation**

- **`artifacts.json`:** regenerated combined manifest passes the checker.
- **Remotion integration fixture:** adopts provisioned dependencies and launch-owned validation, managed input objects and the host’s claim client. Assertions after execution remain. This review did not execute the real render.
- **Publication chain:** retains the first parent’s installed-runtime/native authoring continuation. The additional snapshot assertion follows `timeline_snapshot_ref` into CAS and still compares its config with the proposal. It does not restore the obsolete inline-publication path.

The entire `astrid/sdk/timeline` implementation, `astrid/sdk/remote.py`, schemas, generated client, lock and editing-conformance suite are unchanged from the first parent. R1/R2 reads, owner/binding/previous-value guards, undo and ABA handling therefore have no source delta here.

The preserved transport includes the complete request controls: API/scope/base pair, nonempty commands, label, step IDs/labels/intent/tags/ordinals/patch/reads, merge policy, declared reads, dry-run, source/rationale/group and stable idempotency key. Existing reply handling retains canonical documents/heads/revisions/digests, records/effects/steps/dependencies/bindings/history/undo/attribution, preview `would_status` with null receipt, conflict head/reason and structured invalid diagnostics. This is preservation evidence, not renewed full-v2 qualification.

Music’s production action is registered through `pack.yaml → duck.run`. Its documented adoption path reaches:

```text
Checkout.publish → _commit_document → TimelineSession.submit
→ persisted outbox → client.timelines.commit
```

It uses the existing commit writer. The new action itself only produces managed media; adoption is separate. Runtime execution of that complete workflow remains blocked by the fixture failure.

D40’s `_RuntimeSourceCustody`, captured-byte worker/executor/orchestrator loaders, original external-orchestrator fixture and custody suites are unchanged. Exact owner grants, retained preparation/scope/profile binding, descriptor selection and captured imports remain. Bootstrap changes add diagnostics/output-root handling and exclude owner-only launch facts from ready-marker comparison while retaining live identity verification. Linux relay peer-token custody still refuses outside Darwin; no RunPod custody backend was introduced. Held `a181136220` is not an ancestor.

I cannot independently certify the historical **“12 guards / 6 attacks” node mapping**: the older `tests/stage1/test_installed_external_pack_roots.py` referenced by predecessor reviews is absent from both this base and HEAD. This merge did not delete it, but no aggregate 12/6 execution credit is claimed.

**Deletion and assertion-change inventory**

These changes require explicit Timeline disposition; upstream ancestry and `removed.yaml` explanations do not establish preservation.

| File | Removed or changed obligations |
|---|---|
| `test_h3_continuation_runner_contract.py` | Whole file deleted: three tests, **40 assertions**. |
| `test_hype_cut_invariants.py` | Deletes real-run selection/discovery and `test_hype_cut_invariants_on_discovered_run_dirs`; the synthetic twin remains. Real saved-run invariant coverage is lost. |
| `test_character_swap_cpu_boundary.py` | Deletes workspace-helper pin test: file/non-symlink and SHA assertions. Deletes managed CPU boundary positive with **30 assertions**. |
| `test_c06_public_timeline_visualizer.py` | Deletes saved-artifact readback: one positive plus five corruption cases—sidecar bytes, saved revision, requested frame, render digest and sidecar path. Loses schema/fresh-frame/sidecar assertions and corruption rejection. |
| `test_generic_host_child_bridge_d18.py` | Removes three asserted five-second discovery waits, six future-result deadlines and the four-second admission deadline/failure. Replaces successful oversized-output enumeration plus materialization-budget rejection with earlier output-identity rejection. |
| `test_generic_host_activation_acceptance.py` | Changes fake RunPod fixture to local machine; removes provider-identity case and precommit `ready` failure case. Removes pre-acceptance claim-denial/queued/no-attempt assertions and the “lost reply after host claim” condition. Replaces four identity-failure abort combinations with retained-handle tests, losing the explicit census/signal-order, ready-file removal and child-exit-race predicates. Changed-readiness expectations reverse from absent activation/revoked credential/stopped host to retained activation/credential and unresolved host. |
| `test_media_handoff_render_boundary.py` | Removes child-side timeline/registry type, theme ID/fps, clip count/asset, asset media-ID, local HTTP-origin and fetched-byte digest assertions. Changes exact decoded-frame equality to equal length plus channel-mean error ≤4; spatial equality is no longer checked. |
| `test_generation_runtime_composition.py` | Three production generation assertions change `built_in` to `external`; fixtures migrate to shipped actions and executor-bound credentials. |
| `test_e2_publication_contract_roundtrip.py` | Manifest upload, settlement and managed-readback media-type expectations change from `metadata/result-manifest` to `application/json`. |
| `test_generic_host_external_provider.py` | Replaces combined inline/upload parameterization with separate tests. Inline “no ingest call” becomes a fail-on-ingest stub; output expectations add filename. Upload tests add exact attempt/provenance binding. |
| `test_generic_host_runtime_control2.py` | Expected executor identity changes from `echo-host` to `astrid-pack-host`. |
| `test_runtime_publication_chain.py` | Inline snapshot-config assertion becomes CAS-reference readback with the same config equality. |
| `test_ffmpeg_backend.py` | Expected filter string adds full BT.709 frame parameters; existing color-output assertions remain. |
| `tests/packs/conftest.py` | Node availability assertion moves into the shared validation helper. |

The deleted H3 runner’s 40 assertions cover: named-session default/status, session start/warm policy/input/output paths, config validation and refusal to replace incompatible sessions, absence of unmanaged PID/server startup, live object-info/no-cache/headless mode; setup marker/fingerprint/wheel hash, unchanged-setup messaging, verification/dependency repair/Comfy root, absence of obsolete package-version checks, offline normalizer/source support, persisted fingerprint and model reconciliation; patched-workflow conversion, IR recipe selection/validation/model ensure/run, refusal of the converted workflow path, `WorkflowLens`, guider/conditioning traversal, prompt replacement, compilation, prompt verification and workflow authority.

The deleted managed CPU positive covers success/rows/capabilities; boundary schema, synthetic classification, no Comfy queue/model-byte claim, task/attempt/execution identities and distinct child PID; matching activation-marker schema/identities/classification/profile/candidate digest; matching actual child call/evidence; output existence/non-symlink/digests, observed input digests and verified-candidate output; workspace profile/candidate provenance, no execution-target claim, owner stop and matching stopped Runtime PID.

`tests/removed.yaml` adds five records accounting for **12 deleted cases**. Its claimed upstream owner decision does not resolve the project’s explicit no-weakening requirement.

**Registry/manual/skip changes**

- Removes Windows CI and records `windows_native.no_ci`; ffmpeg/node lose Windows jobs.
- Adds nightly/main integration, opt-in and installed-wheel jobs; Darwin gains Codex CLI.
- Converts integration from manual to dependency-backed and opt-in to scheduled; removes `live`; adds `installed`, `codex_cli`, `workstation`, `app_checkout`, `omp`, `gpu`.
- Default deselection expression follows those changes.
- Moves C06 public acceptance to `workstation`, paired-App generation to `app_checkout`, local image smoke to `gpu`, OMP to `omp`, Codex smoke to `codex_cli`, and three installed CPU tests to `installed`.
- Adds `darwin_native` to local-host control; removes redundant integration marking from the Darwin lifecycle test.
- Lane-registry validation now permits `no_ci`; its provisioning check becomes stricter by removing the platform exemption.
- Skip-report tests adopt the new lane names and add explicit no-CI reporting. No new xfail or direct skip was added.

Restore lost promised coverage and bounded assertions, or obtain an explicit orchestrator reconciliation of the enumerated upstream behavior changes. Keep D46 refusals visible; do not add authority backends to satisfy these tests.

No full, browser, gate or installed-D40 qualification was run. After the fixture/type/whitespace repairs and coverage reconciliation, rerun the permitted affected checks and independent review.