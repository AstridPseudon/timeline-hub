# F D141z findings

## F1 — published originals received; mode custody note

The three genuine Main originals from the 0913 publication are present at the
named `design/runtime-D141z-final-dependency-0913-*` paths with exact expected
hashes and byte sizes: `run-final-services.py` 18,055 bytes,
`core-inventory.json` 25,664 bytes, and `delivery_gate_build.py` 14,909 bytes.
The first two observed modes are 0644 as recorded; the D68 wrapper is observed
0644 although the publication records original mode 0755. The hashes match and
the candidate invokes the wrapper through `sys.executable`, so this is a
publication mode-custody follow-up, not the stale missing-source blocker and
not a source-route failure. All three historical canonical App coordinates are
absent as expected venue state; no historical path was reconstructed.

## F2 — PASS: bound trace and terminal custody

`delivery_lifecycle.py` parses the seven-field binding, opens parents and the
trace with `O_NOFOLLOW`, checks device/inode/owner/mode/link count on every read,
and calls the donor append-final helper before terminal lifecycle output. The
acceptance uses the qualified donor sampler/append-final/validator hashes and
retains the pathname-replacement refusal. No permissive validator or native
primitive was replaced.

## F3 — PASS bounded source route; live admission unverified

The candidate has no private flock, private heavy marker, or second dispatch
gate. `install-map.json` records normal dispatcher ownership of one-heavy
admission, markers, lease, and the single 4,860,000,000-byte external floor.
The exact donor lease and body were run against a tiny private real Store
fixture, but live dispatcher admission was not invoked and receives no credit.

## F4 — PASS bounded route and guards

The unchanged `run-final-delivery.py` is byte-exact from 8e42. Its actual main
route checks the core runner, inventory, D68 wrapper, builder, tuple, gate,
ancestor, hash, scope, path, authorization and artifact guards, then calls
`run_wrapper` → `run_delivery` → D68 → harmless stub builder. Five poisoned
source/tuple/gate controls refused. This is bounded route evidence, not a real
delivery-build result.

## F5 — PASS source-faithful stop propagation

The exact qualified `suite_lease`/`supervise` source and existing shell body
were mounted unchanged. Controls covered real `D/CANCELLED`, lease retention
while a TERM-ignoring descendant lived, parent death, early leader with a live
descendant, `BENCH_CONTROL_FD` group advertisement, broken-reader EPIPE refusal,
normal writer EOF, and release only after TERM/KILL/wait/reap. The candidate
adds PDEATHSIG plus immediate/repeated parent checks and reaps D68 groups before
the donor five-second escalation. EOF after the donor advertises and closes its
writer is treated as normal registration completion, not cancellation.

## F6 — PASS scope

From 8e42 only `check.sh`, `delivery_lifecycle.py`, and `install-map.json`
differ. From 32bc the scope is those three plus the unchanged final caller and
the two authorized tracked CPython bytecode deletions. No new tracked cache or
product/test/generated/pin/wire file was introduced.

