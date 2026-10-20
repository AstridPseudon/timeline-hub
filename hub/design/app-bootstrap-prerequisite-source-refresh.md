# Bootstrap prerequisite source refresh

Completed source-only on App `171a259acbeb3ced855ca8f72fed0943a2f5a5cb` (final013/public12 root). PLAN and `design/app-bootstrap-current-contract-audit.md` were read first. No production activation or writer retirement is claimed.

## Changes and sources

- Ported the narrow existing outbox extension from corrected App `3a1d9c8524f37a2960d37d1b892d041b4c19ed0b`: exact durable pre-create reservation, project-scoped owner discovery, creation acceptance, and original initialization intent/request/head/result retention in the same ACK transaction/store. Existing intent, retry, dependent-prefix, rejection, lock/generation and recovery logic remains. Opaque render/placement continuation fields survive ACKs and reopen.
- Ported its unwired `bootstrapInitialization` adapter and direct tests. Completion verifies the original request/result against scoped history and immutable closure, then loads today's basis. A local completion marker alone is refused. Later edit/inverse/restore ACKs retain the original initialization proof.
- Refreshed pure `bootstrapCapture` and golden against actual extracted Agent `487ca1e0d74edf4aecdd2b4e045294ab089fc273`, including raw-parent read, four absence reads, and `parent.registry.assets` ABSENT → `{}`. Commands and full records equal that commit's own `tests/editing_conformance/fixtures/pristine_initialize.json`; inverse/redo match fresh native execution. Fixture SHA256: `2fe871c23c9b1a38ae44d7c1374c8b7a81128a7b320925bd6e4daef4500dea02`.
- Empty, whitespace, surrounding-whitespace and long authored names are preserved exactly. For these names the optional create name is omitted, while original authored name/slug/defaults remain durable and feed native capture. Explicit unsupported create names still refuse before POST.
- Added/retained direct tests for pre-POST reservation, storage failure/no POST, lost/unpersisted ACK exact retry, scoped discovery, atomic original initialization retention after later ACKs, malformed proof, current-history checks and name recovery.

Changes are confined to `runtime/bootstrapInitialization`, `commands/bootstrapCapture`, `commitOutbox` and direct tests/fixtures. The active helper and its tests, client, generated contracts, commit session, package.json and lock were explicitly compared byte-for-byte with HEAD and are unchanged. Main alias resolution/CAS and all seven original positive requirements stay on the existing publisher path. No create wrapper, caller activation, wire/op/DTO change, second journal or native registration was added.

## Validation

Commands ran from `/home/user/work/wt/app-m2-bootstrap-prerequisite-source-refresh`. Shared node_modules/venvs remained read-only. One private Composition 0.0.12 extraction was aliased from the private config; no dependency installs or shared symlink/cache edits. Vitest used one worker, `--no-cache`, `--configLoader=runner` and a private cacheDir.

The following variable expansions abbreviate the exact paths used by the commands:

```sh
BOOTSTRAP_NOTES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-prerequisite-source-refresh/notes
```

```sh
node node_modules/vitest/vitest.mjs run --config "$BOOTSTRAP_NOTES/vitest.config.mjs" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts
```

**4 files / 127 passed.** Includes unchanged active helper positives.

```sh
node node_modules/vitest/vitest.mjs run --config "$BOOTSTRAP_NOTES/vitest.config.mjs" --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/commitSession.test.ts src/integrations/runtime/timelineCommit.test.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/commands/authoringBundle.test.ts
```

**4 files / 218 passed.** Total App: **345 passed**.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$BOOTSTRAP_NOTES/agent-487" /home/user/work/venv-agent/bin/python src/tools/video-editor/commands/fixtures/bootstrap_parity.py
```

**8 passed / 4 strict xfailed.** Captures/records, native golden equality, exact inverse/redo/replay, authored names and guarded output edits pass. The four xfails are explained below.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$BOOTSTRAP_NOTES/agent-487" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider "$BOOTSTRAP_NOTES/agent-487/tests/editing_conformance/test_pristine_initialize.py" "$BOOTSTRAP_NOTES/agent-487/tests/sdk/test_timeline_pristine_initialize_provider.py"
```

**27 passed.** Actual frozen native/provider suites include bootstrap-history, equal-byte undo/reinitialization and CAS-retry checks. Their DetachedRealm/fake ABI setup is source-level provider evidence, not real Runtime admission.

```sh
node node_modules/eslint/bin/eslint.js src/integrations/runtime/bootstrapInitialization.ts src/integrations/runtime/bootstrapInitialization.test.ts src/tools/video-editor/commands/bootstrapCapture.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitOutbox.test.ts --max-warnings 0
git diff --check
```

**Both passed.** New files also checked for trailing whitespace. No full suite, project tsc, browser, server/socket suite or central suite requested/run.

Initial private Vitest config attempts stopped before tests because runner mode does not define `__dirname`. The private copies replace it with the original absolute directories, retaining the normal config/plugin/setup behavior. Initial native parity failed on the unrelated-opaque inverse probe; its original successful-behavior expectation is retained under strict xfail, not rewritten to refusal.

## Findings, decisions and remaining gate

**New native semantic difference:** the old 31d native parity probe expected bootstrap inverse to preserve a later unrelated `parent.opaque` field (`null`, false, array and opaque object). Actual 487 rejects all four with `inverse_dependency_changed` because its newly recorded raw-parent read changed. The intended successful inverse assertions remain, with `@pytest.mark.xfail(strict=True)` and a comment naming the preservation requirement. No Agent changes or alternate guard policy were introduced. Orchestrator/Agent owner should assess this additional inverse dependency before activation; this source prerequisite is otherwise complete.

Activation remains gated by a real generated/registered matched full additive init release (current final013 does not include init), constrained same-ID truly null/no-head repair, and central normal Door/App journeys. No actual Runtime create/H0/commit admission, browser disk crash, process restart, metadata cutover or zero legacy traffic was verified here. The App tests use fake IDB and mocked authority; their crash/reopen coverage is logical durability evidence.

Recommended next: qualify the matched native successor and null-head repair; resolve/review the opaque-inverse finding; then add the ordinary create wrapper and wire all callers/project discovery while keeping main alias/CAS selection. Only the same qualified consumer migration may delete the publisher. Do not claim any writer retired from this PR.
