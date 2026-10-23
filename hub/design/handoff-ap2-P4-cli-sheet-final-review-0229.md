# Handoff: ap2-P4-cli-sheet-final-review-0229

**Verdict: PASS for the narrow corrected independent-review gate.**

`fe781e4d2` adds exactly 17 assertion lines over `a4a2a8d5`. Only
`tests/sdk/test_p4_cli_sheet_v2.py` changed relative to `68f2b23ff`; no product,
fixture, pin, generated, marker, skip, or xfail changes are present.

The test retains the real parser/handler → NativeSheet → semantic
`capture_move` → session/outbox path and explicit generated-client transport
fake boundary. It asserts the one-commit mutation as one generated call. It
also asserts the original `initial_bundle()` provenance (FPS 30,
clip `a`/`b`, IDs/text/closure), exact `clip.move`, one call, ABI-1 scope/base,
commands, label, complete step metadata including empty semantic patch, fields
merge, source, absent reads, dry-run false, and idempotency key. The new direct
assertions independently preserve the sibling, ordered clips, config, raw
fields, closure, order, and absences, while allowing only authored `at: 5` and
documented native-derived markers. Semantic empty step patch and fields merge
are contract-valid; no doc.patch-only/G3 defect is inferred.

The narrow witness does not prove Runtime or merged/conflict/invalid/preview/
history/show acceptance, complete response-value equality for canonical
closure/digest/head/receipt/authoritative steps/dependencies/merge_mode, or
ten-note/P4DONE/H3 acceptance. These limits are explicit at the fake boundary;
prior e73813PASS/755d3PASS evidence remains scoped. No broad repeat was run.

Targeted pytest, Ruff, mypy, and `git diff --check` all passed; pytest emitted
only the pre-existing unknown `timeout` configuration warning.
