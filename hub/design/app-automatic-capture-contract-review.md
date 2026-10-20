# Automatic capture contract review — HOLD automatic adoption

2026-10-20. Read PLAN first, including the 07:05 automatic-placement decision and 08:04 anonymous-state correction. Review complete; no product port, writer change or policy decision made.

**Verdict: HOLD production automatic placement from these two native builders.** The deterministic birth operations are useful, but the automatic queries run outside the authoritative command recorder. The returned explanation is not a commit guard. Existing command membership/order guards catch structural changes, while consumed timing/lane/collision values can change without conflict. `occurrence.add-media` also lacks exclusive-owner replay protection, including shared-placement images on an inherited lane. This is a bounded Agent contract request, not a reason to invent App guard fields, another recorder or a read operation.

## Exact sources

- App review worktree/base: `/home/user/work/wt/app-m2-automatic-capture-contract-review`, HEAD `1be0efdde5b9ec14f6ef85e0cbcd6bf6b27c80ff`. Product tree unchanged.
- Agent completion: `fb21a629e84e69dec92d90720a570837e14827e6`; combined completion/shared: `d127716061d8b259f65a665f9f6f17f910ac34dd`, read with `git show` / `git archive` in `/home/user/work/agent`. Inspected `astrid/sdk/timeline/native_auto_placement.py`, native placement/media handlers, command recorder/replay, `design/m2-auto-placement.md`, both `tests/editing_conformance/test_recipe_m2_{auto_placement,shared_auto_placement}.py` and their JSON goldens. Goldens are checked by the unmodified native tests below.
- Readiness: `ORCH/design/app-auto-placement-consumer-readiness.md` and `app-auto-placement-outbox-port.md`. These live in ORCH, not App's tracked integration tree. Requester/storage candidate `07f64b46f0b971eecceb1a1735afac733c399526`, `src/tools/video-editor/commands/{placementRequester,commitOutbox}.ts`; both requester branch refs still pointed to that pre-fence commit when read.
- The concurrent async-fence worker has newer **uncommitted** source. Read-only snapshots of its two files are in `notes/support/async-fences-live-read/`; SHA-256 identities in `notes/support-manifest.json`. Source now checks authenticated identity and live claim after awaits, and fences capture linkage/ACK. This review does not rerun or qualify that worker's changes; do not mistake branch HEAD for its pending fixed tree. The earlier requester review's reproduced async defects remain that owner's qualification task.
- Runtime source-only inspection: `94114269d1ce23ab3224d7eca5a85138ce2b5fed`, `runtime_protocol/timeline_commit_port.py`, especially `selected_media`, acceptance recheck, `MediaReads.selection`, `_output_selection_binding`, `_selected_project_media`, `selected`.
- Actual removed completion behavior: `git show ade7b5ff9^:supabase/functions/complete_task/{placement.ts,handler.ts,placement.test.ts}` and `src/tools/video-editor/commands/media.ts`. Exact resolved parent commit and snapshots retained in the support manifest. Current shared behavior: App base `src/shared/lib/placement/{documentPlacement,placementService}.ts`.
- Reusable staged App media seam: `01eee706421b34a84037ca45339af522644cf5da` (`tl/app-m2-popup-exact-vector-confirm-r1`), `occurrenceMediaCapture.ts` and `commitSession.ts::occurrenceMediaPort`; explicit move seam `9a7aee7bf95177f9c5e7b003acd3f581d3dd5c11`, `placementCapture.ts`. Inspected only, not qualified here.

`ORCH` here means `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`. All retained evidence is under `ORCH/workers/app-m2-automatic-capture-contract-review/notes` (N in commands below).

## What is actually recorded

