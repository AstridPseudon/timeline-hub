# AP2 M2 ordinary disjoint rebase review gate

## Result

Not qualified. The fixture-only candidate was tested once through the central
ordinary driver. The repaired same-field setup reached the real retry/rebase
path, but the journey failed at its existing final whole-document undo oracle.
No App production code, pin, schema, dependency, or assertion was changed.

- App commit: `50aab5ed8ec20c1adcd82ae9dea40288b1dcde11`
- App tree: `a99f9460e9c7cec89d2c482fbdafd1daf2c965df`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Composition: public `0.0.13`
- Central request: `ap2-m2-ordinary-disjoint-rebase-review-gate-e2e-m2-ordinary-committed-driver-gate-1020222651-25944`
- Result: exit 1, one test failed, 110 seconds

## Exact evidence

Static preflight passed:

```sh
git diff --check
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-committed-driver-gate/run-central-m2-ordinary.sh
node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-committed-driver-gate/chromium-env-smoke.mjs
```

The one central request was queued and waited exactly once:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-disjoint-rebase-review-gate e2e-m2-ordinary-committed-driver-gate --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The absolute driver selected exactly one ordinary test before build. Chromium
smoke, hosted build, locked source tuple, graph/bin guards, and lock guards
passed. The test reached the ordinary ten-command path, accepted the Agent
label on seeded `S1`, retained the local `V1` label, performed exact retry with
the local label rebased, and passed the undo-label assertion preserving the
Agent `S1` label.

The first product failure was:

```text
tests/e2e/local/three-products.spec.ts:1273
expect(undoOrdinary.data.canonical_document).toEqual(agentEdit.data.canonical_document)
```

The received post-undo document restored the pre-ordinary authored positions
and holds, while the expected `agentEdit` document still contained the
ordinary batch's positions/holds. The diff also included newly materialized
revision/content identifiers. This is an existing whole-document oracle
mismatch; it is not evidence to weaken the dependency-negative or to alter the
fixture further.

Because the failure occurs before the final assertions, this run does not
qualify the final zero-legacy, post-undo opaque, and complete post-undo
preservation checks. The central text log, summary, and request are retained
at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-disjoint-rebase-review-gate/central-result.log
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-disjoint-rebase-review-gate/central-summary.txt
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-disjoint-rebase-review-gate/central-request.txt
```

The driver emitted a Playwright trace path, but its required EXIT cleanup
removed the disposable binary trace before it could be copied; no binary trace
is claimed.

## Decision and next step

The task was read-only after the fixture conversion, so I did not change the
line-1273 oracle, rerun the gate, or weaken any assertion. Do not mark this
candidate qualified. Review the final undo oracle against the already-qualified
duplicate pattern, then queue a new gate only if the orchestrator explicitly
approves a separate source correction.

