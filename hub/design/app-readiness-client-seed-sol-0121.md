**A2 comparison complete. No justified App fix; server cause remains UNKNOWN.** No product, test, harness, pin, schema, lock or retained-input changes. Commit message and `DONE` written.

Read PLAN, source0113, independent0117 PASS, cause0105/four safe exports, caller0053, and P1 retained request/summary/log/report.

| Retained run | App | Agent | Runtime | Result |
|---|---|---|---|---|
| P1 18792 | `f8b15af0` | **`78738040`** | `2a9e347f` | 2 passed; exit 0; 141s |
| P2 10973 | `804134d747` | **`079580ca`** | `2a9e347f` | Bootstrap failed; exit 2; 189s |
| P3 14249 | `804134d747` | **`079580ca`** | `2a9e347f` | Bootstrap failed; exit 2; 194s |

These are **different source tuples**. Retained caller assignments, snapshot trees, child source markers and completed bench leases agree. They do not establish actual daemon imports.

**Concrete seed and bootstrap differences**

| Dimension | Passing P1 | Failing shared bootstrap |
|---|---|---|
| Target seed | Parent-only, one clip/track/asset; no child closure | Two parent clips/tracks; one occurrence, one shot, one internal timeline containing three clips/two tracks |
| Publications before target mount | One accepted seed commit after Runtime bootstrap | One accepted compound seed commit after Runtime bootstrap |
| Expected target history | Two entries: bootstrap plus accepted seed | Two entries: bootstrap plus accepted seed |
| Navigation | Explicit `localProject`/`localTimeline`, normalized to canonical selectors | Bare editor route; discovery selects project and timeline |
| Owner wait | Target owner, 90-second ceiling | Scoped owner/database, default 5-second expectation |

History cardinalities above follow fresh-fixture source sequencing; **actual failed browser history replies/counts were not retained**. Multiple seed commands do not imply multiple accepted publications.

P1’s common harness also initializes an empty timeline; each P1 case creates its own additional chain timeline. The shared leaf defers empty initialization and seeds its sole timeline directly. P1’s `openSeededTimeline()` helper checks visibility; its initial chain mount uses explicit selection and waits for the chain owner.

P1’s trivialboot preflight creates the empty fixture. P2/P3’s earlier native preflight creates the full fixture and verifies authoritative history. Each preflight stops its harness; the browser leaf creates another. **Earlier native/history PASS does not prove later browser history completion.**

**Exact source comparison**

Thirteen seed/bootstrap/loader/client/route/original-journey files are byte-identical between App revisions. Key Git blobs:

| Source | Blob in both |
|---|---|
| Harness/seeding | `793f49af6d039f2d23a75fcc7deaff2f1366c533` |
| Shared bootstrap/helpers | `1099534016d4951389ff00238399f21870670df0` |
| Global setup | `968f574a6f5aa5e009de0b400fcd71c69a879686` |
| P1 spec | `5a2029d5f61a5cb665e1fb59c9fe13c9fff0bfde` |
| Data provider | `fea25c9f28fa617eb3cf252a0a86818ef1218be2` |
| Runtime client | `6e9a894d09959ed9fa8f1c0c6f01b9423441c59b` |

The changed lifecycle hook is `e79e083dbca9d67fbc0c66051a365ad59b897ff5`; changed handoff is `551f2fa739a5932360a7e1a9e59abae45ea97e4d`.

Agent787→079 changes four production files: `_commit_patch.py`, `commit.py`, `inverse.py`, and `store.py`, concerning copy-manifest handling, registry inverse aliases and unpinned checkout hydration. Both seed implementations explicitly supply their base revision/publication. This difference remains a comparison variable; it is not causal proof.

Bench dependencies also differ in identity: P1 uses child `venv-agent-child-app-p1-787-2a9-1829`; P2/P3 select child store entry `child-885870…`. Their source markers match the respective Agent pins. Remotion benches have identical package/lock bytes and installed-module markers; lock SHA256 is `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`. Both record Node `v20.19.4`, npm `10.8.2`. Equal dependency bytes do not establish equal source tuples.

**Client, loader and sequencing**

The unchanged awaited chain remains:

`useTimelineSave → readTimelineOriginalSaveBasis → loadTimelineCommandBasis → listTimelineCommits → request → fetch/arrayBuffer`

- Initial history query is cursorless `GET /api/runtime/v1/projects/:project/timelines/:timeline/commits?limit=50`. It sends no head query parameter.
- The loader captures the returned head, checks pagination consistency, then reads immutable closure revisions. Identity acquisition and durable session creation follow basis completion.
- Seeds finish before browser mounting. Discovery, timeline/registry and health reads can overlap. P2 cancellation restarts a basis read without aborting the earlier request; P3 has no recorded cancellation, so cancellation is not necessary for this failure.
- Door routing, session negotiation and CORS implementation are unchanged. P2/P3 connection and selection pass. Distinct retained door ports are `36707`/`45191`; source binds the hosted build and daemon door consistently. Missing history responses do not establish a CORS refusal.
- Retained build stages support hosted-build execution; disposable builds and actual daemon imports remain unavailable for independent byte attribution.

**Concrete Runtime handoff**

Suggested manager publication:

**Ask:** Use the unchanged harness blob above, specifically `commitNativeSeed()` and `seedThreeProducts()`, as the bounded full-closure input: one bootstrap publication, one accepted compound seed publication, then cursorless history `limit=50`. Compare against P1’s parent-only closure. Preserve records, steps, reads, receipt and dependency closure; do not replace the input with 21 publications or empty history.  
**Owner:** Runtime `R-readiness-commits-hang`.  
**By:** Existing peer deadline, `2026-10-24T01:40Z`.

The missing observation is authentic handler-entry/progress and daemon-source attribution for the browser request. App retained directories supply neither daemon output nor the accepted seed packet/database for that actual browser instance. No completed Runtime server-worker result was available here. Runtime’s existing owner should return bounded reproduction/source findings; this task started no additional server work.

**Validation**

- `python /tmp/w-03a6756ef9/readiness_source_checks.py` — **PASS**: 13 source equalities, P1 body lock, fixed hook blob, three retained tuples/trees/outcomes/leases, child markers, four export hashes, lifecycle sequences, loader ordering and query defaults.
- All **43 original P2/P3 retained files** remained hash-identical during checks.
- `git diff --check` — **PASS**.
- `git status --short` — **clean**.
- Tests/typecheck/lint reused unchanged qualification as instructed; no suites, HTTP, browser or service actions executed.

P1 PASS stands separately. P2’s eight original cases and P3 Gate 5 remain **NOTRUN; no GO**.