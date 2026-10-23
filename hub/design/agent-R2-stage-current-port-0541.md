# agt-R2-stage-current-port-0541 — source PASS; all-three-redo acceptance BLOCKED

Ported ONLY the exact `48d7c5973f6b65db988f5f4dd942f5749a572e8a` delta versus its parent `f677e9bab7def6bcff8cd4faed55f29827b8af30` onto assigned reviewed authored-G234 base `31a5e8d3c858d0e4cb1b333b95175862f07f5fa6`. The worktree has exactly these three changes, each byte-identical to the source commit's corresponding file:

- `astrid/sdk/timeline/_commit_patch.py`: 16 additions / 2 deletions (18-line delta).
- `tests/editing_conformance/test_inverse_stage_images.py`: new, 33 lines.
- `tests/sdk/test_timeline_pristine_initialize_runtime.py`: 61 additions.

No parent ancestry was imported. Harness-assigned own commit is pending; commit message subject is `fix(timeline): port guarded inverse stages (agt-R2-stage-current-port-0541)` (CommitR2-stage-current). No git commit/merge/checkout/fetch/push or internals write was performed by this worker.

## Production behavior and constraints

`RuntimeCommitService.commit` uses `commands.execute`, which constructs `CommitPatch` and calls its `before`, `after`, and `finish` methods (`commands.py:199–249`). The actual mounted service and public client tests exercise this path. The fix pins changed sequential command input images and keeps the actual first inverse-stage input, then chains each following input from its exact preceding output. Historical equal bytes cannot replace that first revision.

Full request/reply handling is unchanged: scope/base, commands, complete metadata/steps/reads/merge, dry run, stable key identity, canonical closure, receipts, records/effects/dependencies/history, inverse allocation facts, structured errors and preview handling retain existing implementations. New Runtime tests cover implicit/explicit metadata, unchanged submitted requests, complete supplied step attribution, receipt/data equality, canonical output, exact retry and unchanged history on retry. No schema/client/pin/generated/executor/Runtime source changes, weakened guards, skips or xfails.

## Runtime provenance and import origins

Private exact archive: `/tmp/w-ae4e0e9662/runtime-495769531`, produced with read-only `git -C /home/user/work/runtime archive 495769531`. Exact Runtime commit `495769531de8d79d27a2d8022851d75b92f04ebe`, tree `0651fbfe829b4cebb0cfb0fa7540d44e9d999344`. Its `runtime_protocol/timeline_commit_auth.py` is byte-identical to reviewed repair `5dd136a`; both SHA-256 `bb7307e61a2eb64f16672545bd52bfa39363dc59788add6ad0b295625064aaaa`.

