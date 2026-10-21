# Agent document-diff second presence safety review

## Verdict

**DO NOT APPROVE** `fa36a85f41aef1ff6270edc3b9e296b5c16c74e7`, tree
`83c3d869e2d82a3ae1bb2c2df07b5bd34ffef4f2`.

The repair closes every concrete counterexample in
`agent-document-diff-presence-track-safety-review.md`, but it does not yet
meet the stronger requirement that a changed document can never return a
zero-command success.

## Closed prior findings

The changed adapter now uses the explicit `MISSING` sentinel for `params`,
`at`, `from`, and `to`; whole-field null/absence transitions visibly refuse
because no lossless native command exists. The held internal-field comparison
uses the union of live and pinned keys, so deleting `layout`, `effects`,
`audio`, or `opaque_timeline` visibly refuses. These refusals happen while
the caller's candidate draft remains unchanged.

The parent and child present-null `hold` clears still emit `clip.set` with
`clear: ["hold"]`; ordinary declared parameters still emit
`clip.set-params`; ordinary parent timing still emits `clip.move`; and parent
track rename still emits `track.set`.

## Blocking counterexamples

Using the existing `tests.timeline.test_authoring_feedback.bundle()` fixture:

1. Add `work["parent"]["new_opaque"] = None`, leaving
   `base_parent_payload` absent. `document_diff_to_commands(work, base)`
   returns successfully with `commands == []`.
2. Add `work["parent"]["config"]["new_opaque_config"] = None`, leaving the
   pinned config field absent. It likewise returns `commands == []`.
3. Set the corresponding Runtime parent and pinned parent field to explicit
   `None`, then delete it from the live parent. This reverse transition also
   returns `commands == []`.
4. A child internal timeline whose Runtime/pinned `registry` is absent but
   whose live `registry` is explicit `None` returns `commands == []`.

The first two and reverse cases are caused by the held-field loops at
`astrid/sdk/timeline/document_diff.py:423-426` and `:437-440`, which compare
`Mapping.get()` results instead of presence-aware `_field()` results. The
registry case is caused by `:385-387` and the intentional registry exclusion
from the union at `:413-414`. Each is a changed authored document accepted as
success without a command or refusal.

The minimal repair is to use presence-aware comparisons for these held maps
as well (and retain the registry's media-specific validation), or to refuse
the corresponding presence transitions before returning. Do not normalize
these cases to `None`/absence equality.

## Acceptance/refusal inventory

| Case | Result on `fa36a85f4` |
| --- | --- |
| `params`, `at`, `from`, `to`: null -> absent | Refused, draft retained |
| `params`, `at`, `from`, `to`: absent -> null | Refused, draft retained |
| Child held `layout`, `effects`, `audio`, `opaque_timeline` deletion | Refused, draft retained |
| Parent/child present-null `hold` clear | Accepted as one native `clip.set` clear |
| Declared ordinary params (`hello` -> ordinary value/clear) | Accepted as `clip.set-params` |
| Ordinary parent timing | Accepted as `clip.move` |
| Parent track rename | Accepted as `track.set` |
| Script/slot `None`/`hello` preservation | Retained prior non-HTTP evidence; not requalified here |
| Parent/config/registry held-field presence changes above | **Incorrectly accepted with zero commands** |

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_feedback.py -k 'document_view_adapter'`
  — **17 passed, 15 deselected**.
- Inline read-only Python probe over both directions of all four scalar
  fields and all four held internal fields — **8 bidirectional scalar
  refusals + 4 held-field deletion refusals; drafts retained**.
- Inline read-only Python positive probe — ordinary child `hello` parameter
  edit emitted `clip.set-params`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/document_diff.py tests/timeline/test_authoring_feedback.py`
  — **All checks passed**.
- `git diff --check` — **passed**; worktree has no product changes.
- Retained prior compact evidence: **88 passed, 2 deselected** from the
  non-integration document/media/provider lane. The requested broad 111 lane
  was not rerun.

The authenticated HTTP fixture diagnosis remains separate and unverified; no
HTTP, Runtime-door, browser, or full-suite pass is claimed here.

## Final candidate identity

- Commit: `fa36a85f41aef1ff6270edc3b9e296b5c16c74e7`
- Tree: `83c3d869e2d82a3ae1bb2c2df07b5bd34ffef4f2`
- Reviewed delta: `aba0346ae..fa36a85f4`
