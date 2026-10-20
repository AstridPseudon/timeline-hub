# App trim capture current inert prerequisite

Status: **SOURCE-ONLY READY; production activation remains intentionally open.**

This ports the approved 'aa0531ec704d3f14500c7f0d54c02e424acd0b67' capture
closure onto current App integration. It adds only the helper, its existing
golden/boundary tests, and the existing exact fixture bytes. No gesture,
session port, writer retirement, ordinary-membership dispatcher, DTO, store,
framework, generated file, or public API was added.

## Source identities and scope

- Current App base: 'd2100a2afe8e3ccf0c9e0752c36ceb4ecd71c8f4',
  tree '19e839e97b57f5b30981ab978b8983fc50ee69bf'.
- Approved donor: 'aa0531ec704d3f14500c7f0d54c02e424acd0b67',
  tree '54055916d6c38fed482b377111d1b68eac4014c2'.
- Exact added paths:
  - 'src/tools/video-editor/commands/clipTrimCapture.ts'
  - 'src/tools/video-editor/commands/clipTrimCapture.test.ts'
  - 'src/tools/video-editor/commands/fixtures/recipe_m2_clip_trim.json'
  - 'src/tools/video-editor/commands/fixtures/recipe_m2_clip_trim_boundaries.json'
- The helper and test are byte-identical to the approved donor. The original
  fixture SHA-256 is '4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152';
  the 17-case boundary fixture SHA-256 is
  '5cf496137b9387ef05e8f3b9a5fc7762c529f30670db2c0114d689cba4959d97'.
- The test is 257 lines; the 2,275-line golden is a reused exact fixture, not
  a new test file or generated fixture.

The export contract is unchanged and available for App2's ordinary member:

- 'captureClipTrim(bundle: AuthoredBundle, select: string, args?: ClipTrimArgs): ClipTrimBasis'
- 'executeClipTrim(bundle: AuthoredBundle, command: EditCommand): { command, bundle, record }'
- 'ClipTrimArgs' is '{ in_s?: number | null; out_s?: number | null }'.
- 'ClipTrimBasis' contains the original 'bundle' basis and captured 'command'.
- 'ClipTrimError' remains the existing 'ClipMoveError' alias; 'AuthoredBundle'
  remains the common primitive type.

The helper retains exact binary64 nearest-even rounding, exact inward flooring
against raw authoritative duration, raw finite/range guards, source-time hold
and speed semantics, opaque/order/identity preservation, and the original 18
known vectors (unchanged golden plus 17 shared boundary vectors). No epsilon,
numeric redesign, extra guard, silent normalization, or new argument was
introduced.

## Current Agent source and parity

Current Agent8130 source was read from commit
'8130a401bf44a518d5a40ae274d398b8c560be55', tree
'236c3e57e0265c52b81ba8085de3193026176bff', using a private archive only.
Relevant product blobs:

| Path | Blob |
| --- | --- |
| 'astrid/sdk/timeline/units.py' | '11bb609c6116fe2d2a50f880fbd3f92c60ee1d43' |
| 'astrid/sdk/timeline/_trim_commands.py' | 'c5dd666a676d09c2a232e3f81031b736feb50916' |
| 'astrid/sdk/timeline/model.py' | 'f8115879a7cd666ea9b99bd5e1884ddbec8b7ab8' |

The existing Agent fixture loader was used to expand its compact record fields;
no fixture was added or changed. The exporter exercised the App original
fixture input plus the 17 App boundary vectors, then the App comparison checked
the exact Agent command, full record, full authored bundle, command replay,
parent/config publication mirrors, and specified refusals. Canonical exported
18-case JSON signature (sorted compact JSON) is:

'd623533182f684c1b6b6196beda71ffc704dfb9eec3da5bf6bcc9481ea32c212'

The independently reviewed old exact-Python-integer issue was checked against
8130 source, not relabeled silently: native and model both accept exact
'D=9007199254740995' at the inward representable endpoint
'9007199254740994.0', and both refuse raw 'D+1' before mutation. The 17
Agent-only huge-integer vectors remain upstream Agent evidence and are not
added to this App prerequisite.

## Evidence

Private13 helper/golden controls (Vitest 4.1.5, no cache, one worker):

    node --require <worker>/../app-m2-trim-exact-policy-independent-review/vitest-runner.cjs <private13>/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --no-file-parallelism --maxWorkers=1 src/tools/video-editor/commands/clipTrimCapture.test.ts src/tools/video-editor/commands/clipMovePrimitives.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/clipScalarCapture.test.ts

Result: **5 files, 223 tests passed, exit 0**.

Current Agent8130 exporter plus App comparison:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private Agent8130 archive> /home/user/work/venv-agent/bin/python <inline exporter> | node --import <tsx>/loader.mjs --input-type=module -e <inline comparison>

Result: **18 exact cases passed, exit 0**. This was a private pipe, not a new
giant fixture.

Integer-bound check against current Agent8130 source:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private Agent8130 archive> /home/user/work/venv-agent/bin/python <inline native/model probe>

Result: exact raw 'D' applies inward to '9007199254740994.0'; raw 'D+1'
refuses in native and model paths, exit 0.

Scoped lint and whitespace:

    node <private13>/eslint/bin/eslint.js --no-cache --max-warnings 0 src/tools/video-editor/commands/clipTrimCapture.ts src/tools/video-editor/commands/clipTrimCapture.test.ts
    git diff --check

Both exit 0. Temporary Agent archive and private cache were removed after
verification. Shared packages, shared node_modules, and shared caches were
not modified.

## Limits and next steps

No full suite, project TypeScript check, install, build, browser, live socket,
Runtime receipt/persistence qualification, or production UI/session activation
was run. App2 may consume the exact helper exports above for its ordinary
membership work; any session/gesture port and writer retirement remain
separate tasks and gates.
