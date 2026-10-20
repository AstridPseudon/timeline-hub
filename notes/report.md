# Current-tuple fixture bootstrap review

**Result: a new official paired cohort with a lossless public fixture-authoring recipe is required.** No supported recipe in the inspected current sources constructs the complete historical fixtures. Updating pins alone, or adopting the narrow `timeline.init` candidate alone, is insufficient. This review is complete; the current consumer gate remains blocked. Manager owns escalation and sequencing.

Only this report and a single `.gitignore` exception retaining it were added (the repository otherwise ignores `*.md`). No product, harness, assertion, generated contract, allowlist or dependency changed. No fallback writer, snapshot restore, test-only provider or fabricated acceptance/manifest was introduced.

## Sources and fixed identities

Read `PLAN.md`, `escalations/app-20261020T0505Z-current-paired-gate-retired-seed.md` and `managers/app/notes/opaque-paired-gate.md` first. Read current source through the integration directories and candidates through `git show`/a temporary `git archive`; did not change their worktrees.

| Source | Identity / contract |
| --- | --- |
| Assigned App | `5912bfc3284da03112ef6c235447cfbeffb678bd`; client 0.2.1, schema `4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d` |
| Current Agent | `4a75f68f`; same client 0.2.1/schema `4e52…` |
| Escalated Runtime | `fe756c83c04b030edbf2f6cf9d764e3c2a1b7e4e`; client 0.2.7, schema `7486348fccf16b9104aa47d2076b68d1163931f765d8a4e7ec29415b5083bf22` |
| Runtime current during review | Initially `78dfe2f`, advanced to `e068f27dac058b499716671db93e459fc7b656f7`; the latter publishes client **0.2.8**, schema `a4e1eebd0c86423db187a92198e9c47fa52063834101ee18af1ee10726afea4a` |
| Agent native-init candidate | `31d02d45ad21f452724091b94b285478d00c9c21`; still vendors client 0.2.1; not integrated/current-release qualification |
| Runtime trusted-bootstrap candidate | `382f523ef957afb2bd299c5e21424ca821b23f05`, `tests/timeline_trusted_bootstrap.py`; referenced by Agent candidate `eaa89740` |

Both pinned Runtime releases retain the exact empty bootstrap and the retired publication boundary. Advancing from 0.2.7 to 0.2.8 did not resolve this fixture problem. The old App session checks accept only `4e52…` (`src/integrations/runtime/contract-metadata.ts`, `client.ts:446`); they must fail closed on either Runtime release. The raw harness seed encounters its 410 before reaching that App session check. Agent's provider factory imports the Runtime digest dynamically (`astrid/sdk/timeline/commit.py:546`); successful ABI loading alone would not establish matching published clients or missing command semantics.

## Where setup stops, and what cannot be discarded

`tests/e2e/local/support/harness.ts:550` creates a project, then sends its first `compositionPublication` to `POST /v1/projects/{project}/timelines/{timeline}/composition-revisions` at line 556. This precedes object ingestion. The supplied central result `restore-opaque-current-integration-1020050237-11837` reports 410 `retired_route`, reason `timeline_commit_required`; it reached no move/save/restore assertions. I did not rerun or relabel that result. The separately reported accepted-M1 compatibility pass 17865 remains historical compatibility only.

The legal collection create is **not** a replacement for the whole seed:

- Runtime `contract/openapi/workspace-v1.yaml` → `CreateTimeline` allows only `{timeline_id, name?}`. `runtime_protocol/server.py:492` rejects extra fields; the normal generated method is `createTimeline`, not a nonempty snapshot-create variant.
- With the startup semantic provider installed, `service.py:1651` atomically creates H0 and its separate publication receipt. `timeline_commit_baseline.empty_bootstrap_document` supplies exactly `{config:{clips:[],tracks:[]}, registry:{}, clips:[], occurrences:[]}`, no children and empty dependency lists. The returned `head_publication_id` is distinct from the `timeline.create` receipt ID.
- The old first seed additionally authors parent `name`, `slug`, output `{resolution:'1280x720', fps:30, file:'out.mp4'}`, V1 and `{assets:{}}`. Its output **omits** background/background_scale; replacing absence with null changes the authored payload.
- `seedThreeProducts` (`harness.ts:685-742`) then needs the full parent config and clips, V1/S1 ordering, `config.x_f2_opaque`, the incoming crossfade on `f2-transition-clip`, real image/video registry identities/digests, `f2-shot` with its immutable shot→internal revision link, `f2-occurrence` with the original placement/source offset/duration/speed/transform/gain/mute/provenance, and all shot payload fields. Its internal payload includes the plate and both Agent clips, their timing/tracks/registries, and `app.f2Opaque`. Empty collections and unknown values must survive too.
- `three-products.spec.ts:151-185` follows the real parent→shot→internal links and checks opaque data in every later revision. A parent-only fixture, replacement child IDs, shortened graph or removed transition/media case changes the requirement. `seedMedia` and `seedExtensions` also use the retired publisher; media bindings, transcript bundle and live-scene package/source objects remain requirements for those consumers.

