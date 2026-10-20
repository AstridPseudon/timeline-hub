# App trim inert prerequisite: independent review

Decision: **HOLD** for source-only approval.

The App candidate is minimal and its App-side evidence passes, but the settled
design's reported current Agent exact-integer fact is not reproducible against
the pinned Agent `8130a401bf44a518d5a40ae274d398b8c560be55` source. The native
Agent path accepts raw `D+1` in the probe below, while the model path refuses it.
I am preserving that discrepancy as a HOLD rather than relabeling the old
historical source or changing the numeric policy.

## Scope and minimality

- App HEAD: `afb774c875d9344132c697b1357a259e8f32f010`.
- Current App base from the design: `d2100a2afe8e3ccf0c9e0752c36ceb4ecd71c8f4`.
- The candidate diff adds exactly four paths: `clipTrimCapture.ts`, its
  257-line test, and the two existing trim fixtures. `git diff --check` passed.
- All four candidate blobs are byte-identical to approved donor
  `aa0531ec704d3f14500c7f0d54c02e424acd0b67`.
- Fixture SHA-256 values remain `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152`
  and `5cf496137b9387ef05e8f3b9a5fc7762c529f30670db2c0114d689cba4959d97`.
- There is no current-tree reference to `clipTrimCapture`, `executeClipTrim`,
  or `ordinaryTrimMember` outside the new helper/test. The command index,
  session, UI, dispatcher, writer paths, DTOs, stores, and public App exports
  were not changed. No old branch code was imported.

The helper exports are unchanged:

```text
captureClipTrim(bundle: AuthoredBundle, select: string, args?: ClipTrimArgs): ClipTrimBasis
executeClipTrim(bundle: AuthoredBundle, command: EditCommand): { command, bundle, record }
ClipTrimArgs = { in_s?: number | null; out_s?: number | null }
```

The separate App2 consumer ref `hub/timeline/app/tl/ap2-m2-ordinary-trim-source-adapter`
confirms the intended adapter contract; it is not part of this candidate:

```text
captureOrdinaryTrimMember(bundle, operation): OrdinaryTrimMemberBasis
finishOrdinaryTrimMember(basis: unknown, ordinal = 0): OrdinaryTrimMemberResult
executeOrdinaryTrimMember(bundle, command, ordinal = 0): ReturnType<typeof executeClipTrim>
```

Its payload is source seconds (`in_s`/`out_s`), maps to the reserved literal
`parent/clip:<target>` identity, and must delegate to this helper rather than
reimplement trim behavior.

## App evidence

The helper source retains the requested contract:

- `clipTrimCapture.ts:51-69` decodes the binary64 value and applies exact
  nearest-even six-decimal rounding; inward flooring is selected only for an
  endpoint rounded beyond the raw duration.
- `clipTrimCapture.ts:175-219` reads the authoritative registry duration,
  rejects mapped/unsupported sources and malformed authored shapes, writes
  source-second `from`/`to`/`hold`, preserves speed semantics, and keeps the
  original guarded recorder/replay path.
- The tests retain original guards, opaque own fields/order/identity and
  config/parent mirrors (`clipTrimCapture.test.ts:36-192`) and exercise all 17
  shared boundary vectors (`clipTrimCapture.test.ts:194-256`). No matrix or
  fixture was added.

Commands run:

```text
TMPDIR=<private review cache> node --require <existing runner>
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts
  --configLoader=runner --no-cache --no-file-parallelism --maxWorkers=1
  src/tools/video-editor/commands/clipTrimCapture.test.ts
```

Result: **1 file, 56 tests passed, exit 0**, Vitest 4.1.5. The repository's
`node_modules` was read-only; the private cache/TMPDIR was removed afterward.
The requested private13 executable was not present in this sandbox, so this
was the read-only installed Vitest lane with a private cache, not a private13
package qualification.

The existing frozen 18-case Agent export was replayed through the current App
helper with this one-shot `tsx` command (no file or fixture writes):

```text
node --import /home/user/work/app/node_modules/tsx/dist/loader.mjs
  --input-type=module -
```

Result: **18 frozen Agent/App cases passed** for exact command, record, full
authored bundle, replay, parent/config mirrors, refusals, and input
preservation. This reuses the known export; it is not a new matrix or fixture.

## Exact-integer HOLD

Using a private archive of Agent `8130a401...`, vended from
`/home/user/peteromallet/astrid-agent` without checkout or modification, the
inline probe used `D = 9007199254740995` and raw `D+1 = 9007199254740996`:

```text
native D: 9007199254740994.0
native D+1: 9007199254740996.0
model 9007199254740995 accepted to: 9007199254740994.0
model 9007199254740996 refused: source range ... must fit inside the file
```

The native result is explained by the pinned source's
`astrid/sdk/timeline/capture.py:24-35`, where `number()` converts the raw
integer to `float` before `_trim_commands.py` performs the range check. Thus
the native path cannot distinguish these two integer values at that point.
This directly conflicts with the design's stated result that both native and
model refuse raw `D+1`. The prior report's native refusal was not reproduced
against the exact pinned source. No App numeric redesign is proposed here.

## Limits and next step

No full suite, project TypeScript check, install, build, browser, live socket,
Runtime receipt/persistence qualification, UI/session activation, dispatcher
activation, or writer retirement was run. The HOLD is specifically for the
unresolved Agent native exact-integer evidence. Agent ownership should resolve
whether native raw-integer preservation is required and then re-run the
18-case App/Agent parity before this inert prerequisite is marked APPROVE.
