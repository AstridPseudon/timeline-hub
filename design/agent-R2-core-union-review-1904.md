# R2 core eight-path union review

## Verdict

**Semantic review: PASS, conditional on the clean port.** The eight requested
paths in `aa358229f9cbfaf7edea4cd484495b8f3a9d943b` match the named independent
source commits byte-for-byte, and the scoped behavioral/static checks passed.

The commit also contains the known ninth tracked path,
`design/agent-R2-core-join-1852.md`. It is a review artifact, not part of the
eight-path product union and is not approved for integration. The clean port
must contain exactly the eight paths below, with the same blobs, and no report
artifact. No semantic review should be repeated once that port hash matches.

## Exact source identity

| source | paths | current blob(s) |
| --- | --- | --- |
| `255751f40a38263b8a032d15b807a3a3e2742a9c` | `_step_undo.py`, `inverse.py`, and four nested/ABA tests | `db1dd6c`, `1b55117`, `0c23acf`, `264a0b3`, `7bff6ba`, `d8ccb0d` |
| `d146b4204f6f9efa526134d810e581a282377a9a` | `_root_inverse.py`, `test_transient_root_baseline.py` | `30f6d78`, `abfc95a` |

All eight comparisons are exact Git-blob matches. The only non-union path in
the joined commit is the known design report artifact above. `git diff --check`
is clean; runtime lock, artifact manifest, commit/store/patch paths, and the
provider caller test are unchanged.

## Review coverage

- Native-only history keeps its existing whole-inverse fallback.
- Accepted publication/step identity, command ordinal, native-write ranges,
  effect ranges, and compiler mirror attribution are rechecked before use.
- Zero-effect and property-only stages reconstruct only authenticated mirror
  images; structural stages recover order without creating members.
- Root birth/baseline restoration checks accepted source ownership, full
  baseline values, stage writes, and the post-commit owner image in detached
  guard state.
- Physical binding, owner/digest, later-consumer, ABA, and existing inverse
  protections remain in the unchanged surrounding implementation. Effect
  patches are used for validation/receipt projection only; mutation proceeds
  through the recorded native writes.
- No credential-like material was found in the eight reviewed paths.

## Commands and results

The first critical-test invocation failed at collection because the shared
Runtime import path was absent (`ModuleNotFoundError: runtime_protocol`); no
test ran. With the worktree and shared Runtime checkout on `PYTHONPATH`, the
same scoped command passed:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_provider_step_undo_v2.py::test_create_edit_whole_undo_redo_retains_transient_roots
23 passed in 17.12s
```

```text
RUFF_CACHE_DIR="$TMPDIR/agt-R2-core-union-review-1904/ruff" /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_nested_parent_mirror_ranges.py astrid/sdk/timeline/_root_inverse.py tests/editing_conformance/test_transient_root_baseline.py
All checks passed!

MYPY_CACHE_DIR="$TMPDIR/agt-R2-core-union-review-1904/mypy" PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml --follow-imports=skip --ignore-missing-imports --namespace-packages --explicit-package-bases --cache-dir="$TMPDIR/agt-R2-core-union-review-1904/mypy" astrid/sdk/timeline/_step_undo.py astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_nested_inverse_order.py tests/editing_conformance/test_nested_native_aggregate_partition.py tests/editing_conformance/test_nested_parent_mirror_ranges.py astrid/sdk/timeline/_root_inverse.py tests/editing_conformance/test_transient_root_baseline.py
Success: no issues found in 8 source files

/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
ok runtime.lock.json

/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
artifacts.json is current
```

No full, Runtime, browser, HTTP, SDK-four, or duplicate joined suites were run.
No source or test files were altered by this reviewer; no merge, commit, or
push was performed.

## Handoff

Approve the clean eight-path port only after independently confirming its tree
has the eight matching blobs and no tracked report artifact. Manager owns the
merge and any final integrated-suite decision.
