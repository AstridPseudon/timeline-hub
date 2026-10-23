# Runtime handoff: OPS-D21b child reuse security review — 1820

**Verdict: FAIL; do not install or merge.**

The 1811 private packet passes its declared installed-client byte/RECORD,
read-only, marker, partial, ambiguity, and legacy-argument fixture cases. An
independent run reproduced those passes, including hash manifest 8/8, flat
`cmp` 4/4, shell syntax, scoped Runtime compile, and clean Runtime source at
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.

It fails the fresh custody acceptance:

* requester reuse does not require or inspect the Agent checkout; a valid
  `.astrid-source-commit` marker is enough;
* wrong Agent metadata version and wrong Agent `direct_url.json` source both
  reused in private copied actual-layout fixtures;
* malformed non-client Runtime RECORD content reused because malformed rows
  are skipped;
* the maker returns success on an existing same-name destination before
  identity/preflight, so a queued failed-reuse request can be reported as
  existing without rebuild;
* dispatcher-to-maker normal and `env -i` flow is unqualified. The installed
  dispatcher hardcodes shared ORCH and the staged maker’s explicit private
  roots are not carried in the pending request.

Exact commands, exits, private probe paths, and limits are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-child-reuse-securityreview-1820/report.md`

No production repair, host install, actual maker/requester/dispatcher,
provision, network, queue, artifact, or shared ORCH operation was performed.
The backend/client key decision remains with the orchestrator; this review does
not authorize client-only completion.
