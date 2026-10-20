# AP2 M2 ordinary approved closure real gate

## Result

The one authorized cache-free central ordinary run was submitted against the
approved closure-oracle source and failed before Playwright/browser startup,
Runtime interaction, or the ordinary journey. No source, assertion, pin,
dependency, schema, or fallback change was made, and no rerun was performed.

- App source: `bbffe1a56a96badc49049bb92ca072d74330c93a`
- App tree: `5542a6c10ebbf60f8592adac54d705c2dd4acfdf`
- Central request/result:
  `ap2-m2-ordinary-approved-closure-real-gate-e2e-m2-ordinary-public13-integration-1020232033-8770`
- Suite: `e2e-m2-ordinary-public13-integration`
- Command: `env PRELIGHT_ONLY=0 sh .../public13-integration-runner.sh "$PWD" ordinary`
- Result: exit 1 in 61s; no test counts

The retained central evidence is in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-ordinary-approved-closure-real-gate-e2e-m2-ordinary-public13-integration-1020232033-8770/`

It contains the sanitized request, summary, log, source-tree snapshot identity,
and exit/status records. No request/response or browser trace exists because
the build failed before the local door and Playwright stages.

## Preflight

Passed before submission:

```text
git rev-parse HEAD / HEAD^{tree}
clean worktree check
exact Agent 8130a401... / tree 236c3e57...
exact Runtime 2c4ac180... / tree 7ab412cc...
current config/vite/vite.config.ts byte-identical to e401af721...
PRELIGHT_ONLY=1 public13-integration-runner.sh "$PWD" ordinary
  public13 integration preflight PASS mode=ordinary grep=M2 ordinary extension batch
```

The preflight verified the public Composition 0.0.13 archive digest
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` with 77
regular files, and independently verified the exact Runtime `2c4…` manifest's
75 artifact entries and hashes. No normal014 copy was active when the run was
submitted.

## First causal failure

The central log's first build error is:

```text
src/tools/video-editor/compositions/playerEvaluation.ts (5:2):
"getSanitizedPlaybackRate" is not exported by
"../../app/node_modules/@banodoco/timeline-composition/dist/evaluation.js"
```

The runner's effective importer resolved through the shared install
`/home/user/work/app/node_modules`, whose package is Composition `0.0.8` with
evaluation digest
`0ee058ca8657a6bbdbe8c127359297f856c5a7b1cb68258bd3bdc20846d98b96`.
That loaded module has neither `getSanitizedPlaybackRate` nor `clipOpacity`.
The locked public13 graph itself is correct: package `0.0.13`, evaluation
digest `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`,
and both exports present. This is the known current-source/shared-install
attachment block, not evidence about ordinary editing behavior.

Because the failure occurred before build completion, none of the requested
ordinary checks were reached: ten complete SDK records, disjoint S1/V1
intent, independent pre-A parent/shot/internal/manifest closure with raw
opaque/order preservation, both undos, lost ACK, restart, exact retry, rebase,
conflict, credential, or zeroLegacy traffic.

## Verification and next step

After the central run, the worker worktree remained clean and `git diff --check`
passed. No full suite, local browser/socket run, assertion edit, fallback cut,
or repeated central request was made.

Recommended next step: repair or select the already-existing effective public13
runner so its verified private Composition 0.0.13 graph is actually mounted for
the App build, then request a fresh ordinary gate from that corrected source
and runner. Do not classify this run as a product pass or failure.
