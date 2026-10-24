## Report

- Applied only the requested oracle hunk in `tests/timeline/test_authoring_media.py`.
- `git diff --check`: passed.
- Focused test failed at the new selector with `KeyError: 'internal_timeline_revision_id'`; checkout data nests the identity under `checkout_shot['internal_timeline']['revision_id']`.
- Stopped without broadening or rerunning. Downstream undo/retry/ABA remains unqualified.
- Wrote `BLOCKED` and commit message. No full suite run.