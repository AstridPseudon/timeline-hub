# AP2 M2 ordinary absolute clip-move member

## Result

App adds only `src/tools/video-editor/commands/ordinaryMoveMember.ts` and its
focused test. The member accepts the closed native patch shape
`{ op: 'clip.move', target, payload: { at } }`, where `at` is a finite,
non-negative absolute timeline value. Optional finite `order` is retained on
the operation for the enclosing batch; it is not turned into a new SDK unit.
`track`, `before`, `after`, and all other payload fields refuse before capture.

The member takes an explicit raw SDK `select`; it does not infer ownership or
rewrite a display ID. It delegates capture, finish, execution, quantization,
source/track checks, relation clearing, and full record production to the
existing `captureClipMove`, `finishClipMove`, and `executeClipMove` helpers.
The frozen basis carries the original operation and native move basis, so a
finish or retry never refreshes the document or clamps invalid input.

## Flat integration hunk proposal

The later atomic generic-batch owner should import the three member functions
and, after whole-patch classification and explicit target resolution:

1. capture each supported move with the current raw authored bundle and its
   resolved `select`;
2. finish it against that captured basis using `payload.at`, assigning the
   batch ordinal after the existing ordered operation list is established;
3. append the returned `command`, `record`, and `bundle` to the same sequential
   command/record accumulator used by hold and label members; and
4. build the local `clip.move` preview from `result.operation.target` and
   `result.previewAt` without using the generic compiler's projected document
   as the durable authored state.

`executeOrdinaryMoveMember` is the retry/replay verifier for the same command
and ordinal. No generic capture, session, outbox, compiler, or shared-core file
is changed by this member.

## Evidence

- TS focused member plus existing move/generic/label neighbors: 4 files,
  162 tests passed.
- TS ESLint for both changed files: passed.
- Project `tsc --noEmit --pretty false`: passed.
- A real TS-produced command/record/bundle was piped into Agent's
  `execute`, `replay`, guarded inverse, and redo paths: all exact assertions
  passed.
- Agent move + parent-label conformance: 147 passed; Agent hold/scalar plus
  parent-label conformance: 117 passed.

No browser, full suite, socket, Runtime-door, dependency, generated, or shared
worktree change is claimed.
