# Discovery readiness contract fix 1153

## Result

Prepared the corrected operational packet at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-discovery-readiness-contract-fix-1153/packet`

No Composition product/source files changed. The packet changes only the
wrong adapter assertion and pre-issuance ordering, with one private helper for
the shared readiness check.

The frozen App0d43 discovery authority returns the exact normalized sentence:

`discovered exactly 5 current native-codec-chrome155 parity cases`

The raw Playwright listing remains separately checked as:

`Total: 5 tests in 1 file`

`prepare.mjs` calls the same private discovery-readiness helper before any
`issue.mjs` invocation. `run.sh` verifies the preflight result is PASS with no
token, browser, Runtime, grant, or marker issuance before allowing the normal
issue path. Existing post-issue tuple, signature, provenance, stage, graph,
lock, source, environment, fd9, short-socket, storage, and cleanup guards are
retained.

The helper uses the actual exported `discover(appRoot)` seam for the positive
case and four one-to-one temporary fixture controls: wrong count, wrong case
name, no tests (`No tests found`), and helper spawn error. Fixtures are small
generated config/test files plus a read-only symlink to the existing dependency
tree; no product/source/package staging, installation, or shared dependency
mutation occurs. Each recorded temporary root is canonical and removed only
by exact path in `finally`.

## Evidence

Targeted local command passed:

```text
{"discovery":"discovered exactly 5 current native-codec-chrome155 parity cases","refusals":{"wrongCount":"refused","wrongName":"refused","noTests":"refused","helperError":"refused"}}
```

Static evidence passed:

- Node syntax checks for all `.mjs` packet files.
- Bash syntax checks for `run.sh` and `preflight.sh`.
- Python AST checks for both `.py` packet files.
- `sha256sum -c SHA256SUMS`: all 11 packet files OK.

Independent review approved the exact packet for one central `--preflight`
only. Review report:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m3-discovery-readiness-assertion-review-1153-REPORT.md`

Review evidence: packet manifest digest
`0ee53582e55a4f9eb8464a2d7581924cf42bb5a56f3d75de362991f3e196299e`, frozen
App controller digest
`f536eff2773cd1ffd87678d647b99facd01c7cfa6d649d98ae7a0b7387038c27`, and
frozen `discover` function digest
`6a8a21cce55f1ded086072c72d8a47fd9f4e61855baf1b96bc9e61d153fe66bd`.

## Not run / blocker

No central preflight, issue/marker issuance, browser, Runtime, helper, full
suite, physical request, or physical pass was run. The required separate fresh
manager note
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/grant-discovery-readiness-1153.md`
was not present when this worker completed. Consequently central readiness and
the physical phase remain unverified; the consumed 1140 marker was not reused.

The next authorized step is exactly one central `packet/run.sh --preflight`
after that fresh grant note exists and names the 1153 packet/stage/marker.
Only a PASS may authorize any later phase; no retry or marker reuse is implied.
