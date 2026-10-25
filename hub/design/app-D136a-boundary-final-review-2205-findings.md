# D136a final independent protected evidence check

## Result

FAIL — corrected inventory is not complete. This is an evidence-citation failure only; it is not a source, Runtime, Agent, setup, or product-fix finding.

The packet retains 45 unique rows, nine final predicates, six MGC groups, 30 condition maps, and 31 AST inventory entries. The prior B022 classification is corrected and remains safe: the retained exact original9 run shows a current Runtime fail-closed refusal at `runtime_protocol/timeline_commit_auth.py:2209`, while regression, causal owner, setup failure, and D54a REG are UNKNOWN/NOT_PROVED.

## Remaining findings, one pass

- F-D136A-FINAL-001 / MGC-01 / B005-B007: the declared `authoring_bundle.py:185-233` range omits `_string`’s final line and `_verify_digest` at `237-244`; the AST entry incorrectly places `_clip_selected_media` and `_clip_selected_media_for_edit` in `679-772`, while their actual definitions and called registry/authority branches are `541-676`. The condition map itself cites `552-620`, but the group’s source ranges do not cover it.
- F-D136A-FINAL-002 / MGC-04 / B021-B025, B029, B032: the AST entry reaches `timeline_commit_auth.py:608-795`, but the group’s source ranges stop at `608-778`; `_reconcile_materialized_owner_images` is `778-795`. The shared range also stops at `1833-2186`, omitting the actual `command_output` caller and refusal branch at `2189-2215`, including line `2209`.
- F-D136A-FINAL-003 / MGC-06 / B018-B019, B034: the AST entry claims `_materializations` at `1567-1597` and `accept` at `1832-1905`, but declared ranges begin at `1576` and end at `1905`; actual `accept` continues through `1915`, including persistence/history checks at `1906-1915`.

These are the only remaining discrepancies found in the finite static audit. Downstream B023-B036 and B-FINAL-001..009 remain unreached/UNKNOWN; no dynamic body outcome is claimed. Exact pristine 886a source absence is not behavior.

See the absolute evidence paths in `review.json`, `coverage.json`, and `handoff.md` for the complete prior-input pointers and source hashes.
