# F D141 final unit-notes custody-return validation

Status: **QUALIFIED_CURRENT_CONTENT_WITH_CUSTODY_LIMIT**.

## Source-backed comparison

- `python3 evidence/comparison.py` — PASS; current canonical targets equal accepted `48013c...f9fc02` / `506e44...63a55`; backups equal `13f2...bc776` / `b299...15b47`; current outside count is `568`; current map equals the independent review map and the retained installer after map.
- The script did not invoke `delivery-build`, `render_readme`, a CLI, or any builder. It retained the independent review's prior function-only render result: placeholders resolved, balanced fences, 32 IDs, two disclosures.
- The exact placement-installer aggregate algorithm was reproduced from the retained installer log. Current paths reproduce the independently retained earlier aggregate: count `568`, SHA-256 `eea4cb8759a00a1ad7e9a5eab5922e4ebeb36d2a6ec0b0bde22c8f63e3c7fded`.

## Custody correction

- The independent prior review remains `FAIL_CUSTODY_LIMIT`.
- The original installer compared its pre/post outside maps in memory, but the first process failed after CAS on an over-strict fallback assertion before durable serialization. The later read-only follow-up populated both retained maps from current bytes. Those maps are not historical pre-CAS evidence.
- Genuine immediate pre-CAS 568-item map and genuine pre/post conservation are **UNKNOWN / NOT_RECOVERABLE**. The original installer sampler PID, exit code, wait, and reap facts are **UNKNOWN** and are not inferred from the new return sampler.
- The earlier placement aggregate is reported only as a separate earlier-to-current interval. It is not immediate pre-CAS evidence, and no absence of transient changes is inferred.

## New read-only return sampler

- `evidence/disk-trace.txt` — PASS; three durable samples at a five-second interval; minimum available bytes `5,674,721,280`, above the `4,000,000,000`-byte floor.
- `evidence/sampler-lifecycle.json` — PASS; own PID `4`, exit `0`, wait called, process reaped. These facts belong only to this read-only return sampler.

No reinstall, rollback, canonical mutation, semantic review, real builder invocation, rerender, product test, type check, lint, full suite, build, or ZIP was performed. Product tests/types/lint are N/A for this documentary custody return.
