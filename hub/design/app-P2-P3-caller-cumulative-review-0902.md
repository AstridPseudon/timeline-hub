## PASS — PREPARED mechanical caller package

Reviewed `1d92503b4c` against `b5fc832b78`, PLAN §3 A2/A3/P2/P3, D21, `commit-v2.md`, author report, qualified design, and source-target-0644 report.

- Only permitted files differ: `caller-publication.py`, `caller-custody.json`.
- Re-executed stale-source witness: original logic fails on actual mounted `P2APP/P3APP=663…` rows.
- Current modeled preparation rebinds both rows, removes stale `663…/9a…`, and preserves 60 P2 + 106 P3 fingerprints.
- Exact 248 outsider rows preserved.
- Source custody accepts matching hashes and refuses changed source blobs.
- Auth controls refuse missing/mutated metadata, receipts, branches, source/tree/parent, dirty targets, and caller-artifact targets.
- C0 inventory includes scoped request fields, command/step fields, merge/read/idempotency fields, `{data,receipt}`, canonical document/digest/id map, authoritative commands/steps, accepted/merged/conflict/invalid/rebased, conflict `current`, and durable receipt fields.

Commands/results:

```text
python3 -m py_compile caller-publication.py                         PASS
python3 -m json.tool caller-custody.json >/dev/null                 PASS
bash -n on decoded P2/P3 inner and outer rows                       PASS
git diff --check HEAD                                                PASS
git diff --check b5fc832b78 1d92503b4c                              PASS
bounded modeled preparation/source/hash/auth controls               PASS
```

No browser, backend, HTTP, service, build, provision, endpoint, process-probe, suite installation, or full/original execution was performed.

Final source SHA/tree/parent, independent final-source review, authorized proof-worker receipt, and integrated P2/P3 execution remain pending. Therefore this is PREPARED only, not READY or run-authorized.