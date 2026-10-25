Private OPS child inventory contract candidate — SOURCE CHECKS PASS; WHOLE-MAKE E2E BLOCKED.

Base: 9428f515fcd8dccaef26193438b3ac89f903f5aa. Exact installed parent is
0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39,
68351 bytes, mode0755. Protected live bench_store123bb and dependency116b
hashes and all 29 inherited test/source controls remain unchanged. The candidate
retains the previous archive installation fix and all diagnostic lifecycle fixes.

The complete pre-edit audit is evidence/audit-all-checks.json (20 conditions and
prerequisites, original source line1142 through verifier end). Source line1154
through end includes source-file ancestry, exact markers, metadata row order,
all source metadata fields, six report header values, section boundaries and
provenance bytes, installed distribution enumeration, local/direct and dependency
row rendering, canonical tuple sort/duplicates, complete text equality, file size,
file executable mode and returned inventory. Missing/malformed/unreadable data
remain failures. The audit binds the exact installed source hash above.

Fault proved by source and real pip freeze: pip freeze has a different contract
from the verifier. It uses direct references for dependencies carrying direct_url,
sorts raw names and deduplicates canonical names. The verifier requires every
installed distribution, canonical tuple ordering, exact raw dependency Name and
Version, and local source references from authenticated installed provenance.
The new producer uses ONE explicit installed-site distribution inventory for
both report sections. It retains strict local Name/Version matching, copies
source URLs/hashes from validated installed direct_url, preserves dependency
names and duplicate rows, bounds output to1MiB, and writes maker files0600.
No report content grants ownership. STORE_VERIFY and STORE_PY are byte-exact.
Relocation, archive authentication, RECORD hashes, registration and all reserves
remain unchanged. No product/schema/generated/pin/C0 wire edit was made. D130
SWAP/WAL is untouched.

Farm's supplied log proves report equality failed after readonly-source. It does
not expose the report or installed inventory. The EXACT differing production
rows remain EXACTMISSING; no dependency/path is invented as the actual culprit.
evidence/requested-census.md specifies the minimal safe in-place Farm census.

Exact acceptance commands (from this worktree):

```sh
bash -n ops-child-custody/make-child-venv
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests
git diff --check
```

Results: shell syntax exit0; unittest40/40 PASS in4.124s (all inherited29 plus
11 added controls), Ruff exit0, whitespace exit0. The suite compiles all seven
embedded Python blocks in memory; an independent compile() check also passed
for those seven and all four test Python files. Explicit compile() checks ran
in memory; acceptance used PYTHONDONTWRITEBYTECODE=1 and Ruff --no-cache.
Durable unittest output: evidence/unittest.log. A new exact-shell-stage test first
failed because its fixture omitted TIMEOUT_BIN; adding the real timeout command
to that fixture fixed it without changing any producer/verifier expectation.

New controls cover real pip freeze RED versus installed-inventory producer GREEN
on a synthetic installed layout; exact shell invocation/0600 output; optional
Farm schema order; both source kinds; every header/section/origin/metadata/freeze
row mutation and newline/order; dependency duplicates; strict local Name identity;
installed inventory scope; executable metadata; and producer size cap. These
controls execute the actual unchanged verifier with exact-argument Git archive
doubles. They are NOT real whole-make end-to-end evidence. The ten-path model and
all inherited controls likewise receive no genuine E2E credit.

Prepared genuine E2E: tests/e2e_inventory.py. fixture_sources() defines exact tiny
Agent/Runtime packages, canonical-client bytes, actual Runtime CLI entry points,
and two private dependencies whose raw punctuation ordering differs from the
canonical inventory order. The input writer ran successfully, creating only
small source files in TMPDIR; it does not write Git or initialize a Store.
The runner requires manager-admitted preinitialized private fixture Stores,
clean exact committed tiny sources and already-available local no-index wheels.
It runs the whole parent0857 make to report refusal, the whole candidate make
through real installation/unchanged verifier/normal fixture Store registration,
then unchanged sealed verification and adversarial report/metadata/marker checks.
It never mocks a verifier/installer/Git command, initializes a Store, changes a
reserve or substitutes a venv/profile. Raw stderr/private bodies/URLs are not
persisted. This route is prepared, not qualified by execution.

Exact attempted E2E command:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python ops-child-custody/tests/e2e_inventory.py --venue-manifest "$TMPDIR/ops-child-inventory-venue.json" --result /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-inventory-contract-sol-1725/evidence/e2e-result.json
```

It exited2: EXACTMISSING
approved private fixture venue manifest, Store custody, committed tiny sources
and local wheels. evidence/e2e-result.json records whole_make_e2e=NOTRUN,
parent_red=false, candidate_green=false, adversarial_checks=0. No full make,
package installation, child request or body ran. Do not count this as E2E PASS.

Observed admission: 5027573760 bytes free versus unchanged normal child reserve
5905580032 and diagnostic reserve8589934592. Default /home/user/work/bench-store
is absent. No new bench, production Store, profile or replacement venv was
created. Ordinary-body floor5GB and stop4GB remain binding; source floor4.6GB,
cap3/no-heavy are unchanged. Type baseline N/A: Composition has no configured
Python mypy/pyright baseline; no product TypeScript changed. No full suite was
requested, and no localhost/browser/live-socket test ran.

Handoff: obtain the existing Farm retained-child safe census and an authorized
private fixture venue/local inputs with real unchanged admission; execute the
prepared genuine E2E. Independent source/security review follows, then a separate
exact installer only after manager acceptance. No Agent/Farm request is authorized
by this report; each issues ONE changed request only after installed receipts.
The candidate is not release-qualified while genuine E2E remains NOTRUN.

## D137 source-only update (2026-10-25)

The fixture E2E gate is withdrawn by owner authorization; its result remains
`NOTRUN`. No fixture body, Store, child request, acquisition, or install was
run here. The maker now hands each failed `run_stage` command's stderr to the
private maker-owned `tests/provision-stderr/<request>.<stage>.stderr` route
before Store cleanup. The payload is mode `0600`, single-link, bounded to 1 MiB
with truthful original-size, retained-size, truncation, and SHA-256 metadata.
The public failure marker and summary retain only stage, exit status, timing,
source identities, lock identity, and the fixed diagnostic string.

The final maker source in this worktree is 75,503 bytes, mode `0755`,
SHA-256 `f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`.
The reviewed embedded `STORE_PY` and `STORE_VERIFY` blocks remain byte-exact
at `0889b24010e67bd31f28f5efbaec37fed43adf1a0d5ebe8c4fcd57a8248ca50c` and
`f7c7ebcc26221958ce24e36025faad167c6015a2889202752d267e03d5eda209`.

The imported installer-prep route is based only on installer1826 source
`a3e707dbcb80a200dbb5d8f60a8f0d63fd807da4`. Its D137 gate accepts an exact
owner decision input binding the final 40-hex source commit, this maker hash
and 75,503-byte candidate, with `WITHDRAWN`/`NOTRUN` E2E and
`CAS_MANAGER_ONLY`; it does not fabricate E2E PASS. The route retains the
descriptor-bound lock, no-follow/no-clobber backup, target identity CAS,
atomic rename, protected-helper hashes, and source/RECORD checks. The actual
install remains UNVERIFIED and was not attempted.

Targeted evidence: bash syntax, 44 unittest controls, private CAS dry-run,
Ruff, Python compile, verifier-block comparison, and diff check all pass as
reported in the worker handoff. No full suite or live socket/browser run was
requested.
