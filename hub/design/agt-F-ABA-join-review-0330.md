## PASS — joined ABA projection review

Reviewed `bb172407fc` on `622b30a8c3`.

- Combined `_commit_patch.py` functions preserve current guarded reorder/history/list-move and root behavior while adding authenticated inverse-stage projection:
  - `CommitPatch.after`
  - `CommitPatch.finish`
  - `rebase_patch`
  - `_materialization_sites`
  - `inverse_address_resolver`
- Production caller: `astrid/sdk/timeline/commit.py`, `RuntimeCommitService.commit`; Runtime remains authoritative.
- C0 v2 request/reply ABI unchanged.
- Donor test blob matches exactly: `e7f006...ab95c4`.
- Original `test_authoring_media.py` unchanged: `e22fb9...9015c`.

Tests:

- Donor lane: **55 passed**
- Neighbor lane: **112 passed**
- Current reorder/history lane: **42 passed**
- All 16 corrupt-carrier negatives: **16 passed**
- Ruff, private mypy, vendor lock, artifact manifest, and `git diff --check`: **passed**

No product edits were made. No blockers.

Limitations remain as disclosed: original live service141, full/browser suites, and known broader transient-create/edit and multistage-child probes were not rerun or waived.