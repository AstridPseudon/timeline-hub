# G5 retained-restore oracle — independent no-weakening review (1948)

## Disposition

**PASS for this targeted oracle review.** The `697c8fd3b` → `68fbe54e8`
change is a faithful C0 identity correction and does not weaken the
retained-restore behavior assertion. It is not whole-G5 approval, merge or
activation approval, or a P1 GO.

## Findings

- The diff is exactly one file, `tests/sdk/test_timeline_checkout_history_runtime.py`,
  with 9 insertions and 1 deletion. Only
  `test_retained_restore_does_not_reopen_consumed_draft_steps` differs; the
  other three original test functions, fixture, and helper bodies are
  AST/source-identical to `697c8fd3b`.
- The expected bundle changes only `base_parent.publication_id`, binding it to
  the actual restore receipt. Exact base-parent identity, full
  `Checkout(expected).document()` equality, and explicit
  `source_mapping['_runtime_document']` equality remain. Revision, digest,
  payload, children, pins, owners, null/opaque values, registry/media,
  transcript/source identity, and closure remain protected.
- Consumed unsent undo/redo refusal and fresh post-reset undo/redo assertions
  remain verbatim. No partial compare, schema reinterpretation, guessed
  identity, history rewrite, fake fixture, or production change was found.

## Evidence

Corrected preflight passed on Agent `68fbe54e83929a7959e92cf71dc69b0f235dba52`
(tree `0f68605f43f8773df21112816bb8b3e822967039`) and Runtime
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` (tree
`f79a2355cfb39d9ada7721978bd20d5702105778`). The authentic archive SHA-256
was `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`;
verify/restore and all body locks passed; credential findings were zero.

The required changed node ran once and passed: `1 passed in 19.54s`. The
observer recorded child boot first, 37 lines, 13 seam entries/exits, zero
seam exceptions, zero observer failures, and 3418/3418 expected module hashes
matching the exact Agent/Runtime roots.

Current and base-stdin Ruff produced the same four inherited diagnostics
(F401, F811, I001, F811). Private mypy reported `Success: no issues found in
1 source file`; vendor lock, artifact manifest, and `git diff --check` passed.

## Limits

The prior 1937 original FOUR result is reused accurately: the other three
functions passed and this original target was the one failure. This review ran
only the changed node, not another FOUR or the full suite. The permitted
observer still does not expose the second reset's public `open_bundle` success
body; no identity was inferred from it. Keep G5 draft-only and P1 NO-GO.
