# CommitV2-D12-boundaries — agt-V2-boundaries-return-0553

**Readonly review: PASS for the bounded source fix and required source/quality controls; FAIL for an all-green original-three acceptance claim.** The final original-three run is **2 passed, 1 failed**. The remaining failure changes the legacy anchor's source window and must retain its existing refusal under the supplied brief. No 54-test claim. Harness commit pending.

Base: `bfa799284bc5e941151ac2568fb00f7eca30b737`. Changed only `astrid/sdk/timeline/validation.py`, `astrid/sdk/timeline/_commit_timing_validation.py`, and new `tests/editing_conformance/test_commit_boundaries_d12.py`. Read PLAN §3, BOARD-HEADER including D12/D12a, commit-v2 §§1–5, the V4 five-case report and actual first-five.log, and R2 stage-current-port-0541.

## Changes and production caller

- Existing final validation compares each interval's authored fields and its actual baseline occurrence/asset bounds. Untouched legacy overruns survive unrelated edits byte-for-byte. New/changed clips, changed occurrence durations, reduced asset extents and replaced physical owners remain strict. Track/asset reference retention likewise requires an unchanged reference and unchanged missing target. Comparisons distinguish missing/null and JSON numeric spellings; no epsilon/equivalence policy was introduced.
- Existing timing adapter still executes the compiler, bindings and physical closure preparation. It retains an unsupported legacy map only when compilation refuses that map and the complete captured timing basis is unchanged, ignoring unused tracks and opaque clip params. The authored map, clips and declarations are neither interpreted nor removed. Changed timing/declarations, source inputs or owners remain refused. This is a return in the existing validation owner, not a new executor or validator.
- Explicit-null speed follows existing canonical behavior, rather than receiving a new default policy: `astrid/core/timeline/duration.py:106–110,141–142` accepts null and computes `speed ?? 1`; `_timing_evaluators._value(..., "speed", 1)` does the same; `_clip_commands.py:36` already admits explicit null for native literal clip creation. The original `literal_row(speed=None)` now passes final validation and remains literal null in the canonical output. Boolean/nonpositive/nonnumeric speed guards remain active. This is permitted canonical/native timing behavior, not an exemption for an untouched legacy speed.

Mounted production `RuntimeCommitService.commit` at `commit.py:1117–1125` calls `validate_final_candidate` on the completed plan with the actual landing baseline, retained schemas, realm and authenticated inverse sources. The new production tests exercise that caller for accepted and preview cases, retaining step records and literal child images. The real original-three tests use RuntimeService and its registered production provider, in process without localhost/sockets.

Request/reply/recorder/history/idempotency code is untouched. Full v2 request fields remain at that source: api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands/label/steps(id,label,intent,tags,command_ordinals,patch,reads)/merge(fields|atomic)/reads/dry_run/source/rationale/group_id. Full {data,receipt}, accepted/merged/authentic historical rebased, canonical closure/head/revision/digests/records/effects/steps/dependencies/history/undo_steps, conflict reason/head, invalid code/path/hint/suggested command, and preview would_status accepted|merged retain their existing implementations. Bounded tests are not an independent qualification of every DTO/history scenario. Current fork authentication, exact FPS arithmetic, reference/anchor guards and source_bundles handling remain in place. No original tests/fixtures/recipes, pristine tests, G234/stage/replay/root-inverse/fork/provider code, schema/pins/generated files, baselines, shared dependencies or git internals were edited. No skips or xfails.

## Exact environment and imports

Worktree `/home/user/work/wt/agt-V2-boundaries-return-0553`; scratch `/tmp/w-174915ddb6`, as named by the worker tmpdir locator. Shared dependencies were read-only. Python `/home/user/work/venv-agent/bin/python` 3.13.16; persistent 0529 typechecker `/home/user/work/venv-agent-typecheck-v2/bin/python` 3.11.17.

Created a private archive with `git -C /home/user/work/runtime archive 495769531de8d79d27a2d8022851d75b92f04ebe | tar -x -C /tmp/w-174915ddb6/runtime-495769531` after creating that private directory. Runtime commit `495769531de8d79d27a2d8022851d75b92f04ebe`, tree `0651fbfe829b4cebb0cfb0fa7540d44e9d999344`. Verified all 466 tracked archive files byte-for-byte against a fresh read-only archive after testing. Shared Runtime was only the Git locator for the original fixture's immutable historical seed (`80973d34ae10e498d7213c30287012c9876f4b1a`); measured Runtime imports were asserted under the private 495 archive.