Normal Python: `/home/user/work/venv-agent/bin/python`, Python 3.13.16. Persistent private typecheck environment: `/home/user/work/venv-agent-typecheck-v2/bin/python`, mypy 1.17.0. Author's former `/tmp/astrid-u2-typecheck` does not exist; used the current G234 lane's persistent environment. Dependencies were read-only; caches and scratch stayed in `/tmp/w-ae4e0e9662` (the harness's worker `tmpdir` file points there).

Verified direct imports:

- `astrid`, `_commit_patch`, `astrid_runtime_client`: this assigned worktree.
- `banodoco_timeline_schema`: `/home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema/__init__.py`.
- `runtime_protocol` and `runtime_protocol.timeline_commit_auth`: exact private Runtime archive above.

The central integration command prints/asserts the service snapshot's Astrid package and preloads/asserts exact Runtime 495 before collection. `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime` is used only as the real Git locator required by existing `use_runtime(commit=vendored_runtime_commit())`; already loaded Runtime package/submodules execute from the exact archive. No helper monkeypatch or submitted claim synthesis.

## Exact targeted commands and results

Direct source-control environment:

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/tmp/w-ae4e0e9662/runtime-495769531
export ASTRID_RUNTIME_CHECKOUT=/tmp/w-ae4e0e9662/runtime-495769531
export TMPDIR=/tmp/w-ae4e0e9662
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_stage_images.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_pristine_initialize_provider.py tests/sdk/test_timeline_clip_add_provider.py tests/sdk/test_timeline_semantic_reservations.py
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_commit_provider.py -k aba
```

**PASS: 92 passed in 9.78s; 8 passed, 106 deselected in 5.52s.** Includes authenticated physical closure, corrupt/missing history, successor provenance, per-step undo and consumer guards, original allocation facts, occupied/retired-ID collisions, and ABA controls. Logs: `/tmp/w-ae4e0e9662/source-controls.log`, `aba.log`.

Runtime security controls (cwd exact archive):

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-ae4e0e9662/runtime-495769531:/home/user/work/wt/agt-R2-stage-current-port-0541 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_commit_authentication.py -k 'inverse_omitted_created_claim'
```

**PASS: 5 passed, 68 deselected in 1.12s.** Omitted default inverse claims accepted only with exact restoration identity; explicit empty/forged claims, ordinary command mismatch, wrong publication/step/fact/write rejected. Log: `/tmp/w-ae4e0e9662/runtime-inverse-auth.log`.

Central test-service command (one narrow suite entry appended to the named shared `tests/suites.conf`, no full suite):

```sh
$ORCH/bin/request-test agt-R2-stage-current-port-0541 agt-R2-stage-current-0541-exact495 --files 'tests/sdk/test_timeline_pristine_initialize_runtime.py tests/editing_conformance/test_commit_runtime_first_clip.py'
$ORCH/bin/wait-test agt-R2-stage-current-port-0541-agt-R2-stage-current-0541-exact495-1023054548-22087 1
```

Exact named command:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime TMPDIR=/tmp/w-ae4e0e9662 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/tmp/w-ae4e0e9662/runtime-495769531" /home/user/work/venv-agent/bin/python -c 'import pathlib, astrid, runtime_protocol, pytest, sys; assert pathlib.Path(astrid.__file__).resolve() == pathlib.Path.cwd() / "astrid/__init__.py"; assert pathlib.Path(runtime_protocol.__file__).resolve() == pathlib.Path("/tmp/w-ae4e0e9662/runtime-495769531/runtime_protocol/__init__.py"); print("Agent:", astrid.__file__, "Exact Runtime 495769531:", runtime_protocol.__file__, flush=True); raise SystemExit(pytest.main(["-q", "-p", "no:cacheprovider", "-m", "integration", *sys.argv[1:]]))' tests/sdk/test_timeline_pristine_initialize_runtime.py tests/editing_conformance/test_commit_runtime_first_clip.py
```

**FAIL: 1 failed, 5 passed in 9.53s; service exit 1 in 12s.** Tested Agent tree `e1e0efeb48b8fcb42552b99df4ad67fee31ebac5`. Passing: both new implicit/explicit input cases, original pristine crash/resume/reload/undo/retry/redo, original live public create/reload/replay, original non-nullable first-clip exact reload/inverse/redo/undo-redone. No caller-created restoration claims were forged.

Failing original node: `tests/editing_conformance/test_commit_runtime_first_clip.py::test_empty_bootstrap_first_clip_client_commit_exact_reload_inverse_redo[True]`, at line 95, **initial clip.add before undo or redo**. Error: `candidate.parent.clips['first-clip'].speed: must be a finite number`. The assigned base already contains `validation.py:136`, `_number(clip.get("speed", 1), ..., positive=True)`, which rejects explicit null. Validator source is unchanged from base, SHA-256 `257c0b946f8b28a7761d8b24a378a48b547624ab2f4e9e665273ebd1f9f4dfc0`. This is an independently introduced V2/base integration blocker, not Runtime's repaired inverse-claim mismatch. **The brief's expectation that all three redo paths now pass does not hold on this required base.** I did not change the out-of-scope validator or original expectation.

Full log: `$ORCH/tests/agt-R2-stage-current-port-0541-agt-R2-stage-current-0541-exact495-1023054548-22087/log.txt`.

Initial service attempt `...1023054433-9173` had 3 failed / 3 passed: two fixture locator failures because a plain archive cannot answer the existing Git-commit lookup, plus the same nullable-speed failure. Corrected only the named service environment/locator, retained the exact imported Runtime, and reran due to those unresolved setup failures. The corrected run above supersedes it; no repeated green or full suites were requested.

## Quality commands and results

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_commit_patch.py tests/sdk/test_timeline_pristine_initialize_runtime.py tests/editing_conformance/test_inverse_stage_images.py
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-ae4e0e9662/mypy-scoped /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/_commit_patch.py --follow-imports=skip --ignore-missing-imports
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/w-ae4e0e9662/ruff make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-ae4e0e9662/mypy-ratchet /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

All **PASS**. Scoped Ruff clean; scoped mypy no issues in one file; normal Ruff 2149/2149; normal mypy 1914/1914. No budgets/baselines changed. Vendor lock current; artifact manifest current; whitespace clean. Logs: `/tmp/w-ae4e0e9662/{scoped-ruff,scoped-mypy,ruff-ratchet,mypy-ratchet,vendor,artifact}.log`.

Exact source-file SHA-256 values verified against `git show 48d7c5973:<path>`:

- `_commit_patch.py`: `5022bbb658fb865f72f120d80589f490a8c65bd45db69e56100f6d76328acdb6`.
- `test_inverse_stage_images.py`: `2365ad33012766f7531077f0608308d458452b57d210c85654b725b2584da338`.
- `test_timeline_pristine_initialize_runtime.py`: `1a27844dbf166b1a128796b593874a5fbe023ac57376a47c1a6cd80dc5bfbb6b`.

## Handoff and limits

Source port PASS; joined Runtime/source publication and complete all-three-redo acceptance remain pending. **Not overall R2/G4 DONE.** No full/browser/heavy/native14/crash24/farm or Proof-owned P4 HTTP-body runs. Broad contract preservation is supported by unchanged request/result code and bounded existing controls, not claimed as complete cross-product qualification.

Recommended next steps: independently review this exact three-file port; route explicit-null speed validation to its V2 owner; manager performs any necessary merge-forward after authored G234 lands, then requalifies the final combined tree. Current integration `900ba8f09cff705b5d2db8d31021e4c2ad3f7786` has a separate authenticated root-input helper: `inverse_closure` now delegates to `Closure(bundle, source_bundles=sources)`. Preserve that helper and its guards during merge; apply only this worker's before/after stage hunks, never replace the whole older file. No integrated source was modified here.

`BLOCKED` records the acceptance blocker; `DONE` is intentionally absent. Commit message is ready for harness; final own SHA will be assigned after worker exit.
