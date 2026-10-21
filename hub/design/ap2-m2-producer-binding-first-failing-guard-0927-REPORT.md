# AP2 M2 producer binding first failing guard — 0927

## Diagnosis

The first product guard that differs when the unchanged 0822 controls are run
against the final 0908 source is `SPEC_SHA` in
`producer-startup-custody-gate-0717-owned.sh` (the guard at line 85 of the
preserved old control):

```text
old0717: d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
final:   6666c0365d13f302725788e6fbfcce9e0fb283e4b30c40661886522a67f270e6
```

The final value is the SHA-256 of the final keeper's
`tests/e2e/local/producer-ownership-current-pin.spec.ts`. The old value is the
SHA-256 of the old0717 keeper's same file. The spec changed in the approved
0903 oracle correction (`transcript-lane-chip` ->
`transcript-lane-occurrence`, and authored `at` wire observation -> native
`on`), then in 0908 for the row-local zero-legacy observer/assertions. The next
guard, `HELPER_SHA`, also differs, but is not first:

```text
old0717: d86721bd680691e29e705900e03862497a7d97b069f2e43c6192d739cbc9e09b
final:   df1faac404b69efa8a5fb06297814e6ca3b5d52b4a5856633706c7ac2e3ae949
```

Therefore the old controls cannot be reused unchanged as a positive/final
chain against the final source. This is a pure source-binding refusal, not a
producer behavior failure. The first textual difference in
`minimal-reverse.diff` is the retention-helper path, but that is only a path
rebinding; it is not the first failing guard.

## Why attempt8 stopped

`controls-failed-attempt8/before` is the decisive preserved output. Its
translated command reaches the outer `sh` invocation, while its dispatch log
contains only that one shell event. The old custody script then refuses before
dispatching the physical gate because its stale `SPEC_SHA` is checked before
`HELPER_SHA`.

`outer-controls.py:120` unconditionally requires the first four nested shell
names for every control, including `control('before', OLD, 'failure')`. That
assertion is invalid for this deliberately stale-source negative control. The
recorded `stub-sh [...]` line is only the launch stub's diagnostic print; the
stub's `sh` branch execs `/bin/sh`. There is no evidence of a real producer,
Playwright, browser, socket, or child-harness failure. The harness failure is
the subsequent dispatch-order assertion:

```text
AssertionError: ['producer-startup-custody-gate-0717-owned.sh']
```

This conclusion uses the guard order in the preserved custody script and the
attempt8 dispatch/output, not the final traceback alone.

## Smallest correction recipe

1. Preserve the final 0917 chain and the 0908 source exactly. Do not change
   product source, the spec/helper, pins, schemas, or the retention helper.
2. Repair only the outer-control expectation: treat the `before` case as an
   expected early refusal with the single outer custody-shell dispatch; apply
   the four-shell dispatch-order assertion only to controls that are expected
   to pass custody and reach the child boundary.
3. Keep the final chain's source/hash bindings below. Do not make the old
   control pass by reverting the final spec/helper hashes. Do not authorize an
   actual until the repaired five-control preflight completes.

No unnecessary edit was found in the final chain's reverse diff: the retention
helper is byte-identical, and all other changes are required path, source
identity, or transitive hash rebinding to the final keeper. Any temporary
`stub-sh`/debug instrumentation is harness noise and should not be retained in
the repaired control implementation.

## Source and keeper identity

Final protected keeper:

```text
path: /home/user/work/wt/app-pin-09171792
HEAD: 09171792bd626f5eabd421d1f1c2b497a4fc9786
tree: 31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89
status: clean
wrapper SHA-256: 329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352
spec SHA-256: 6666c0365d13f302725788e6fbfcce9e0fb283e4b30c40661886522a67f270e6
helper SHA-256: df1faac404b69efa8a5fb06297814e6ca3b5d52b4a5856633706c7ac2e3ae949
node_modules: /home/user/work/app/node_modules (canonical symlink target)
```

Old0717 comparison keeper:

```text
path: /home/user/work/wt/ap2-m2-producer-helper-expect-import-0717
HEAD: 6b0267c62aa8773132f1496d5014279e6c1edf61
tree: c1ac3383624322ae8d67b10dee36965670d91cd7
status: clean
spec SHA-256: d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89
helper SHA-256: d86721bd680691e29e705900e03862497a7d97b069f2e43c6192d739cbc9e09b
```

Frozen cohort retained by the manifest: Agent `8130a401bf44a518d5a40ae274d398b8c560be55`
(tree `236c3e57e0265c52b81ba8085de3193026176bff`), Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a` (tree
`7ab412cc4bcbe517efcfa806e092336390312e18`), Composition `0.0.13`.
No current014 or future017 qualification is claimed.

## Exact final artifact hashes

From `manifest.json` / `artifacts.sha256`:

| Artifact | old0822 SHA-256 | final0917 SHA-256 |
|---|---|---|
| `producer-retain-failure-artifacts-0753.sh` | `dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75` | `dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75` |
| `producer-public13-runner-0717-owned.sh` | `d1a6616d477f6529de8c949286278fca906df44a1f5e9fe24b78e3ccb4cc4f10` | `af18eae504e27bfcf529202e5ea80edb2fc68f92025431f919c80ee150bccfdc` |
| `producer-runner-0717-owned.sh` | `0f57d4885999f265ee43a14acb14a9abe58014dc773edc9edb3423687f8add39` | `def88cbff626291b52ce7ab695366da131ea753824d940a9342f8a896cb38cd3` |
| `producer-physical-keeper-gate-0717-owned.sh` | `0f193b6c54bcb9f2333acfe7bd39c67c56b58ee60bce498212577b3e115cc499` | `8765c08e2f374b1d403e9a0cf2ee9519452862832a233ff6928da9812865690a` |
| `producer-startup-only-probe-0717-owned.mts` | `a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f` | `a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f` |
| `producer-startup-module-format-probe-0717-owned.mts` | `d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3` | `d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3` |
| `producer-startup-only-gate-0717-owned.sh` | `10abb0571dc927aa1945ec8f1ae4008bcf995b594225fbda1e96c3d67381010b` | `50ce59385a4d5f5f44802059998f4076dcff34750545e41956d98e4f453914` |
| `producer-startup-custody-gate-0717-owned.sh` | `b7c6f4806c02d8315b3eb69c4b4c469e7b908375603a5a0c967df5bbae60efb9` | `9ca0ee53322ad281417e77b8e87d5ec96d6dfb6cbfd38e8ddf6decd7cca513b5` |

Relevant preserved artifacts:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-oracles-traffic-binding-0917/manifest.json
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-oracles-traffic-binding-0917/minimal-reverse.diff
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-oracles-traffic-binding-0917/controls-failed-attempt8/before/output.txt
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-final-oracles-traffic-binding-0917/controls-failed-attempt8/before/dispatch.jsonl
```

## Verification boundary

No controls, actual, browser, build, daemon, socket, service, install, or full
suite was run by this diagnosis worker. Existing preserved evidence only was
read. The 0917 packet remains stopped at `STOPPED`; no qualification claim is
made.
