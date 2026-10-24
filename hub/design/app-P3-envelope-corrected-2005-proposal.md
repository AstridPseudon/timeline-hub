# P3 recorded-command envelope proposal (corrected artifact return)

## Decision

The oracle at `tests/e2e/local/three-products.spec.ts:1820` is wrong for the C0 record envelope. The product path is authentic: App submits the original `doc.patch` command, Agent produces the authoritative recorder command, Runtime persists that recorder in the receipt-bound history entry, and `/commits` projects it unchanged. The failing equality compares two intentionally different shapes.

No product defect or App request mutation is proposed. This is a strict protected-test proposal only; it is not applied and is not a P3 GO.

## Exact proposal

Artifact: `proposal.patch` in this directory. Its bytes are unchanged from author1948.

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

## Correction record

The author1948 proposal and patch are retained unchanged except for this document's hash inventory. The only correction is the full virtual protected-spec SHA: author1948 published `ef05a482b17bf1cc37be0f264610ec0bbbe2335921565f6699ff00e7992650c4`, but exact application of the unchanged patch to the exact base produces `93c2bf4c72ac3c91442a1a52174e36311113751ab9d8b7e0f52e4a958559a64b`. The patch SHA, base SHA, helper-region SHA, and B-region SHAs are independently recomputed below and are not changed by this correction.

## Hashes and patch controls

Pinned base/source: `f6a21c285267d6475816adbda74233907ac93911`.

The machine-readable complete inventory and predicate map is [hashes-and-predicates.json](./hashes-and-predicates.json). Region hashes use UTF-8 bytes of the specified source line slice joined by `\n`; the helper slice includes its terminal newline, while the B slices use the exact original region convention without an additional terminal newline.

| Artifact | SHA-256 |
|---|---|
| Exact-base protected spec | `736fd38108283b9c8b5faac47adff4a9c1abd087cb326184a6bfec480e491e05` |
| Exact unchanged review patch | `80127a0bc4174b8a5b25d9bc34a52d01c712f76a32a1076245ad9547c0846733` |
| Exact-base + exact-patch virtual spec | `93c2bf4c72ac3c91442a1a52174e36311113751ab9d8b7e0f52e4a958559a64b` |
| Virtual helper region, lines 957–977 | `312ded75179f64711c83ee2b9e2e764283eab7905ec5602437733cefe18390c2` |
| B region before, lines 1819–1822 | `67e2292e268a86cfc51c045cfdddfdf8951846821d20c32bf0604eec892434b6` |
| B region after, lines 1840–1843 | `f0c857e32eeca8fcdc8362c3adf6382dc9d2bf7e9d4be8c7504921a73a1e54f5` |

The exact patch applies cleanly with `git apply --check` against the clean exact-base tree. The retained control covers the positive canonical fixture plus 21 independent mutations: each raw field family, each authoritative field family, missing and extra keys, wrong before/value/identity/order, and key/order-shape failures.

Node 20 fault-order control:

`/opt/node20/bin/node --import tsx --test tests/e2e/local/support/gate5-fault-order.test.mjs` — PASS, 3/3 subtests.

No browser, live Runtime, full suite, original P3 rerun, source edit, generated edit, pin, registry change, or protected-spec application was made.
