Private OPS child custody candidate; actual layout UNVERIFIED.

The maker is preserved byte-for-byte from held WIP ad120ae33, SHA-256
0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39,
mode 0755. Its only difference from live maker 1243cb6c is to reuse the
existing authenticated archive installation route for unseeded builds too.
Both retained source snapshots therefore remain committed-only while pip
unpacks and builds the archives outside those snapshots. No verifier,
metadata whitelist, owner marker, Store, dependency helper or reserve changed.

Production chain: source_state -> STORE_PY.build -> STORE_BUILD source
archives and archive installations -> provenance/freeze/relocation ->
Store.ensure('child', ..., verify, seal=seal) -> unchanged STORE_VERIFY ->
registration. The diagnostic branch retains its existing --staging verifier
invocation, seals even on failure/cancellation, and never calls registration
or Store.ensure. The outer STORE_PY and STORE_VERIFY blocks are byte-identical
to their live preimages. Source manifest binds all three live sources,
candidate/test hashes, exact Git trees, archive hashes and file inventories.

Acceptance commands:

```sh
bash -n ops-child-custody/make-child-venv
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests
git diff --check
```

Results: shell syntax PASS; 29 unittest tests PASS; Ruff PASS; whitespace PASS.
The unittest suite compiles all seven embedded Python blocks in memory:
STORE_PY, STORE_VERIFY, STAGING_INVENTORY, RELOCATE, PROVENANCE_SCRIPT,
DIST_METADATA_SCRIPT and IDENTITY_SCRIPT. Python mypy/pyright comparison is
not applicable: this Composition repo has no configured Python baseline;
no product TypeScript changed.

The parent RED / candidate GREEN control executes the real source/install
shell branch, with exact-argument Git and installer doubles, then executes
the unmodified embedded verifier. Parent directory provenance and candidate
archive provenance match their actual branches. The installer double models
in-place build/lib and egg-info writes; it does not invoke pip or build real
packages. A bounded read-only census lists all 10 extra fixture paths,
including every extra directory ancestor and file; the candidate has zero.
These are fixture observations, not observations of the lost actual layout.

Controls retain every inherited WIP expectation and add missing-file, clean
exact source identity, foreign snapshot, editable provenance, committed
symlink, and source/carrier/metadata ancestor replacement challenges. Other
controls cover empty/generated/foreign paths at several depths, changed
source/archive bytes, direct_url location/hash, source markers, RECORD
hashes and additions, license bytes, foreign owners, hardlinks, writable
sealed trees, and the existing exact lib64 exception. Initial held-WIP
fixtures lacked an executable fake interpreter, one supported Git archive
argv, and two report identity fields; those fixture defects were repaired
without weakening assertions or changing production code.

The qualified D127a1535/1540 lifecycle predicates were rerun against the
candidate: success, verifier refusal, cancellation, seal refusal, unchanged
index/no final entries/no journal, all six publication/body barriers false,
normal Store.ensure dispatch, exact staging argv, malformed/unknown/duplicate
and missing options, and diagnostic reserve rejection before build. The
earlier review reports no retained authored test blobs; these current tests
exercise the real installed lifecycle functions. D131 is untouched:
normal child reserve 5905580032 bytes; runtime and diagnostic reserve
8589934592 bytes. No additional D131 reserve change was needed.

Read-only exact-source checks PASS: Agent a4e016b6 has 3565 files/694 archive
directories; Runtime 5e9ad1c6 has 535 files/33 archive directories. Every
archive directory is a committed-file ancestor; no symlink or unsupported
archive entry exists. The independent1637 generator diagnosis and historical
Farm refusals are preserved. No actual offending path is invented.

Actual Main diagnostic/build NOTRUN. At 16:48:06Z free space was
5221408768 bytes, below normal child reserve by 684171264 bytes and below
diagnostic reserve by 3368525824 bytes. Main's default
/home/user/work/bench-store is absent. Exact Agent and Runtime checkouts
are present and clean. Manager must provide authenticated Store custody and
disk/body admission before any diagnostic; no Store was initialized here.
The normal unseeded invocation also contains package installation stages;
the no-acquisition restriction remains binding and no alternative bootstrap,
wheelhouse, profile or venv was introduced.

No live build/registration/adoption/reuse/publication/READY action, package
acquisition, full/core/browser/P4/original body, hub write, Git mutation or
SWAP WAL/recovery action occurred. C0 sections 1-7 and all wire, authority,
privacy and no-write semantics remain unchanged.

Handoff: independent Luna custody review, then a separate exact installer.
Agent alone issues ONE new normal request after publication. Actual retained
layout census remains UNVERIFIED pending the authorized diagnostic inputs.
Per D30 this worker does not write design/ or report.md; the harness captures
the final report and the manager can publish safe flat evidence.
