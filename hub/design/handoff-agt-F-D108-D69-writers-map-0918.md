# F-D108/D69 independent semantic predicate review — bounded five-function group

Status: **SOURCE-ONLY EXACT REVIEW; 71/71 assertion multiplicity units PASS**. No product behavior, full-suite, retirement, or scope completion claim is made.

Inputs: original membership `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-D108-original-membership-next.json` SHA-256 `af04bc82117976029346a9a6646b956ab16390627a9d764be6a30ef668ee0411`; upstream `08e6b905114a3ee2b05c3e7980421f26b4abf15c`; captured `d6294843286c18e57af3c1874cf1996be42212d2`; current normal `d0ecf1d69a7b37f86034bc52004f73f6c6231603`. Exactly five assigned functions are reviewed; row-level JSON/TSV retain every supplied membership record and ID.

## Decision summary

| Function | Removed | Added | Verdict | Route |
|---|---:|---:|---|---|
| `test_daemon_backed_authoring_proposal_publishes_one_canonical_render_task` | 3 | 7 | PASS | test_runtime_publication_chain.py:874-1016 -> runtime_stitch.py:104-175; requester commitTimeline result then renderer task pinned to accepted pair. |
| `test_daemon_backed_host_executes_authoring_and_final_render` | 0 | 24 | PASS | test_runtime_publication_chain.py:1133-1367 -> sync.py:224-293,320-369,422-462 -> runtime_stitch.py:104-175. |
| `test_publish_uses_one_compilation_and_returns_complete_mapping` | 2 | 8 | PASS | authoring_bundle.py:1833-1914 -> authoring_commit.py:84-187; one compilation, one v2 request, canonical reply and feedback. |
| `test_catalog_import_remains_reusable_after_later_parent_cas_conflict` | 0 | 10 | PASS | authoring_bundle.py:1833-1914 -> authoring_commit.py:84-187 -> writer.commit_timeline/commitTimeline; catalog import is pre-publication. |
| `test_document_publish_forwards_new_stale_head_to_runtime` | 0 | 17 | PASS | timeline_document.py:252-333 -> TimelineSession.open/_bundle/commit_many -> commitTimeline. |

Removed rows are approved replacements under C0/G4/G5: old numeric publication/version and old next-action assumptions map to accepted revision/publication identity, settled proposal equality, canonical render pins, v2 base/command/step envelopes, and saved-revision-pair feedback. Added rows are additive preservation or exact v2-route provenance checks.

## Row-level source comparison

The JSON and TSV contain complete source assertion text, old/new line selectors, fingerprints, body/blob references, production route, purpose, decision, and approval refs for every row.

