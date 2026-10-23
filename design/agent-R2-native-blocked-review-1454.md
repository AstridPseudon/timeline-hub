# R2 native redo blocked review 1454

Status: **FAIL for behavioral acceptance; PASS for diagnostic fidelity.**

This is an independent review of `tl/agt-R2-redo-native-source-sol-1436`
against PLAN §3 R2 and C0 §§1/2/5. The product source remains the 805 baseline;
this review contains no product repair and the Sol candidate is not mergeable.

## Decision and owner

The retained diagnostic is faithful. The immutable packet, accepted history,
request shape, candidate behavior, and validator locals agree. The initial
working-alias versus canonical-physical-input refusal is Agent-owned, as
already confirmed independently by Runtime1438. The candidate's source-bound
normalization clears that first refusal, but does not establish the next
intermediate stage.

The behavioral acceptance remains **FAIL**. Runtime cfa0 correctly refuses the
candidate's grouped native/effect correspondence; this is not evidence for a
Runtime guard relaxation or a contract change.

Dispatch the next correction to the existing Agent inverse staging seam:
`astrid/sdk/timeline/inverse.py` (`apply_inverse`) and
`astrid/sdk/timeline/_step_undo.py` (`inverse_stages`), with
`_commit_patch.py` projection only if the staged representation requires it.
The correction must retain the authenticated original `fork-edit-0` / `fork-edit-1`
boundary when re-inverting the single-step `undo-0` record, or otherwise emit a
strictly equivalent authenticated representation in which the created-shot
root is not claimed as the final image after the later `params.text` removal.
It must preserve the physical occurrence/source bindings, authored order,
full-v2 request and reply/history fields, identity allocation, and every
existing guard. Do not swap orientation, guess a successor, rewrite accepted
history, copy a root, or weaken Runtime validation. If current C0 cannot encode
that nested boundary, return the seam as a contract question rather than
changing Runtime.

Runtime1442's separate parent/occurrences physical-observation work is not the
cause shown here. No Runtime1442 handoff is requested by this review.

## Exact causal facts

Durable source-complete packet:
`design/agent-R2-redo-native-source-1436-b54d2efee42e0934.json`, SHA-256
`b54d2efee42e093485e7ad6a4c73e7fca2c8318ad0b02cdbcde9330c3750eff3`.
Its retained actual fixture is SHA-256
`9a47bb934b879efa0f6147d673038cee76299ba4e30ab22b6d5bcb1377ade589`.

The accepted source history is exact:

- `txn-7d039d147e1b4c5ba6cc7ca912b95cba` (`fork-edit`) has two steps:
  `fork-edit-0` creates the selected shot and changes the occurrence to
  `selected-shot`; `fork-edit-1` removes `params.text` from
  `f2-agent-clip`.
- `txn-75285c95600949c8b1267a71f8e71a9d` (`undo`) has one `undo-0` command
  with three authored writes. Re-inverting it produces the native order
  shot-root creation, occurrence attachment, then the later leaf removal.
- The source root creation carries `f2-agent-clip.params={"text":"hello"}`;
  the authenticated complete stage after the later leaf removal carries
  `params={}`.

The exact validator boundary is retained in `next-stage.json`; its canonical
SHA-256 is `570a7fc665e50b1a10b7977bea973f6067987b5f5dfc07b983909507fab8eb26`.
The minimized complete boundary input is:

```json
{
  "root": "shot:selected-shot",
  "observed": {"state": "absent"},
  "before_claim": {"state": "absent"},
  "physical": [],
  "write": {
    "ref": "occurrence:f2-occurrence/clip:f2-agent-clip",
    "path": ["params", "text"],
    "before": {"state": "present", "value": "hello"},
    "after": {"state": "absent"}
  },
  "after_claim": {
    "state": "present",
    "root": "shot:selected-shot",
    "internal_timeline_revision_id":
      "authoring-timeline-revision-7a359d276a5221748b217fbe94b7b28bad96bd8fe5a8d4db98c75466c7cd4b56",
    "clip_id": "f2-agent-clip",
    "params": {"text": "hello"}
  },
  "authenticated_stage_after": {
    "internal_timeline_revision_id":
      "authoring-timeline-revision-7a359d276a5221748b217fbe94b7b28bad96bd8fe5a8d4db98c75466c7cd4b56",
    "clip_id": "f2-agent-clip",
    "params": {}
  },
  "source_boundary": {
    "publication_id": "txn-75285c95600949c8b1267a71f8e71a9d",
    "step_id": "undo-0",
    "command_ordinals": [0],
    "native_write_range": [0, 3],
    "effect_range": [0, 4]
  }
}
```

The complete unabridged boundary is embedded in the packet; the hash above is
for that retained JSON, not for this summary projection. No scratch-only path
is required to interpret this handoff.

## Verification

- Candidate removal/source equality: PASS. `git diff --exit-code
  80523b472 -- astrid` is clean; current `_commit_patch.py` is
  `c41946a5...`, matching the packet's final-origin hash; candidate helper
  symbols are absent. No assertion rewrite, skip, or xfail was introduced.
- Offline retained-facts reconstruction: PASS. Packet hash, source history,
  full-v2 request keys, exact native writes, and the `next-stage.json` root/
  leaf mismatch all assert consistently.
- Retained targeted controls: PASS, **15 passed in 6.87s**, using the pinned
  Runtime cfa0 checkout: captured media closure, inverse-stage images,
  inverse-binding tests, and the selected authoring-bundle timing guard.
- Reused unchanged prior evidence on the exact source tree: inverse guards
  **74 passed, 1 deselected**; Ruff **2149/2149**; mypy **1912/1912**;
  authoring Ruff **2149/2149**; vendor lock, artifact manifest, and diff
  checks passed.
- Strict positive redo acceptance: FAIL, retained actual-red and candidate
  strict-cas logs. No public redo retry or known-failed body repeat was run.

The prior targeted invocation first failed only because this worker's prescribed
`tmpdir` is a regular marker file and pytest could not create `--basetemp`
beneath it; the corrected private `/tmp` invocation above is the qualified
result. No product or shared dependency state was changed.

## Next gate

Keep G5/P1 NO-GO. A new Agent candidate must first pass the exact retained
strict validator and negative/no-write controls, with the original full-v2
request/records/bindings/effects/deps/history/undo_steps and canonical IDs
unchanged. Only after that independent source review may the orchestrator
authorize the single public fork → free edit → whole undo → redo → exact retry
journey.
