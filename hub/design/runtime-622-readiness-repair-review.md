# Runtime 622 readiness-repair review

Date: 2026-10-20
Reviewer: `rt-m2-review-622-readiness-repair`
Base requested: `285a3b437c69d20e2af281c3d7fdd212cb784d1a`
Candidate reviewed: `ff0f69b11e12d5b2a0ea2f07a443874a15f51ca9`
Candidate parent: `e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`

## Verdict

**APPROVE `ff0f69b11e12d5b2a0ea2f07a443874a15f51ca9` for the next private
generation step.** This is generator compatibility tooling only. It is not
approval of normal generation, a Runtime artifact, a version, a consumer pin,
or a release.

## Exact diff reviewed

The candidate commit changes exactly two paths:

```text
M generators/command_schema_compatibility.py
M tests/test_command_schema_compatibility.py
```

The helper implements the approved historical 0.2.2 path: it first accepts a
direct containment result, otherwise deep-copies the previous schema, applies
only the five reviewed regex widenings plus the reviewed `track.set`
selection widening, and then proves containment of that intermediate schema
in the candidate. It does not rewrite candidate constraints.

The comparison uses JSON-structural equality (`json.dumps(..., sort_keys=True)`)
for enum/type values and sibling keywords, so JSON booleans and numbers are
not conflated. The existing public v1 floor remains unchanged. The helper
source is byte-identical to the approved Runtime proof at `62b5f8e` (content
SHA-256 `57cfb2e5c8cf50be2d5c47ec815e7e0f5d1109dc41bfb405402889a4dd11b90b`)
and retains the approved private helper semantics (Agent helper content
SHA-256 `542536e1ea1a4bdc18de8bf81c692b74162f751cfb56047fee408f378e450de9`).

The one new regression asserts that an unknown keyword whose value is JSON
`null` is still present and is rejected by both compatibility paths. There is
no candidate edit, error allowlist, samples-only shortcut, blanket regex
waiver, or new frozen JSON.

No operation inventory, DTO, generated artifact, package metadata, or normal
generator output changed in the candidate commit.

## Evidence

From an ephemeral archive of the exact candidate SHA (no checkout or
worktree movement):

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_command_schema_compatibility.py \
  tests/test_timeline_current_union_contract.py \
  -k 'not normal_generation'
```

Result: **186 passed, 9 deselected, 32.99s**. The deselected cases were the
normal-generation tests, intentionally not run for this review.

The exact candidate collected 131 compatibility cases and 64 current-union
cases. No full, native, live, or normal-generation run was requested here.

The candidate worker's exact-SHA targeted evidence (recorded before this
review) was:

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tests/test_command_schema_compatibility.py
```

Result: **131 passed**.

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tests/test_timeline_commit_type_generator.py \
  tests/test_timeline_current_union_contract.py
```

Result: **69 passed**. I did not repeat that generator-contract lane because
this review explicitly excludes normal-generation work; the isolated
compatibility/union run above is the review evidence.

Relevant passing tests include:

- `test_unknown_keyword_with_null_value_is_not_treated_as_absent`
- `test_historical_regex_rewrites_are_not_claimed_as_proven_widenings`
- all five `test_current_union_preserves_each_exact_floor[...]` cases,
  including the old public v1 floor
- `test_new_refs_and_union_require_a_structurally_retained_old_branch`
- `test_legacy_regex_proof_does_not_hide_other_constraints[...]`
- `test_legacy_regex_proof_does_not_hide_track_selection_narrowing`
- `test_shot_settings_keep_boolean_number_distinction[...]`

## Scope and next step

The candidate is ready to feed the approved helper into the next private
generation attempt. The next worker must still use the frozen Agent
357/613 source and manager-approved generation/version decisions, then qualify
the generated outputs independently. This review did not run normal
generation or validate generated artifacts. The Agent 357/613 freeze
acknowledgement was already recorded at 17:19.
