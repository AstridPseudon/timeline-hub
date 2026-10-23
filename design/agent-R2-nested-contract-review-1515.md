# R2 nested contract review 1515

Disposition: **BLOCKED; no qualified product fix and no merge recommendation.**

This is an independent diagnostic review of `tl/agt-R2-staged-redo-sol-1500`.
The worktree retains no Agent product or test repair. The branch only carries
the predecessor-report replacement already present at this review's base.

## Evidence identity

The complete source packet was read without overwrite:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-staged-redo-sol-1500/agent-R2-staged-redo-1500-3a718d9537faec49.json`

- bytes: 4,790,931
- SHA-256: `3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09`
- predecessor packet SHA-256: `b54d2efee42e093485e7ad6a4c73e7fca2c8318ad0b02cdbcde9330c3750eff3`
- retained accepted fixture SHA-256: `9a47bb934b879efa0f6147d673038cee76299ba4e30ab22b6d5bcb1377ade589`
- minimum actual-facts digest: `sha256:0b1612ac82c8d02c4e0e3d99ac483a9ecd805b5aa87f8c12cfc5ef9469aaf899`

The packet contains the actual candidate source/diff, accepted writes and
effects, request/base, history, stage metadata, pinned Runtime source, C0 text,
strict probe, diagnostic probe, and predecessor packet. Its manifest records the
candidate hashes (`_commit_patch.py`, `_step_undo.py`, and `candidate.diff`);
the original complete captures remain at their original absolute paths.

Recorded source origins are Agent `bfab1f4caafec5b55dc95e407bfc92620e20daf7`,
Runtime `cfa0af0d476e6954df041c08d7ef378fd6782932`, and the packet's Runtime
pin is unchanged. Current Agent source files match the packet manifest exactly.

## Actual candidate and causal facts

The retained request is one normal inverse command, based at:

```text
publication: txn-75285c95600949c8b1267a71f8e71a9d
revision:    document-diff-e0c6162a4844471b99fd8d1076df92e9-parent-revision
command:     timeline.inverse(publications=[txn-75285c95600949c8b1267a71f8e71a9d])
source step: undo-0, command_ordinals=[0], effect count=9
```

The accepted inverse command has three native writes, in stored reverse order:

```text
occurrence:f2-occurrence/clip:f2-agent-clip  [params, text]
occurrence:f2-occurrence                     [shot_id]
shot:selected-shot                            []
```

Its authenticated source publication is `txn-7d039d147e1b4c5ba6cc7ca912b95cba`
with source steps `fork-edit-1` and `fork-edit-0`. The candidate's only source
change split those already-authenticated ranges while retaining the outward
immediate identity `txn-75285c... / undo-0`:

| candidate segment | native writes | effects |
| --- | --- | --- |
| first | `[1,3)` | `[0,5)` |
| second | `[0,1)` | `[5,9)` |

The candidate preserves the accepted command objects and reverse execution order:
create `shot:selected-shot`, attach the occurrence, then clear
`params.text`. It does not fabricate a source publication, ordinal, accepted
edge, root, allocation, or compact history. Its strict positive remains a
positive canonical-restoration/retry assertion; it was not rewritten to expect
refusal.

## Diagnostic fidelity versus behavior

**Diagnostic fidelity: PASS.** With the candidate files loaded in a private
package overlay, the exact source-contract diagnostic passed **8 tests**. It
verified exact source slices, reverse order, unchanged fixture bytes, two
candidate nested groups, and refusal of gap/overlap/foreign-publication range
mutations. The pinned Runtime diagnostic derived exactly one expected stage for
`undo-0` with three native sites and rejected both attempted two-stage
provenance encodings at the authenticated stage-count check.

**Behavioral acceptance: FAIL.** The exact candidate strict positive failed
**1 test in 2.93s**, before Runtime acceptance, with:

```text
shot 'selected-shot' has competing selected media between shot items and internal clips
```

Therefore this review does not claim a public receipt, accepted redo, exact
retry, or post-admission SQL no-write proof. The retained packet's earlier
pre-candidate probe separately reaches Runtime and reports the unchanged
`inverse stage write differs from its sequential input`; that is not conflated
with the candidate's earlier compiler failure.

The independent Runtime source trace is decisive for representation: current
`_inverse_stage_history` derives one expected stage from the public `undo-0`
step, and `_inverse_stage_ranges` requires `len(stages) == len(expected)` before
checking ranges and images. A candidate that exposes two nested stages cannot
pass that current guard. A collapsed one-stage effect projection also cannot be
declared equivalent from this evidence: the source has three native sites while
the captured closure transition has four canonical root/leaf effects, and the
strict root/leaf continuity guard remains active.

## Contract and ownership seam

C0 §1 states exactly:

> Each step contains a stable unique `id` ... `command_ordinals` ... and
> `patch` ... Steps partition the command array into nonempty contiguous runs in
> execution order. Each command belongs to exactly one step.
>
> All changes of a command share its step.

C0 §5 additionally requires:

> For a grouped inverse/redo, retain each reversed/replayed target-step boundary
> in the authenticated command recorder and associate its ordered effect range
> with that boundary.

This is an implementation seam conflict, not evidence that C0 should be
changed: C0 requires the target-step boundaries to remain authenticated, while
the current Runtime validator recognizes only the single outward inverse step.
No contract amendment is recommended merely because the candidate's two-stage
encoding fails.

The exact next seam is Runtime-owned unless Agent can prove a strictly
equivalent one-stage capture. Two concrete mechanical options are:

1. **Agent-owned one-stage representation:** emit one outward `inverse.stage`
   whose native/effect ranges cover the complete accepted command and whose
   authenticated metadata still retains the two original target-step boundaries
   without changing public request/history. This must pass the current Runtime
   sequential input, root/leaf, effect coverage, allocation, and future redo
   guards. The existing candidate does not do this, and no such candidate is
   qualified here.
2. **Runtime-owned private authentication sequence:** keep the normal public
   `timeline.inverse` redo body and one outer `undo-0` command/step, but teach
   Runtime authentication to recursively validate the two inherited source
   ranges against `txn-7d...`'s `fork-edit-1`/`fork-edit-0` records, with exact
   sequential segment images and effect ranges. The public body, schema,
   caller, guards, and history identities remain unchanged; only the private
   authenticated stage interpretation changes.

Until one option is implemented and independently accepted, Agent must not
retain an unqualified inverse source repair. G5/P1 remains gated. The production
caller remains the normal public redo path.

## Verification

- Candidate diagnostic with private overlay: **8 passed in 1.24s**.
- Candidate exact strict probe: **1 failed in 2.93s**, unchanged compiler media
  guard before Runtime acceptance.
- Retained unchanged controls:
  `pytest -q -o addopts= -p no:cacheprovider
  tests/editing_conformance/test_captured_redo_media_closure.py
  tests/editing_conformance/test_inverse_stage_images.py
  tests/sdk/test_timeline_inverse_binding.py` — **14 passed in 3.62s**.
- Ruff baseline comparison: **2149 current / 2149 baseline**.
- Prior packet mypy baseline comparison on byte-identical source:
  **1912 current / 1912 baseline**. The independent rerun was terminated after
  the comparison produced no completion output; no fresh mypy pass is claimed.
- Packet evidence: vendor lock, artifact manifest, whitespace diff, and source
  equality all passed. Current source-file hashes match the packet manifest.

No full suite, browser, HTTP/public journey, daemon, provisioning, dependency
mutation, Runtime repair, schema/pin/client change, Git write, or classifier/tool
denial occurred.