| Requirement | Exact native behavior |
| --- | --- |
| Original basis | Builders take a bundle supplied by the caller. They cannot prove it is the pre-admission approved closure. Requester storage retains `input.head`, `readClosure`, owner, anchor, lane, fallback, policy, output and IDs; caller binding must validate them. Using today's editor/selection or freshly recapturing at completion would change approval. |
| Anchor presence | Builder scans raw occurrence clips. `capture.anchor` contains only ID and present/absent state. The birth command records the whole clip collection's membership **and order**; adding/removing/reordering clips refuses in probes. This incidentally protects absence but does not record the anchor's timing values. |
| Anchor timing | Completion reads `_end_frame(found, origin, fps)` outside recording. Command has no read of anchor `at/hold/from/to/speed`; capture explanation has no such inputs either. Native tests explicitly assert moved-anchor replay keeps the literal start. |
| Lane | Completion always uses the occurrence lane, recorded through existing occurrence map/track reads. Shared uses a found anchor's `track`, otherwise occurrence lane. Shared capture explains the lane, but the anchor's track is not an authoritative read. Validity of the chosen target track is guarded; why that track was chosen is not. |
| Extent | Occurrence `duration_ms`, origin/map, activity and rational fps are guarded by media birth. Lane-end/whole-shot maximum over clip timing is computed outside the recorder. Native shared tests widen the occurrence to 20 seconds; ordinary migration-sized append can refuse at `occurrence_boundary`. Growing extent is not implemented. |
| Collision | Shared explicit frame clamps to zero, shifts +1 for occupied **start** frames, and records `skipped` in its explanation. Clip membership/order is guarded; existing clip start values and the occupied-frame set are not. Interval overlap is intentionally allowed. |
| Exclusive occurrence | Capture counts all occurrences referencing the shot. `placement.create` rechecks `placement.owners` at replay. `occurrence.add-media` does not. This affects all completion videos, shared videos, and shared **images when inherited lane differs from home lane**. Retargeting an existing occurrence to the shot preserves occurrence IDs/order and escapes the birth's collection guard. |
| Birth identity | Caller raw clip ID is retained; create-or-require exact registry binding uses `media.asset`. Existing different binding/occupied clip refuses. No UUID is allocated by these builders. Outbox must retain the same IDs/pin/command; duplicate completion after acceptance/undo must never issue another birth. Unchanged-media re-place remains move; replacement reserves a fresh identity. |
| Media | Exact five-field selection (`asset,generation_id,variant_id,object_id,catalog_digest`) plus detached verified media/type and video duration. No primary-variant lookup. Native records retain `media.new` dependency and registry/created-ID guards. |
| Task/attempt | Neither automatic builder accepts or invents a task fence. Existing Runtime selection authority checks exact durable output, registered variant, completed task, settled current attempt and historical lease/executor/fence/epoch; catalog digest includes the managed binding, and acceptance rechecks it. Requester matches the original approved output and task/run/attempt before selection. This is source agreement, **not executed Runtime fencing proof**. |

**Fixed intent is retained.** An approved literal start must not chase a moved anchor on replay. The native fixed-start test is not rewritten or declared a regression merely for staying fixed. But fixing the result does not, by itself, declare that all queries used to obtain approval can be discarded. PLAN 4.1 records consumed reads/selections unless an explicit merge policy allows otherwise. The separate capture explanation never enters `replay(plan, head)`; both builders return only ordinary birth commands. In `commands.execute`, supplied read/selection claims must equal the handler's own authoritative capture, so App cannot append additional reads to fix this locally. The unresolved issue is original-query accounting/conflict policy, not a demand for follow-anchor behavior.

## Executable counterexamples

`notes/test_native_gaps.py` runs against exact d127 source. Each case retains full `before`, captured `commands`, authoritative `records`, changed `head`, `after`/records or refusal, fresh comparison capture and the concrete created row in `notes/probe-d127716061d8b259f65a665f9f6f17f910ac34dd/*.json`. The original fixture sibling is moved to 100 seconds **before capture**, so ordinary native moves do not cross its boundary. This fixture adjustment is explicit in the probe and retained before image. No authoritative source/test was edited.

