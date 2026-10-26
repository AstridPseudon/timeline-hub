# Validation

Source-only review; no product source, tests, providers, imports, generated
files, pins, requests, CAS, service body, installer, browser, package,
typecheck, lint, or full suite was run.

Read-only checks performed:

1. `python3 -m json.tool` on this review's `review.json` and
   `source-manifest.json`, plus the author's `per-id.json` and
   `source-manifest.json`, and the bound `restoration-manifest.json` — all
   passed.

2. A Python read-only inventory loaded the author packet's IDs and the bound
   restoration manifest. Result: author assigned `15`, unique `15`; restoration
   assigned `15`, unique `15`; overlap `15`; no missing or extra IDs. The exact
   IDs are n=4 through n=18.

3. `git show`/`git rev-parse` read pristine blobs from Agent `64197afa`,
   current blobs from `445b9c1`, and production paths. All 15 named original
   functions are present in the restored current test files. The current tree
   is `6806fec5657f26097d0d0f3da29082907e6faadd`. File SHA-256 and Git blob
   witnesses are in `source-manifest.json`.

4. Static source tracing confirmed the supported commit chain through
   `cli.py`/`cli_native.py`, `TimelineSession._flush`/`submit`,
   `WorkspaceClient.commit_timeline`, and Runtime provider paths. It also
   found the current `Checkout.publish`/restructure caller and the still-
   exposed `publish_parent_composition` Agent surface, which are the route and
   source-of-truth conflicts recorded in findings.

5. The author's exact disk trace was inspected read-only. It has five
   approximately one-second samples (timestamps 11:32:07, 09, 10, 11, 12Z)
   and `df` headers, not the required five-second review-lifetime trace.

6. The worktree remained clean: `git status --short --branch` reported only
   `## tl/agt-F-D141ee-writers15-scope-review-1137`.

Historical limitation: the earlier private XML paths and the configured
`scratchpad/luna/reports/` directory are absent here. The retained summaries
and per-ID JSON are not represented as raw test output, and no test was rerun
to manufacture history.

The corrected foreground sampler for this review is the exact output
`evidence/disk-trace.txt`; it ran continuously at five-second intervals from
11:42:08Z through finalization (6 samples, 6,586,617,856 bytes minimum), and
was stopped after the completion marker. The initial background attempt did
not persist under the execution wrapper and is not credited.
