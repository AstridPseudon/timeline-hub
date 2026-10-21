# Parent ADD cut/cause 0236 report

## Outcome

No App product files were changed. No legacy ADD leaf was deleted because the
required full mounted ADD proof did not execute successfully. The worktree is
clean at `tl/ap2-m2-parent-final-case-cut-or-cause-0236`, HEAD
`743d3464d` (the current `tl/integration` base).

## Frozen source and review evidence

The final source packet was independently approved before the central request:

- App source commit `da6d910f7ab3dfc71142ece7f632d43341238882`;
- App source tree `6809757f93ca5e166b24b8bc0160ca09005e984a`;
- final parent selector in `normal014-source-common.sh` points to that commit/tree;
- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`;
- Runtime/producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
- approved helper hashes:
  - `normal014-source-common.sh`
    `3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014`;
  - `normal014-parent-media-central.sh`
    `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd`;
  - `normal014-app-central.sh`
    `8f70ed7adafa42d90b3053f5972bd763a653ae690c1b2dfda352e3704615686e`.

The custody review is recorded in
`ap2-m2-parent-final-frozen-code-custody-review-0236-REPORT.md` and approves
the exact committed source and helper packet. Its source-only preflight passed
with 76 artifacts, the expected manifest/schema, ancestry, clean-source and
identity-negative guards. It did not qualify the mounted gate.

## One central attempt and first failure packet

Submitted once, with no retry:

```text
R=$(request-test ap2-m2-parent-final-case-cut-or-cause-0236 \
  normal014-integration-parent-media-accepted)
wait-test "$R"
```

Result ID:
`ap2-m2-parent-final-case-cut-or-cause-0236-normal014-integration-parent-media-accepted-1021024051-16303`

Central result: **FAIL, exit 1, 2 seconds**. Snapshot App tree:
`82a556ccb651d4a4c5ab4f1380394d0670f16568`.

The first packet contains no test assertion or HTTP request: `log.txt` and
`runner.log` are both zero bytes, counts are blank, and the summary only says
the named command exited 1. The result metadata records external refs Agent
`04fdd64205b4a2365e50455bd3ac81b027c617f3`, Runtime
`9d1c43c647301da48a6e86ad82e466b501bd2418`, and Composition
`7bb54bbd64107e5090643ecca1e4d33164173e85`.

The request metadata records `nocache=0`; I did not pass the central
`request-test --no-cache` flag. The driver itself disables pytest's cache
provider, but this does not repair the request-level omission. Per the task
rule, I did not resubmit or retry.

There is an additional source/gate mismatch: the registered suite line in
`scratchpad/orch/tests/suites.conf` invokes
`normal014-parent-media-central.sh run`, whose committed `run` branch runs the
native parent **swap** pytest case. The approved packet names
`tests/e2e/local/support/run-parent-manual-drop-evidence.sh` as the existing
manual ADD driver, but that driver is not what the available suite registration
invoked. Because the central job failed before its empty log was populated, no
swap request was observed either; I did not call the forbidden HTTP swap case
or any old partial mounted proof.

Therefore this run provides no mounted ADD assertion, no actual ADD/recovery
packet, and no evidence for writer retirement.

## Live callers and deletion boundary

Current live native/ADD callers include:

- `src/tools/video-editor/hooks/useAssetManagement.ts:295` — prepared video
  placement calls `commands.addClip`;
- `src/tools/video-editor/hooks/useTimelineCommandsService.ts:458` — native
  prepared-media path verifies the selection and submits through
  `state.ops.parentClipAddMedia`;
- `src/tools/video-editor/commands/parentClipAddCapture.ts` — native
  `clip.add-media` capture/execution and retry basis;
- `src/tools/video-editor/commands/commitSession.ts` and
  `useTimelineCommandSession.ts` — shared native ADD session/port;
- `src/tools/video-editor/hooks/useAddVariantAsGeneration.ts:94` and
  `src/tools/video-editor/components/AstridTimelineEditor.tsx:587` — duplicate
  generation callers that must remain separate;
- `src/tools/video-editor/hooks/useTimelineState.ts:1060` — legacy
  `buildAddMediaCommand` producer remains present and is the smallest
  candidate legacy ADD leaf, with its direct command-surface/tests.

The qualified deletion boundary is **none**. If and only if the exact manual
ADD gate later passes, review the `useTimelineState.ts` legacy
`buildAddMediaCommand` leaf and direct neighbors as one bounded cut. Keep the
duplicate-generation callers, shared command/session writer, serializer, and
unadopted pin boundaries intact. No semantic, DTO, or executor change is
justified by this failed pre-execution packet.

## Tests

- Frozen source-only preflight and custody checks: PASS, as reported by the
  approved 0236 packet; no browser/socket/actual gate.
- Central named suite, one submission: FAIL before execution, exit 1 in 2s;
  zero assertions and zero log output.
- No local browser/socket/full suite/install was run.

## Next step

The orchestrator should repair or register the exact source-bound manual ADD
suite using the approved existing driver, then authorize one correctly formed
`--no-cache` central submission. Do not delete the legacy leaf until that run
proves the complete ADD, retry/restart/reload/undo, opaque-data, and zero-legacy
assertion body.
