# Agent G5 current-refresh draft report

## Verdict

**Source-only PASS.** The reviewed G5 47-path delta was ported onto current
base `78738040d72ce74c42ddf7731221aecb06f9246d`. This remains a draft:
P1 is NO-GO, so no merge request, integration merge, activation, or source
actor approval is claimed.

## Source union and scope

- Donor: `bda966e9c491e1fa4b683cda8913dddeaa14c63d`.
- Reviewed scope: exactly the 47 paths in `6531622c8..bda966e9c`.
- Worktree source union: 47 changed paths, with no extra product/test files.
- All donor blobs outside intentional protected overlaps match the donor
  exactly. `astrid/sdk/timeline/document_diff.py` was deleted with
  `apply_patch`.
- `store.py` is the required mechanical context merge: reviewed G5
  retirement content plus the current exact Runtime head
  revision/publication reader. The obsolete revision-only unique-publication
  lookup was not restored.
- Preserved unchanged from current: the 75f current-pair reader/test, R1
  f078 commit and `_commit_patch.py`, registry 22f inverse, A4 track and
  transcript witness files, legacy d1d validation/commit/timing files, and
  all other current product/test blobs.
- Production route scan found no active `commands-file`,
  `publish_bundle`, `three_way`, retired `document_diff.py`,
  separate-publish, `apply --native`, or legacy publication CLI writer.
  An inherited stale old-route mention remains in
  `astrid/packs/rendering/docs/SKILL.md:229`; it was not changed.

## Checks

- Current-pair reader, Runtime pin `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`,
  authentic archive SHA
  `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3):
  **16 passed**.
- Existing owner-scope controls:
  `tests/sdk/test_remote_timeline_owner_scope.py`: **6 passed**.
- Bounded reviewed acceptance set, Runtime pin `d9e2a71e`, 8 specified
  files: **184 passed in 46.11s**.
- Ruff ratchet: **2148 current = 2148 baseline**.
- Private Python 3.11 mypy ratchet: **1911 current = 1911 baseline**.
- Vendor lock: **ok** against `/home/user/work/wt/rt-pin-34eac004`.
- Artifact manifest: **current**.
- `git diff --check`: **pass**.
- Credential-shaped scan over existing reviewed-scope files: **0 matches**.

## Limits and decisions

The reader test initially hit the known harness `tmpdir`-is-a-file issue;
the final run used a fresh private `/tmp` directory. A mechanical add-file
header artifact was corrected before the final tests; all five added donor
files now match their donor blobs. No SDK FOUR, c271, public redo, old 14/110/9,
full suite, browser, live HTTP/socket, P1/P4, or other prohibited body was run.
The joint-audit evidence remains qualification FAIL/unproven, and P1 remains
unchanged.

No commit, merge, push, or integration request was performed. The conventional
G5 commit message and empty DONE marker are present for the harness commit.
Permanent SHA and credential-scan evidence is in the worker evidence
directory.
