"""Explicit-only diagnostic: pytest tests/readiness_commits_probe.py.

Reconstructs the unexecuted 0125 probe using frozen fixture source, not old evidence.
No browser journey runs. Captures contain timings/stacks/identities, never credentials
or request/response bodies. The filename keeps this machine-specific probe out of
ordinary test discovery while permitting the central service's relative --files.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import time
from urllib.parse import quote
import urllib.error
import urllib.request
import uuid

import pytest

WORKTREE = Path('/home/user/work/wt/rt-R-readiness-probe-sol-0138')
SOURCE = Path(__file__).resolve().parents[1]
BASE = '2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d'
APP_FAILED = '804134d74782d40855146aa568ff289200b79142'
AGENT_FAILED = '079580ca46af77e0292d49dc34386b25c8391f99'
APP_P1 = 'f8b15af0a66ed14e7711a4bb7f1ed5b62b4988b5'
AGENT_P1 = '78738040d72ce74c42ddf7731221aecb06f9246d'
NODE = '/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node'
NODE_MODULES = Path('/home/user/work/app/node_modules').resolve()
APP_FILES = [
    'tests/e2e/local/support/harness.ts',
    'tests/e2e/local/support/astrid.ts',
    'tests/e2e/local/support/quick-descriptor.ts',
    'src/shared/lib/editorTourVersion.ts',
    'tests/e2e/local/three-products.p1-chain.spec.ts',
]


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def archive(repo, revision, destination, files=()):
    destination.mkdir()
    result = subprocess.run(['git', '-C', repo, 'archive', revision, *files],
                            check=True, capture_output=True)
    subprocess.run(['tar', '-x', '-C', str(destination)], input=result.stdout, check=True)


def events(capture):
    result = []
    for path in sorted(capture.glob('events-*.jsonl')):
        for line in path.read_text().splitlines():
            try:
                result.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # A live writer can have an incomplete final line.
    return result


def until_state(root, stages, process, seconds=150):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        state = read_json(root / 'state.json')
        if state and state['stage'] in stages:
            return state
        assert process.poll() is None, f'fixture exited {process.returncode}; private log: {root}'
        time.sleep(.025)
    raise AssertionError(f'fixture stage deadline; private log: {root}')


def get(state, suffix, *, door=False, preflight=False):
    start = time.monotonic()
    headers = {'Origin': state['origin']} if door else {
        'Authorization': 'Bearer ' + read_json(Path(state['credential']))['token'],
    }
    if preflight:
        headers.update({'Access-Control-Request-Method': 'GET',
                        'Access-Control-Request-Headers': 'content-type',
                        'Access-Control-Request-Private-Network': 'true'})
    req = urllib.request.Request((state['door'] if door else state['endpoint']) + suffix,
                                 headers=headers, method='OPTIONS' if preflight else 'GET')
    result = {'path': suffix.split('&cursor=')[0], 'door': door, 'preflight': preflight,
              'started': start}
    cursor = None
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            raw = response.read()
            value = json.loads(raw) if raw else None
            result.update(status=response.status, bytes=len(raw),
                          cors=response.headers.get('Access-Control-Allow-Origin'))
            if isinstance(value, dict) and 'items' in value:
                cursor = value.get('next_cursor')
                result.update(items=len(value['items']), has_cursor=bool(cursor), head=value['head'],
                              publications=[item['publication_id'] for item in value['items']])
    except urllib.error.HTTPError as exc:
        # Do not export the response body, which can contain request details.
        result.update(status=exc.code, error='HTTPError')
    except Exception as exc:
        result.update(status=None, error=type(exc).__name__)
    result.update(finished=time.monotonic(), seconds=time.monotonic() - start)
    return result, cursor


@pytest.mark.parametrize('mode', ['native21', 'p1'])
def test_history_conditions(mode):
    # Fixtures/archives stay in harness-cleaned TMPDIR; only safe captures are durable.
    scratch = Path(os.environ.get('TMPDIR', '/tmp/w-a1885cc6b0')) / f'readiness-{mode}-{uuid.uuid4().hex[:8]}'
    scratch.mkdir()
    capture = WORKTREE / 'diagnostics' / 'readiness' / scratch.name
    capture.mkdir(parents=True)
    app_sha, agent_sha = (APP_P1, AGENT_P1) if mode == 'p1' else (APP_FAILED, AGENT_FAILED)
    app, agent = scratch / 'app', scratch / 'agent'
    archive('/home/user/work/app', app_sha, app, APP_FILES)
    archive('/home/user/work/agent', agent_sha, agent)
    # Links point outwards to an existing read-only install. Nothing writes inside it.
    (app / 'node_modules').symlink_to(NODE_MODULES, target_is_directory=True)
    local = app / 'tests/e2e/local'
    spec = (local / 'three-products.p1-chain.spec.ts').read_text()
    seed = spec[spec.index('async function seedOneClip('):spec.index('\nasync function history(')]
    seed = seed.replace('async function seedOneClip(', 'export async function seedOneClip(', 1)
    (local / 'p1-seed.ts').write_text(
        "import { randomUUID } from 'node:crypto';\n"
        f"import {{ expect }} from '{NODE_MODULES}/@playwright/test/index.mjs';\n"
        "import { ASTRID_PYTHON } from './support/astrid.ts';\n"
        "import type { AstridCli } from './support/astrid.ts';\n"
        "import type { DirectHarness } from './support/harness.ts';\n"
        "type ChainSeed = { projectSlug: string; timelineId: string; sourceId: string };\n"
        "const SOURCE_ID = 'p1-chain-source';\n" + seed)
    (local / 'probe.mts').write_bytes((SOURCE / 'tests/readiness_probe.mts').read_bytes())
    manifest = {'mode': mode, 'runtime_base': BASE, 'runtime_source': str(SOURCE),
                'app': app_sha, 'agent': agent_sha, 'new_observation': True,
                'fixture_files': {file: hashlib.sha256((app / file).read_bytes()).hexdigest()
                                  for file in APP_FILES},
                'probe_files': {file: hashlib.sha256((SOURCE / file).read_bytes()).hexdigest()
                                for file in ['tests/readiness_commits_probe.py',
                                             'tests/readiness_probe.mts',
                                             'tests/readiness_probe_site/sitecustomize.py']}}
    write_json(capture / 'manifest.json', manifest)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    env = dict(os.environ, ASTRID_RUNTIME_CHECKOUT=str(SOURCE),
               ASTRID_RUNTIME_PYTHON='/home/user/work/venv-runtime/bin/python',
               ASTRID_CHECKOUT=str(agent), ASTRID_PYTHON='/home/user/work/venv-agent/bin/python',
               READINESS_SITE=str(SOURCE / 'tests/readiness_probe_site'),
               READINESS_DOOR_PORT=str(port), TMPDIR=str(scratch),
               PYTHONDONTWRITEBYTECODE='1', TSX_DISABLE_CACHE='1')
    results = []
    failure = None
    with (scratch / 'node.log').open('w') as output:
        process = subprocess.Popen([NODE, str(NODE_MODULES / 'tsx/dist/cli.mjs'),
                                    str(local / 'probe.mts'), str(scratch), str(capture), mode],
                                   env=env, stdout=output, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            state = until_state(scratch, {'baseline', 'error'}, process)
            assert state['stage'] == 'baseline', f'fixture setup failed; private log: {scratch}'
            route = f"/v1/projects/{state['project']}/timelines/{state['timeline']}/commits?limit=50"
            result, _ = get(state, route)
            results.append(dict(condition='baseline', **result))
            before = time.monotonic()
            (scratch / 'GO').touch()
            until_state(scratch, {'writer', 'idle', 'error'}, process)
            # Observe a genuine seed commit entering; no artificial pause or lock is inserted.
            deadline = time.monotonic() + 90
            while time.monotonic() < deadline:
                if any(e.get('event') == 'enter' and e.get('method') == 'commit_timeline'
                       and e['time'] > before for e in events(capture)):
                    break
                current = read_json(scratch / 'state.json')
                if current and current['stage'] in ('idle', 'error'):
                    break
                time.sleep(.01)
            if mode == 'native21':
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                    futures = [pool.submit(get, state, route),
                               pool.submit(get, state, '/v1/health'),
                               pool.submit(get, state, route, door=True),
                               pool.submit(get, state, route, door=True, preflight=True)]
                    for future in futures:
                        result, _ = future.result()
                        results.append(dict(condition='concurrent-native-seed-comparison', **result))
            state = until_state(scratch, {'idle', 'error'}, process)
            assert state['stage'] == 'idle', f'fixture seed failed; private log: {scratch}'
            route = f"/v1/projects/{state['project']}/timelines/{state['timeline']}/commits?limit=50"
            for door in (False, True):
                result, _ = get(state, route, door=door)
                results.append(dict(condition='completed-seed-no-writer', **result))
                publications, head, cursor = [], None, None
                for page in range(10):
                    suffix = route.replace('limit=50', 'limit=1')
                    if cursor:
                        suffix += '&cursor=' + quote(cursor, safe='')
                    result, cursor = get(state, suffix, door=door)
                    results.append(dict(condition='pagination', page=page, **result))
                    assert result['status'] == 200, result
                    assert 'head' in result, result
                    head = head or result['head']
                    assert result['head'] == head
                    publications.extend(result['publications'])
                    if not cursor:
                        break
                else:
                    raise AssertionError('pagination exceeded diagnostic bound')
                full = next(r for r in results if r['condition'] == 'completed-seed-no-writer'
                            and r['door'] == door)
                assert publications == full['publications']
                assert len(publications) == len(set(publications))
                assert page >= 1, 'seed did not exercise a real cursor'
            assert all(r['status'] in (200, 204) for r in results), results
        except BaseException as exc:
            failure = type(exc).__name__
            raise
        finally:
            (scratch / 'STOP').touch()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=15)
            write_json(capture / 'responses.json', results)
            manifest.update(failure=failure, node_exit=process.returncode,
                            captured_files=sorted(p.name for p in capture.iterdir()))
            write_json(capture / 'manifest.json', manifest)
            # Negative credential control against every minted credential in this fixture.
            secrets = []
            for file in (scratch / 'fixture').rglob('*.json'):
                value = read_json(file)
                if isinstance(value, dict) and isinstance(value.get('token'), str):
                    secrets.append(value['token'].encode())
            for file in capture.iterdir():
                raw = file.read_bytes()
                assert not any(secret in raw for secret in secrets), f'credential in {file.name}'
            print(f'CAPTURE {capture} observations={len(results)} fixture_exit={process.returncode}')