## Native init and trusted setup do not supply the missing operation

Current Agent `astrid/sdk/timeline/commands.py:34-64` registers only `clip.move` and `track.create`, with inverse/restore handled separately. Direct execution of its real validator refused `timeline.init`, `clip.add`, and `test.trusted-legacy-bootstrap` as `unsupported_operation`. Track creation cannot author parent output, config opaque fields, clips, assets, shots or occurrences. Inverse/restore require existing accepted history and cannot originate the missing film.

Candidate `31d02d45` adds exactly `timeline.init` v1 through `astrid/core/timeline/schema/edit-command.schema.json` → `TimelineInitArgs` and `astrid/sdk/timeline/_init_commands.py`. Its closed arguments are **name, slug, output**; output requires resolution, integer fps, file, background and background_scale. It records only `config.output`, `name`, `slug`, and `registry={assets:{}}`, and refuses a parent other than the exact pristine empty bootstrap. Its 32 native conformance cases passed here. The real schema rejects the unchanged historical first-seed output because both background keys are absent, and rejects additional config/shot/internal/occurrence arguments. It has no graph import or opaque-root initialization contract. Do not widen it in App or reinterpret a track row as a root writer.

Candidate `382f523` explicitly says “Never submit that operation to a product endpoint.” `seed_trusted_legacy_parent` validates `CanonicalDocument`, then rejects any shot revisions, internal revisions or parent occurrences, and also requires legacy `config.pinnedShotGroups`. It uses private `_timeline_commits`, an authored `test.trusted-legacy-bootstrap` operation, a whole-parent recorded replacement and direct `commits.accept`. This is Runtime storage-boundary test setup, not a supported public Agent command. It cannot accept the three-products graph even in its intended lane. I inspected it; I did not execute it or adapt its guard/provider/manifest. Current Agent's real validator independently rejects its opname.

Current Runtime also already permits collection POST in `runtime_protocol/door.py` (`GET,POST /v1/projects/:/timelines`), including at fe756c83. The older bootstrap review's GET-only Door observation is therefore resolved in these inspected sources; no allowlist change is needed. Its truly no-head same-ID adoption limitation remains: `adopt_empty_shell` rejects no head row/null revision. That is separate from creating a new harness timeline and is not authorization to change the preserved App repair positive.

## One recommended owner handoff

**Agent editing manager owns the missing semantic recipe; Runtime manager owns its official request/closure schema and paired release; App manager owns later harness adoption.** Supply one reviewed, published cohort containing the recipe and compatible clients, then migrate setup through normal create→command commit. Do not revive the publisher.

Required handoff, before App implements anything:

