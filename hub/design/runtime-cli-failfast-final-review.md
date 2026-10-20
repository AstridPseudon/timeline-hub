# Runtime current HTTP/CLI fail-fast final review

Date: 2026-10-20 UTC  
Review timestamp: `2026-10-20T16:53:37Z`

## Decision

**APPROVE** `current-http-cli-durability` as bounded qualification evidence
for the fixed wrapper. This supersedes the semicolon-based REJECT in
`runtime-cli-source-fixture-review.md`.

The approved wrapper is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-current-http-cli.sh`

Its SHA-256 is
`c66acf7042677867788b2b0826f00f81cb084386dcce3649d18675ee8ab3ec07`.
The named suite line is the fixed wrapper invocation, with line SHA-256
`823ca7aec2d4b5ae4daae0e976a3a5a172fbd5b91169469b32ccbae3b8ed7833`.

## Evidence

Central result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-cli-suite-failfast-fix-current-http-cli-durability-1020164442-248/`

Exact executed suite command:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/runtime-current-http-cli.sh
```

Result: **pass, exit 0**. The wrapper's first-failure smoke passed; the
pre-override source and artifact proof passed for all 75 manifest entries;
the Agent invocation passed **12 tests in 43.88s**; and the Runtime HTTP
durability invocation passed **1 test in 3.17s**.

The guards establish:

- Runtime server source `6ab3243972f8dc49105819e6d7ba7aef1a2888b8` through
  `refs/heads/tl/rt-m2-cli-current6ab-actual`;
- Agent source `2f8b9cc53648a392da8684016c6ee15e589ea060`;
- immutable producer source `2c4ac180c2220bdad966bc01e95ad230e99ce26a`;
- schema digest `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`;
- artifact version `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`;
- byte equality and manifest SHA-256 validity for all 75 artifacts before
  the test-helper source-selection override.

The wrapper materializes the frozen Runtime source in a private temporary
clone. It does not rewrite producer metadata or relax real health, actor,
realm, authentication, provider, or authorization checks.

## Boundaries and disposition

The CLI parser/handler coverage is in-process, not a spawned OS CLI
subprocess. The durable ACK-loss case uses the existing post-acceptance
response-send fault seam, not a physical socket EOF. These boundaries are
kept explicit; this approval does not claim broader transport coverage.

The prior raw logs remain unchanged. No live or full suite was rerun for this
review, and no test was skipped, weakened, or newly marked expected-to-fail.
