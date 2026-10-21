# Pending HOME handoff transport diagnosis — 2026-10-21

## Verdict

Transport is healthy. All three exact HOME requests are now delivered to the
correct repo owner and are waiting on owner review; none is locally queued in
the viewing area and none is sync-stalled. No resend, close, result invention,
or product change was made.

| request | request record | exact source ref | current delivery state |
|---|---|---|---|
| App admission | `hub/merge-requests/app/vw-m3-gate6-admission-only-reviewed-source-0914` → `0d4323913b92c4e0e3830bf14ec7f35d981475ca` | `refs/remotes/hub/timeline/app/tl/vw-m3-gate6-admission-only-reviewed-source-0914` | `hub/merge-results/app/vw-m3-gate6-admission-only-reviewed-source-0914`: `PENDING owner review (0d4323913)` |
| App seek producer | `hub/merge-requests/app/vw-m3-queued-seek-existing-callback-producer-0935` → `13bf239d9d8170b2f31a512745639d123f6b25fd` | `refs/remotes/hub/timeline/app/tl/vw-m3-queued-seek-existing-callback-producer-0935` | `hub/merge-results/app/vw-m3-queued-seek-existing-callback-producer-0935`: `PENDING owner review (13bf239d9)` |
| Agent Theme fixture | `hub/merge-requests/agent/vw-m3-normal-theme-qualified-fixture-home-port-0924` → `2ff901ebe16666bbd4c1667da40c8f859b01acd7` | `refs/remotes/hub/timeline/agent/tl/vw-m3-normal-theme-qualified-fixture-home-port-0924` | `hub/merge-results/agent/vw-m3-normal-theme-qualified-fixture-home-port-0924`: `PENDING owner review (2ff901ebe)` |

## Delivery timeline

- Agent processed the Theme request in hub-sync `agent 2026-10-21T09:37:33Z`
  (`6ad7c8af8`, committed `09:39:02Z`) and created its PENDING result.
- Viewing published the two App request records in hub-sync `viewing
  2026-10-21T09:45:36Z` (`678a94972`, committed `09:46:41Z`). App's preceding
  sync was `app 2026-10-21T09:42:39Z` (`2309df088`, committed `09:44:16Z`),
  before those request files were published. Their temporary absence was
  therefore expected ordering, not a transport failure.
- App then processed both requests in hub-sync `app 2026-10-21T09:49:18Z`
  (`27871dc73`, committed `09:50:51Z`) and created both PENDING results.
  Current App status header reports that same sync and a live dispatcher
  heartbeat; current Agent and Viewing status headers are also present.

## Source identity checks

- `0d432391...`: parent `d00a66134f330672ea7471dc69db38c1566d94cf`, tree
  `5a1e0e85d0f336f642426b91ccf3b3f1984ebd14`, one `cases.ts` change.
- `13bf239...`: parent `4db86a76acd505dd1c7dc798695e2b7a9c932170`, tree
  `11012554aa20aaacf8293ab496e8610555d9b361`, the two RemotionPreview paths.
- `2ff901...`: parent `c4b964f6a050edf63a4278d35717e46a88a80386`, tree
  `610096b9b685af9d8539fc0af070e0cdbdc5aa03`, one Theme fixture test path.

All three refs resolve in the local hub-tracking refs and the request records
name the matching repo and `viewing` area.

## Supported transport interpretation

The current `COMMS.md` and `bin/hub-sync` make `hub/merge-requests/<repo>/<worker>`
the HOME code handoff. The owning machine fetches the branch, appends its
manager INBOX, and writes `hub/merge-results/<repo>/<worker>`; the script
explicitly creates `PENDING owner review` until the owner acts.

`hub/inbox/<area>.md` is the orchestrator-decision/manager-INBOX channel, and
`$ORCH/hub/inbox/*.md` is a local peer-message staging path consumed into a
manager INBOX. `design/peer-*.md` is the cross-machine design/evidence mirror.
Neither is the transport record for these HOME code requests. No repair is
requested.

## Tests

No product or test suite was run; this was a read-only operational diagnosis.
