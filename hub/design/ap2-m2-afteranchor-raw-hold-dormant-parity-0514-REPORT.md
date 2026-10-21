# App2 after-anchor raw-hold dormant parity — report

Date: 2026-10-21 UTC

## Result

Reconciled the dormant App after-anchor capture with Agent452's independently
reviewed source successor. The App now permits an absent or explicit-null raw
video `hold` only on the dormant after-anchor source-window path. The cloned
raw field is preserved exactly; placement remains derived from the anchor's
source window and speed. Explicit zero, nonvideo, ordinary append, and
replacement-style positive-hold validation remain strict.

No live caller, UI, Provider/session route, published014 schema, generated
client, Runtime path, native/pin path, or `afterClipId` wire alias changed.

## Exact identities

- Agent SOURCE ACK: commit `452eceb391408185bfcc0c9e029e271d0ae3a229`, tree
  `18fc7e0b1cde4df1a24637509fa14b2351340c9e`.
- App base before this worker: HEAD `bc6f9dd39c7e5154ddf075cb87b7202cf5702e65`,
  tree `4cd13d09b7cffd60612d8521f1a2921ca4e762d2`.
- Post-harness App commit/tree: not available before worker exit; the harness
  must assign them when it commits this worktree. No commit or Git metadata was
  created by this worker.
- Changed App file SHA-256:
  - `src/tools/video-editor/commands/parentClipAddCapture.ts`
    `6e036a410faea95f3104e602d19285b904975f85f29f9eb7c6af3d66541411a6`
  - `src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts`
    `9415a4ea8ff89c2fc3fa4348d1657c773f0315cb9a67b9d090d24da6ac82fc03`

## Change boundary

The only product correction is the row-local guard in
`parentClipAddCapture.ts`: after-anchor rows with `hold == null` continue to
the existing raw-window validator, which derives video duration from
`to - from`; non-null holds still pass the existing positive-number check.
That validator still rejects zero and nonvideo rows. Ordinary append and
replacement remain outside the after-anchor exception and retain strict
positive-hold validation.

The dormant direct test now carries both absent and null video holds through
capture, replay, both mirror compilations, exact record comparison, and raw
field preservation. It also retains zero refusal and adds direct nonvideo and
ordinary-birth refusal/mutation guards.

## Evidence

1. `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts`
   — **2 files, 18 tests passed**.
2. `PARENT_AFTER_PARITY_OUTPUT=<private TMPDIR>/parity.json ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts`
   — **12 tests passed**; parity output had 10 samples: 6 accepted, 4 refused,
   one absent-hold row, and one null-hold row.
3. Exact Agent comparison used a private archive of Agent452:
   `git -C /home/user/peteromallet/astrid-agent archive 452eceb391408185bfcc0c9e029e271d0ae3a229 | tar -x -C <private TMPDIR>`, then
   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<Agent452 archive>:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python <parity checker>`
   — **6 complete commands/records/bundles/replay results matched; 4 refusals matched**.
   The documented `/home/user/work/venv-agent` was absent; the existing
   `venv-app2-native` was used without installation or shared-dependency edits.
4. `./node_modules/.bin/eslint src/tools/video-editor/commands/parentClipAddCapture.ts src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts --max-warnings 0`
   — passed.
5. `git diff --check` — passed.

No full, browser, socket, HTTP/native Door, install, generated, matrix, pin,
or activation suite was run.

## Live callers and deletion limits

The non-test grep for the dormant helper found only its own declarations and
internal aliases; there are **zero live external callers**. The
`afterClipId` grep found only the existing negative test assertion and no wire
field in either helper. Nothing was deleted: no live writer, schema, route,
provider/session path, or replay/native path was in scope or touched.

