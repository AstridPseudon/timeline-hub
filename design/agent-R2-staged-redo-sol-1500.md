# R2 staged redo source repair 1500

Ownership: `inverse.py:apply_inverse`, `_step_undo.py:inverse_stages`, and
`_commit_patch.py` inverse projection only. No Runtime, compiler, R1, commit
service, carrier, schema, dependency, publisher or client changes.

Proposed existing metadata seam: retain the accepted inverse command's
`inverse.stage` bindings (`publication_id`, `step_id`, `command_ordinals`,
`native_write_range`, `effect_range`) when reversing its native writes. Each
range must remain authenticated against the actual accepted source command;
the generated command still targets its real immediate source publication.
The original fork-edit-0 / fork-edit-1 split must survive this operation without
inventing source history or changing an accepted record. Verify representability
against pinned Runtime cfa0 before any live public body.

Retained source-complete packet SHA-256:
`b54d2efee42e093485e7ad6a4c73e7fca2c8318ad0b02cdbcde9330c3750eff3`.
The initial occurrence alias mismatch and the subsequent root/leaf stage
continuity failure are both required acceptance boundaries. Runtime1442 is a
distinct observation; this task does not depend on it.

## Disposition: BLOCKED, no qualified product repair

The bounded source attempt split a selected accepted inverse command at its
existing native/effect ranges in `inverse_stages`. It preserved the original
accepted command objects and the authored reverse order: create selected-shot,
attach the occurrence, remove params.text. Its two groups retained the actual
immediate publication and step identity (`undo-0`); no history was invented.
The 1436 experimental alias projection was included only in this experimental
candidate, not claimed to establish the full occurrence/allocation proof.

The exact retained strict-positive probe was run once after this source change.
It failed before acceptance: compiling the first intermediate selected-shot
image (`params.text=hello`) trips the unchanged competing-selected-media guard.
The current inverse baseline recovery accepts complete publication boundaries;
the intermediate image appears in accepted step effects, not as one of the two
publication documents loaded for undo-0. No synthetic source document, copied
root, private carrier, substituted prepared bytes or compiler exception was used.
Neither alias acceptance nor complete stage continuity is qualified GREEN.

Separately, a direct diagnostic using the exact accepted undo history established
the representation barrier in pinned Runtime cfa0:

1. `_inverse_stage_history` derives exactly one expected stage, undo-0, with
   three native sites. It does not descend into that command's two authenticated
   inverse.stage bindings.
2. Retaining both ranges under the immediate undo-0 identity is rejected by
   `_inverse_stage_ranges` at its stage-count check. Retaining the original
   fork-edit-0 / fork-edit-1 identities is rejected at the same check.
3. C0 §1 makes all changes of one command share one public step. Splitting the
   accepted single command into two public steps would invent history; splitting
   the submitted command would change the full original request.
4. A single outward stage has the previously established intermediate-root /
   final-leaf mismatch. Canonical effect projection is not a lossless escape:
   Runtime additionally fixes native-range length to the three source sites,
   while the collapsed closure transition has four canonical effects. Coalescing
   actual captures into fabricated no-op leaf captures or replacing the root is
   outside this task's source-fidelity constraints.

The diagnostic tests establish these source facts only. They are outside product
suites and are not reported as positive redo acceptance or the requested full
negative matrix. Their first run used the wrong exception class (2 failed,
6 passed); correcting only that diagnostic harness produced 8 passed. The
positive canonical-restoration/retry expectations were never weakened.

Contract question for the orchestrator: **What existing C0 representation may
retain both inherited authenticated source ranges under the unchanged immediate
undo-0 publication/command, when pinned Runtime requires exactly one stage for
that public step?** If recursive interpretation of the existing metadata is
intended, its authentication semantics must be settled at that boundary before
another Agent-only candidate can claim acceptance. This report does not change
Runtime or infer permission to relax any guard.

The unqualified candidate was retained outside the product and then removed.
`git diff --exit-code 80523b472 -- astrid` passes. There are no product or test
changes. Only the predecessor's three report artifacts were removed, after
copying exact bytes into this worker's durable evidence; the predecessor packet
and all its source facts remain embedded unchanged in the new packet.

## Verification

- Retained targeted controls: 14 passed in 3.69s.
- Candidate-only nested metadata facts: 8 passed in 0.32s.
- Candidate exact strict positive: 1 failed in 2.29s, intermediate compiler
  media guard; no receipt or public redo/retry was reached.
- Ruff: 2149/2149; private-cache mypy: 1912/1912. Product source is byte-identical
  to the prior baseline, so there are zero added diagnostic identities.
- Vendor lock, artifact manifest, source equality and diff whitespace: passed.
- Retained fixture SQL after the failed candidate differs only in the one
  runtime_lifecycle INSERT updated by RuntimeService startup; the other 149
  dump lines are exact. The probe did not capture a post-admission SQL baseline,
  so this is not claimed as a complete post-admission SQL no-write proof.

No full suite, public journey, browser, HTTP, daemon, provisioning, dependency
mutation, Git write or tool/classifier denial occurred. The complete requested
negative matrix and public receipt/history/idempotency qualification remain
unverified. G5/P1 remains gated. Do not merge a product repair from this task.

Detailed exact commands/results: worker `report.md`. Durable flat packet:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-staged-redo-sol-1500/agent-R2-staged-redo-1500-3a718d9537faec49.json`
(4,790,931 bytes), SHA-256
`3a718d9537faec492723efcd0b49a86675054ae03cfa580361058c58ba780c09`.
Its manifest and candidate source/diff, original fixture, complete predecessor
packet, diagnostic code, logs, C0 text and actual module origins are retained
beside it. Runtime pin remains cfa0af0d476e6954df041c08d7ef378fd6782932.
