# Runtime R2r native-order observation handoff

Status: bounded scope confirmed; one Runtime inverse-stage observation correction is justified by the retained authority. No contract decision is made here.

## Retained facts

The three lossless packets named by `agent-G5-inverse-1416.manifest.json` were read and custody-checked. They are the actual original-body packet and the cfa/859 offline replays. The source packet hash recorded in each replay is `01ccdec35f2a8f3e72e99541092f99ec20bda2de036adc6fe77d7f773157aaeb`.

- Accepted source: event117, publication `txn-17252a1958a443a2878f1cb4ed4d9631`, parent revision `caa332cc...`, config digest `e6d3e22782252ab1f325c0013214ad30cd9669bcae8b7502321717371fbff4a9`.
- Predecessor: event129, parent revision `a58d0cd6...`, config digest `3261318905a6bb014857b56b1705960454c99ae9b3e7266dd898cb4867f56115`.
- Inverse input orientation is accepted source `caa332...` → predecessor `a58d...`; `prepared.expected_head` is `txn-17252a1958a443a2878f1cb4ed4d9631` / `caa332...`. The earlier labels that reversed these facts are disproved.
- The accepted source has three occurrence rows; the predecessor has one. The current native inverse recorder captures the authored occurrence rows without the managed `shot_revision_id` field.

## Exact offline validation boundary

The retained `actual_input` supplies the exact `context`, `previous`, accepted `source`, complete accepted `history`, and refused `prepared` value. The cfa replay invokes the production call as:

```python
validate(
    request=actual_input["context"]["request"],
    prepared=actual_input["prepared"],
    source=actual_input["source"],
    base=actual_input["previous"],
    history=actual_input["history"],
)
```

The same call is replayed against Runtime859 in the second lossless packet. Both unchanged validators refuse at the first native inverse write whose `ref/path` is `parent/["occurrences"]`; the exact message is `inverse stage write differs from its sequential input`. The first three native writes pass, including the preceding `parent/["config"]` write. The physical observed rows equal the authored before rows in membership, order, ownership and every non-pin value after removing only `shot_revision_id` from each physical row.

The scratch-only pin-lift diagnostic adds those already-authenticated physical pins to the native capture and turns both replays green. It changes prepared bytes and is not a product candidate or permission to inject pins into Agent.

## Runtime owner boundary

The defect is confined to `runtime_protocol/timeline_commit_auth.py` inverse-stage observation/comparison: `_inverse_stage_state` compares the canonical physical `parent/occurrences` collection directly to an authored native collection that intentionally omits the managed pin. A bounded correction may normalize only this exact parent occurrence-collection observation by removing `shot_revision_id` from physical rows after proving each pin against the authenticated physical shot closure. It must preserve list order, membership, ownership, and every other field, and must reject missing/foreign/ambiguous pins and native claims that include a wrong pin. No sequential verifier, source-chain helper, storage, allocation, Agent code, schema, pins, or redo `shot_id` behavior is in scope.

The existing source/history, effect, digest, owner, range, ABA/later-history, foreign, closure, and final-equality guards remain authoritative. No blanket revision-key stripping or trust of provider-supplied native snapshots is allowed.

Evidence custody and command log are under worker `rt-R2r-native-order-observation-1442/evidence/`; the complete packets are copied there byte-for-byte with their manifest hashes.
