# P1/A2 reviewed composition handoff

## Owner merge packet

The App worktree is based on the actual merged owner base
`23b0901ba1991f9720dd5d2522a76a8b89e45202` (tree
`87c00cb43a076b21264896c3224e859b545d78ee`) and has exactly six authorized
reviewed blobs present as worktree changes. The harness should commit this
stack without borrowing ancestry from `11b57f63f`.

The production path remains:

`inspector SourceIn -> existing useTimelineCommit rowsToConfig ->
withHeldClipSourceFields -> mounted A2 handoff/outbox`.

The helper restores only row-authored numeric held-clip `from`, `to`, and
`speed` fields; absent values remain absent, explicit null remains null,
`hold` remains the row-authored duration, and opaque/app fields remain
carried by the existing clip spread. The caller remains non-mutating.

The mounted regression preserves the canonical predecessor -> dependent new
ID chain: split creates the local new ID, SourceIn trim is authored while the
predecessor is pending, the dependent intent stays chained, the predecessor
ACK rebases it onto the accepted base pair, and canonical adoption completes
the outbox. Assertions retain API v1, project/timeline scope, base
revision/publication, doc.patch, exact before/reads, fields merge, dry_run
false, per-step patch, no legacy save, accepted/merged/refused behavior,
restart/lost-ack retry, and the structured v2 reply/error contract.

## Evidence

- Exact focused A2/P1 run: 9 files / 183 tests passed.
- Joined A2/A3 targeted union: 12 files / 256 tests passed.
- Root, App (180-second practical timeout), and Node TypeScript: PASS.
- Scoped ESLint, vendor lock, unchanged caller guards, origins, diff check:
  PASS.
- P1 list: 2 tests; P3 list: 1 test.
- Private Composition graph: version 0.0.14, 80 files, artifact SHA
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Shared App install remained at realpath
  `/home/user/work/app/node_modules` and was not edited.

No browser/body/service/full-suite result is claimed. The owner should run the
live P1/P3 journeys through the central service if end-to-end credit is
needed, then verify the harness-created commit contains only the six listed
paths.

