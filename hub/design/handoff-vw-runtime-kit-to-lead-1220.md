# Runtime kit handoff — approved successor

**Status: APPROVED for the successor validation correction only.** The
independent review approved the new hunks; the Runtime manager/lead owns any
kit application. The Composition base was `tl/integration` at
`df7b86308902fae90eda1dc3080d17d8fc30ea78`.

Approved artifacts:

- Patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-child-existing-env-carrier-1156-successor.patch`
  — SHA-256 `12937a65da6a96eb5934ef83fddbfa3e6d7309a39eb18a28ffa19f445b3442ca`.
- Actual-hunk fixture:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-child-existing-env-carrier-1156-successor-fixture.sh`
  — SHA-256 `2c034ec72189b63ba87dee8c5dd9cd81c60e43f6ebbfd8247e0c20d181e8ba7d`.
- Exact command record — SHA-256
  `e069cd6f668d2e5d11a1b55e56a3f0c00de6ad34c1a0c53338d3fe2f3f10eb03`:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-child-existing-env-carrier-1156-successor-COMMANDS.txt`.
- Actual test log — SHA-256
  `1f428099f1406e5b3c7bf9cc172bd3b68ccf56696fa9c4e257ab412737abe3ba`:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m4-runtime-child-existing-env-carrier-1156-successor-TEST.log`.

Evidence actually recorded:

- `bash -n .../vw-m4-runtime-child-existing-env-carrier-1156-successor-fixture.sh`;
  private patch dry-run/apply and `bash -n` for both kit scripts passed.
- `bash .../vw-m4-runtime-child-existing-env-carrier-1156-successor-fixture.sh`
  passed the actual-hunk probes. Runtime missing, foreign, broken, and
  duplicate suite carriers were red on 1156 (reached archive, status 1) and
  green on the successor (status 2 before archive or `$D.partial`). Child
  duplicate carrier and duplicate selector were red on 1156 (reached venv
  allocation, status 1) and green on the successor (status 2 before Python
  allocation). Positive runtime and child probes accepted both flat and
  nested carrier paths and retained one carrier/selector. The log contains
  every exact command and status; `git diff --check` and clean Composition
  worktree also passed.

Layout boundary: the generated runtime remains the nested `$D/remotion`
project plus the sibling `$D/astrid` source closure (including the existing
`LiveSceneClip`/`SceneSurface` rendering sources). This is distinct from the
legacy child carrier input: both `/home/user/work/runtimes/$RT` (old flat) and
`/home/user/work/runtimes/$RT/remotion` (new nested) are accepted exact carrier
values. Accepting the existing flat child carrier must not flatten or replace
the nested Remotion-plus-sibling source layout.

Prerequisite before any application or live creation proof: the lead must
restore and confirm the true `0012` baseline bytes, specifically
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-remotion-0012.env`
and exactly one `agent remotion-0012-nodes` row in
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`.
They were absent during this review; no baseline was invented or restored.
No runtime/child creation, venv or package install, build, network, browser,
server/socket, render, physical proof, central test service, or full suite was
run.
