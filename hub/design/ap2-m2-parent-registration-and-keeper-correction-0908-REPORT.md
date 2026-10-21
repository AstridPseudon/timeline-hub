# Parent registration and keeper correction 0908

## Result

The 0900 submission stopped before execution because it registered the 0855
gate digest as a manually truncated 62-character value. The actual 0855 gate
digest was `45b10f9bbae7d33030be1166d7447090d6a9fc98e9b08c041d13b69a022bd1`
(64 lowercase hex characters). No product test ran in that submission.

This task copied the existing 0855 gate into the durable worker record and
changed only these three assignments:

- protected keeper: `/home/user/work/wt/app-pin-8eb4d08e`;
- KEEP predicate: `.../workers/app-pin-8eb4d08e/KEEP`;
- fresh `EVIDENCE_ROOT` under this worker's `record/` directory.

The exact detached checkout is present and unchanged:

- path: `/home/user/work/wt/app-pin-8eb4d08e`;
- HEAD: `8eb4d08e60f434b938ea885c8cadca4bd87151b3`;
- tree: `ea317333400d1a342f2520556eef8ce9399666c1`;
- Git status: clean;
- active marker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-pin-8eb4d08e/KEEP`.

The checkout is not ready for the gate: it has no
`/home/user/work/wt/app-pin-8eb4d08e/node_modules` symlink. I did not alter
that source, install dependencies, create an ephemeral copy, or submit a
test-service request. This is the exact remaining prerequisite.

## Computed artifact identities

All digests below were computed directly by
[`generate-registration.sh`](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/generate-registration.sh>),
validated as lowercase 64-hex values, and inserted into the generated command.

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| corrected gate | [`final-keeper-gate.sh`](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/final-keeper-gate.sh>) | `81676d3b04606ad0a9276008db2173cf636fce18c8aab77dd7e718e5d490fb55` |
| existing helper | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh` | `96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109` |
| existing driver | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/run-parent-manual-drop-evidence.sh` | `34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2` |
| existing source runner | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-parent-media-central.sh` | `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd` |

The machine-readable manifest is
[`artifact-manifest.json`](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/artifact-manifest.json>).
The minimal reverse diff is retained in
[`gate-custody-diff.patch`](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/gate-custody-diff.patch>);
the proof records three hunks and six changed lines (three removed and three
added), with no helper, driver, source, product, spec, or pin-version change.

## Old 31285 packet preservation

The retained packet at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-central-keeper-command-preflight-0508/evidence-final95-parent-a304-central/run`
was not overwritten. Its before/after hash lists compare byte-for-byte:
[`old-31285-packet-hashes-before.tsv`](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/old-31285-packet-hashes-before.tsv>)
and
[`old-31285-packet-hashes-after.tsv`](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/old-31285-packet-hashes-after.tsv>).

The eight retained file hashes are:

```text
bounded-browser-evidence.json  8d30ef1faa4552571f50c9ebe9b8764b67de371be1102b2747241ea5655bf6cb
error-context.md               293c424c3149a83655f5f838e2acf8ae8edff75a987614cdf1f20dd07aee705c
evidence-presence.json         0ab19165d6ac03ac502930a7e33b5f6cfda679e7b450e33b0f75b477b689374b
playwright-trace.zip           09d290be3f5d929a76d785f24c959dd47555cc076767553a5159a39cfabfcf99
result.txt                     6afccb5b43a157a7f5bc8cdb2dce50e3f6c196db3420f6082169f13ce1775ae9
retention.log                  c5410c8014ec39b4476d5918a05d6f147fda9a0cba263817dfc21553ab8f6149
runner-tail.log                6c55ae0c2e82dfb65835d896089f4cb2b1aeb64192dd0f53e04a0c28cedb6b4d
source-identity.txt            ceadc2fce3d7f05d3d9dfa783bc3ebfbc9f14102cfe980dbf58a0b2127acd816
```

## Controls and generated command

The generator passed these local controls:

- 62-character wrong-length digest: refused;
- valid lowercase 64-hex digest: accepted;
- wrong source tree: refused;
- wrong pin tree: refused;
- missing/wrong KEEP marker: refused;
- stored command contains the exact computed gate/helper/driver bytes: passed;
- old 31285 packet hashes before/after: unchanged;
- existing driver launch-only probe: passed, including its zero-test refusal
  control and evidence-before-cleanup control.

The generated later-actual command is retained in
[`registration-command.txt`](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/registration-command.txt>):

```text
app ap2-m2-parent-registration-and-keeper-correction-0908-actual test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/final-keeper-gate.sh' | cut -d' ' -f1)" = '81676d3b04606ad0a9276008db2173cf636fce18c8aab77dd7e718e5d490fb55' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh' | cut -d' ' -f1)" = '96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109' && test "$(sha256sum -- '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/run-parent-manual-drop-evidence.sh' | cut -d' ' -f1)" = '34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2' && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-registration-and-keeper-correction-0908/record/final-keeper-gate.sh' run
```

It was syntax-checked but not registered or submitted. No product success is
claimed; no actual, browser, build, daemon, socket, install, full suite, or
service run occurred.

## Commands run

- `sh -n record/generate-registration.sh` — passed.
- `sh -n record/final-keeper-gate.sh` — passed.
- `record/generate-registration.sh` — passed all controls and regenerated the
  manifest/command from direct file hashes.
- `sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-projection-final-owned-binding-0855/run-parent-manual-drop-evidence.sh probe` — passed the existing
  launch-only seam controls.
- `git -C /home/user/work/wt/app-pin-8eb4d08e rev-parse HEAD`,
  `git -C ... rev-parse HEAD^{tree}`, and clean-status check — exact identity,
  clean status; readiness stopped only on the missing `node_modules` symlink.

No App source files changed; the assigned worktree remains clean.
