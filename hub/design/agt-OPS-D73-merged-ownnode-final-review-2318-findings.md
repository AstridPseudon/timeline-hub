# D73 / D139 / D140 final source review

## Verdict: PASS

Both findings from review2307 are resolved in the return. The two real
`suites.conf` rows now run private `pre-dispatch.py` before the unchanged
mandatory pinned launcher. The guard rejects duplicate/malformed/missing
manifest input, current Agent/Runtime tuple mismatches, and runtime-lock
provenance/count/hash mismatches without touching the D66 output path.

The rendered-row controls independently exercised, for both selected4 and
fork1:

- valid run-mode admission: launcher stub exit 17, exactly one body call;
- wrong source, wrong lock, source-SHA poison, duplicate key, and malformed
  manifest: nonzero pre-admission refusal, zero new launcher calls, zero new
  preflight calls, and no output directory.

The exact row parser was used. Alternate suite spellings matched no row, and
the `*-nodes` request guard still requires `--files`. External D73 manifest,
request, evidence, and Agent-path environment values were supplied as hostile
overrides; the row's `env -i` assignments remained authoritative.

Protected launcher, selected4, fork1, focused launcher-control, and
`tests/helpers/runtime.py` bytes are exact versus Agent 2eca. Runtime lock
provenance is current Runtime f103 with all 15 canonical hashes matching.
Historical 2eca/ab1e evidence remains historical and was not retargeted.
Only `ops-d73-exact-nodes/` changed on the candidate branch.

## Separate receiving status: NOT_READY

Receiving is not qualified. The source census reports missing current Agent
and Runtime checkout receipts, a genuine rendered receipt-backed manifest,
App/Composition receipt-derived inputs, central row installation, fresh
per-ID results and disk witnesses, and real interpreter/import/preflight
evidence. No central request, install, product import, real preflight, product
body, service, browser/socket suite, Store, child/core, acquisition, or Git
write ran.

No unresolved source boundary remains. The next boundary is normal receiving
with the genuine finite inputs above; no historical receipt or result may be
reused.
