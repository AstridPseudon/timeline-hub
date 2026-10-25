# D33 Report — `rt-D86-17724-wholepath-0627`

Completed read-only whole-path audit for actual17724 opaque6/script4.

- Historical path traced: client → C0 request → Runtime `0c62dfa` → registered Agent provider → authoritative record checks.
- Source identities recorded for Agent `bde578`/current `8c88ea`, Runtime `0c62dfa`.
- All 10 cases remain `UNKNOWN_UNAPPLIED`; source alone cannot prove fixture, producer, or verifier fault.
- Exact missing inputs: historical per-command provider records, captured C0 bodies, Runtime rejection ordinal/ref, physical-promotion evidence, and pinned `inspect_timeline` response.
- D100 membership capability remains separate and held; it does not supply these missing records.
- Existing 0517/0518 fixes conserve claims and authenticated inputs but do not establish historical outcomes.
- Genuine passing comparators reviewed: numeric native move exact image/history/retry; video inverse and opaque registry/order round-trip.

Artifacts:

- [Audit report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D86-17724-wholepath-0627/evidence/README.md)
- [Per-case dispositions](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D86-17724-wholepath-0627/evidence/per-case.tsv)
- [Source audit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D86-17724-wholepath-0627/evidence/source-audit.tsv)

Checks:

- In-memory AST compile: PASS, current Agent 14 files and historical Runtime 5 files.
- Scoped Ruff `0.12.0 --no-cache`: PASS.
- `git diff --check`: PASS.
- No pytest, fixture, provider, Runtime body, HTTP, browser, collector, or full suite run.
- Worktree unchanged.
- Empty `DONE` marker created.
- Commit message written: `docs: record rt-D86-17724 whole-path source audit`.