# Runtime ledger evidence-format correction

Updated only `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.runtime.md`.

## What changed

- Recovered the exact eight-column Runtime-owned rows from the backed-up combined ledger, selecting all 14 rows whose owner value starts with `runtime`. This includes `runtime + agent` rows and excludes rows whose first owner is `agent`.
- Preserved all row IDs and unchanged evidence; restored the owner column and rows missing from the compressed copy (`D13`, `RT07`, `WC10`).
- Corrected only the requested areas:
  - `RK02`: promotion merged at `81f8c7e`, text/replay resolution merged through `9f211fc`, with the original two promotion and four text-binding tests named.
  - `RT02`: catalog/text positives do not complete all FILM writer positives; remaining retired endpoint and native consumer gates remain open.
  - `D13`: records the actual `16608` and `16434` source/result environments and keeps the seven visual-seam failures unclassified.
  - `RT08`: marks the private `7b` carrier/current composition as internal and not public adoption.
  - `D04`: records the `6ab324` current integration and APPROVED clip-parity evidence while retaining the current public-013 parent-operation strict xfail and both consumer migration holds.
  - `D11`: retains the actual Agent `130b4937` architecture replacement and zero-reference check.

## Backups

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-ledger-evidence-format-fix/deletion-ledger.runtime.md.before`
  - SHA-256: `32f8a07f283df584c0c3c6401345539e4cd95fe9714df8be2f3d2dea5e958112`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-ledger-evidence-format-fix/deletion-ledger.md.before`
  - SHA-256: `24cb151b7c2c812b40293f72d3f0e7089d1b6d885ebe608e8cd4a0cdff3910a0`

## Checks

- Structural awk check: **PASS** — 14 rows; every data row has 8 columns; every owner starts with `runtime`.
- Required named-test check: **PASS** — both promotion tests, all four text-binding tests, and D04 refusal tests remain present.
- Stale-marker check: **PASS** — no mixed-owner-first, compressed, proposed/unmerged, text-in-flight, or pending-full markers.
- Product worktree `git status --short`: **clean**.
- No Runtime tests or central test requests were run, per task instructions.

