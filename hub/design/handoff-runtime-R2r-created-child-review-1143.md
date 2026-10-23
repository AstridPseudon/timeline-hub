# Runtime R2r created-child independent review — FAIL

Exact candidate `e99c4221428943279029036c575f6d48598bf886` was reviewed against
PLAN §3 R2r and C0 §§1–3. Targeted Runtime checks pass (**239 passed**, Ruff,
Pyright, AST/diff checks), and the candidate preserves the d106 frozen schema
digest with a two-file diff.

The review cannot qualify the candidate:

- A bounded authenticated public `RuntimeService.commit_timeline` run using the
  real Agent provider reached the final grouped native create → child track →
  child held-image request, then Runtime refused it at
  `timeline_commit_auth.py:329` with `provider dependency union omits a captured
  read`. No accepted receipt/store/history/readback exists for this required
  caller path. The author’s direct helper witness is not sufficient.
- `_project_created_child` chooses the first accepted shot revision matching a
  `shot_id` (`next(...)` at lines 1040–1044) instead of refusing an ambiguous
  physical root. A direct probe returned `accepted_without_refusal`.
- With `identity_scope`, lines 1082–1087 derive authoring physical IDs but do
  not assert equality with the accepted closure’s physical IDs. A probe with
  foreign accepted IDs returned `accepted_without_refusal`.

The first item is the exact missing caller authority; the latter two are
independent authentication gaps. Runtime/Agent owners should repair the
provider dependency-union seam and add explicit ambiguity/identity refusal
coverage before re-review. No product or test changes were made by this
review, and no full/prohibited suite was run.
