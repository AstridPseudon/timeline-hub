## Result: FAIL — author attribution

The Runtime fixture is valid; the refusal is an Agent V2 defect.

- Exact test command failed 1 test in 1.77s:
  `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_acceptance.py::test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated`
- Failure occurs before Runtime `port.accept`, at Agent `validation.py:308`, path:
  `candidate.shots['shot-1'].internal_timeline.clips['clip-1'].clipType`.
- Archived source has `clipType: "media"` and this exact unchanged legacy `elementRef`:

  `{"anchor":{"document_id":"transcript:17355111119f90c26b53f1be25ebc2a0589a646edb85a498b2d16071bcdbeeab","word_id":"word-1"},"binding_id":"4510c89c-f3a9-5605-aa0a-9289d6060ab6","kind":"text"}`

  It has no `id`. The isolated project has the equivalent project-scoped value.
- Native move targets `parent/clip:music-bed` and only writes its timing fields; it does not modify `shot-1/clip-1` or its `elementRef`.
- Agent V2 unconditionally selects `elementRef.id` in `_validate_params`, even with unchanged/absent params, then rejects when missing. This violates approved D12 preservation.
- D12’s negative controls remain correct: new, modified, and target-invalidating timing declarations are 422 invalid; unchanged unresolved legacy declarations are accepted and retained.

Provenance: Runtime `be5848e17` / tree `d6f20f84`; Agent current `f95f1e169` / tree `a356b2d2`; V2 checkpoint `9729c07b7`. Validation blob is identical across Agent current and V2 checkpoint. Worktree is clean; `git diff --check` passes. No product or fixture changes made. `DONE` and commit message were written.