1. Agent supplies exact supported operation names/versions, native capture functions, and parameter schemas/goldens from `astrid/core/timeline/schema/edit-command.schema.json` plus their registered handlers. `timeline.init` v1 is identified above but is insufficient. Missing contracts must losslessly originate the historical parent config/output/opaque fields, clip/asset/track rows, immutable shot/internal graph and occurrence links, including all original child payload fields. Preserve source absence/null distinctions. No exact public operation providing those capabilities exists in the inspected current registry; **do not invent its name or DTO in App**. Whether existing candidate commands compose into that recipe is Agent's qualification task, not permission for a generic root replacement.
2. Runtime publishes the matching projection in `contract/schemas/edit-command.json`, the existing `timeline-commit.json`/`timeline-commit-bundle.json` closure and `shot-composition.json` definitions as applicable, generated clients/metadata/artifact locks, and a fixed source tuple retaining current safety guards. Agent/App consume those exact published bytes. Schema pin alignment without the semantic recipe is insufficient.
3. Seed stage: retain project creation and real object ingestion; create the empty timeline using `createTimeline` and a stable request/key; retain and verify the original H0 revision/publication pair and bootstrap history. Capture the owner-supplied fixture commands in authored order, with stable preallocated fixture identities and actual managed-media references, then submit through `commitTimeline` at H0 with one unchanged retry identity. Use only the returned/immutable-read real closure and manifest. Do not derive an accepted manifest in the harness. Preserve the original first initialized seed revision and subsequent three-products revision/history roles; creating H0 must not skip the authored seed stage.
4. Before consumer qualification, compare the entire authored parent/child graph against the original fixture (with only legitimate project/media/revision identity binding), then retain every current opaque, transition, source-binding and media assertion. Exact retry/restart and undo must keep the graph intact. Manager can authorize one bounded central no-browser consumer run on the fixed paired cohort; this review requested none.

Expected strict refusals remain: authenticated legacy publication 410 `timeline_commit_required`; incompatible client session `runtime_incompatible`; unsupported current Agent operation `unsupported_operation` (provider maps semantic errors to 409 refused); invalid closed init arguments/schema rejection; non-pristine init `not_pristine`; no-provider semantic commit unavailable (503); occupied/mismatched/headed/nonempty same-ID adoption conflict with no writes. Never recapture init at an advanced head merely because undo restored empty bytes: retain original H0/request and intervening-history guards. These are source/validator expectations here, **not new HTTP/service acceptance evidence**.

## Executed checks

From this App worktree, unchanged main-suite tests:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/integrations/runtime/createDefaultTimeline.test.ts src/integrations/runtime/timelineCommit.test.ts --maxWorkers=2
```

**PASS: 2 files, 46 tests, 2.83s.** All seven existing creation positives remain unchanged. These use fixture transports and do not qualify current Runtime setup.

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/integrations/runtime/client.test.ts --maxWorkers=2 -t 'fails closed on a Runtime schema digest mismatch|fails closed on a stale additive Runtime contract'
```

**PASS: 2 selected tests, 1.54s; Vitest reports 23 skipped by the name filter.** No test source/skip marker was changed.

Native candidate suite, exact command (temporary archive removed automatically):

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python - <<'PY'
import io
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path
with tempfile.TemporaryDirectory(prefix='.native-init-', dir=Path.cwd() / 'notes') as target:
    archive = subprocess.check_output(['git', '-C', '/home/user/work/agent', 'archive', '31d02d45ad21f452724091b94b285478d00c9c21'])
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        source.extractall(target, filter='data')
    environment = {**os.environ, 'PYTHONPATH': target, 'TMPDIR': target, 'PYTHONDONTWRITEBYTECODE': '1'}
    result = subprocess.run(['/home/user/work/venv-agent/bin/python', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
        'tests/editing_conformance/test_timeline_init.py', '--basetemp', str(Path(target) / '.pytest-tmp')],
        cwd=target, env=environment)
    raise SystemExit(result.returncode)
PY
```

**PASS: 32 tests, 0.61s.** Native candidate only; no Runtime, socket or official-release acceptance claim.

Read-only current-engine probe, exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python - <<'PY'
import json
from pathlib import Path
from astrid.sdk.timeline.commands import operations, validate_command
from astrid.sdk.timeline._command_state import CommandError
from astrid_runtime_client.contract_metadata import CONTRACT_VERSION, SCHEMA_DIGEST
print('Agent source:', Path(__import__('astrid.sdk.timeline.commands', fromlist=['x']).__file__))
print('Agent client:', CONTRACT_VERSION, SCHEMA_DIGEST)
print('Agent registered operations:', sorted(operations()))
commands = [
    {'schema_version': 1, 'op': 'timeline.init', 'version': '1', 'select': 'parent',
     'args': {'name': 'Main', 'slug': 'main', 'output': {'resolution': '1280x720', 'fps': 30,
              'file': 'out.mp4', 'background': None, 'background_scale': None}}},
    {'schema_version': 1, 'op': 'clip.add', 'version': '1', 'select': 'parent', 'args': {}},
    {'schema_version': 1, 'op': 'test.trusted-legacy-bootstrap', 'version': '1', 'select': 'parent',
     'args': {'document_digest': 'sha256:' + '0' * 64}, 'created': []},
]
for command in commands:
    try:
        validate_command(command)
    except CommandError as error:
        print(command['op'], '=>', error.kind, str(error))
        assert error.kind == 'unsupported_operation'
    else:
        raise AssertionError('unexpected supported operation')
print('PASS: current semantic engine has no initializer, clip constructor or trusted-test operation')
PY
```

