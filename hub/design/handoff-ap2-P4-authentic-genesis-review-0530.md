# Handoff — P4 authentic genesis independent review

## Verdict

Source review **PASS**; P4 acceptance **BLOCKED**; no P4 GO. Reviewed
`3696239c48f9705568af30f2704855cc6a9175e5`, tree
`94f7f4ff4d60a798d9cd664638a2b182234ad82c`, against base
`0afe4e082fd01fc7ffbff469b842538dc21fa50b`, tree
`41b002d59bcbcca0840a774b2bb8b7620e4c92f4`.

## Accepted source findings

The candidate changes only genesis setup plus its report. Original fixture,
case data, trusted seed helper, and `_note_values`-through-test-end assertions
are byte-for-byte unchanged. `tiny.png` is 69 bytes,
`b1ff9c8ea3a780bad09b346c423d2d0e46815926879b18e841d928376a946640`.
The setup uses `RuntimeService.ingest`, asserts the observed managed digest and
size, exhaustively maps the three original media paths, reverses the mapping
with full encoded equality, preserves both occurrences as one physical
`chapter-shot/shot-1` and one `chapter-1/internal-1`, and creates the proper
`chapter-1` owner through normal `create_timeline`. Compiler materialization,
product changes, direct-store changes, auth bypass, and assertion weakening are
absent. The unchanged test body retains the C0 v2 base-pair, command,
label/steps/patch/reads, merge/dry-run/key, accepted/merged canonical head,
digest/receipt/dependency/history/conflict/invalid/refusal, and inverse/redo
coverage; it was not executed here.

## Seam classification

1. The two `WORKING` `shot-placement-*` IDs are an intentional authoring
   projection of two occurrences. C0c §2 requires unique physical closure-root
   resolution and explicitly counts two occurrences pointing to one image as
   one match; it does not require working aliases to equal. The current adapter
   (`astrid/core/timeline/authoring_bundle.py:218–228,413–456`) retains one
   physical source mapping while creating two working entries. The unchanged
   line-196 positive therefore remains unqualified, but this is an oracle/
   projection seam, not evidence that product identity must change or that the
   positive should be weakened.

2. The internal reader scope is a genuine owned production-path bug. The real
   call chain is `timeline.open` → `fetch_bundle`
   (`astrid/sdk/timeline/store.py:641–651`) → `open_bundle`
   (`astrid/sdk/_remote_timeline.py:27–89`). The reader passes parent `film`
   to `get_project_timeline_revision` at line 86, while the faithful row is
   owned by `chapter-1`. Runtime’s exact lookup at the pinned
   `runtime_protocol/service.py:2312–2317` requires the same
   `(project_id,timeline_id,revision)` and returns not-found for
   `(film,internal-1)`. `authoring_revision_diff.py:56–64` has the same scope
   shape. The setup owner creation makes admission valid but cannot repair this
   read. The previous report’s owner-check line citation is corrected to the
   pinned `_record_internal_revision:1410–1416`; conclusion unchanged.

## Evidence / limits

- Offline witness: **PASS** for three-media mapping, 69-byte digest, trusted
  closure shape, one physical source image, and two working placement IDs.
- Pytest collection: **PASS**, 1 test collected; existing unknown `timeout`
  warning.
- Ruff, private mypy, and `git diff --check`: **PASS**.
- Original fixture/cases unchanged and `_note_values` onward byte comparison:
  **PASS**.
- No HTTP, socket, service instantiation/call, test body, browser, build, full
  suite, central test request, or unchanged rerun. Live ingest persistence,
  authenticated readback, accepted/merged replies, history, and inverse/redo
  remain unverified.

Manager handoff: route the Agent owner-scope reader repair and decide the
physical-boundary positive/oracle. Do not spend the original-node retry until
both seams are resolved or explicitly accepted by the orchestrator.
