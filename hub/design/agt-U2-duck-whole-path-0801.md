## U2 whole-path report

- Read `PLAN.md` §3, `commit-v2.md` §§1–5, and `BOARD-HEADER.md`.
- Classification: fixture inconsistency, not a product/API gap.
- `create_empty()` seeds both `parent.clips` and `parent.config.clips` as `[]`.
- The failing seed edits only `parent.clips`; `Checkout.open()` does not reconcile mirrors.
- `Checkout.publish()` reaches the Agent emitter, where strict validation rejects the unequal mirrors with `contradictory parent mirrors` before Runtime commit.
- Runtime is therefore never reached. Duck execution, adoption, and tagged rerun remain unexecuted.

Existing faithful seams:

- Canonical fixture: `tests/packs/timeline/test_parent_clips.py::app_shape`, which mirrors the list into both fields.
- Public helper: `astrid/sdk/timeline/lookup.py::_parent_clip_list`; accessing `tl.clips`/`tl.clip(...)` synchronizes the mirrors when only one is populated.
- Existing emitter tests confirm contradictory nonempty mirrors must remain rejected.

No source, test, assertion, guard, or fixture changes were made. No local pytest run was performed; the managed result was `135 passed, 1 failed in 39.04s` for the prescribed suite, failing at the seed publication.

Verification:

```text
git status --short && git log -1 --oneline
# clean
# ccf87bd949 test(agent): restore U2-boundary-final behavioral coverage
```

Required commit message and `DONE` marker were created.