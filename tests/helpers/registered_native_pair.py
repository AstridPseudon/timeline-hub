"""Private generated qualification pair; public contracts and dependencies stay read only."""
from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile

from tests.helpers.runtime import runtime_checkout

AGENT = 'b5cfce5096f91f39bfb86d39823f97f0f59ce8a2'
RUNTIME = '2c4ac180c2220bdad966bc01e95ad230e99ce26a'


def prepare_pair(source, root):
    """Use reviewed native source and all S2 clauses, then the normal generators."""
    agent, runtime = root / 'agent', root / 'runtime'
    for repo, commit, target in ((source, AGENT, agent), (runtime_checkout(), RUNTIME, runtime)):
        raw = subprocess.check_output(['git', '-C', str(repo), 'archive', commit])
        target.mkdir()
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            archive.extractall(target, filter='data')
    overlays = ('astrid/core/contracts/runtime_orchestration.py',
                 'astrid/core/execution/generic_host.py', 'astrid/sdk/workspace_client.py',
                 'astrid/sdk/timeline/assembly.py', 'astrid/sdk/timeline/sync.py',
                 'astrid/packs/rendering/pack.yaml',
                 'astrid/packs/rendering/actions/assemble_timeline/run.py',
                 'tests/packs/rendering/test_registered_native_assembler.py',
                 'tests/packs/rendering/test_registered_proposal_requester.py',
                 'tests/packs/rendering/test_registered_assembler_admission.py',
                 'tests/packs/rendering/test_registered_assembler_producer.py')
    for name in overlays:
        shutil.copyfile(source / name, agent / name)
    schema = agent / 'astrid/core/timeline/schema/edit-command.schema.json'
    shutil.copyfile(schema, runtime / 'contract/schemas/edit-command.json')
    (runtime / 'generators/release.json').write_text('{"contract_version":"0.2.14"}\n')
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONPATH': str(runtime)}

    def run(*args):
        subprocess.run(args, cwd=runtime, env=env, check=True)

    run(sys.executable, 'generators/generate.py')
    generated = root / 'conformance'
    command = ('node', 'tools/generate_typescript_conformance.mjs', '--contract',
               'contract/openapi/workspace-v1.yaml', '--schema-manifest', 'contract/manifest.json',
               '--component-manifest', 'contract/component-manifest.json')
    run(*command, '--output-root', str(generated))
    for client in json.loads((runtime / 'contract/component-manifest.json').read_text())['clients']:
        if client['language'] == 'typescript':
            for output, dest in (('output', 'source'), ('metadata_output', 'metadata_source')):
                shutil.copyfile(generated / client[output], runtime / client[dest])
    run(sys.executable, 'scripts/artifact_manifest.py')
    run(sys.executable, 'generators/generate.py', '--check')
    run(*command, '--fixture-root', 'conformance/fixtures', '--check')
    run(sys.executable, 'scripts/artifact_manifest.py', '--check')
    # Copy the normally generated client into this disposable pair only. This is
    # an uncommitted candidate, so it cannot be a source_commit or public lock update.
    manifest = json.loads((runtime / 'contract/artifacts.json').read_text())
    for name, digest in manifest['artifacts'].items():
        assert 'sha256:' + hashlib.sha256((runtime / name).read_bytes()).hexdigest() == digest
    for path in (runtime / 'packages/python/astrid_runtime_client').glob('*.py'):
        shutil.copyfile(path, agent / 'astrid_runtime_client' / path.name)
    print(json.dumps({'agent_source': AGENT, 'runtime_source': RUNTIME,
                      'private_contract_version': '0.2.14',
                      'schema_sha256': hashlib.sha256(schema.read_bytes()).hexdigest(),
                      'artifact_manifest': manifest['version'],
                      'overlay_sha256': {name: hashlib.sha256((source / name).read_bytes()).hexdigest()
                                         for name in overlays}}, sort_keys=True), flush=True)
    return agent, runtime
