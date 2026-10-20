> Historical worker draft, superseded by PUBLISHED design/runtime-current-tuple.md at11:28:51Z. Its proposed consumer-before-source-publication order was not adopted: consumers need the exact published source in order to qualify. Exact-tree passing results are reusable; no repeat of all five unchanged lanes or external package-registry publication is required.

# Runtime S2 publication draft

Status: draft only. This document is not the published Runtime tuple and does not authorize a pin, merge, activation, or package publication.

## Approved candidate

The approved release review is for this exact composed Runtime candidate:

| Field | Exact value |
|---|---|
| Server candidate/source commit | `f7081c14efd9a5b834987e7a1e2abf597b66313b` |
| Candidate tree | `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Composed Runtime base/parent | `8609333456b9537339ee1a5dfc7ffd9609242de8` |
| Contract/client release | `0.2.13` |
| Protocol | `workspace.v1` |

The candidate is approved as source and bounded qualification only. The final review did not publish it, move consumer pins, activate a consumer, run a full suite on this release tree, run a browser journey, prove capture/F3 pairing, or complete frame/audio/owner-film qualification.

## Contract identity and inventory

All values below were recalculated or independently reproduced from the exact candidate tree.

| Item | Exact value |
|---|---|
| Generated schema digest | `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4` |
| Raw S2 Agent schema SHA-256 | `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` |
| S2 Agent schema shape | `48` definitions, `22` operations |
| Artifact count | `75` (including `operation-handle.ts`) |
| Artifact version digest | `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56` |
| Raw artifact manifest SHA-256 | `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497` |
| Component manifest SHA-256 | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| HTTP operation IDs | `133`, unique; `52` GET, `1` HEAD, `72` POST, `5` PATCH, `2` PUT, `1` DELETE |

The 22 supported EditCommand operations in the S2 Agent schema are:

`clip.add`, `clip.move`, `clip.set`, `clip.set-params`, `clip.set-element`, `clip.trim`, `clip.split`, `clip.delete`, `track.create`, `track.set`, `occurrence.add-media`, `occurrence.swap-media`, `occurrence.duplicate`, `occurrence.delete`, `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`, `shot.set`, `producer.guard`, `timeline.inverse`, and `timeline.restore`.

The raw S2 Agent source is `26ef2bbb31b4892fdd7c15ee5b20700bd40cb933`. S1 remains immutable and is retained as a compatibility floor. S2 adds only the optional `ClipSetElementArgs.schema_source: DocumentPin` field and its description relative to S1; it does not add F3, parent birth, native text-clear, or another unfrozen operation.

## Verified reads and persisted views

The verified-read family remains four wire operations, with one shared helper and route table:

- `getProjectMediaSelection`
- `getProjectVerifiedMedia`
- `getProjectVerifiedDocumentObject`
- `getProjectVerifiedDocument`

They are reads, not a new merged wire operation. Project authorization and retained source/document custody checks remain read-only.

Persisted `POST /v1/projects/{project_id}/timelines/{timeline_id}/views` is a mutation in this candidate. It requires `projects:write` (or the existing admin authority) and an explicit valid `Idempotency-Key`; `projects:read` alone is rejected before ingestion. `POST .../inspect` remains a pure `projects:read` operation with no key. Identical retries reuse the same key and request body and return the original view across head advancement/restart within the existing replay window; changed input under the same key is refused. No receipt wrapper was added. The browser door continues to deny `/views`.

The final official client signatures are:

```text
Python:     create_timeline_view(project_id, timeline_id, options=None, *, idempotency_key)
TypeScript: createTimelineView(projectId, timelineId, options, idempotencyKey)
```

Caller migration remains a release prerequisite:

- Agent caller source `tl/agt-m2-view-write-caller` resolves read-only to `0cfdddd5b85d5a32e5319365e64cb58293381490`. Its facade and remote dispatch must forward the explicit stable key, remove view creation from the read classification, and use `projects:write`. Agent owns live SDK/CLI qualification.
- App has no production persisted-view invocation in the accepted inventory. It must copy the final four-argument official client and matching pin together, and typecheck the pair. Any future direct view caller needs `projects:write` and a stable retry key.
- `inspect` stays read-only. No browser route is opened by this release.

## Connector boundary

The approved connector source is `78d14ec045c9b67f32ac2b340c48d4ae9b715345`. Its direct `OperationHost`/`OperationHandle` is intentionally bounded: immediate same-owner dispatch uses a fixed target, credential, and options. It does not support an awaiting forwarding wrapper, hidden target/credential reselection, automatic browser requesting, or hosted/absolute Runtime-door activation. Cookies remain omitted and redirects are refused. A supported owner must negotiate and use the same handle/client and live identity callback; opaque in-process ACK fixtures do not prove remote Runtime acceptance or replay.

## Older affected tuples

The old published tuples must not be treated as equivalent to this candidate:

| Tuple | Runtime commit/tree | Contract/schema | Required handling |
|---|---|---|---|
| `0.2.9` | `94114269d1ce23ab3224d7eca5a85138ce2b5fed` / historical tree recorded in `runtime-current-tuple.md` | `sha256:8d7f29873ff3417cda746e243ebc81cb9d54e41c972596d4d3ae591fc1de00cf` | Affected by the restored-publication F1 occupied-destination overwrite and F2 hidden legacy-document adoption defects; remains historical and must not be relabeled. |
| `0.2.10` | `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` / `bb2d3b6235cc7bf819373d2078d7437360c322d4` | `sha256:3e5e78d0a689b32c46738455b5f7875999eb7d3da4917a38bd6a9eaaf41d0f3c` | Also affected by F1/F2; do not leave consumers on this tuple after the paired replacement is qualified. |

Staging `0.2.11` and `0.2.12` were intermediate connector/view artifacts, not public consumer targets. They must not be pinned. The safe target is one coordinated `0.2.13` tuple after merge and consumer qualification.

## Final five candidate gates

All five central gates below ran against exact tree `7ab412cc4bcbe517efcfa806e092336390312e18`; these are the final candidate results, not a claim that the post-merge integration tree has the same identity.

| Gate | Exact service result |
|---|---|
| Runtime targeted contract/behavior lane | `rt-m2-release-s2-final-compose-targeted-1020110503-8618`: **800 passed, 1 deselected, 1 unchanged strict text-clear xfail**, exit `0`, `173.56s`. The xfail is `tests/test_timeline_text_selection.py::test_clear_removes_the_live_binding`; the file is unchanged and native text-clear is not claimed. |
| TypeScript client/build/public API | `rt-m2-release-s2-final-compose-ts-client-check-1020110503-30973`: **61 passed, 0 failed, 0 skipped**, exit `0`. |
| Runtime/Agent commit integration | `rt-m2-release-s2-final-compose-commit-integration-1020110503-17965`: **9 passed**, exit `0`, `8.92s`. |
| Occupied-destination integration | `rt-m2-release-s2-final-compose-occupancy-integration-1020110503-17107`: **1 passed, 17 deselected**, exit `0`, `1.19s`. |
| Frozen Agent S2 producer integration | `rt-m2-release-s2-final-compose-producer-agent-s2-integration-1020110503-5266`: **5 actual passes with `--runxfail`**, exit `0`, `3.06s`, using the immutable Agent `26ef2bbb` archive rather than a fake provider or schema overlay. |

Prior full evidence is historical only: request `full-restore-integration-1020095412-22308` on the earlier `8609333` integration tree recorded **5194 passed, 7 same baseline failures, 18 skipped, 25 xfailed**. Those seven failures remain a baseline record, not an all-green result. **No full suite was run or claimed on release tree `7ab412cc…`.**

## Publish-after-merge checklist

The following must be completed by the Runtime manager/orchestrator after the candidate is merged; this worker does not perform these actions.

1. Merge the approved candidate through the merge queue into `tl/integration`; record the resulting exact Runtime commit SHA and tree. If the merge changes any source or generated blob, treat `0.2.13` evidence as stale and requalify the resulting tree.
2. On that exact post-merge tree, rerun normal generation, TypeScript conformance generation/check, artifact-manifest check, client parity/public API checks, and the final Runtime targeted, TypeScript, commit, occupancy, and immutable Agent S2 producer lanes. Keep the unchanged text-clear xfail visible.
3. Verify the post-merge contract identity against the candidate values: contract `0.2.13`, schema digest, raw S2 schema SHA, 75 artifacts, artifact-version digest, raw artifact-manifest SHA, component-manifest SHA, 133 HTTP operations, and 22 EditCommand operations. Record any intentional identity change instead of silently reusing this draft.
4. Complete Agent’s paired view qualification using the official client and caller source `0cfdddd5b85d5a32e5319365e64cb58293381490`: read-only refusal, successful `projects:write` mutation, explicit stable key forwarding, exact retry identity, and unchanged inspect/read behavior.
5. Complete App’s paired client/pin/typecheck qualification. Copy the final official client and matching Runtime pin together; do not pin staging `0.2.11` or `0.2.12`. Confirm no production App persisted-view caller was missed; browser `/views` remains denied.
6. Recheck the connector boundary on the merged tuple: fixed-target/direct-handle limits, authenticated identity capture before later awaits, no cookies, no redirects, and no browser/hosted requester activation. Do not turn connector unit evidence into a browser or live Runtime acceptance claim.
7. Confirm the F1/F2 safety fixes are present in the merged tree and document the migration/remediation path for consumers still on `0.2.9` or `0.2.10`. Preserve the old tuples as historical records.
8. Only after steps 1–7 pass, update `design/runtime-current-tuple.md` as the single current tuple, with the actual post-merge commit/tree, publication timestamp/actor, exact client and artifact identities, consumer qualification references, and the remaining limitations. Then perform the separately owned package publication, exact consumer pin moves, and activation checks.

## Missing post-merge metadata

This draft intentionally cannot fill in values that do not exist until merge/publication:

- actual post-merge `tl/integration` Runtime commit and tree;
- post-merge rerun IDs/results for all five gates and normal generation/artifact checks;
- Agent live SDK/CLI view qualification result and the final paired caller/pin identity;
- App final copied-client/pin identity and qualification result;
- publication timestamp, publishing actor, registry/package record or URL, and activation result;
- final consumer pin SHAs and the exact runtime checkout used for each pin.

Until those fields are filled by the owner of publication, this file remains a draft and `runtime-current-tuple.md` must remain unchanged.
