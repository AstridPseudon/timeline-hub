# Commands and recovered native witness

## Recovered exact prior witness command

The prior worker's last successful command was recovered from
`workers/vw-m3-native-inactive-fixture-witness/log.txt` lines 7569–7622.
It ran against Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` and Agent
`d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, using the worker's flattened
`handoff-vw-m3-frame-retained-genesis-fixture-fixture.py` and
`handoff-vw-m3-frame-retained-genesis-fixture-proposal.py`.

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B - <<'PY'
import copy, hashlib, importlib.util, io, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path
RUNTIME_REV = '2c4ac180c2220bdad966bc01e95ad230e99ce26a'; AGENT_REV = 'd8749a9ce12a699672faf3ad96b4e4cbea9245c2'
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design'); PREFIX = ORCH / 'handoff-vw-m3-frame-retained-genesis-fixture-'; root = Path(tempfile.mkdtemp(prefix='native-inactive-witness-', dir='/tmp'))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
def archive(repo, rev, paths, dest):
    data = subprocess.check_output(['git', '-C', repo, 'archive', rev, *paths])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive_file: archive_file.extractall(dest, filter='data')
def cas_files(service): return sorted(str(path.relative_to(service.store.cas_root)) for path in service.store.cas_root.rglob('*') if path.is_file())
def object_items(service, project): return service.list_project_objects(project)['items']
def stable_integrity(report):
    report = copy.deepcopy(report); report.get('checks', {}).get('deep_verification', {}).pop('verified_at', None); return report
try:
    source = root / 'source'; source.mkdir(); archive('/home/user/work/runtime', RUNTIME_REV, ['runtime_protocol', 'packages/python'], source); archive('/home/user/work/agent', AGENT_REV, ['astrid', 'pyproject.toml'], source)
    shutil.copy2(str(PREFIX) + 'fixture.py', source / 'handoff-vw-m3-frame-retained-genesis-fixture-fixture.py'); shutil.copy2(str(PREFIX) + 'proposal.py', source / 'handoff-vw-m3-frame-retained-genesis-fixture-proposal.py'); sys.path[:0] = [str(source), str(source / 'packages/python')]
    fixture = load('retained_fixture', source / 'handoff-vw-m3-frame-retained-genesis-fixture-fixture.py'); proposal = load('retained_proposal', source / 'handoff-vw-m3-frame-retained-genesis-fixture-proposal.py')
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider
    from runtime_protocol.util import canonical_json
    realm = root / 'realm'; prepared = proposal.prepare_inactive_realm(realm, fixture.build_fixture); document = prepared['fixture']['canonical_document']; project, timeline = document['project_id'], document['timeline_id']; request = fixture.restore_request(document, prepared['head']); path = f'/v1/projects/{project}/timelines/{timeline}/commit'
    service = RuntimeService(realm); service.register_timeline_commit_provider(load_timeline_commit_provider('astrid'))
    try:
        result = service.commit_timeline(project, timeline, request, idempotency_key='image-cap-restore', publisher='fixture-owner-test', invocation_path=path, authorize=service._assert_mutation_admitted); assert canonical_json(result['data']['canonical_document']) == canonical_json(document)
        accepted_head = service._timeline_commits()[0].head(project, timeline); assert accepted_head == {'revision_id': result['data']['accepted_revision_id'], 'publication_id': result['receipt']['receipt_id']}; service.close()
        service = RuntimeService(realm); service.register_timeline_commit_provider(load_timeline_commit_provider('astrid')); retry = service.commit_timeline(project, timeline, request, idempotency_key='image-cap-restore', publisher='fixture-owner-test', invocation_path=path, authorize=service._assert_mutation_admitted); assert retry == result
        closure = service._timeline_commits()[0].revision_closure(project, timeline, document['parent_revision']['revision_id']); assert canonical_json(closure) == canonical_json(document); assert service._timeline_commits()[0].head(project, timeline) == accepted_head; assert service.store.integrity_report()['ok']; print('RESTORE PASS: native inactive realm setup, restore, exact retry after restart, byte-identical closure/head/integrity')
        capability = 'rendering.timeline_visualize'; capability_digest = 'sha256:' + hashlib.sha256(capability.encode()).hexdigest(); service.register_capability({'capability_id': capability, 'definition_digest': capability_digest}); service.register_executor({'executor_id': 'fixture-probe', 'capabilities': [capability]})
        projection = service._timeline_commit_provider.project_capture(document); parent = document['parent_revision']; authority = {'project_id': project, 'timeline_id': timeline, 'parent_revision_id': parent['revision_id'], 'parent_content_digest': parent['content_digest'], 'expansion': projection['expansion']}; snapshot = {'config': projection['config'], 'registry': projection['registry'], 'metadata': {'capture_authority': authority, 'canonical_timeline': authority}}
        def request_for(value, key):
            context = {'mode': 'composed_capture', 'project_id': project, 'timeline_id': timeline, 'revision_id': parent['revision_id'], 'capture_snapshot': value}; return {'project': project, 'capability_id': capability, 'capability_digest': capability_digest, 'input_object_ids': [], 'idempotency_key': key, 'spec': {'authority_context': context, 'inputs': {'filmstrip_authority': canonical_json(context)}}}
        baseline_objects, baseline_cas = object_items(service, project), cas_files(service); positive = service.create_task(request_for(snapshot, 'image-cap-capture-positive')); saved_ref = positive['task']['spec']['spec']['authority_context']['capture_snapshot_ref']; assert saved_ref['source_kind'] == 'revision' and service.object(saved_ref['digest'])[1]; print('CAPTURE POSITIVE PASS: normal create_task saved server snapshot ref ' + saved_ref['digest']); assert len(object_items(service, project)) == len(baseline_objects) + 1 and len(cas_files(service)) == len(baseline_cas) + 1
        mutations = {'config': lambda value: value['config']['clips'].__setitem__(0, {**value['config']['clips'][0], 'hold': 99}), 'registry': lambda value: value['registry'].__setitem__('forged_registry', {'media_id': 'sha256:' + '0' * 64}), 'digest': lambda value: value['metadata']['capture_authority']['expansion']['shots'][0].__setitem__('content_digest', 'sha256:' + '0' * 64), 'missing-media': lambda value: value['registry']['assets'].__setitem__('image-occurrence:image', {**value['registry']['assets']['image-occurrence:image'], 'media_id': 'sha256:' + '0' * 64})}
        for label, mutate in mutations.items():
            value = copy.deepcopy(snapshot); mutate(value); before_objects, before_cas, before_integrity = object_items(service, project), cas_files(service), stable_integrity(service.store.integrity_report())
            try: service.create_task(request_for(value, 'image-cap-capture-negative-' + label))
            except RuntimeErrorBase as exc: message = str(exc)
            else: raise AssertionError(label + ' mutation was admitted')
            assert object_items(service, project) == before_objects and cas_files(service) == before_cas and stable_integrity(service.store.integrity_report()) == before_integrity
            print(f'CAPTURE NEGATIVE PASS: {label} refused before CAS/task writes: {message}')
    finally:
        try: service.close()
        except Exception: pass
