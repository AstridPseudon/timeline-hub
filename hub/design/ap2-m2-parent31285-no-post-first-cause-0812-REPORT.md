# actual31285 first-failed-boundary report

## Result

Diagnosis only. No App source, test, harness, or shared file was changed.

The first retained failure is an App-side native parent-media validation refusal after Runtime media selection succeeds. The selected drop is represented as `track: S1`; the refusal value is exactly `track is the lane of an occurrence-owned shot`. This happens before any commit/outbox POST, so the observed `wire.attempts === 0` is not evidence of an accepted ADD or a lost ACK.

## Source and retained packet

- Worktree: `/home/user/work/wt/ap2-m2-parent31285-no-post-first-cause-0812`
- App source: `af1605a28f31a53b5a3472251493d44941b618fe`, tree `b0cb1f973c0e1b465241ebef38bd267fd39f0434` (clean before this report)
- Retained source identity: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/run/source-identity.txt`
- Pinned Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
- Pinned Runtime/producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00`
- App pin: `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`
- Durable packet directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/run/`
- Packet manifest `evidence-presence.json` confirms `trace`, `error_context`, `request_response_console_summary`, `source_identity`, and sanitized summary `bounded-browser-evidence.json`. The packet also retains `playwright-trace.zip`, `error-context.md`, `runner-tail.log`, `result.txt` (`runner_status=1`), and retention metadata.

## Boundary and exact values

The retained execution collected and ran one test and failed once at `tests/e2e/local/three-products.spec.ts:1557` after the 90-second predicate ceiling. The predicate expected `attempts: 1` and observed `attempts: 0`.

The first, deliberately wrong flow remains proven as intended: verified selection returned `404` with `code: not_found` and the original assertions remained unchanged. The later valid flow reached all of these milestones:

- `POST /api/runtime/v1/projects/f9d20d640a9441a0a3c1172fe6b79416/media-imports` → `201`
- `GET .../media-selection` → `200`
- `GET .../media-selection/verified` → `200`
- `asset/object_id`: `sha256:5d4268f2d6ada2cf339a0b8f4cf2478c67d6fa7443e3ea780ad1ec6bd980d0c7`
- `generation_id`: `generation-task-dc3e243e21b8447eb768e1a6154cbb0a`
- `variant_id`: `initial-930b16fc662eb18fd3b85be0869506bcaac31eb190c624897d6daf744d42220`
- `catalog_digest`: `sha256:241caf0438b2951e72f3b9e7f23752f6fb9fa5adb0b25d1b7e7286b873332929`
- imported entry: `manual-drop.webm`, `video/webm`, `160935` bytes

Immediately after the valid drop, the trace shows the transient uploading clip on `data-row-id="S1"` with `data-action-id="uploading-..."`. The final DOM shows the transient clip removed and the exact toast:

```text
Failed to save asset
track is the lane of an occurrence-owned shot
```

The local source boundary is:

- `src/tools/video-editor/lib/external-drop-utils.ts:456` creates the skeleton with `track: compatibleTrackId`; the retained DOM proves that value was `S1`.
- `src/tools/video-editor/lib/external-drop-utils.ts:524` passes that track to the prepared video drop.
- `src/tools/video-editor/hooks/useAssetManagement.ts:303-317` routes prepared video placement through `commands.addClip` and surfaces the returned refusal.
- `src/tools/video-editor/commands/parentClipAddCapture.ts:379-385` checks selected occurrences and throws `ClipMoveError('track is the lane of an occurrence-owned shot', 'unsupported_ownership')` when an occurrence track equals `row.track`.
- `src/tools/video-editor/hooks/useExternalDrop.ts:647-650` displays the retained toast.

This is the first causal value available in the packet: `row.track = S1`, followed by the exact `unsupported_ownership` refusal. The trace does not expose an internal call stack or a serialized `clip.add-media` command because capture stops before the wire layer. It therefore does not prove whether `S1` was selected by a row-order/layout projection defect or was the intended target under the mounted state. It also does not establish an accepted ADD, an ACK, or a Runtime refusal.

## No data-safety loss established

The chosen media is still represented by the Runtime import receipt and verified five-field selection above. The trace has no commit POST after the valid `verified=200`; across the whole trace there are 21 POSTs: 3 handshakes, 16 inspect calls, and 2 media imports, with zero `/commits` POSTs. `astridCalls` is empty. Recovery UI and `astrid.timeline-drafts` reads remain empty/null after the refusal. Thus no recoverable command draft is shown to have been lost: the existing carrier is the Runtime import/selection record, not an outbox or timeline draft.

## Decision and follow-up

No source patch is justified by this evidence. `parentClipAddCapture.test.ts` already locks the occurrence-owner refusal as an intentional no-mutation contract. Relaxing that guard, normalizing `S1`, changing readiness/timeouts, or adding a guessed command field would violate the settled plan. The next investigation should prove the canonical row/track projection that produced `S1` and compare it with the intended drop target before proposing a minimal App-owned fix. No HOME service/session/Provider/harness patch is proposed.

## Commands and counts

Read-only inspection used:

```text
git status --short --branch && git rev-parse HEAD && git rev-parse HEAD^{tree}
nl -ba src/tools/video-editor/{lib/external-drop-utils.ts,hooks/useAssetManagement.ts,hooks/useExternalDrop.ts,commands/parentClipAddCapture.ts}
unzip -p "$PACKET/playwright-trace.zip" 0-trace.network | jq -s '[.[] | select(.snapshot.request.method == "POST")] | length'
unzip -p "$PACKET/playwright-trace.zip" 0-trace.trace | rg -n 'uploading-|track is the lane of an occurrence-owned shot|timeline-command-recovery|astrid.timeline-drafts'
```

Results: source tree matched the retained identity; POST count was `21` overall and `/commits` POST count was `0`; trace markers showed the `S1` skeleton, refusal toast, and null recovery/draft probes. No browser, build, daemon, socket, actual journey, test-service submission, retry, install, targeted test, or full suite was run for this diagnosis.
