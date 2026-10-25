# R2 bounded original validation

## Inputs and admission

The exact immutable inputs were clean before and after the body:

- Agent `d4ba991638f7d94e6b9f91f5a463cd3587af00eb`, tree `6abf383217363d08fe0cf00558b010f5a9dd506f`.
- Runtime `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- App `d4e5284dfcc20801977cef12253b12f9cc8798fd`, tree `5efca939546f30b039cb9cacba7a29d7db690f2a`, existing normal receipt `app-U4p-R2-normal-home-1624.json`.
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`.

Read-only admission before the body was 5,130,645,504 bytes free. The 5,000,000,000-byte light floor passed, the 4,600,000,000-byte source-only floor passed, and the 4,000,000,000-byte stop line was clear. No concurrent heavy body was observed. Postflight free space was 5,108,240,384 bytes and still passed the floor. No profile, registry, route, package, venv, fixture, source, guard, pin, or generated-file change was made.

## Source guards and origins

The exact occurrence test source hash is `f1d86c7a95140a3f69a60e3ac348511eedf2eca52d75da135eb04450f9935ca1`, matching the retained D124 guard. Its AST hash is `5e50f752afe0fb6b8edb34fd6f710ba51252dea38281c475df361fdea72b8d25`; the three guarded members and line spans are recorded in `source-map.json`. The retained no-legacy-writer/renderer guard and all original assertions and inputs remain unchanged.

Before and after origin checks resolved Agent modules from `/home/user/work/wt/agt-pin-d4ba9916` and Runtime modules from `/home/user/work/wt/rt-pin-ab1e4f61`; the full paths are recorded in `manifest.json`'s source tuple and `source-map.json`. Both immutable checkouts remained clean.

## Exact body

Command, run once from the Agent checkout:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-pin-d4ba9916:/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-R2-original-True-after-ab1e-1713/evidence/original.xml 'tests/editing_conformance/test_commit_runtime_occurrence_create.py::test_bootstrap_birth_child_media_exact_history_inverse_redo_retry[True]'
```

Result: exit 1, one test failed in 8.188 seconds. The exact retained failure occurs during `redo-birth` at the Runtime auth boundary: `provider occurrence alias is outside its boundary`. The outer original assertion is the unchanged `result.returncode == 0` at test line 70. Source attribution is `UNKNOWN`; no Agent or Runtime ownership is inferred from the trace.

`original.xml` is the durable JUnit output (16,823 bytes, SHA-256 `9464f762b8606e04a3680a42791f038c142ce1ab02e271ec78b93c8183f3bdfb`). No second body, native smoke, old control, full suite, P4, tour, collector, or alternate route was run.

The synthetic three-case receipt and source-only Agent diagnosis were not relabeled as this original closure. D130's SWAP/WAL safety hold was not read or retried; this occurrence inverse proof is unrelated.