| Probe | Visible authored result |
| --- | --- |
| Ordinary native `placement.move` changes completion anchor from local 1 to about 2 seconds | Image and video replay accept at original global frame **330** (11.011 s), while anchor-after now resolves to **360** (12.012 s). No anchor read appears in the birth. This confirms the documented fixed result and the unrecorded consumed timing. |
| Ordinary move changes last clip on completion fallback lane | Replay accepts at **450**; fresh lane end is **480**. The inserted clip overlaps the extended occupied interval. |
| Ordinary move extends shared whole-shot maximum | Replay accepts append at **510**; fresh extent is **540**. |
| Ordinary move puts clip-a at frame **391**, after original explicit-frame 390 policy skipped to 391 | Replay still creates at **391**, giving two clips exactly the same start. Fresh collision resolution chooses **392**. This is a concrete lost start-frame-shift guarantee, even though interval overlap is allowed. |
| Existing occurrence fixture retargeted to the same shot after capture | Home-lane image birth refuses; video birth accepts, and `State(after).entity('occurrence:occ-b/clip:placed')` equals the created occ-a row. Shared inherited-lane image and video also accept and appear through both occurrence scopes. A fresh capture refuses all these shared owners. |
| Anchor lane fixture changed overlay → picture | Both shared births keep overlay, while fresh inheritance selects picture. |
| Delete/reorder/add clip, change occurrence extent, change occurrence home lane | Both completion kinds refuse. These are functioning guards; do not claim membership/order/extent guards are entirely absent. |
| Selected video duration reduced to 3 seconds | Native completion's default 5 and shared's 4 both refuse `unsupported_timing`; no birth is emitted. |

First four rows use **actual native intervening commands and their records**, passed into server replay. Ownership/lane and structural rows use explicit changed-head fixture mutations; they prove command-engine semantics, not acceptance of a concurrent ownership migration by a live Runtime/compiler. The sibling-row equality is a concrete authored-model visibility result; no browser pixels or accepted server revision is claimed.

The review probe's 26 green assertions document current observed outcomes, including unsafe acceptance. They are not replacement positive behavior tests. The original native conformance tests and original App success expectations are untouched. A first probe draft had 8 setup refusals because the supplied fixture's next occurrence was too close; `probes-development.log` retains that run (14 pass/8 fail), and the explicit pre-capture fixture correction above addresses only that setup. No test was skipped or expectation weakened to claim adoption.

## Completion 5 seconds versus shared 4 seconds versus actual old App

- Native completion image is always 5 seconds, ignoring a supplied `duration`; video defaults to 5 or uses the explicitly supplied duration, with source window `0..duration`, speed 1. Native shared is always 4 seconds for image/video; video authors `0..4`. Both enforce verified source length.
- Old `executePlacement` resolved a **live anchor** plus `preferred_track_id`, or used the **saved `fallback_at` and `fallback_track_id`**. A present anchor plus missing preferred lane refused. It did not compute a new lane end on missing anchor. Historical tests pin anchor 8 + 2.5 → **10.5**, and absent anchor → saved **22.25**. Native completion accepts neither preferred/fallback lane nor saved fallback time: it uses occurrence lane and recomputed lane end. Do not relabel this as parity.
- Old completion's registry entry omitted duration, so normal video add used a five-second source window; simply passing the newly discovered full source duration would change behavior. Short-media refusal is newly observable and needs explicit preservation/policy treatment rather than silently changing success to refusal. Old completion add also authored opacity/volume and manual-track layout defaults; the native minimal birth row omits them. Rendering equivalence of those defaults was not tested here.
- Old `timeline_placement` used literal target lane/insertion time; its `replace` flag was logged but still added a clip. Native automatic completion is not that literal-policy adapter and does not cover parent-owned completion.
- Old shared append uses selected group's clip IDs across lanes, numeric fps (fallback 30), default hold 4, empty group frame 0, group/first-group/first-track/`V1` lane fallback. Native uses canonical exclusive owner, pinned rational fps, occurrence-local clips and origin; migration must preserve the old group bindings under PLAN's canonical ownership/rational timing rules. Native handles start-frame shift and overlapping intervals on the captured basis, but does not guard the consumed starts during replay. It rejects noninteger explicit frame; old code rounds it.
- Native shared pool/promote/keepAsPooled is unavailable (two strict upstream xfails), and unplace is image-only. Append beyond fixed occurrence extent is unavailable. Existing native docs propose operations for these; **this review does not approve or introduce those operations**. No lost behavior is accepted as an ordinary permanent refusal.

