# Runtime R5 supported-seed independent review

**Result: PASS.** The reviewed seam report is accurate when bounded to an
empty timeline and honest about the missing complete-fixture importer.

Reviewed exact pair:

- Runtime `49ce53289bc37d9387a7d9e6b9c9b16072162181`, tree
  `364380ae064c512c0a0d2b8903a599b7026642f4`.
- Agent `ef851b22c506245441b9a630c093b3460e39cbdc`, tree
  `b11eee891208d11e23c55950f8954ddd3377d5a8`.

## Production trace

The supported empty path is:

`RemoteTimelines.create_empty` (`astrid/sdk/remote.py:482-595`) → authenticated
timeline shell POST (`runtime_protocol/server.py:524-535`) →
`TimelineSession.open` (`astrid/sdk/timeline/sync.py:137-181`) → captured
`timeline.init` (`astrid/sdk/timeline/native_initialize.py:7-34`) plus emitted
`doc.patch` config → `TimelineSession.commit_many`
(`astrid/sdk/timeline/sync.py:313-358`) → public commit POST
(`runtime_protocol/server.py:294-319`) →
`RuntimeService.commit_timeline` (`runtime_protocol/service.py:2433-2508`) →
startup-registered provider and authenticated `RequestCommitPort`.

This preserves the ordinary v2 request/reply and Runtime custody boundary:
base revision/publication, semantic or `doc.patch` commands, label/steps,
`fields|atomic`, reads, dry-run, source/rationale/group/idempotency, and the
complete accepted/merged/conflict/invalid/preview response data. The caller
does not author manifests, pins, receipts, canonical wrappers, or managed
edges.

## Missing seam and non-seams

The App's `seedThreeProducts`/`seedOneClip` setup still uses the retired
`composition-revisions` POST, which Runtime directly rejects at
`runtime_protocol/server.py:586-591`. On the exact reviewed pair there is no
public importer for a complete parent/shot/internal closure.

The public restore route (`server.py:610-630`; `service.py:2585-2607`) restores
only an authenticated historical revision in the same timeline. Admin
`/v1/backup` and `/v1/restore` (`server.py:462-473`) can restore an
independently authenticated precut realm, but are not fixture migration. The
Runtime `install_verified_baseline`, `adopt_empty_shell`, and `bootstrap`
helpers (`runtime_protocol/timeline_commit_store.py:1351-1451`) are private
existing-store paths and empty/baseline-only. None supplies the requested
public imported closure.

## Newer D17 note (not pair evidence)

Newer Agent `ce1d1cca87379029924b0be6f98564f556597107`, tree
`68dee9124ab8f4026ac4119f816eceec654f0bba`, registers
`timeline.duplicate` (`astrid/sdk/timeline/commands.py:29-68`). Its source
reader/handler (`astrid/sdk/timeline/native_timeline_duplicate.py:23-126`)
requires an exact authenticated source ref, Runtime source-closure port, raw
media capture, an empty destination, and complete fresh injective ID maps. The
public wrapper is `astrid/sdk/timeline_duplicate.py:243-310`.

Therefore D17 can copy an already authentic source timeline into a new empty
destination if that newer Agent is paired with a Runtime/provider that loads
it. It is not present in reviewed `ef851`, and it remaps shot/occurrence IDs
and normalizes the copy, so it is not an exact-ID importer for the current App
fixture requirement. Do not relabel it as current `49ce+ef851` evidence.

## Original20 and evidence

Original20 remains the old Runtime `c6c69f36a64d83baeb081cb980d130883719d6b9`
plus Agent `ef851b22c506245441b9a630c093b3460e39cbdc` proof. Its setup
(`requester_factory.start`, `tests/test_timeline_render_publication.py:29-70`,
and `_connect`, `:14-25`) creates a fresh Runtime realm/project/empty timeline
and connects with `AstridClient.open`/`TimelineSession.open`. Those functions
prove empty bootstrap and public editing custody only; porting them cannot
prove import custody for the complete App closure, including raw/meta/null/
absence/order, IDs, sharing, media pins, dependency manifests, and owner
manifest authority.

Checks completed by the independent reviewer:

- AST parse: 6 Runtime files and 8 exact Agent-ref Python sources passed with
  `PYTHONDONTWRITEBYTECODE=1`.
- `git diff --check`: passed.
- `git status --short`: empty.
- No broad, native14, original20, browser, P1/P2/P3, or full suite repeated;
  source tracing was sufficient. Typecheck/lint: N/A for this read-only review.

## Next owner/action

Proof owns migration of the authentic fixture and its request/body/browser
evidence. Runtime/Agent ownership is needed only if the team chooses to add a
new explicitly paired public authenticated source-copy/import seam. Until
then, qualify only the empty/init/commit route or use a separately authenticated
precut backup as private setup; never revive the rejected route or fabricate
closure authority.