Verified imports: astrid, both validation modules and astrid_runtime_client resolve inside this assigned worktree; banodoco_timeline_schema resolves from `/home/user/work/venv-agent/lib/python3.13/site-packages`; runtime_protocol, service, timeline_commit and timeline_commit_port resolve from `/tmp/w-174915ddb6/runtime-495769531/runtime_protocol`.

Protected original blobs were asserted byte-for-byte before both original-three invocations and verified after testing:

- native test equals `5292b388a`, SHA256 `ab07f5b9cda3a42d0c9273917b46d9486c39b453b979d2ad5d39df5528d4179f`.
- native fixture equals `38e806316`, SHA256 `4ebec0fa3d56a51a2fdd59a23f04bf256dc50fbcf45659086217baa9f51b6553`.

## Exact targeted commands and results

Common direct environment (all runs from the assigned worktree):

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/tmp/w-174915ddb6/runtime-495769531
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
export TMPDIR=/tmp/w-174915ddb6
P=/home/user/work/venv-agent/bin/python
```

```sh
$P -m pytest -q -p no:cacheprovider tests/editing_conformance/test_commit_legacy_text_reference.py tests/editing_conformance/test_commit_fps_d12.py tests/editing_conformance/test_commit_anchor_d12.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_commit_boundaries_d12.py
```

**PASS: 133 passed in 4.72s**, final product/test source (`required-final.log`). Includes the required existing 110 plus 23 new boundary/source/default regressions. Existing 110 independently passed before the final guard tightening, 110 passed in 5.86s (`required.log`). New regressions separately passed 23 in 1.70s (`boundaries-final.log`). The first new-test attempt had 13 failures/10 passes due to my new helper retaining a stale immutable dependency manifest and looking for fake-port accepted steps in data rather than prepared records; fixed only this new helper/assertion location, without changing any original expectation or production guard.

```sh
$P -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_provider_occurrence_fork.py tests/editing_conformance/test_recipe_occurrence_fork.py tests/editing_conformance/test_native_word_anchor_vectors.py tests/editing_conformance/test_recipe_m2_clip_add.py
```

**PASS: 93 passed in 5.75s**, final source (`controls.log`), including the required existing 25 fork controls, source negatives and unchanged original literal/null-speed creation behavior.

Exact original-three command (the -c preamble asserts immutable imports and protected blobs, without changing fixtures or production code):

```sh
env -u ASTRID_WORD_ANCHOR_SEED_RUNTIME PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/tmp/w-174915ddb6/runtime-495769531 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime TMPDIR=/tmp/w-174915ddb6 /home/user/work/venv-agent/bin/python -c 'from pathlib import Path; import subprocess, hashlib, sys, pytest; import astrid.sdk.timeline.validation as validation; import runtime_protocol, runtime_protocol.service, runtime_protocol.timeline_commit, runtime_protocol.timeline_commit_port; modules=[validation,runtime_protocol,runtime_protocol.service,runtime_protocol.timeline_commit,runtime_protocol.timeline_commit_port]; [print(m.__name__,m.__file__,flush=True) for m in modules]; root=Path("/tmp/w-174915ddb6/runtime-495769531"); assert all(Path(m.__file__).is_relative_to(root) for m in modules[1:]); assert Path(validation.__file__).is_relative_to(Path.cwd()); protected={"tests/editing_conformance/test_native_word_anchor.py":"5292b388a", "tests/editing_conformance/native_word_anchor_fixture.py":"38e806316"}; [(print(p,hashlib.sha256(Path(p).read_bytes()).hexdigest(),flush=True), Path(p).read_bytes()==subprocess.check_output(["git","show",ref+":"+p]) or sys.exit("protected file differs")) for p,ref in protected.items()]; raise SystemExit(pytest.main(sys.argv[1:]))' -s -q -o addopts= -p no:cacheprovider -m integration 'tests/editing_conformance/test_native_word_anchor.py::test_native_acceptance_refuses_review_source_counterexamples_before_writes[short-occurrence]' 'tests/editing_conformance/test_native_word_anchor.py::test_native_acceptance_refuses_review_source_counterexamples_before_writes[raw-source-window]' tests/editing_conformance/test_native_word_anchor.py::test_stale_anchor_refuses_when_intervening_window_excludes_selected_word
```

**FAIL: 1 failed, 2 passed in 4.88s; exit 1**, final source (`original-three-final.log`). Both short-occurrence and raw-source-window now complete setup, reach the intended original source/anchor refusal assertions, and pass. Stale-anchor still fails at line 528, `trim-before-anchor`, before its intended stale request: `candidate.timing: legacy word anchor is missing`. First invocation after the meaningful fix was also 1 failed/2 passed in 4.95s (`original-three.log`); final invocation followed additional guard tightening (exact duration spelling, asset target identity, separate parent/shot timing-basis keys). No repeated identical-tree run and no original54/native14 invocation.

## Retained refusal / fixture-contract issue

The protected seed already contains `parent/clip:card.app.astrid.on = '\"again\" in line #2 +1f'`. The stale test's comment that no authored reference exists refers to the absence of word_anchors; it does not remove this legacy declaration. `fixture.window` changes `occurrence:occ/clip:voice.from` from 2 to 4 (to remains 6). This changes the legacy text-search target basis, while the ordinary window request has no selected transcript pin to authorize a replacement. The existing `_reference_basis`/`_legacy_exemptions` guard therefore stops exempting that declaration. Allowing it would contradict the required unchanged-target condition and the passing existing `test_new_modified_or_invalidated_legacy_word_is_refused[target-invalidate]` control. I retained the refusal as explicitly directed, and did not edit the protected fixture, test, recipe or native_word_anchor.py.

Evidence changes the expectation that all three supplied originals can pass under the unchanged fixture plus current target-invalidation contract. Orchestrator should resolve that fixture/contract issue; this worker did not decide a different policy. The V4 summary says both seed errors are half-open bounds, but its actual first-five.log shows raw-source-window also fails at `unsupported explicit map source_window`; that remaining legacy check is addressed here.

## Quality checks

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-174915ddb6/ruff $P -m ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py tests/editing_conformance/test_commit_boundaries_d12.py
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-174915ddb6/mypy-scoped /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/validation.py astrid/sdk/timeline/_commit_timing_validation.py --follow-imports=skip
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/w-174915ddb6/ruff make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-174915ddb6/mypy-ratchet /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. $P scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. $P scripts/artifact_manifest.py --check
git diff --check
```

