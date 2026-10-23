# V4 D16 window adaptation — first return

## Change

Changed only `tests/editing_conformance/test_native_word_anchor.py`, in
`test_stale_anchor_refuses_when_intervening_window_excludes_selected_word`.

- Restored the original legacy seed: `parent/clips/id:card/app/astrid/on`,
  with no persisted `word_anchors` declaration.
- Restored `pick(case, 1)` and captured the selected command at the original
  base pair before any edit.
- Preserved the captured source, transcript pin, and selected stable word ID
  as explicit assertions.
- D16 mapping: the original accepted `window4..6` edit followed by stale
  replay is now represented by the `window4..6` edit refusing at that same
  original base, because it would orphan the existing legacy declaration.
  The captured stale request remains auditable but is not submitted, since the
  rejected edit cannot become an intervening head.
- Preserved the original refusal message match, `invalid_anchor` reason, and
  no-write/head assertions. Added the required exact legacy path assertion:
  `parent/clips/id:card/app/astrid/on`.

The old stale-replay `status=conflict` observation cannot remain observable
without accepting the now-invalid window edit or inventing a replacement
scope; the ruling requires the earlier refusal to be `status=invalid`. No
authored anchor, fixture rewrite, or alternate scenario was introduced.

## Source trace verdict

The independent review traced the missing structured path to the provider:

1. `astrid/sdk/timeline/_timing_evaluators.py:564-598`, `_bound_words`, raises
   `TimingCompileError` for the excluded word at line 598.
2. `astrid/sdk/timeline/native_word_anchor.py:378-381`, `compile_recorded`,
   catches it and raises `CommandError(..., kind='invalid_anchor')` without a
   `ref` or `path`.
3. `astrid/sdk/timeline/commit.py:1161-1174` propagates the empty path.
4. `astrid/sdk/timeline/_commit_errors.py:74-80` serializes it as `[]`.

The adapted test therefore intentionally expects the normative legacy path
and remains behavior-verification **PENDING** until the Agent provider error
path fix is available. Delivery behavior under test: source-window edits that
would orphan an anchor are refused at edit time with no head write.

## Checks

- `ruff check --no-cache tests/editing_conformance/test_native_word_anchor.py`
  — PASS.
- `git diff --check` — PASS.
- Typecheck — N/A; test-only adaptation.
- Known behavior command was not run, per task instruction, because the
  provider source correction is not yet available.
- No full, native14, browser, heavy, or other broad suite was run.

No merge, V4DONE, or behavior PASS claim is made.
