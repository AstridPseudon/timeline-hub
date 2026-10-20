# AP2 M2 selected P1 history fixture review gate

## Verdict

**Source APPROVED; central DEV gate NOT QUALIFIED.** The repaired fixture now
uses the existing native producer correctly, but the one authorized central
run exited before test collection/browser execution and produced no qualifying
DEV result. It was not rerun.

Candidate: `d0c563bc452b2d39b7202df574684ecb7b7f410f` /
tree `f53e3f5ecdcf45d494e701aecb72ab3d1a1a56ab`.

## Focused provenance recheck

The only candidate product diff is `tests/e2e/local/support/harness.ts`:

- the initial hold-effect carrier keeps the existing same-id/effect/hold/no-
  media shape but has `elementRef.revision: 'draft-1'` and no `packId`;
- the normal Agent `timelines update-element` command is therefore not a
  same-reference PARAM update;
- the harness reads accepted Runtime history for that exact returned head and
  fails unless the receipt commands are exactly
  `clip.set-element`, then `clip.set-params`.

The existing Agent producer path reviewed at
`astrid/sdk/timeline_elements.py` reads the authenticated project-pack
document, verifies the admitted P1 owner/id/kind/revision, reads the admitted
snapshot object through the Runtime document-object path, constructs the exact
`DocumentPin`, and executes the native command batch. This is the real binding,
document, and object path; no history record is fabricated and no legacy
composition writer stands in for P1 authority. The fixture's later resolver
read validates the project-derived document id, project id, integer version,
and full `sha256:` content digest.

The unchanged journey still asserts P2 admission and source removal, reload
and retained P1 value `8`, P1-schema refusal for `16`, P1 `schema_source` on
the refused request, lost-ACK exact body/key retry, reload recovery, mounted
inverse undo, and zero legacy POST traffic. No browser hash, `2a`/`8e` alias,
new provider/wire/API/store, or product/shared source was introduced.

A direct read-only producer probe against the current Agent source passed and
returned the required operation order:

```text
native producer probe: pass ['clip.set-element', 'clip.set-params']
```

## Central suite and result

Added the unique App suite registration
`ap2-m2-selected-real-p1-history-fixture-fix`, targeting exactly
`tests/e2e/local/three-products.selected-param-dev.spec.ts`. Its private
runner guards Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and the locked Composition
`0.0.13` graph. It clones Agent/Runtime privately, uses a private node graph
and caches, collects exactly one test before the hosted build, then runs only
the selected DEV test. Failure output is retained under the worker record.

Exactly one central request was submitted:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-draft-p1-review-gate ap2-m2-selected-real-p1-history-fixture-fix) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: `ap2-m2-selected-draft-p1-review-gate-ap2-m2-selected-real-p1-history-fixture-fix-1020214132-29175`, exit 1 in 3 seconds. The service reported no test counts; the log contained only the runner's retained-trace line. The retained trace directory is empty, so no collection, build, browser, socket, or DEV journey evidence is claimed. This is the first and only causal result; no retry or diagnostic loop was run.

## Checks

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-app2-native/bin/python - <<'PY' ... _calls(...) ... PY` — passed; exact native operation order confirmed.
- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh` — passed.
- `git diff --check HEAD~1 HEAD` — passed.
- Candidate-provided focused evidence: ESLint, TypeScript, and 2 files / 16 Vitest tests passed (recorded by the fixture-fix worker).
- Candidate-provided selected source collection: one Playwright test listed (recorded before this review).

No local browser, localhost/live socket, full suite, neighboring Gate5, dirty-
source run, dependency install, or product/shared edit was performed.

## Next step

The fixture repair is ready for integration review, but the selected DEV gate
must be treated as open. The orchestrator should inspect the central runner's
silent pre-collection/setup exit and, only after that is resolved, schedule a
new uniquely identified central run. Do not interpret this run as browser
qualification.
