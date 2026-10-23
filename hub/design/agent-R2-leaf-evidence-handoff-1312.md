# R2 leaf evidence custody handoff 1312 — PASS

## Result

Published the bounded Luna 1246 capture for Runtime leaf-inverse review:

- `agent-R2-leaf-1246-e97f81ce7c350f08.json`
- `agent-R2-leaf-1246-e97f81ce7c350f08.manifest.json`

The package is flat, immutable-by-convention, and contains complete JSON values rather than a causal summary in place of facts. It includes complete `auth-input-35.json`, `stage-comparison-01.json`, and `causal-summary.json`; service-01 preview boundary evidence; service-02 source request, accepted reply/receipt, and before/after state; service-03 undo request, refusal, before/after state; and the final `origins.json` snapshot.

The package is 426,995 bytes with SHA-256 `1123978b7b18c59d280f73c9ad9155b5ba18d0c64b24e45b8bdd02af30a887b0`. The manifest is 3,801 bytes and records exact original source sizes and SHA-256 values, compact serialization sizes/digests, and the package digest.

## Custody and limits

- Source evidence was read from `ORCH/workers/agt-R2-fork-emitter-undo-diagnosis-1246/evidence`; no source file was overwritten.
- Compact UTF-8 JSON serialization round-trips semantically for every copied artifact. The manifest hashes the exact original evidence bytes as well as the compact forms.
- The credential check passed: no bearer value, authorization header, Codex credential, or request body was copied. Recorded `source` fields are retained because they are part of the production evidence; no source body was expected.
- `origins.json` is the final 144-module origin/hash snapshot only. No before/after origin snapshots or temporal module comparison is claimed.
- The existing `design/agent-R2-fork-emitter-undo-regression-1246.py` was retained unchanged.

## Evidence interpretation

The retained 10-check causal result remains the settled classification: the first failing boundary is Runtime leaf inverse physical materialization turnover, not an Agent-only authored-field omission. The accepted forward service-02 evidence preserves the production request/reply shape and the service-03 refusal preserves the no-write fact. The Runtime owner `rt-R2r-leaf-inverse-materialization-1304` should use the complete stage/native/effect/ownership/binding images for its authorized correction and proof.

## Validation

Commands and results:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python ORCH/workers/agt-R2-fork-emitter-undo-diagnosis-1246/analyze.py
PASS: 10 offline causal checks; no service or validation replay

python3 package validation script (source hashes, manifest/package hash, JSON round-trip,
required IDs/fields, no-write equality, 144 origins, credential scan)
PASS

sha256sum on auth-input-35.json, stage-comparison-01.json, causal-summary.json
PASS; source hashes retained in the manifest
```

No product, test, suite, pin, live probe, source fix, observer, daemon, or Git operation was performed. No full suite was requested. No blocker remains for this custody handoff; the combined undo behavior itself remains unresolved pending the Runtime owner’s implementation and integrated proof.