All **PASS**: scoped Ruff clean, private mypy no issues in 2 source files, normal Ruff **2150/2150**, normal mypy **1915/1915**, lock OK, artifacts current, whitespace clean. No budget increase. Logs are `scoped-ruff.log`, `scoped-mypy.log`, `ruff-ratchet.log`, `mypy-ratchet.log`, `vendor.log`, `artifact.log` under scratch. Initial Ruff sorted only the new test's imports with `ruff check --fix`.

## Handoff

Bounded implementation complete; DONE marks completion of this assigned fix/report, not all-green native acceptance or integrated delivery. Recommended next steps: readonly review of this exact three-file diff; orchestrator decision on the protected stale-window fixture/contract conflict; R2 owner joins this nullable-speed correction with its reviewed stage port and performs the actual redo qualification there. No known-failing redo was run on this base, which lacks the 48d stage fix. No full/browser/socket/heavy/farm/native14/crash24/P4 HTTP-body run, no 54-pass claim, no integration merge or git commit performed.

Final tested source SHA256:

```json
{
  "astrid/sdk/timeline/validation.py": "dc47fc582f6320f78a5bfd0413e543c7fb0db33816c6d80aeba778b3bc2c5073",
  "astrid/sdk/timeline/_commit_timing_validation.py": "5aa5bed99d020458a8e91952e3f6aaf53fc8f6d72dc5d62fe405f275403b6a16",
  "tests/editing_conformance/test_commit_boundaries_d12.py": "651f32e8a6b88bf4267737a474039e5a1d39898b220ea6c6d1a739feea03cb53"
}
```
