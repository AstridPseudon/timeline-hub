# Runtime handoff: G5/R2r authentic historical SDK fixture

## Result

The historical fixture is now qualified as an authentic old-writer carrier.
The final archive is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/evidence/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz`

It is 26,543 bytes with SHA256
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`.
The archive contains the authenticated backup layout under `backup/` and is
below the 50 MB custody limit.

## Authoring authority

The old source was the exact object-store commit
`0ba9622a3e98a85577ef893be85988ba7f203b88`, tree
`c0bbd76656ac21439d11bf928eb970d60fe6e690`. Because its normal checkout was
pending, `git archive` was used read-only into the worker temp root; no Git
internals, refs, branches, or checkout were changed. The adapter asserted the
old `runtime_protocol.service.__file__` origin and compiled the old service,
backup, and pre-cut loader sources before opening a realm.

The existing pre-cut-v31 loader restored two disposable copies from the
committed pre-cut archive. The authoring copy was read by the old public
`RuntimeService` and `verify_baseline`. The exact four setup mutations were:

1. append `{id: music-other, kind: audio}` to `config.tracks`;
2. set the original `music-bed` clip app object to the packet’s complete
   legacy `word:word-1` declaration, including explicit nulls and opaque data;
3. append the packet’s `music-other` sibling clip with
   `extension.opaque == [null, {keep: true}]` and no app/volume/effects;
4. set `config.clips` to a deep copy of `clips`.

No child, registry, occurrence, media, source document, direct SQLite row, or
CAS body was authored. The old public service was called once with expected
head `film-parent-v1`, a UUID revision `a3e671256f1c42b8837d3e118c97b21b`,
and UUID idempotency key. No literal `m1-journey-baseline`, forced ID, current
retired route, provider acceptance, guard waiver, or direct writer was used.

## Qualified closure

- Parent content digest is exactly
  `sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`.
- Genuine publication receipt is
  `txn-11c90075be6c4c8bb9e2627366f0fe4f`.
- The retained predecessor is `film-parent-v1` with receipt
  `txn-55c0651b2cd64255ae06e73f9708220a`.
- The readback has exactly two publication entries, with the new entry’s
  `previous` pointing to that predecessor.
- The three shot and three internal-timeline content digests are the packet’s
  required values: `b97de3b8`, `a59a980c`, `d621270c`, `1264224e`,
  `848e75df`, and `9fb7e21a` (full values are in the raw JSON).
- The dependency manifest retains all five required media identities and CAS
  bytes, including the music asset and transcript/reference media. Physical
  sharing and all source/occurrence pins remain unchanged.
- The packet’s absent-versus-null and opaque assertions were checked against
  the public service result and baseline readback.

The authenticated backup manifest has manifest SHA256
`c76824ce644868ee8878a25df1eae06754d79b1a83a6eeeb6fb8272344e9841f`, HMAC
`5885a742b9215a62018c5d1c195a181d49e26ce47b508fd41e240a62ba061f7b`, and CAS
manifest SHA256
`9964c3fb382ae717525039324e307b719627061156dce8a400663f2e365c80eb`.
The existing public fixture key was used; the key itself was not retained.

## Current-reader qualification

The final archive was independently verified and restored with current Runtime
commit `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b` from the assigned worktree.
Current `runtime_protocol.service.__file__` resolved inside that worktree.
Current `verify_baseline` read the restored duplicate and matched the old
readback’s complete canonical document, head pair, predecessor, receipt,
event witness, dependency manifest, child images, and parent digest. The
current final-artifact check log is retained beside the archive.

## Evidence files

The following are retained under the same absolute ORCH design evidence path:

- `g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz` — final archive.
- `g5-sdk-authentic-capture-20261023-b6069d1d-fullraw.json` — complete old and current raw readback, without media bodies or key material.
- `g5-sdk-authentic-capture-20261023-b6069d1d-backup-manifest.json` — detached authenticated backup manifest.
- `g5-sdk-authentic-capture-20261023-provenance.json` — source, publication, predecessor, receipt, and event witness.
- `g5-sdk-authentic-capture-20261023-restore.json` — old backup verification and current restore qualification.
- `g5-sdk-authentic-capture-20261023-adapter.py` — bounded capture adapter and source assertions.
- `g5-sdk-authentic-capture-20261023-final-artifact-check.log` — final archive current-reader check.
- `g5-sdk-authentic-capture-20261023-sha256sums-final.txt` — hashes of retained evidence.

## Evidence commands

- Old bounded capture with `/home/user/work/venv-runtime/bin/python -B` and
  `PYTHONPATH=<archived-old-source>:<archived-old-source>/packages/python:<archived-old-source>/tests` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-G5-authentic-capture-1632 /home/user/work/venv-runtime/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-0666d206e4/pytest-loader tests/test_precut_realm_fixture.py tests/test_timeline_commit_film_fixture.py` — **10 passed in 1.43s**.
- Current final archive check through current `verify_backup`, `restore_backup`,
  and `verify_baseline` — PASS.

## Handoff boundary

This is fixture authority only. No Agent four-body behavior test was run,
rewritten, skipped, or weakened. No full suite, browser/native lane, current
writer retry, SQL/store write, direct CAS write, provision/daemon operation,
network fetch, or permission/safety retry was performed. Independent archive
fidelity review is next; after that, the manager may run the original four
unchanged against this actual restored base/publication pair.
