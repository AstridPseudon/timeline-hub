# F-D86 source-only handback: D99 MAIN13 + D95 NEW2

This packet is source/input evidence only. It does not claim behavioral success,
does not submit or install a runner, and does not take ownership from the
existing MAIN receiver `rt-D86-current-delta-bind-0407` / successor receiver
0419. Runtime coalesces proof ownership.

## D99

Use exactly the 13 selectors in `d99-main13-selectors.tsv` and JSON. They are
the nine media-role selectors and four emitter-error selectors from the safe
per-ID export of actual 11789. The reviewed source is c354c6e9 and its exact
SHA-256 is 69fc3544; import 0441 is commit 0a9552a8. The protected source
review is `agt-F-D99-sheet-review-0435-report.md` (PASS_SOURCE). It confirms
10 test ASTs, 239 body assertions, all 17 assigned selectors retained, and no
assertion requiring image/video cross-MIME identity.

The three CLI cases and one omitted-row case remain LIVE/unqualified. They are
not retired, rerun, or silently counted into MAIN13. D99 source presence is not
behavior proof; the old IDs are eligible only through this reviewed source
delta.

## D95

The two separate NEW-FIRST selectors are the parametrized `rebind` and `clear`
cases in `d95-new2-selectors.tsv`/JSON. Source 33be3933 is present in normal
merge 5faeec5b and has exact SHA-256 79da31ce. Protected review 0425-A is
PASS_SOURCE. Original IDs 99 and 101 are retired legacy-only under the reviewed
deletion appendix; the unbound inverse positives remain LIVE and unchanged.
This is not the historical ID5 word-recipe restore body.

## Preserved ownership and exclusions

Immutable current96 actual 6058 remains owned by its existing packet and is not
retargeted. Its result metadata is recorded in `export-inventory.tsv` only;
no per-ID publication was found, so no selector is inferred from it. The next
33, optional 5, and media 18 ownership remains with the existing receiver.
Inverse7, D91 ten, P4 critical single, held parent/word/restore, original 550,
and the 23 omitted historical rows are excluded.

The production source path remains the registered `commitTimeline`/provider:
`TimelineSession.commit_many` -> SDK commit_timeline forwarding -> registered
Runtime provider. All C0 request/reply fields, opaque values, assertions,
refusal, retry, inverse, ABA, and no-write guards remain source inputs or
predicates. No product/test/generated/pin/ledger/framework/body was changed by
this handback.
