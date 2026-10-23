# OPS-bench-store core test correction 1928

Source/private evidence only. **COMBINED FAIL / UNQUALIFIED / NO INSTALL** remains.
Independent core1923 SOURCE PASS applies to the exact exported core SHA256
`88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3`.
Core bytes, creator API, caller/lease1918, C0v2 shapes and frozen34e are unchanged.
Runtime assigned/integration head remains clean `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

## Correction and bounded controls

Only the reclamation fixture changes behavior: its 64 KiB old payload has unique
fixture bytes, and the oracle searches the entire store for those bytes instead
of requiring an inode number never to be allocated again. It rejects both an old
payload left in place and one renamed into quarantine. Real unlink passes;
unrelated new metadata is permitted. No implementation monkeypatch is used by
the corrected fixture or oracle controls. Existing reserve/fault tests retain
their original test-only hooks.

All original assertions except global inode nonreuse remain, including actual
free-space increase of at least 32768 bytes observed in the build callback,
old entry path/env/suite absence, no pending eviction, failure preserving
eviction, retained second entry and unrelated registration bytes, and refusal
of retired suite lookup. Explicit old index-entry and owned-registration
absence checks are added before build. The remaining 17 fixtures are byte-exact
source matches, covering crash recovery and last-two-plus-leased retention.
`fixture.patch` exposes the complete fixture delta for independent no-weakening
review. This author result does not replace that review.

## Portable validation

All packet members have the unique `handoff-runtime-OPS-bench-store-core-test-sol-1928-`
prefix. Frozen inputs are copied under `input-<original filename>`; their
original expected hashes remain in `input-hashes.json`. Original 1858/1915 and
caller/lease1918 files are never overwritten. The standalone validator checks
these copies, exact core identity, protected lifecycle methods, every retained
original assertion, fixture count, caller source wiring, scoped in-memory Python
compilation, shell syntax, clean Runtime baseline, and fresh TMPDIR patch replay
plus `cmp`. It checks the final packet manifest before and after validation.
There is no historical writer-worktree or preseeded replay-directory dependency.

Run from the current clean assigned Runtime worktree, using a private writable
TMPDIR. Explicit path flags are available for another assigned review worktree
and the read-only integration Runtime; absent paths, wrong heads and dirty trees
fail rather than being skipped:

```sh
D=/path/to/flat/packet
P=handoff-runtime-OPS-bench-store-core-test-sol-1928-
python3 -I -B "$D/${P}test-core.py"
python3 -I -B "$D/${P}test-oracle.py"
python3 -I -B "$D/${P}validate.py" --runtime "$PWD" --integration-runtime /home/user/work/runtime
(cd "$D" && sha256sum -c "${P}hashmanifest.sha256")
git status --porcelain
git diff --check
```

The corrected core suite passes all 18 tests. Oracle controls pass retained,
renamed, deleted and new-metadata cases. Final validator/integrity command
results and exact author paths are recorded in the worker report/logs.
Unchanged projection15 and lease24 suites are not repeated: projection1915 and
independent1923 evidence remains scoped to the same exact core identity.

## Remaining RED and next step

Readonly child publication/rollback EACCES and permission stop1905 remain
unresolved. No combined child creation, Store.ensure actualchild, readonly
publication/deletion, HOST/testservice, chmod, denied-path retry, alternative
cleanup/publication, live kit/config/queue/bench/install/provision/network or
Runtime product/test/generated/pin change is authorized or attempted. No full
suite requested. Independent Luna must review the single expectation correction
and standalone validator next. This packet supplies no combined qualification.
