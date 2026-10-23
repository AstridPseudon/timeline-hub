# R2 nested compiler and emission — agt-R2-nested-emission-sol-1603

Agent offline source qualification: **PASS**. Independent review and actual joint Runtime/public positive: **not run / not claimed**. No blocker to independent source review.

## Source and lossless evidence

- Worktree `/home/user/work/wt/agt-R2-nested-emission-sol-1603`; base `98ef2f9c95fd43d88cca2909d8d1518302e3050c`.
- Read PLAN §3, the independent 1515 report, the lossless 1500 packet and its retained predecessor, original b54d packet, and Runtime's 1543 handoff including its private-range interface.
- Full packet: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-staged-redo-1500-3a718d9537faec49.json`; 4,790,931 bytes, SHA-256 `3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09`. All 31 embedded text entries checked against their stored byte counts and hashes.
- Original packet SHA-256 `b54d2efee42e093485e7ad6a4c73e7fca2c8318ad0b02cdbcde9330c3750eff3`.
- One added test file embeds the **entire untransformed retained 1404 capture**, 444,166 bytes, SHA-256 `9a47bb934b879efa0f6147d673038cee76299ba4e30ab22b6d5bcb1377ade589`. No fabricated/minimized history, new ordinal, source retargeting or accepted edge is introduced. Its SQL dump is replayed in memory to read the original persisted canonical documents, then checked byte-for-byte by `iterdump`; no realm provisioning, Runtime writer or public inverse is invoked.

## Correction and exact interface

1. `_step_undo.inverse_stages` partitions the accepted immediate inverse's native writes by its retained inverse.stage bindings, rejects missing/overlapping/foreign coverage, and reverses the slices. It preserves the immediate publication, step and command ordinal. The view carries the exact inverse of each accepted effect slice internally; accepted source records are never rewritten.
2. `_root_inverse.restore_root_baselines` installs the existing native-only `_RestoredShot` provenance at the restored intermediate root. It requires an accepted nested inverse, the same immediate historical allocation and owners, an exact historical shot payload and the exact captured complete native root. This keeps the legitimate intermediate text difference relative to the authenticated compiler baseline. The competing-media guard stays active; no authoring compiler or guard waiver changes.
3. Inverse execution retains each intermediate bundle. `_commit_patch` compares inherited inverse effects against the independently compiled stage effects before retaining their exact reversed source order, then emits bindings for each intermediate closure using current request attribution. No root copy, caller history injection, original-publication retargeting or new materialization edge.

Exact retained immediate source:

- Publication `txn-75285c95600949c8b1267a71f8e71a9d`, revision `document-diff-e0c6162a4844471b99fd8d1076df92e9-parent-revision`, step `undo-0`, command ordinals `[0]`.
- Its accepted inherited partitions are native `[0,1]` / `[1,3]`, effects `[0,5]` / `[5,9]`. Their original source is `txn-7d039d147e1b4c5ba6cc7ca912b95cba`, steps `fork-edit-1` ordinal `[1]` then `fork-edit-0` ordinal `[0]`; these identities remain immutable historical facts.
- Outward request still has exactly one `redo-0` step / `[0]` command. TWO inverse.stage bindings both target the SAME immediate `undo-0` / `[0]` identity, in execution order: native `[0,2]`, effects `[0,4]`; then native `[2,3]`, effects `[4,9]`.
- Every emitted native capture equals the exact reversed immediate source capture with before/after exchanged. All nine canonical effects equal the exact reversed immediate source effects. The twelve commit.effect bindings preserve the corresponding historical physical refs, owners, pins and digests with exchanged sides while using the current request base/head/step attribution. No commit.materialization binding is invented. The complete canonical output equals the retained expected document, including opaque data and retained inputs.

The initial hypothesis that changing only the Closure call would solve compilation was insufficient: the intermediate restored root differs from the immediate historical source in accepted text state. The retained source root and its immediate compiler baseline must remain distinct. The final fix installs provenance at restoration; the original Closure call remains unchanged.

## Commands and results

Commands below run from the worktree unless a `cd` is specified. No full, broad58/281/40, P1–P4, native14, publicredo, browser, localhost or live socket suite was run or requested.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_captured_nested_redo.py --basetemp=/tmp/w-dbb84adcc5/pytest-release
# PASS: 11 passed in 1.06s (final test/source hashes below).
```

The eleven cases cover exact output/partition/attribution, original native slices, native gaps/overlaps, effect gaps/overlaps, foreign publication, changed owner, source digest, source scope and tampered accepted effect; refusal paths preserve input data. No passing pre-existing test was changed, skipped, weakened or xfailed.

Causal RED, on the same final test file. `baseline-source` contains the four exact `git show HEAD:<path>` source files; other package files are read-only links to this unchanged worktree. `sliced-source` differs from that baseline only in `_step_undo.py`, using this candidate's actual partitioning. These are private source overlays, not dependency changes or injected history.

