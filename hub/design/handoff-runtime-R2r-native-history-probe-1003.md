# Runtime R2r native history probe 1003

Result: **FAIL on candidate `21b329935785e4040775ed34b4a01ebf31ec6683`**.

The separately named corrected diagnostic
`agent-R2-stage-repro-1003-store-authenticated.py` ran the retained split+note
case through the real Runtime store and Agent provider. It supplied the
inverse validator with the exact accepted forward history entry obtained from
`TimelineCommitStore.history_entry`; no detached realm entry or inverse/future
record was supplied. Forward AUTH passed. Candidate inverse production
acceptance and direct AUTH both refused with:

`invalid_records: inverse stage write differs from its sequential input`

The full JSON, including the exact request, input/output documents, prepared
records, stage facts, history argument, provenance, module origins and hashes,
is at `/tmp/w-71481117c1/candidate.json` (SHA-256
`c4d528ffc7cdbf56bb25298e3211fbd229ec1c0b1c08e543f2fb48f16968fe05`).

Negative probes for missing history, forged source-step history, and an extra
future history entry all refused. The unchanged original 0912 repro hash was
verified as `47399344d70ecb35bca0f843aea5c7245cae35a623cdbbcfd777465d47810f8a`.

The same exact request against original1365 accepted the inverse and reported
direct auth pass, but original1365 has no authenticated-history validator
parameter; this confirms the candidate binding mismatch only and is not a
qualification result. Full comparison JSON:
`/tmp/w-71481117c1/original1365.json`.

Limits: no product repair was authorized or made; no HTTP/browser/full suite,
original58, original20, or P5 rerun. The result is a retained production
defect requiring orchestrator judgment before any repair task.