**PASS (exit 0):** registry `['clip.move','track.create']`; all three calls refused `unsupported_operation` before handler argument semantics. The synthetic digest above only exercises refusal of the helper opname; it is never a fixture, accepted document or manifest.

Read-only published-schema/source probe, exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python - <<'PY'
import ast
import json
import subprocess
from jsonschema import Draft202012Validator

def source(repo, revision, path):
    return subprocess.check_output(['git', '-C', repo, 'show', f'{revision}:{path}'], text=True)

def literal(repo, revision, path, name):
    for row in ast.parse(source(repo, revision, path)).body:
        if isinstance(row, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in row.targets):
            return ast.literal_eval(row.value)
    raise AssertionError(name)

runtime = '/home/user/work/runtime'
agent = '/home/user/work/agent'
for revision in ('fe756c83c04b030edbf2f6cf9d764e3c2a1b7e4e', 'e068f27dac058b499716671db93e459fc7b656f7'):
    path = 'packages/python/astrid_runtime_client/contract_metadata.py'
    version = literal(runtime, revision, path, 'CONTRACT_VERSION')
    digest = literal(runtime, revision, path, 'SCHEMA_DIGEST')
    print(revision[:8], version, digest)
    assert digest != literal(agent, '4a75f68f', 'astrid_runtime_client/contract_metadata.py', 'SCHEMA_DIGEST')
    tree = ast.parse(source(runtime, revision, 'runtime_protocol/timeline_commit_baseline.py'))
    function = next(row for row in tree.body if isinstance(row, ast.FunctionDef) and row.name == 'empty_bootstrap_document')
    payload = next(ast.literal_eval(row.value) for row in function.body if isinstance(row, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'payload' for t in row.targets))
    assert payload == {'config': {'clips': [], 'tracks': []}, 'registry': {}, 'clips': [], 'occurrences': []}
    print('  exact empty bootstrap:', json.dumps(payload, sort_keys=True))
schema = json.loads(source(agent, '31d02d45', 'astrid/core/timeline/schema/edit-command.schema.json'))
validator = Draft202012Validator(schema['$defs']['TimelineInitArgs'])
args = {'name': 'Main', 'slug': 'main', 'output': {'resolution': '1280x720', 'fps': 30, 'file': 'out.mp4'}}
errors = sorted(error.message for error in validator.iter_errors(args))
assert errors == ["'background' is a required property", "'background_scale' is a required property"]
print('Candidate init on unchanged historical seed output:', errors)
args['output'].update(background=None, background_scale=None)
assert not list(validator.iter_errors(args))
for field, value in [('config', {'x_f2_opaque': {'keep': True}}), ('shot_revisions', []), ('internal_timeline_revisions', []), ('occurrences', [])]:
    errors = list(validator.iter_errors({**args, field: value}))
    assert errors and any(error.validator == 'additionalProperties' for error in errors)
    print('Candidate init rejects graph/root argument:', field)
print('PASS: both Runtime releases mismatch current clients; empty create plus candidate init cannot reproduce the historical fixture')
PY
```

**PASS (exit 0):** both exact Runtime metadata mismatches, both exact empty payloads, both missing historical output keys and all four extra-argument refusals confirmed. This checks actual published source/schema, not service/database admission.

No full suite, browser, localhost/socket suite, build, tsc or install ran. No Runtime mutation or end-to-end current consumer was executed. No temporary archive/build output remains. The task's allowed notes-only outcome is intentional: an executable App seed helper would currently require an unsupported operation or a second writer.
