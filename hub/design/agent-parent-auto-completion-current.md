# Parent automatic completion — private S3 follow-up

Base Agent **537c2ecd28f92b391c79e383e0e045fd71b3258f**. Small separate follow-up to the ongoing S3 review; harness commit pending. No integration edit, public schema freeze/adoption, generated-client pin change, App cutover, or render qualification.

Parent image/video completion now uses the existing `auto_place_completion` recipe and **one ordinary `clip.add-media` v1**, with unchanged wire args `{row, media}`. Python callers give `owner='parent'`, `ownership='parent'`, an explicit existing raw `track`, and a previously reserved raw clip ID. No display identity or owner inference. The existing `preferred_track` / `fallback_track` parameters carry the saved main `preferred_track_id` / `fallback_track_id`; `fallback_at` is global seconds. No new public command field or operation is needed.

The anchor end, saved fallback, or lane end resolves once against the original supplied bundle. The row stays literal on replay. Present anchor uses its guarded end; missing anchor uses the saved fallback time/lane when supplied; only an unsaved time uses lane end. Missing/invalid saved lanes refuse, including empty/boolean values; they never choose today's default. Completion image is five seconds even with a supplied duration; video defaults to five seconds or uses the supplied completed duration. Existing shared four-second placement is unchanged. Media remains the exact five-field completed pin, even after a newer primary variant is promoted.

## Capture and replay

The builder queries through the existing `Recording` and adds its original read constraints to the existing birth capture. **Those provisional query facts are not authoritative records.** The actual `clip.add-media` handler independently calls `ctx.read` for each additional constraint in the SAME recorder that performs birth; normal execution verifies original values before the handler and compares the final complete capture. Extra parent placement constraints are limited to existing raw parent clips and `at`, `at_ms`, `track`, `hold`, `from`, `to`, `speed`. No supplied snapshot is copied into record facts. No new query kind, recorder, operation, policy DTO, coordinator, table, journal, or root replacement is added. Ordinary literal births keep their original captures and disjoint timing behavior.

Existing birth recording supplies fps, source-window, active visual target-track, occurrence-lane exclusion, registry binding, collection membership/order, and reserved-ID guards. Collection membership covers named-anchor absence and insertion. Anchor mode adds only its seven timing/lane field states. Lane-end mode adds every existing clip's lane and timing only for clips on the chosen lane, so another lane's extent can change without a conflict while moving it into the chosen lane refuses. Saved fallback adds no unrelated extent dependency. Opaque clip fields, params, and volume rebase; absent/null timing branch states remain distinct. The selected target track remains a conservative whole-row read, as in the existing birth operation.

A different literal birth or removal of optional query constraints is a **different command/request**, not an exact retry. Upstream durable requester approval must bind the original owner, immutable basis, policy, reserved ID, exact pin, and request bytes. This change does not infer or retroactively approve anonymous old tasks. A conflict requires visible refusal or an explicitly approved new capture, never silent in-flight request replacement.

## Preserved original positives and captures

The four original strict cases passed with `--runxfail` **before** their two xfail decorators were removed: **4 passed / 81 deselected**. Both original function bodies are AST-identical to base; no assertions or expected outcomes changed. The complete original parent-media file initially passed **85 tests** with `--runxfail`.

Portable fixture at 30000/1001 fps (exact commands/read arrays: worker notes `portable-captures.json`):

| Media | Policy | Resolution | Frame | Seconds |
| --- | --- | --- | ---: | ---: |
| image/video | anchor `ov-a` | anchor-after | 60 | 5 |
| image/video | absent anchor, saved 22.25 s on overlay | fallback-at | 667 | 5 |
| image/video | absent anchor, no saved time | lane-end | 210 | 5 |

Each reserves `parent/clip:born` and the exact asset alias once. Provider/native Runtime checks prove the ID remains reserved after undo, redo restores it exactly, and exact retry after reopen returns the original accepted result without invoking semantics again.

## Private normally generated pair

Runtime source **2c4ac180c2220bdad966bc01e95ad230e99ce26a**, archived into this worker's own notes directory. Complete candidate schema supplied ONLY through normal `contract/schemas/edit-command.json`; normal generation/check and artifact-manifest generation/check all passed. Runtime source deltas are only that input and expected generated artifacts/manifest (`private-runtime-delta.json`). No shared venv or node_modules changes, generated-file hand edits, embedded-schema patch, synthetic accepted history, prepared-provider bypass, direct SQL mutation, daemon, socket, or browser.

Agent canonical schema SHA256 **8a55a9fd84d6fc188e48f63976dacc1c27ea25c7747ea88e7eba7589974dd85a**, unchanged **54 definitions / 28 operations**. The normally generated Runtime embedded schema equals that complete JSON object. Public `runtime.lock.json`, `artifacts.json`, schemas, generated clients, and source pin remain unchanged. Exact file hashes: worker notes `source-facts.json`.

Real managed image/video settlement and normally loaded Agent provider passed anchor, saved fallback, and lane-end births after a disjoint accepted params edit; reload/reopen, original request retry, exact undo to the disjoint head, reserved-ID refusal and redo; exact completed variant after primary promotion. Every automatic test makes legacy publication and renderer methods fail if called. Relevant native move, hold edit, and selected-lane label edit refuse before accept, with **zero mutating SQL statements**, unchanged SQL dump, and unchanged nonempty CAS/staging/snapshot file map. No fabricated revisions or baseline publisher is used. The existing pristine S3 initialization → occurrence/media → parent swap → word anchor → grouped inverse/reload/retry journey also passes.

## Validation and limits

- Original strict cases before marker removal: **4 passed**, 1.07 s.
- Broad targeted portable/source/schema lane: **636 passed**, 262.41 s. Includes original parent, new parent, occurrence automatic reads/defaults/fallback, shared collision/pool behavior, pristine initialization and complete schema/floor checks. This run preceded only the final invalid-saved-lane hardening; the final affected parent lane below covers that change.
- Final affected parent lane: **188 passed**, 39.52 s (85 original + 103 new).
- Final private Runtime/S3 lane: **15 passed**, 33.92 s. A final non-vacuous CAS-map assertion was subsequently added to the stale tests; its focused result is recorded in the worker report.
- Touched-file Ruff and `git diff --check`: pass.

No full/full* suite requested/run. All tests are bounded targeted tests; real Runtime calls are in-process with no live sockets. No public/HTTP/client transport, App submission/outbox/cutover, pixels/audio, registered automatic producer-attempt admission chain, owner film, macOS, or production automatic adoption is qualified. The existing short-video default refusal and existing whole-row target-track conservatism are unchanged; no success requirement is rewritten to refusal. Track kind/deletion/lane movement are covered as changed-head conformance fixtures; the real current command contract exposes track label edits, not those authoring operations.

Next: independent review of this bounded follow-up and its supplemental read constraints, then harness/manager publication of its commit and tree. Keep the S3/public/App/automatic-adoption holds until their separate actual-pair and requester qualification completes.

Exact commands, logs, hashes, patch and remaining limits: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-parent-auto-completion-current/notes/report.md`.
