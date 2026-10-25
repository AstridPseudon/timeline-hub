## F/D134 report

Prepared durable evidence under `evidence/`:

- Exact frozen source tuple and static provenance.
- Conditional measurement recipe preserving 22 roots, `-n 3`, cleared addopts, no cache provider, timeout 45.
- Gated positive/poison preflight recipe.
- Finite `EXACTMISSING` inputs and refusal disposition.

Source audit: PASS for clean frozen trees, Runtime lock, schema equality, profile hashes/version, and Node `v20.19.4`.

Missing prerequisites:

- Exact-tuple `P4_D73_MANIFEST` and paired evidence directory.
- Genuine MAIN positive/poison controls and fresh counters.
- 20:00Z custody verdict `NOT_GREEN` plus gated authorization.
- Ordinary preflight acceptance, which was intentionally not run here.

Validation passed:

```text
bash -n evidence/measurement-command.sh evidence/preflight-command.sh
python3.11 -m json.tool evidence/{readiness,source-manifest,missing-inputs}.json
git diff --check
```

No suite, request-test, preflight body, collection, package install, child build, or measurement body was run. D128’s existing custody refusal remains preserved; no suite row was changed.

Completion marker and `F/D134` commit message were written.