## Exact browser capture seam and portable subset

Use the **existing** requester injection:

```ts
capture?: (original: OutboxPlacementContinuation, scope: OutboxScope)
  => ReturnType<OutboxPlacementCapture>;
// OutboxPlacementCapture = (original) => Promise<OutboxJson>
```

1. Authorized ingress must validate producer admission and explicit canonical owner/anchor/lane/fallback/policy; reserve all birth IDs, original accepted head/read closure, output selector and auto-approval with exact normal task bytes/key **before admission**. No unsaved preview/current selection substitutes for that basis. High-level `createTask` currently allocates a fresh in-memory key; it is not an exact recovery adapter.
2. On finite reconnect recovery, claim the saved owner; reread its saved task ID and match the one originally approved result over all managed pages; use existing `getProjectMediaSelection` and `getProjectVerifiedMedia` for the exact pin and detached verified facts. The capture callback already receives saved `input` and persisted `mediaPin`; do not add a new task/attempt DTO. Missing immutable basis or unresolved bindings must remain recoverable, never inferred.
3. Rehydrate **the saved immutable closure** into the existing authored bundle/state. A pure browser mirror of the Agent builder would consume `(bundle, raw occurrence owner, reserved raw clip ID, exact media pin, explicit ownership, verified_media, original anchor, explicit policy arguments)` and return the exact native `{commands, capture}`. Completion signature has `anchor`/`duration`; shared has `frame`/`anchor`/`pooled`. The saved fallback/lane/policy cannot be dropped merely because today's native signature cannot represent them: incompatible approval remains held for an owner-qualified contract.
4. Reuse `captureOccurrenceAddMedia` / `executeOccurrenceMedia` and their **existing recorder**, pure-state checks and exact input/command/record golden comparisons for explicit occurrence media. Reuse the existing placement adapter for unchanged-media movement. Use the existing compiler/projector for local preview. No new command, query key, recorder, whole-document writer or numeric-on shortcut is authorized. Match Agent binary64/rational rounding and end-frame duration precedence; do not replace it with generic `Math.round(at + duration)` arithmetic.
5. Existing `box.capturePlacement` persists the media pin before callback and links payload plus one normal intent atomically at `input.head`. Ordinary `box.dispatch` freezes the generated commit bytes/key. Retain original command guards, IDs and scope across retry; no recapture on ACK/conflict. Accepted/cancelled linkage survives newer edits/undo. Newer async fences must retain original identity/claim through these awaits. The semantic explanation alone is not a payload authority.

**Can port now:** inactive exact-golden browser adapters for already explicit fixed placement/media births, existing durable preparation/recovery wiring with native capture still unavailable, and explicit unchanged-media move. These remain candidate work, subject to their existing tuple and exclusive-owner limits; explicit video's missing replay isolation must be fixed before claiming occurrence-only safety. A narrowly empty exclusive occurrence/image case has no existing clip timing to consume, but it is not blanket approval to activate historical completion fallback or shared placement. **No production automatic subset is qualified by this review.** Keep existing shared writers and all positive behavior requirements; this review does not restore the removed edge writer.

## Smallest owner requests / next steps