```bash
cd /tmp/w-dbb84adcc5
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-dbb84adcc5/baseline-source:/home/user/work/wt/agt-R2-nested-emission-sol-1603:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q --import-mode=importlib -p no:cacheprovider /home/user/work/wt/agt-R2-nested-emission-sol-1603/tests/editing_conformance/test_captured_nested_redo.py --basetemp=/tmp/w-dbb84adcc5/pytest-causal-final-baseline
# Expected RED, exit 1: 7 failed, 4 passed in 1.26s; flattened native/effect ranges and absent partition tamper checks.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/w-dbb84adcc5/sliced-source:/home/user/work/wt/agt-R2-nested-emission-sol-1603:/home/user/work/wt/rt-pin-cfa0af0d /home/user/work/venv-agent/bin/python -m pytest -q --import-mode=importlib -p no:cacheprovider /home/user/work/wt/agt-R2-nested-emission-sol-1603/tests/editing_conformance/test_captured_nested_redo.py --basetemp=/tmp/w-dbb84adcc5/pytest-causal-final-compiler
# Expected RED, exit 1: 1 failed, 10 passed in 1.26s; actual competing-selected-media compiler refusal before Runtime.
```

Logs: `/tmp/w-dbb84adcc5/causal-final-baseline.log`, `/tmp/w-dbb84adcc5/causal-final-compiler.log`. Earlier two-case exploration gave baseline 2 FAIL and slices-only 1 FAIL / 1 PASS; final eleven-case runs supersede those counts. Intermediate new-test assertion mistakes concerning boundary field names and optional owners were corrected against the actual captured bindings; no original behavioral expectation was weakened.

Static and integrity checks:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d RUFF_CACHE_DIR=/tmp/w-dbb84adcc5/ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
# PASS: current=2149 baseline=2149.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/w-dbb84adcc5/compare_scoped_ruff.py
# PASS: introduced code/message diagnostics against exact HEAD source = [].
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-cfa0af0d MYPY_CACHE_DIR=/tmp/w-dbb84adcc5/mypy-private-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
# PASS: current=1912 baseline=1912.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/inverse.py astrid/sdk/timeline/_root_inverse.py astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/_commit_patch.py --cache-dir /tmp/w-dbb84adcc5/mypy-scoped --hide-error-context --no-pretty
# PASS: no issues found in 4 source files.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
# PASS: ok runtime.lock.json.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# PASS: artifacts.json is current.
git diff --check
# PASS.
```

Environment-only failed attempts, without dependency mutation: initial pytest omitted Runtime's import path and stopped during conftest import (`ModuleNotFoundError: runtime_protocol`); the corrected commands above use the frozen cfa0af0d import tree. Initial mypy with `/home/user/work/venv-agent/bin/python`, `MYPY_CACHE_DIR=/tmp/w-dbb84adcc5/mypy-cache`, otherwise the same baseline command, failed before checking due to missing yaml stubs and numpy Python-version syntax. The existing read-only private typecheck environment passes both required checks. No stubs or shared environments were installed or changed.

## Artifacts, decisions and remaining work

- Early exact interface: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-nested-emission-sol-1603-interface.md`.
- Exact candidate request, records, steps, canonical output and source hashes: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-R2-nested-emission-sol-1603-emission.json`, 91,782 bytes, SHA-256 `0d8ea4eded46ff7b0e9a0eef6e58a248eb0511ad98d4bbb0dc9def62c4138174`.
- Decisions: follow the settled Runtime immediate-identity interface; use existing accepted native provenance for the actual compiler baseline; keep exact inherited effect order after independent compilation comparison. No contract decision changed.
- Only the four permitted inverse source files and one focused captured regression changed. No commit.py, private R1, CLI, publisher, native_auth, schema, client, pin, lock, dependency, archive or tracked report changes. No Git mutation or shared dependency/cache writes.
- Full C0 v2 request fields remain intact in the retained complete request and no request/reply routing code was changed. Runtime accepted/merged receipts, preview would_status, and structured errors were not exercised here; no public end-to-end claim.
- Next: manager assigns independent Agent source review, obtains independent Runtime source PASS, and only then assigns the actual joint positive. This worker did not duplicate Runtime private verification or advance that gate.

## Final SHA-256

- `astrid/sdk/timeline/_commit_patch.py`: `06e35825df4f6578ef192de92ab27dbc5131484d99c4953f001293f9bad9490c`
- `astrid/sdk/timeline/_root_inverse.py`: `0d81d995582622367cca770855d7604735d3a707a7e8d6d6d5d6102367c4949a`
- `astrid/sdk/timeline/_step_undo.py`: `6cedff390a06ff74a957b962199efb4144b82e2e7e48664269098f39fbae8915`
- `astrid/sdk/timeline/inverse.py`: `4e00ec2e1c629af6d0fa84a4b6f8992b0990b38460561849cb0bb11c70921325`
- `tests/editing_conformance/test_captured_nested_redo.py`: `36e2ea620e558e7516ccf93e0090c65d4f3fa85a3487ecc4c0d001a741b20fa4`