finally: shutil.rmtree(root, ignore_errors=True)
PY
```

## Recovered six PASS stdout lines

```text
RESTORE PASS: native inactive realm setup, restore, exact retry after restart, byte-identical closure/head/integrity
CAPTURE POSITIVE PASS: normal create_task saved server snapshot ref sha256:bac1004db17ee73de4d7a6ff437944bcc7e7b7666ecd4418d88ddf6fde429a21
CAPTURE NEGATIVE PASS: config refused before CAS/task writes: capture differs from authoritative config
CAPTURE NEGATIVE PASS: registry refused before CAS/task writes: capture differs from authoritative registry
CAPTURE NEGATIVE PASS: digest refused before CAS/task writes: capture expansion differs from authoritative projection
CAPTURE NEGATIVE PASS: missing-media refused before CAS/task writes: capture differs from authoritative registry
```

## This worker's commands

```text
npx eslint tests/e2e/local/support/harness.ts tests/e2e/timeline/viewing-parity/fixture.ts tests/e2e/timeline/viewing-parity/harness.ts tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts --report-unused-disable-directives --max-warnings 0
node --import tsx --test tests/e2e/timeline/viewing-parity/harness.test.ts tests/e2e/timeline/viewing-parity/media.test.ts tests/e2e/timeline/viewing-parity/canvas.test.ts tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts
R=$(.../request-test vw-m3-frame-native-retained-fixture-port integration-viewing-native-retained-fixture) && .../wait-test "$R"
```

Central result: **1 pass, 0 fail**. No browser, render, full suite, install,
network, or shared-dependency writes were used.