1. Agent owns the contract: publish authoritative accounting/conflict policy for the queries the automatic builder actually consumes (anchor presence/timing/lane, lane/shot extents, occupied starts and their membership/order), preserving fixed literal replay. Reuse the recipe; do not require App to manufacture a read op/schema/recorder. Close exclusive-owner replay on the `occurrence.add-media` path, including inherited-lane images. Supply executable goldens/probes that preserve approval under the interleavings above.
2. Orchestrator/Agent must reconcile the concrete old saved-fallback/preferred-lane semantics with the new lane-end/home-lane signature, and explicitly settle short-video/source-duration and omitted manual defaults. Full-length duration is not the old completion default. This is evidence of a mismatch with the original approval, **not a decision to deviate**. Parent-owned cases, append growth, pool and video unplace remain separately blocked; do not enlarge the first port silently.
3. Runtime publishes the official Agent/schema/client tuple for only the adopted operations, reusing normal selected/verified-media and commit authority; prove task/attempt changes refuse at acceptance. This review ran no Runtime process and claims no current paired release readiness.
4. App can then bind the pure seam to original saved approval and qualify real completion/reconnect, native reload, undo/redo, exact retry, duplicates after A/B/C/undo and zero legacy traffic before writer retirement. Old anonymous tasks remain manual under the decided wording: proven retirement → “Not placed: place manually”; otherwise “Placement unconfirmed: place manually”. No retrospective approval or owner inference.

## Exact executable evidence

All commands below ran with shared dependencies read-only. No installs, full suite, build, browser, tsc, socket, new API, commit, merge, checkout or push. `PYTHONDONTWRITEBYTECODE=1` and disabled pytest cache keep source/dependencies unchanged. Extracted source is outside every repo, with no `.git`, config, dependency install or whole private checkout. It includes authoritative core/SDK modules, test Python dependencies and the two goldens. `-c /dev/null` avoids project-wide pytest configuration; root `tests/conftest.py` is not loaded. Upstream tests themselves use their existing detached `runtime_abi` fixture; all command/provider execution remains actual native source, while Runtime ABI exceptions/metadata are test doubles. Each run reports one harmless unknown integration-marker warning from an imported helper because project pytest config was deliberately not loaded.

```sh
N=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-automatic-capture-contract-review/notes
python "$N/extract.py"
```

Exact git-archive extraction at fb21: 1,282 files; d127: 1,284. SHA-256 manifests retain their identities. Earlier inspection commands: `git -C /home/user/work/agent show --stat <SHA>` and `git -C /home/user/work/agent show <SHA>:<path>` for the exact sources listed above.

```sh
cd "$N/fb21a629e84e69dec92d90720a570837e14827e6"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -c /dev/null --confcutdir="$N" tests/editing_conformance/test_recipe_m2_auto_placement.py
```

**28 passed, 1 warning, 1.95 s**, `fb21-tests.log`.

```sh
cd "$N/d127716061d8b259f65a665f9f6f17f910ac34dd"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -c /dev/null --confcutdir="$N" tests/editing_conformance/test_recipe_m2_auto_placement.py tests/editing_conformance/test_recipe_m2_shared_auto_placement.py
```

**58 passed, 2 xfailed, 1 warning, 3.70 s**, `d127-tests.log`. The two unchanged strict xfails are the missing pool behavior, not adopted functionality.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$N/d127716061d8b259f65a665f9f6f17f910ac34dd" /home/user/work/venv-agent/bin/python -m pytest -q -s -p no:cacheprovider -c /dev/null "$N/test_native_gaps.py"
```

**26 passed, 1 warning, 2.72 s**, `probes-d127.log`. This green result reproduces the gaps listed above, not an automatic-placement acceptance claim. Ordinary before/commands/records/after evidence is retained beside that log. Initial record-dump helper was briefly named `inspect.py`, shadowing Python's stdlib; it was renamed `record_probe.py` before any valid probe run. No native source changed.

```sh
python "$N/capture_support.py"
git -C /home/user/work/wt/app-m2-automatic-capture-contract-review diff --check
```

**PASS**: both extracted source manifests unchanged (1,282 / 1,284 entries), 13 supporting source snapshots retained; App diff check clean. App product tests, live Runtime acceptance, browser capture parity, released tuple and pixel/audio default equivalence remain **UNRUN**. Do not use historical requester test counts as fresh qualification.
