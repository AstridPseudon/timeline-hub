# D09 label handoff — owner-ready d93, terminal native result

## Decision

**APPROVE exactly the d93 owner-ready label/source scope.** d93 is not
integrated: at the final check, `git merge-base --is-ancestor d93b4ff6a
tl/integration` returned exit 1; `tl/integration` was
`f133a87986d839d7716d3efac2c2ba25fe036098`. The current owner head was
`30fc8dd154015a7c58cf4ce7b065ccc46f470ee8`.

The owner-ready Agent SHA is
`d93b4ff6a99b0a421ecad47131467754deff3445`, based on
`634867fed71b4ae53acaa3c3162315527c2bdb23`. Its six-file delta is:

```text
astrid/packs/rendering/actions/timeline_visualize/provenance.py
tests/packs/rendering/test_fast_lane.py
tests/packs/rendering/test_live_source_label_native.py
tests/packs/rendering/test_scene_source_carry.py
tests/packs/rendering/test_timeline_filmstrip_cards.py
tests/packs/rendering/test_timeline_filmstrip_execution.py
```

## Terminal central evidence

The old request `1020155244-1525` remains recorded as a pre-pytest clean-helper
failure (`runtime/astrid` was absent). It was not relabeled or replaced.

The repaired, named central request
`1020160329-27058` (`integration-viewing-live-source-label-native-clean`)
passed **18 tests in 95.40s**. The wrapper changed setup only: it stripped
ambient Python/Node/Git loader variables, set explicit Agent and Runtime source
roots, and rebound the private `runtime/astrid` leaf to the central Agent
snapshot.

The exact recorded import origins were:

```text
astrid:
/home/user/work/wt/.test-vw-m3-d93-central-env-runtime-fix-integration-viewing-live-source-label-native-clean-1020160329-27058/astrid/__init__.py
astrid_runtime:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d93-central-env-runtime-fix/stage-20261020/runtime-source/astrid_runtime/__init__.py
runtime_protocol:
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d93-central-env-runtime-fix/stage-20261020/runtime-source/runtime_protocol/__init__.py
```

The physical tuple was preserved across the private setup and central run:
owned Node SHA256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`,
Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, clean f816 peer graph,
and Composition public12 archive SHA256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` with 77
files. The shared f816 worktree was clean at inspection; no shared dependency
or cache was changed. The private stage was cleaned after qualification, so
the recorded manifests/log are the evidence of the physical pre/post tuple,
not a claim that the temporary stage still exists.

## What the 18 cases prove

- Saved input reaches the admitted source and is labeled committed with actual
  R1.
- A real unsaved candidate reaches the same source path, retains candidate
  status with base R1 and no actual revision, and is carried into Root props.
- Retaining R1 while the accepted head advances to R2 does not relabel the
  retained source; the head remains R2 and R2 does not appear in its label.
- Forged config, registry, expansion, and media mutations are rejected before
  writes; SQL, CAS, and staging bytes remain unchanged.
- The path is not all-mocked: `CaptureRuntime.materialize()` calls the
  production `GenericPackHost._materialize_inputs`; the test then calls the
  production `_prepared_remotion_root`, validates materialized assets/theme,
  and queries `scene_answers.host_frames_at` from the resulting Root props.
- Metadata-only/CAS/unclaimed inputs remain `UNCERTIFIED` with
  `actual_revision_id: None`; a candidate may retain its honest R1 hint.

The adjacent source-carry assertions passed **3 in 3.57s**. The prior owner
handoff's non-native neighbors remain **118 passed, 37 deselected**.

## Explicit limits

**REJECT** these broader claims: d93 owner integration, a fresh exported-PNG
certification, a whole-D09 deletion, or any new product/dependency change.
The `VW-LABEL` rows remain in progress; metadata-only replacement remains
honestly uncertified. No browser, fresh PNG export, full suite, or rerun was
performed for this terminal worker.

Machine-readable origin/package records and the exact command transcript are
flat-copied beside this report as `*-preflight.json`, `*-postflight.json`, and
`*-COMMAND.md`.
