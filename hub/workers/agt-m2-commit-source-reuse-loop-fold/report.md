Implemented the cleanup in [commit.py](/home/user/work/wt/agt-m2-commit-source-reuse-loop-fold/astrid/sdk/timeline/commit.py:306):

- Folded opened-source and historical parent-revision reuse into one ordered scan.
- Preserved historical precedence, exact digest/manifest matching, and all existing source/closure behavior.
- No tests or schemas changed.

Tested:

`python3 -m pytest -q tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_commit_provider_scalar.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/editing_conformance/test_recipe_occurrence_duplicate.py`

Result: **159 passed**, 2 existing config warnings.

Commit message written and `DONE` created. No blockers; no full suite run.