# Runtime R5 supported seed handoff

Runtime `49ce53289bc37d9387a7d9e6b9c9b16072162181` (tree
`364380ae064c512c0a0d2b8903a599b7026642f4`) and reviewed Agent
`ef851b22c506245441b9a630c093b3460e39cbdc` (tree
`b11eee891208d11e23c55950f8954ddd3377d5a8`) provide one supported public
sequence for an **empty** timeline:

`RemoteTimelines.create_empty` (`astrid/sdk/remote.py:482-595`) -> authenticated
timeline shell POST (`runtime_protocol/server.py:524-530`) -> `TimelineSession.open`
(`astrid/sdk/timeline/sync.py:137-181`) -> `timeline.init` plus config
`doc.patch` -> `TimelineSession.commit_many`
(`astrid/sdk/timeline/sync.py:306-358`) -> public commit POST
(`runtime_protocol/server.py:294-319`) -> `commit_timeline`
(`runtime_protocol/service.py:2433-2508`) -> registered provider.

Prerequisites are the authenticated project/client, exact bootstrap
revision/publication pair, loaded provider, stable idempotency, and
Runtime-verified media custody. The v2 request/reply contract remains the
current full shape; callers cannot forge manifests, CAS pins, canonical
wrappers, receipts, or provider-managed edges.

This does **not** seed the App `seedThreeProducts` / `seedOneClip` complete
parent/shot/internal closure. Runtime correctly rejects their old
`composition-revisions` POST. Reviewed Agent has no source-copy command in
`astrid/sdk/timeline/commands.py:40-65`; `timeline_adopt` is local/remapping and
reviewed `timeline_duplicate.py:172-230` ends through retired publish and also
remaps/strips data. Runtime `install_verified_baseline`, `adopt_empty_shell`,
and `bootstrap` are private existing-store helpers, not public import routes.

The authentic precut backup fixture can prove private setup followed by public
authenticated edits, but not public fixture migration. Original20 remains an
old Runtime `c6c69` + Agent `ef851b22` proof, not a current49ce rerun.

Status/checks: AST parse passed for 7 Runtime and 8 exact reviewed Agent Python
sources; `git diff --check` passed; `git status --short` was empty; no broad
test suite was run because source tracing resolved the question.
