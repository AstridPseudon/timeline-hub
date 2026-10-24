# P3 recorded-command envelope proposal (review-only)

## Decision

The oracle at `tests/e2e/local/three-products.spec.ts:1820` is wrong for the C0 record envelope. The product path is authentic: App submits the original `doc.patch` command, Agent produces the authoritative recorder command, Runtime persists that recorder in the receipt-bound history entry, and `/commits` projects it unchanged. The failing equality compares two intentionally different shapes.

No product defect or App request mutation is proposed. This is a strict protected-test proposal only; it is not applied and is not a P3 GO.

## Exact proposal

Artifact: `proposal.patch` in this directory.

The patch has one source-file delta:

1. Add `expectRecordedDocumentPatchCommand` immediately before `expectV2History`.
2. Replace only the merged-B assertion at line 1820 with a call to that helper.

The helper strictly requires the submitted B command to have exactly these six keys:

`args`, `created`, `op`, `schema_version`, `select`, `version`.

It strictly requires the authoritative recorded command to have exactly those raw keys plus the seven provider additions:

`authorship`, `bindings`, `expect`, `intent`, `reads`, `resolved`, `selections`.

It then deep-compares the complete object. Expected values are independent of the response: `seed3.appClipId`, the submitted `doc.patch` body, and the contract/provider fact that B reads and moves `at` from 5 to 7. The exact expected additions are:

- `authorship[parent/clip:<appClipId>::at] = direct`;
- empty `bindings`, `intent`, `resolved`, and `selections`;
- `expect[parent/clip:<appClipId>::at] = present(5)`;
- one exact `reads` entry for `parent/clip:<appClipId>/at`, present(5).

The existing record-level `reads.length > 0` and `bindings.length > 0` assertions remain unchanged. Exact request, receipt, head, history, wait, key/body/order/count, recovery-mount, downstream-B, preview, Agent, canonical, and undo assertions remain unchanged.

## Source and contract proof

- C0 §1 lines 102–110: submitted step patches are checked claims; provider fills accepted patches/effect records, and replies/history contain complete provider-derived facts.
- C0 §1 lines 144–155: accepted dependencies and `records.commands` are provider-only/authenticated recorder facts; caller-authored recorder facts are not authority.
- C0 §4 lines 705–715: the success envelope is `{data, receipt}` and returns normalized commands and complete steps.
- C0 §7 lines 4611–4626: history stores the provider command recorder and authenticated attribution; history agrees with the accepted result rather than reconstructing authorship from App metadata.
- App `src/tools/video-editor/commands/localSaveSession.ts:165–185`: recovery rebuilds only the original persisted command/step/read/created bytes and advances only the base pair.
- App `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:565–577`: mounted document edits are emitted as the `doc.patch` intent; no recorder metadata is added to the request.
- Runtime `runtime_protocol/timeline_commit_store.py:947–949`: accepted `data.commands` is projected from provider `records.commands`.
- Runtime `runtime_protocol/timeline_commit_store.py:1424–1448` and `442–475`: the recorder is receipt/event authenticated, durably stored, and returned by history without replacing it with the request command.
- Agent `astrid/sdk/timeline/_recording.py:246–280`: the provider derives `reads`, `selections`, `bindings`, `created`, `expect`, and `authorship` while finishing a record.
- Agent `astrid/sdk/timeline/commands.py:280–304`: generated recorder fields are checked and the normalized command is retained as the authoritative record.

The observed failure is consistent with those sources: the submitted B command has the six raw keys; the recorded command has the seven exact additions. No product source change is justified.

## Hashes and patch controls

Pinned base/source: `f6a21c285267d6475816adbda74233907ac93911`.

| Artifact | SHA-256 |
|---|---|
| Protected spec before | `736fd38108283b9c8b5faac47adff4a9c1abd087cb326184a6bfec480e491e05` |
| Virtual spec after | `ef05a482b17bf1cc37be0f264610ec0bbbe2335921565f6699ff00e7992650c4` |
| Virtual helper region | `312ded75179f64711c83ee2b9e2e764283eab7905ec5602437733cefe18390c2` |
| Virtual merged-B region before | `67e2292e268a86cfc51c045cfdddfdf8951846821d20c32bf0604eec892434b6` |
| Virtual merged-B region after | `f0c857e32eeca8fcdc8362c3adf6382dc9d2bf7e9d4be8c7504921a73a1e54f5` |
| Review patch | `80127a0bc4174b8a5b25d9bc34a52d01c712f76a32a1076245ad9547c0846733` |

`git apply --check proposal.patch` passes against the clean worktree. The worktree remains unchanged.

Node 20 controls:

- `/opt/node20/bin/node --import tsx --test tests/e2e/local/support/gate5-fault-order.test.mjs` — PASS, 1 test file / 3 subtests.
- In-memory strict-envelope control — PASS, 3 checks: valid exact projection, missing authoritative field rejected, unexpected authoritative field rejected.
- `/opt/node20/bin/node --test ...` without the `tsx` loader — FAIL because the existing `.mjs` control imports `.ts`; this is a runner invocation error, not a proposal result. The loader-correct command above is the valid Node 20 result.

No browser, live Runtime, full suite, original P3 rerun, source edit, generated edit, pin, or registry change was made.
