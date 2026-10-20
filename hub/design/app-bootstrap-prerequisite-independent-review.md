# Bootstrap prerequisite independent review

2026-10-20 — **APPROVE the source-only prerequisite; HOLD production activation and publisher deletion.**

Reviewed App `dcf52eb3943dffb3554f616f6ecd738717e29d74` against normal013Root `171a259acbeb3ced855ca8f72fed0943a2f5a5cb`, following PLAN, `app-bootstrap-current-contract-audit.md`, and `app-bootstrap-prerequisite-source-refresh.md`. No blocking defect found within the authorized source-only scope. No product/test/Agent changes were made.

## Source and behavior review

- The complete diff is eight files: 283 added product lines and six removed product lines (195-line initialization adapter, 53-line capture, outbox +35/-6); the remaining additions are direct tests and one full native golden. It reuses the existing store, owner/lock/generation mechanism, recording primitives and generated mutation types. There is no new dependency, framework, journal, endpoint, operation registration, schema, compatibility floor or pin. The literal `timeline.init` command targets the existing frozen native prerequisite; this PR does not make it available on normal013.
- No active caller imports or invokes `reserveBootstrapInitialization`/`resumeBootstrapInitialization`. Only the unwired adapter uses `captureBootstrap`; production still uses `createDefaultTimeline` and its publisher. `client.ts`, generated client/types, commitSession, editor/project callers, package and lock are byte-identical to normal013Root.
- `reserveCreate` stores the full payload plus exact POST path/body/key and reserved timeline identity in one strict-durability transaction before any transmit callback. It requires an unused owner, scoped canonical route/body, legal key, and no fabricated head. Ordinary `append` cannot create an unreserved headless flight. Failed reservation leaves earlier state intact. The adapter checks that the persisted body serializes exactly as generated create would serialize it before sending.
- Project-only `list` removes only the timeline coordinate from the comparison; realm, actor and project still participate. Explicit owner recovery and generation fencing remain. A random reserved timeline can be found before a URL or server row exists. This is source inspection plus the source-refresh discovery test inspection, not a fresh discovery run here.
- Dispatch returns the original pending request before invoking a builder, so neither create nor commit retry allocates a new key, changes its base/guards/IDs, or recaptures against today's head. Existing unsent/dependent/rejected intents, acknowledged revision/publication identity, independent suffixes and unknown-flight fencing retain their original logic. Existing outbox tests are additions-only: zero original test lines removed.
- Creation ACK retains the original request/defaults. The first init ACK records `{intent, request, head, value}` atomically with prefix removal and dependent-base advancement. Later ACKs can replace `accepted` without replacing `initialization`. Existing opaque owner fields survive the read/modify/write clone; the added continuation test proves storage preservation for render/placement JSON, not the entire render/placement lifecycle.
- Before fresh capture, the adapter checks original H0 pair, sole bootstrap history, scope/receipt/payload/digest and immutable empty closure. After ACK it checks original base/commands/result/receipt against historical publication and immutable parent, including paginated history; then it loads today's verified basis. Local kind tags alone are not completion authority. Later edit/undo/equal-byte restore cannot reinstall defaults. Headless create remains incomplete, with the original flight retained.
- Capture source matches Agent `487ca1e0d74edf4aecdd2b4e045294ab089fc273`: raw-parent read, four absence reads, field writes including `registry.assets` ABSENT→`{}`, and sequential whole-entity V1/A1 creates with membership/order/identity guards. Both golden commands and full records are structurally identical to that Agent commit's `pristine_initialize.json`. App golden SHA256 is `2fe871c23c9b1a38ae44d7c1374c8b7a81128a7b320925bd6e4daef4500dea02`. Existing MoveRecording supplies the same claims; unsupported nonpristine content refuses unchanged. Authored empty/whitespace/long names remain in persisted defaults/capture while unsupported optional create names are omitted.
- The entire active helper and its test file are byte-identical to normal013Root: all seven original positives (reuse, fresh defaults, same-ID null-head shell repair, reassigned Main, concurrent chat/CAS, additional named timeline, stable lost-ACK retry), the opaque-headed positive and Main alias/CAS bodies are unchanged. Comparing with origin/main shows only the already-existing added opaque-headed test; the helper itself is also byte-identical to origin/main. No passing behavior was changed to refusal.

## Four native expected failures: policy, not demonstrated independence defect

The only added expected-failure marker is one Python `@pytest.mark.xfail(strict=True)` over four newly added opaque-parent vectors. It names the preservation requirement and retains the original successful-inverse assertions. There are no added App/Vitest failure, skip or only markers, and no old passing test was weakened.

