# P3 fixed-checkout handoff

## Verdict

**Operational PASS; Gate 5 execution remains BLOCKED.**

The sole `app ap2-P3-gate5-h6-0348` row in `tests/suites.conf` now uses the
owned clean exact Agent checkout `/home/user/work/wt/agt-pin-f894c3c9` in both
`ASTRID_CHECKOUT` and `PYTHONPATH`. No other row or row field was changed.
Current row SHA-256 is
`9cdbe46e5862b4a9cd42222e1030d44e5af57b633ecb24ca05b477d91d634c25`.

Source preflight passed:

- Agent: `f894c3c9dda25ab03527eeb7f52da5da31d627c1`, clean, tree
  `d24f25a65be282a56b3fcd814a8718a3c0587b9b`.
- Runtime: `34eac0041b0891e9011966b39bcbd26053fde5bc`, clean, tree
  `9853574865f25e08284e82ffb26c0bdecaa16a30`.
- Both bundle SHA values match these exact heads.
- Both Python lookups pass and resolve to `/usr/bin/python3.12`.

The durable 0407 graph remains live and exact by its retained manifest: 80
Composition files, 73,451-byte archive, SHA-256
`819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, official
Node exports to `dist/*`, and no synthetic root entries. The historical source
archive itself is absent, so this return relies on the recorded byte-identical
manifest plus live graph/export checks.

The original selector collected exactly one test with `--list`. No browser,
service, build, body, socket, or full-suite run occurred; no journey credit is
claimed. The App Vite public-export resolver issue and P3 Sol strong-assertion
follow-up remain execution blockers. `19140` and `29980` remain setup failures,
not acceptance.

The full request contract remains preserved for the future actual caller:
scope/base pair, commands, label, per-step patches and reads, merge mode,
optional reads, `dry_run`, idempotency key, complete canonical accepted/merged
receipt/steps/dependencies/history, and conflict/invalid/preview replies.

Next step is App-owned resolver correction, followed by one central exact-case
Gate-5 execution.
