# Runtime saved-revision real-capture review

Verdict: APPROVE.

Reviewed Runtime tree `d962e7a1d4abfabdbc4a12e35b5b647b750cfa8a` (tree `6bfe0591b64cda6e9b0bb48656e4a4cd7dc5643e`) against `7e160c5d254a9b3d42a28672a2d7e2ac1acd5ca8`. The only changed product-repo path is `tests/test_spec_reference.py`; no Runtime product code, DTO, endpoint, renderer, scene evaluator, second verifier, or save writer changed.

The port preserves the target's persisted-authority redaction/no-mutation assertions, exact saved `parent-1` revision hydration, host materialization equality, and missing retained-parent refusal. It now ingests the fixture's `source video`, accepts the fixture publication through the existing `TimelineCommitStore`/schema validator helper, and projects the accepted closure through the Agent provider loaded by `load_timeline_commit_provider("astrid")`. The managed media digest is explicitly admitted in `input_object_ids`.

Provenance and hashes checked:

- Final Runtime source: `d962e7a1d4abfabdbc4a12e35b5b647b750cfa8a`; final tree `6bfe0591b64cda6e9b0bb48656e4a4cd7dc5643e`.
- Final Agent checkout used by direct/service checks: `/home/user/work/agent`, `a760ecca02111b0e0841510926f200e398f3b6cb`.
- Ingested bytes hash to `sha256:34edefb5a55a8cf230cf951322f466a6b19ee29f7147caeaddd69cc85b026141`, matching the fixture media ID and publication references.
- Canonical parent payload hashes to `sha256:9e3c93e1cce58dddb37c775b2e1a0ee6c90548edbf3d8485d065472121052369`, matching the saved authority digest and the accepted closure's runtime digest.
- Fixture child payload hashes checked: shot `sha256:583bab39d29808729c9c9d988b8ac90b89182949a788fd8bc4b9fa2e5c668138`; internal timeline `sha256:1916ab9ac6df998f7d81b1575df507070bc1a03551badaca0279b56b49a379ce`.

Evidence:

```text
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source
1 passed in 2.88s
```

Required central final-source scoped service run also passed:

```text
capture-legacy-integration --files "tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source"
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source
1 passed in 1.61s
```

The service snapshot was Runtime tree `6bfe0591b64cda6e9b0bb48656e4a4cd7dc5643e` with Agent source `a760ecca02111b0e0841510926f200e398f3b6cb`.

The earlier central batch (`165 passed, 5 failed, 4 deselected`) was on the pre-correction snapshot and is not final evidence. Its four neighboring `RenderRequest.verified_source` failures are separate and were not changed. No broad/full suite, renderer, browser, PCM, scene-evaluation, or live-socket claim is made.
