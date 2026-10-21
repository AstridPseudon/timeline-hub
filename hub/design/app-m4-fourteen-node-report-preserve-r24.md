# App full24749 fourteen-node handoff

Recovered from `app-m4-full24749-fourteen-node-classify-r23/log.txt`; detailed
row-by-row evidence is in the worker's `notes/fourteen-nodes.md`.

## Verdict

The retained central run `1021044001-24749` used App commit
`e1e153091b23aeafd09a15c500616384fba4330a`, tree
`aa20a99731b91c2fa5e36b258c131147f3d7d651`, and the canonical wrapper command
`bash .../run-current-published014-full-canonical.sh full`, whose inner command
was `npm test -- --maxWorkers=2 --configLoader=runner --no-cache`. It collected
1,520 files: 1,514 passed and 6 failed; 19,428 tests passed, 14 failed, and 3
authorized expected failures. The run is **not qualified** because the keeper
drifted to App `bc6f9dd3` / tree `4cd13d09`.

## Failure groups

- `src/integrations/paired/pairedRoutePolicy.test.ts` — nodes 1–2:
  `createTimeline` was missing from the local-door-only classification, so
  `classifyPairedRoute` returned `undefined` for both `/api/runtime` and
  `/api/astrid`. App transport-test owner; add the explicit refusal cases using
  `04ffb3c20` / `470d9d33e`, with no relay route.
- `src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx`
  — nodes 3–7: all stopped at line 266 with `commands.port === undefined` after
  the delayed resolver. Cause remains **UNKNOWN under full scheduling**; App
  command-session owner should run one scoped full-like scheduling diagnosis.
- `src/tools/video-editor/runtime/element-admission-build.test.ts` — node 8:
  child `tsx` hit `EADDRINUSE` on `full-run/tmp/tsx-0/25317.pipe` before
  admission compilation. Central runner/test-harness owner should isolate each
  child IPC root; this is not an admission-behavior finding.
- `src/tools/video-editor/runtime/extensionOperationalAnalytics.test.ts` —
  node 9: browser has `haus.astrid.threejs-live-editor`, server has
  `haus.astrid.live-scenes`; merge `969941059` reverted the server side after
  rename `a546f0bf1`. App integration and Viewing/vendor peers should restore
  one deliberate ID authority; no alias was intended.
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx`
  — node 10: line 356 saw no `commands.port` after resolver release and stayed
  on legacy preview. Cause remains **UNKNOWN under full scheduling**; diagnose
  with nodes 3–7, without changing assertions.
- `src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx`
  — nodes 11–14: mounted `clipScalarPort` readiness failed at line 131. Reuse
  assigned r3 repair `8814467fe` and r4 refusal-oracle follow-up; do not add a
  duplicate repair.

## Next three

1. Classify `createTimeline` as local-door-only and add its explicit refusals.
2. Isolate `tsx` IPC temp roots for concurrent full workers.
3. Reconcile extension IDs, then diagnose the six UNKNOWN full-scheduling
   readiness nodes; notify App editing, Viewing, and vendor-source peers.

No tests were run in this recovery; no source/product/test edits were made.
