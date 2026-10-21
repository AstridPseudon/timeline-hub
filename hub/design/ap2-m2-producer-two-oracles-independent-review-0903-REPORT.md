# AP2 M2 producer two-oracle independent review — 0903

## Decision

**APPROVE.** Both deterministic test corrections are one-to-one behavior-oracle
conversions. No product source, live caller, actual, or fixture behavior was
changed by this review.

Reviewed App branch:

- branch: `tl/ap2-m2-producer-two-oracles-independent-review-0903`
- HEAD: `4d6ff2176c6a19fc8b5831662beb8e6d7d0e5de6`
- tree: `16d17331db3c0b4949844872851c9c868dfe7312`
- spec: `tests/e2e/local/producer-ownership-current-pin.spec.ts`
- spec Git blob: `76495a3132cf4763609125a5eb25e35f0f1dd6da`
- spec SHA-256: `f84589a25a5ce03eb157d5f95153125e98d87f20c3d8e36461cd2dcc629eea2`
- reviewed one-line second-delta patch SHA-256: `e151939d8cee6130492a8c931e6d697a1f098b164e366b35ee33fd1e7965f9f4`

## Exact two corrections

1. The first delta, inherited from `3c2dac2a75ad9790bd8a9a85c82d20b149ec21fc8c`
   (actual full SHA `3c2dac2a75ad9790bd8a9a85c82d20b149ec21fc8c`), changes only
   the initial mounted transcript selector at spec line 94:

   ```diff
   - getByTestId('transcript-lane-chip')
   + getByTestId('transcript-lane-occurrence')
   ```

   The expected count remains exactly `2`. The retained packet
   `failure-1792572330-28858` has two mounted occurrence buttons, with the
   expected foreign/user labels and source IDs; the stale source item is outside
   the carrier window. The mounted production component
   `vendor/astrid-browser/astrid/packs/rendering/ui/transcript-lane/TranscriptLane.tsx:253-265`
   emits `data-testid="transcript-lane-occurrence"` (blob
   `f24acf4b6ab066b22a1334e59553abc0011c692e`), while the retired dev marker is
   not mounted. This is exactly the old retired marker to the current production
   marker conversion; it does not widen the selector or alter the source,
   labels, IDs, count, or protected rows.

2. The second delta is the only change from the 0855 parent (`3c2dac2a7`):
   spec line 163 changes only the observed native wire spelling:

   ```diff
   - args: { at: 1 }
   + args: { on: 1 }
   ```

   The exact selector, command set, value, and all neighboring assertions are
   unchanged. This is the pinned native wire field, not an App authored-value
   change.

## Frozen schema/provider and lowering proof

The review used the requested frozen pins, not current-main or private017:

- Agent commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Both frozen schema files have blob
  `11ff4399dfa4830f3f6177a5124475d970600da5`.

At `ClipMoveArgs` lines 399-411 in both schemas, `on` is the sole numeric,
required property, with `additionalProperties: false`. Agent's frozen native
provider/capture emits `{'on': _seconds(moment)}` at
`astrid/sdk/timeline/native_checkout.py:149-159` and `{'on': on}` at
`astrid/sdk/timeline/capture.py:241-244`. Runtime's frozen typed provider
declares `ClipMoveArgs = TypedDict('ClipMoveArgs', {'on': float})` at
`runtime_protocol/timeline_commit_types.py:25`.

App lowering remains authored `{at: alignment.time}` at
`src/tools/video-editor/dev/scene-phase-markers/extension.ts:722-731` (blob
`947dd512269974f0114eaa406c7345902326b8d6`). The test's raw authored readback
remains `{at: 1, hold: 5}`. Therefore the observed POST oracle must use native
`{on: 1}`, while intent/readback correctly remain `{at: 1}` / `{at: 1,hold:5}`.

## Whole direct-neighbour case audit

No deterministic unreachable or mismatched oracle was found. The complete case
retains:

- the visible atomic-refusal branch and zero-request/head-unchanged checks;
- exact transcript `clip.delete` selector and empty `args: {}`;
- exact scene command count/order `['clip.move', 'clip.set']`;
- exact scene selector, native move value `1`, hold value `5`, and `clear: []`;
- accepted lost-ack handling, reload, exact retry `rawBody`, and exact retry key;
- post-retry authored readback `{at: 1, hold: 5}`;
- undo request `timeline.inverse`, reload/head transitions, and `{at: 30, hold: 2}`;
- protected foreign/user row identity, every-field equality, and order equality.

The original case/support pair contains no separate `zeroLegacy` assertion; no
such check was deleted, weakened, or widened. The four protected foreign/user
rows remain covered by the existing `protectedClipState` equality. No skips were
deleted and no object expectation was broadened.

Command/count inventory retained: initial mounted occurrences `2`; transcript
accepted command set `1` (`clip.delete`); scene command set `2` (`clip.move`,
`clip.set`); undo command set `1` (`timeline.inverse`).

## Retained evidence and checks

The retained packet checksum verification passed (`5/5` files):

```text
(cd .../failure-1792572330-28858 && sha256sum -c SHA256SUMS)
PASS: browser-output/.last-run.json
PASS: browser-output/.../error-context.md
PASS: browser-output/.../trace.zip
PASS: child.log
PASS: identity.txt
```

Packet `SHA256SUMS` SHA-256 is
`d0129ef8aca5c59e044c99a7b7ea87df1c3657350ad6f17c956e9f5e77ca2d5e`.
The retained DOM failure is the obsolete `transcript-lane-chip` count-0
assertion; it is not evidence against the production occurrence renderer.

Previously available static checks were accepted as evidence:

- `./node_modules/.bin/eslint tests/e2e/local/producer-ownership-current-pin.spec.ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `git diff --check` — PASS (also rerun on the reviewed tree).
- The exact diff is one file, one insertion, one deletion for the second
  correction; the first correction likewise changed one assertion and only
  added explanatory comments.

No browser, build, actual producer run, historical replay, daemon/socket,
localhost/service, install, full suite, or new test matrix was run, per the
task boundary. Live callers changed: **NONE**; only test oracles are involved.
