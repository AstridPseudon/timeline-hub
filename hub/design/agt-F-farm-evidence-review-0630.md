# Evidence review report

Both packets PASS their review scope.

- Farm diff packet: PASS.
  - Source hashes matched all six manifests.
  - Historical basis: 172 closed / 95 open.
  - Official current census: 202 closed / 65 open.
  - Failed partition: 88 historical possible regressions + 8 newer closed + 185 unresolved = 281 unique failed lines.
  - Errored: 187 unique unresolved lines.
  - Summary gap preserved: 288 reported failures − 281 listed = 7 missing.
  - Confirmed non-environment failures: 0.
  - Farm PASS IDs: 0; JUnit and raw log unavailable, so no absence-based PASS credit.
  - Environment-only promotions: 0; no per-node causal proof.
  - Manager copies are byte-identical.

- Environment snapshot packet: PASS.
  - Current full-row hash: `3e3bfc3b...`; exact row verified against `suites.conf`.
  - Working row remains stale/unqualified at Runtime `3b926efa` / tree `b7941705`.
  - Safe projection contains only the requested six keys.
  - Node `v20.19.4`, profile `agent-remotion-v3-819acf-1110`, Composition archive `819acf6b...`, lock/profile hashes, and version `0.0.14` match retained receipts.
  - Runtime source `f3208b26` and owner-selected `1d9ddba` are distinguished; installed-child proof is separately identified as Agent `ba8f0bc8` + Runtime `f3208b26`.
  - No installation, source selection, working-row relabel, or full-green claim.

Contract scope was checked against PLAN §3, `commit-v2.md` §§1–5, and BOARD-HEADER. Neither packet claims full v2 wire-field acceptance or production-caller integration; no such credit is granted.

Checks run:

- Stdlib-only JSON/list/hash/partition verification: PASS.
- `python3 -m json.tool` on both packets: PASS.
- `git status --short`: clean.
- No product tests, static suites, probes, environment dumps, browser/gate runs, or reruns.

Unavailable primary proof: retained farm raw log and JUnit. Recommended next step is to preserve these packets as bounded evidence and require a fresh authorized run with complete rawlog/JUnit before assigning causes or PASS IDs.

Required `commit-msg` and `DONE` marker created.