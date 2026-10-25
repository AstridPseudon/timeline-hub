## D108 metric custody report

- Recovered the manifest-backed parser source and provenance in [evidence/original-parser-source.py](/home/user/work/wt/rt-F-D108-metric-custody-0811/evidence/original-parser-source.py).
- Preserved exact totals: Agent `129 changed / 113 removed / 287 added`; Runtime `113 changed / 72 removed / 205 added`.
- Full per-function/assertion membership is `EXACTMISSING`; only limited historical examples survived. Details and hashes are in [metric-record.md](/home/user/work/wt/rt-F-D108-metric-custody-0811/evidence/metric-record.md) and [input-hashes.sha256](/home/user/work/wt/rt-F-D108-metric-custody-0811/evidence/input-hashes.sha256).
- No product changes, recomputation, tests, lint, or full suite runs.

Checks:

- Parser compile: PASS
- `git diff --check`: PASS
- Evidence size: 11,097 bytes
- `DONE` created; commit message written for D108 metric custody.

Blocked/unverified: complete membership cannot be recovered without the original omitted stdout or a newly authorized audit.