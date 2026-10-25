# D134 root-008 independent source validation

Result: **FAIL** on evidence quality only; no source or behavior change was made.

- Base/head: `96a6b2deea46eb33ba5184203a10e966cc5e9179` / same.
- Owned files: both byte-identical to their base blobs; function ASTs are unchanged.
- Root membership: authoritative cluster count is 18; the author map has 18 entries, but its raw node IDs omit `tests/editing_conformance/`. Raw set equality is false; prefix-normalized equality is true.
- Frozen R4 SDK reference: both owned paths are absent, so no frozen test blob was substituted.
- Runtime source boundary: the trusted provider loader is `runtime_protocol/timeline_commit_provider.py:70-90`; accepted Runtime derives `recorder_abi` from physical bindings at `timeline_commit_store.py:1832-1853` and stores the authenticated history metadata at `:2058-2082`.
- Agent source boundary: `CommitPatch.v2` is opt-in from request controls at `_commit_patch.py:277-295`; physical enrichment is at `:493-501`; legacy fork proof and authenticated ABI selection are at `commit.py:770-922,997-1022`.

Commands run:

- `PYTHONPYCACHEPREFIX=$TMPDIR/pycache /usr/bin/python3.11` AST parse and compile for both owned files: **PASS**.
- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_fork_abi1_binding_set.py tests/editing_conformance/test_recipe_occurrence_fork.py`: **PASS** (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy --cache-dir=$TMPDIR/mypy tests/editing_conformance/test_fork_abi1_binding_set.py tests/editing_conformance/test_recipe_occurrence_fork.py`: **PASS** (`Success: no issues found in 2 source files`). This is unchanged-source baseline evidence.
- `git diff --check`: **PASS**.
- `git status --porcelain=v1`: **PASS**, empty; tracked tree equals base: **PASS**.

Not run by instruction: pytest, collection, original18, replay, service/runtime calls, sockets, browser, native replay, family/full/core/tour/profile/collector/build/install/acquisition, or any body run. No retry or alternate qualification was attempted.

No product, test, fixture, schema, generated, pin, Runtime, upstream, hub, or other-worker file was modified.
