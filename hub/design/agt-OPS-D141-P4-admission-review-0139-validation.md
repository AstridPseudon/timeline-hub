# OPS P4 D141c validation

## Static checks

- `bash -n ops-d141-p4-admission/admission-controls.sh` — PASS.
- `bash -n ops-d141-p4-admission/test-run` — PASS.
- `git diff --check HEAD^ HEAD` — PASS.
- `git status --short --branch` — clean; no source or product edits from review.
- `git diff-tree --no-commit-id --name-status -r HEAD` — exactly the three candidate kit files: `admission-controls.sh`, `source-manifest.json`, and `test-run`.

## Identity and scope

- Candidate `test-run`: SHA-256 `8aa75771f6d3b3e7b65570580131a4866f3e65440d9d815a717c1189e323f5ce`, 15,113 bytes, mode `0755`.
- Live canonical preimage: SHA-256 `0be17b74ad1e324bc84e50e61e50e3e07390b262b7abe17a37ad22b9bd10d0fe`, 14,962 bytes, mode `0755`.
- Candidate and canonical realpaths are distinct and `os.path.samefile` is false.
- The candidate parent is `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`; its tree is `5ab5191a296980a0a6bcd1178ab6902d6478a148`, matching the manifest.
- Full unified comparison contains only the exact named-suite heavy classification, named 4.7 GB floor, and the associated admission message/predicate update. No general bypass, environment override, row rename, or unrelated byte change is present.

## Offline controls

Command:

```text
TMPBASE=/tmp/w-ae8a21dde3/ops-d141c-review0139 ops-d141-p4-admission/admission-controls.sh ops-d141-p4-admission/test-run review0139
```

Result: PASS. All 12 requested cases returned their expected status and launch count. The control output reported `central_body_invoked=false`; only private ORCH, disk, and `setsid` stubs were used. No central queue, suite registration, service request, product body, or live installation was touched.

The 12 cases cover named P4 floor/below-floor, light floor, default-heavy equality/above-floor, core floor/below-floor, global guard, invalid disk, unreadable disk, and both reciprocal heavy-busy directions.

Product typecheck/lint/pytest: N/A; no product code delta.