| Row ID | Side | Mult | Decision | Old | New | Purpose |
|---|---|---:|---|---:|---:|---|
| `p0-f52-a-0` | added | 1 | PASS/preservation | — | 992 | Settled Runtime proposal equals the producer proposal before publication. |
| `p0-f52-a-1` | added | 1 | PASS/preservation | — | 1001 | Accepted publication identity equals the Runtime receipt identity. |
| `p0-f52-a-2` | added | 1 | PASS/preservation | — | 999 | Reply is an accepted/merged/rebased v2 success envelope. |
| `p0-f52-a-3` | added | 1 | PASS/preservation | — | 1005 | Renderer targets the requested timeline. |
| `p0-f52-a-4` | added | 1 | PASS/preservation | — | 1007 | Render pin carries the accepted publication identity. |
| `p0-f52-a-5` | added | 1 | PASS/preservation | — | 1006 | Render pin carries the accepted revision identity. |
| `p0-f52-a-6` | added | 1 | PASS/preservation | — | 1000 | Accepted revision is present before render creation. |
| `p0-f52-r-0` | removed | 1 | PASS/approvedreplacement | 127 | — | Old numeric publication version is replaced by accepted revision/publication identity under C0. |
| `p0-f52-r-1` | removed | 1 | PASS/approvedreplacement | 132 | — | Committed authored config remains equal; settled whole-proposal equality is stronger. |
| `p0-f52-r-2` | removed | 1 | PASS/approvedreplacement | 133 | — | Renderer uses the Runtime-authoritative canonical revision/publication pin. |
| `p0-f120-a-0` | added | 1 | PASS/approvedreplacement | — | 1771 | Exact source text and body/blob references are recorded; assertion remains at the reviewed function boundary. |
| `p0-f120-a-1` | added | 1 | PASS/approvedreplacement | — | 1781 | Fake writer exposes no legacy method; no product-route retirement is inferred. |
| `p0-f120-a-2` | added | 1 | PASS/approvedreplacement | — | 1774 | Authoring publication uses C0 v2 envelope. |
| `p0-f120-a-3` | added | 1 | PASS/approvedreplacement | — | 1776 | Original publication pin retained. |
| `p0-f120-a-4` | added | 1 | PASS/approvedreplacement | — | 1775 | Original revision pin retained. |
| `p0-f120-a-5` | added | 1 | PASS/approvedreplacement | — | 1780 | Authoring publication remains atomic. |
| `p0-f120-a-6` | added | 1 | PASS/approvedreplacement | — | 1773 | Project/timeline/idempotency scope retained. |
| `p0-f120-a-7` | added | 1 | PASS/approvedreplacement | — | 1777 | Compiled candidate has concrete commands. |
| `p0-f120-a-8` | added | 1 | PASS/approvedreplacement | — | 1778 | History label is nonempty. |
| `p0-f120-a-9` | added | 1 | PASS/approvedreplacement | — | 1779 | Per-step metadata is present. |
| `53:added:0` | added | 1 | PASS/preservation | 185 | 1334 | Ordinary public renderer is admitted. |
| `53:added:1` | added | 1 | PASS/preservation | 185 | 1328 | Post-commit scope is a valid Runtime head. |
| `53:added:2` | added | 1 | PASS/preservation | 185 | 1336 | Render admission returns a nonempty task ID. |
| `53:added:3` | added | 1 | PASS/preservation | 185 | 1324 | Restart flush returns accepted identities and clears flight. |
| `53:added:4` | added | 1 | PASS/preservation | 185 | 1337 | Exactly one rendering.render task exists. |
| `53:added:5` | added | 1 | PASS/preservation | 185 | 1272 | Admission retains child association/media identity. |
| `53:added:6` | added | 1 | PASS/preservation | 185 | 1295 | Settled proposal retains target, child media and replace-clips. |
| `53:added:7` | added | 1 | PASS/preservation | 185 | 1273 | Admission retains child association/media identity. |
| `53:added:8` | added | 1 | PASS/preservation | 185 | 1298 | Settled proposal retains target, child media and replace-clips. |
| `53:added:9` | added | 1 | PASS/preservation | 185 | 1291 | Authoring task reaches terminal settled state. |
| `53:added:10` | added | 1 | PASS/preservation | 185 | 1293 | Settlement emits proposal/timeline/assets artifacts. |
| `53:added:11` | added | 1 | PASS/preservation | 185 | 1325 | Exact source text and body/blob references are recorded; assertion remains at the reviewed function boundary. |
| `53:added:12` | added | 1 | PASS/preservation | 185 | 1271 | Admission retains child association/media identity. |
| `53:added:13` | added | 1 | PASS/preservation | 185 | 1269 | Admission selects assemble_timeline. |
| `53:added:14` | added | 1 | PASS/preservation | 185 | 1316 | Lost acknowledgement preserves the original idempotency flight. |
| `53:added:15` | added | 1 | PASS/preservation | 185 | 1301 | Settled proposal retains target, child media and replace-clips. |
| `53:added:16` | added | 1 | PASS/preservation | 185 | 1279 | Admission carries exact target/order. |
| `53:added:17` | added | 1 | PASS/preservation | 185 | 1362 | Post-commit scope is a valid Runtime head. |
| `53:added:18` | added | 1 | PASS/preservation | 185 | 1363 | Restart flush returns accepted identities and clears flight. |
| `53:added:19` | added | 1 | PASS/preservation | 185 | 1276 | Admission carries exact target/order. |
| `53:added:20` | added | 1 | PASS/preservation | 185 | 1270 | Admission carries exact target/order. |
| `53:added:21` | added | 1 | PASS/preservation | 185 | 1305 | Queueing uses producer.guard. |
| `53:added:22` | added | 1 | PASS/preservation | 185 | 1302 | Admission retains child association/media identity. |
| `53:added:23` | added | 1 | PASS/preservation | 185 | 1365 | Restart flush returns accepted identities and clears flight. |
| `115:added:0` | added | 1 | PASS/preservation | 364 | 733 | Saved-pair and current-head follow-ups are distinguished. |
| `115:added:1` | added | 1 | PASS/preservation | 364 | 718 | Only registered doc.patch/media.admit operations. |
| `115:added:2` | added | 1 | PASS/preservation | 364 | 724 | Saved-pair and current-head follow-ups are distinguished. |
| `115:added:3` | added | 1 | PASS/preservation | 364 | 728 | Saved follow-ups retain exact from/to revisions and formats. |
| `115:added:4` | added | 1 | PASS/preservation | 364 | 716 | Exact original base revision. |
| `115:added:5` | added | 1 | PASS/preservation | 364 | 717 | Compiled batch remains atomic. |
| `115:added:6` | added | 1 | PASS/preservation | 364 | 720 | Returned document is canonical Runtime result. |
| `115:added:7` | added | 1 | PASS/preservation | 364 | 719 | Result reports accepted Runtime head. |
| `115:removed:0` | removed | 1 | PASS/approvedreplacement | 379 | 703 | Saved-pair and current-head follow-ups are distinguished. |
| `115:removed:1` | removed | 1 | PASS/approvedreplacement | 375 | 703 | Result reports accepted Runtime head. |
| `121:added:0` | added | 1 | PASS/preservation | 227 | 356 | Exact source text and body/blob references are recorded; assertion remains at the reviewed function boundary. |
| `121:added:1` | added | 1 | PASS/preservation | 227 | 370 | One v2 step covers command ordinal zero. |
| `121:added:2` | added | 1 | PASS/preservation | 227 | 365 | Media rebind is the registered occurrence.swap-media command. |
| `121:added:3` | added | 1 | PASS/preservation | 227 | 359 | Original idempotency key is unchanged. |
| `121:added:4` | added | 1 | PASS/preservation | 227 | 360 | C0 v2 request envelope. |
| `121:added:5` | added | 1 | PASS/preservation | 227 | 364 | Exact original publication pin forwarded. |
| `121:added:6` | added | 1 | PASS/preservation | 227 | 363 | Exact original revision pin forwarded. |
| `121:added:7` | added | 1 | PASS/preservation | 227 | 368 | Publish is not preview. |
| `121:added:8` | added | 1 | PASS/preservation | 227 | 366 | Publish document label retained. |
| `121:added:9` | added | 1 | PASS/preservation | 227 | 367 | Document publication remains atomic. |
| `121:added:10` | added | 1 | PASS/preservation | 227 | 361 | Project scope retained. |
| `121:added:11` | added | 1 | PASS/preservation | 227 | 369 | Script attribution retained. |
| `121:added:12` | added | 1 | PASS/preservation | 227 | 362 | Timeline scope retained. |
| `121:added:13` | added | 1 | PASS/preservation | 227 | 307 | Opened session is pinned to exact pair. |
| `121:added:14` | added | 1 | PASS/preservation | 227 | 371 | One v2 step covers command ordinal zero. |
| `121:added:15` | added | 1 | PASS/preservation | 227 | 358 | Project scope retained. |
| `121:added:16` | added | 1 | PASS/preservation | 227 | 372 | Verified media is captured before commit. |

## Approval and scope boundaries

- C0/G4/G5/R2 and the named D52/D69/D72 source reviews authorize the current requester/`commitTimeline`/provider route and v2 identity/reply shape used by these comparisons.
- `publish_parent_composition` absence is reviewed only as the new fake-writer interface in the catalog test. Existing ledger WC1/WC10 holds remain unchanged; this review does not retire the Runtime route or close whole G5/P1.
- No tests/typecheck/lint were run because this is a read-only source review. JSON parse, in-memory AST compile, source blob reads, TSV parse, and `git diff --check` were performed.

