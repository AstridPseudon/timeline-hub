# R2 core join 1852

## Union and source identity

Base: `78738040d72ce74c42ddf7731221aecb06f9246d`.

Imported exactly eight paths and no ancestry or report artifacts:

- `255751f40`: `astrid/sdk/timeline/_step_undo.py`, `astrid/sdk/timeline/inverse.py`,
  `tests/editing_conformance/test_inverse_aba_partition.py`,
  `tests/editing_conformance/test_nested_inverse_order.py`,
  `tests/editing_conformance/test_nested_native_aggregate_partition.py`,
  `tests/editing_conformance/test_nested_parent_mirror_ranges.py`.
- `d146b4204`: `astrid/sdk/timeline/_root_inverse.py`,
  `tests/editing_conformance/test_transient_root_baseline.py`.

Every working-tree blob was compared byte-for-byte with its named source. Git blob IDs:

```text
db1dd6cc09a6f9b7cf59f8af9e49cdb9d682eb74  _step_undo.py                         255751f40
1b551173ebdf7a31a012573a92a02190918218ca  inverse.py                            255751f40
0c23acf7599509d325c09afe02256eebe4ff50a6  test_inverse_aba_partition.py        255751f40
264a0b336a67e21afacb1d4f93f81e482589638d  test_nested_inverse_order.py         255751f40
7bff6baef0e5c1559a401a4e812dc50756b07fae  test_nested_native_aggregate_partition.py 255751f40
d8ccb0d5db11e8645768ed683494f270292a55aa  test_nested_parent_mirror_ranges.py 255751f40
30f6d7803e1a76ecdcda1daf3c6d8496c7ea4d57  _root_inverse.py                      d146b4204
abfc95afc351957fb19789900d4c9e01392bc963  test_transient_root_baseline.py      d146b4204
```

The eight SHA-256 source/working-tree matches and evidence hashes are in the permanent
worker evidence directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-core-join-1852/evidence/SHA256SUMS`.

## Joined behavioral proof

The explicit-node joined selection collected exactly **170 tests** and passed **170** in
84.72s. It contained the existing 110 focused tests, five split nodes, fourteen original
media nodes, all 22 ABA nodes, all 10 new transient-root nodes, the original transient-root
node, and eight captured-redo restoration controls. No test body, skip, xfail, filter, or
schema change was made.

The exact joined invocation used `venv-agent/bin/python -m pytest -q --tb=short -p
no:cacheprovider` with these four complete files:

```text
tests/editing_conformance/test_nested_parent_mirror_ranges.py
tests/editing_conformance/test_inverse_registry_containers.py
tests/editing_conformance/test_nested_inverse_order.py
tests/editing_conformance/test_nested_native_aggregate_partition.py
```

It added explicit node IDs for the five split cases, fourteen named original media cases,
`test_inverse_aba_partition.py`, `test_transient_root_baseline.py`, the original
`test_create_edit_whole_undo_redo_retains_transient_roots`, and the eight named
`test_captured_redo_media_closure.py` controls. A preliminary multi-`-k` collection probe
was discarded because pytest applies only its last `-k`; it ran no tests.

Critical capture reruns passed:

- `test_inverse_aba_partition.py`: **22 passed** in 52.71s.
- `test_transient_root_baseline.py` plus the original transient-root node: **11 passed** in
  4.79s.

The retained capture plugins were adapted to this worker's own permanent evidence path,
not pasted into tests. They captured module origins and hashes, provider requests/replies,
full accepted history, stage bindings, root inputs, effect validation, refusals and private
pre-validation captures. JSON captures are gzip-compressed to keep permanent evidence at
13 MB. Before/after module hashes agree for the modules loaded in both capture processes;
the root process also records `_root_inverse.py` before root validation in
`original-postpatch.json`.

## Static and boundary checks

- Ruff on all eight paths: passed.
- Private mypy on all eight paths: `Success: no issues found in 8 source files`.
- Ruff ratchet: `current=2149 baseline=2149`.
- Mypy ratchet: `current=1912 baseline=1912`.
- `scripts/vendor_lock.py check runtime.lock.json`: `ok runtime.lock.json`.
- `scripts/artifact_manifest.py --check`: `artifacts.json is current`.
- `git diff --check`: passed.
- Tracked changes are limited to the three modified product files; untracked changes are
  exactly the five new focused tests. All other tracked paths are byte-identical to base,
  including `_commit_patch.py`, `commit.py`, `store.py`, registry/R1/A4/legacy paths,
  frozen pins, and generated/artifact files.
- Credential scan over source and permanent evidence, including decompressed captures:
  no credential patterns found.

The independent ABA review `agt-R2-ABA-final-review-1852` subsequently completed **PASS**:
22 new ABA cases, 129 existing selections, static/ratchet/vendor/artifact checks, and
credential scan all passed. This worker made no merge/request; Runtime and broader suites
remain outside this qualification.
No full, browser, HTTP, Runtime, P1/P4, or other out-of-scope suites were run.