I ran precisely those unchanged four vectors with `--runxfail`: all fail with `CommandError(kind='inverse_dependency_changed')` at `inverse.py:330`, for `parent`, path `[]`. The native initializer intentionally calls `ctx.read('parent')` and requires exact pristine empty bytes. After reversing the four initializer writes, `parent.opaque` still differs from that recorded whole-parent input. `_validate_inputs` therefore correctly detects a changed recorded dependency. The earlier 31d initializer read selected fields and omitted the root guard; its behavior is not evidence that the guarded successor has an inverse algorithm bug. The Agent handoff explicitly documents the complete raw-parent guard.

These vectors mutate the native bundle directly; they do not demonstrate a legal Runtime publication, lost data, a changed independent *unread* property, or a provider-history/CAS bypass. Strict pristine entry/replay and ordinary inverse dependency validation are separate checks: the inverse failure comes from the recorded raw-parent dependency, not an attempt to run init again. The changed property is outside the write set but inside the deliberate read set. Thus these four failures establish the narrower fact that undo is refused after any such parent change; they do not establish a new native blocker under the settled strict policy. An alternative policy allowing that undo would need an Agent-owner decision, not an App guard omission or blanket inverse-check exception.

No blocker was appended to the existing current-contract audit. The source-refresh report's “new native semantic difference” is reproducible, but should not be promoted to an independent-property defect on this evidence. These strict xfails are not green release evidence and remain unchanged in this review.

## Fresh checks

Run from `/home/user/work/wt/app-m2-bootstrap-prerequisite-independent-review`. Exact path abbreviation:

```sh
REVIEW_NOTES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-prerequisite-independent-review/notes
```

```sh
node node_modules/vitest/vitest.mjs run --config "$REVIEW_NOTES/vitest.config.mjs" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

**Exit 0: 2 files, 104 passed.** Covers exact retry, ACK/reservation rollback, dependent intents, original init proof after later ACK, opaque continuation JSON preservation, owner fencing, and accepted pair identity. Session tests inject an in-memory Transport; no socket/server was started.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$REVIEW_NOTES/agent-487" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --runxfail src/tools/video-editor/commands/fixtures/bootstrap_parity.py -k test_inverse_preserves_unrelated_opaque_parent_fields
```

**Exit 1 as intended: 4 failed, 8 deselected**, all `inverse_dependency_changed`. One unknown integration-mark warning originates in an imported frozen helper module; no integration test ran. No source or assertion was changed to reproduce the failures.

```sh
git diff --check
```

**Exit 0.** Additional read-only Git byte comparisons and JSON equality checks establish the source identities above. Fresh commands/logs and private config are retained under this worker's notes. The private config copies normal config behavior, fixes runner-mode `__dirname`, redirects Composition to an own 0.0.12 copy and cacheDir to this worker. Frozen Agent source was extracted from Git. Shared deps/venvs were read-only; no installs. Extracted source/package/cache temporary directories were removed afterward.

No full, browser, sockets, build, tsc or central service request ran. Bootstrap adapter/capture positives and native/provider passing suites were inspected but not rerun; the source-refresh report's 345 App / 27 provider / 8 native passes remain historical evidence, not fresh results here. No real Runtime admission, physical browser durability, process restart, or consumer cutover is qualified by this review.

## Exact next release gate

1. Agent/Runtime owners produce and freeze the **normal013-successor full additive matched release**, incorporating the guarded native initializer without dropping any normal013 schema/operation/compatibility behavior, and regenerate/register the ordinary consumer contract/provider. Frozen 487 alone and an App string op are insufficient.
2. Qualify through the real normal Door: create → tracked H0 → scoped bootstrap history/immutable reads → init commit, original create/init exact retry before semantic execution after restart, changed-payload rejection, history/CAS pristine refusal, and the **same-ID truly null/no-head shell repair positive**, while retaining nonempty/opaque/archived/foreign-project denial. Unpublished-revision adoption alone does not meet the null-head positive.
3. Only then wire the existing generated create mutation wrapper, all existing helper callers and project-scoped owner recovery, preserving current ID/name/Main alias/CAS behavior. The same consumer change must pass central named App/Runtime journeys for all seven positives, both lost/unpersisted ACK boundaries, restart/reload, later edit/undo/equal-byte restore and zero composition-publisher traffic. Publisher deletion and direct retired-writer rejection land in that qualified step.

The orchestrator selects/submits those central release runs; this bounded review did not request them. No implementation work is blocked here; production activation remains on HOLD at the existing release gate. No writer is retired by this prerequisite.
