# AP2 M2 parent synthetic-snapshot custody review

## Verdict

**APPROVE the worker0156 custody fix and the existing parent command.** The
smallest change is correct: final95 App consumers accept either the exact
declared parent `HEAD`, or a different `HEAD` only when the declared commit is
an ancestor. The exact frozen tree, clean state, four pin bytes, and all
producer/source checks remain strict. No arbitrary source identity or root
override was added.

## Exact identities

- App parent source: `25155ccb22728780a3ecd6379a929cad75cc1400`
- App parent tree: `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
- Runtime and producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`
- Artifact manifest: `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
  76 entries
- Schema: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

Four App pin bytes matched:

```text
runtime.lock.json                770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
generated-contract-metadata.ts   4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
generated.ts                     c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
timeline-commit-types.ts         f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
```

## Checks run

- Exact retained parent checkout: `verify_app_source` passed; source `HEAD`,
  tree, clean status, and all four pins matched.
- Synthetic guard probe passed with a different `HEAD` and verified ancestry.
  Refused: changed tree, dirty state, wrong pin, and missing provenance.
  Exact-`HEAD` acceptance also passed.
- Invalid `NORMAL014_PROFILE` and `NORMAL014_APP_SOURCE` selectors both
  refused with exit 2.
- `sh -n` passed for all three normal014 helpers.
- Central source-only preflight
  `ap2-m2-parent-frozen-source-single-gate-0138-normal014-parent-source-identity-preflight-1021020355-15103`
  passed in 19s. It verified 76 artifacts, the schema digest, Agent/Runtime
  imports and collection, the locked public13 graph, and the parent marker.

The existing parent command remains exactly:

```text
env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent bash design/normal014-parent-media-central.sh run
```

Current observed helper hashes are:

```text
normal014-source-common.sh        c76c48fa5f73b72ada6ba8fa857f229778e2ed6948568e77000bf4c1a8490270
normal014-parent-media-central.sh 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
normal014-app-central.sh          5876aeedade27229536e14c82ae1b2bd6b3ad8593fd44d4d02d0c039590b22c3
tests/suites.conf                 d360d5cb087dc7eb463b44950b6bbabe9b71ba6525c8a13be6f7937bdd020576
```

The first two are the reviewed custody unit. The App wrapper and suite file
were concurrently modified by worker0154 while this review was running; they
are reported for provenance but are not part of the worker0156 approval.

## Not run / remaining qualification

No browser, localhost, live socket, package install, full suite, or actual
parent gate was run. The parent behavior itself remains unqualified until the
orchestrator runs the existing command from the exact parent source snapshot.
The assigned App worktree is clean and no product or Git metadata was changed.
