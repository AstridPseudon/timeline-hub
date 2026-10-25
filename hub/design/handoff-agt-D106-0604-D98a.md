# F-D86 D106 D98a caller source handback

Disposition: **SOURCE-QUALIFIED / BEHAVIOR-PENDING**. This is the exact caller-source publication, not a functional PASS, full-core result, retirement, or normal merge.

## Exact source and receipt

- Source candidate: `a09ebcbd80fa7d9a83288f1ceded790321ce1877`; reviewed against parent/current normal `bde578505c035ae949ee8176b466bf8297772904`.
- Listed source path: `tests/editing_conformance/test_commit_runtime_occurrence_media.py`; source blob `c4f54e34536dabbf196fd9a17c337b78394506e3`; SHA-256 `cf73444ebe59c7a5e62f29cff072d3c3dea87ead85043d92ef632d433cb110a1`.
- Independent review: `handoff-agt-D98a-review-0550-report.md`, 1454 bytes, SHA-256 `1d7dd6a551ef5f29f0cd16d90fbc7976055f1b9c47b83af3af88c4c5c7f59c33`, **PASS_SOURCE**.
- Normal receipt: `a90bc7f9e1653e94384c094aaa87adf32239f5bc` (`normala90b`), the normal publication pair.
- D106 source body: `rt-D86-new-source-body-0537-report.md`, 1364 bytes, SHA-256 `c5ca88d0db6866f502b01ddac116912c01acbe704a1f851dc3d928591b664cce`; bounded NO-GO, no behavior credit.

## Conservation and boundary

The caller uses registered `capture_occurrence_create` with exact original inputs `chapter-shot`, `occ-a`, `Chapter One`, `picture`, `on=8`, and `duration=10`. The source review preserves the four original test ASTs and 48 selectors (`4 + 24 + 4 + 16`), all opaque values, pins/media, steps/reads, preview/history, refusal, ABA, inverse, retry, and no-write guards. `created` remains recorder-derived (`shot:chapter-shot`, `occurrence:occ-a`); it is not an authored manager claim. Runtime `validate_claims` remains authoritative.

The D82 classification remains the distinction: the 28 recorder-enrichment paths are not promoted to proof, while `commands[2].command.created` is not treated as D82-only. D72 is source-qualified / behavior-pending only. No functional PASS, `fullcore`, retirement, D103 duplicate, D100 fixture-valid phrase, normal merge, or hub write is claimed.
