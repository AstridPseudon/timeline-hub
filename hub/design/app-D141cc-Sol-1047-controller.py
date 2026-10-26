"""Read-only native submit custody inspection; dispatch procedure is in dispatch-recipes.json.

No service creation or artifact repair lives here. In particular an incomplete
artifact never authorizes another native submit. Controls call the real exported
native submit with intercepted commands, separately from this inspector.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess


ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
EVIDENCE = ORCH / 'workers/app-P-D141cc-submit-owner-sol-1047/evidence'
BUILDER = Path('/home/user/work/app/scripts/testing/d66-plain-stack.mjs')
BUILDER_SHA256 = '2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f'
BUILDER_BLOB = '59b65214bc74c1ca118b097bc3b13c0ffe480a93'
NODE = '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node'
TARGET = 'app-pin-82e9e13d'
ADMISSION_BYTES = 5_200_000_000
STOP_BYTES = 4_000_000_000
SOURCE_TUPLE = {
    'app': {'sha': '82e9e13ddf1d7ec6c736521b2eb091dca9877598', 'tree': '6a6e49eb4461b5ca1a7fa1247653bc794f26d710', 'checkout': '/home/user/work/wt/app-pin-82e9e13d'},
    'agent': {'sha': 'ecdc242ed9b673f641759ecf029f95e89a2c6f92', 'tree': 'd362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735', 'checkout': '/home/user/work/wt/agt-pin-ecdc242e'},
    'runtime': {'sha': '95d98f038320d5d46bd679ac000ab3e15825c935', 'tree': '78df31d62c5b9ba4c84dee4ea346e43a767718c1', 'checkout': '/home/user/work/wt/rt-pin-95d98f03'},
    'composition': {'sha': '635f4de06fda22a85fc2e4cfc764d0153a4c9f40', 'tree': '5ab5191a296980a0a6bcd1178ab6902d6478a148', 'checkout': '/home/user/work/wt/vw-pin-635f4de0'},
}
SELECTORS = ('p2-popup-add', 'p2-parent-move', 'p2-transition-none-single',
             'p2-transition-none-bulk', 'p2-register-asset', 'p1', 'p3')
COMMAND_HASHES = (
    '27fcd174df3f214502bbca1e67b0eb366c361c11e1f5ae5c0c48d7a987582501',
    'c77b6a97e0807d43a2590624e3d47590a5e76d5ed5841f7f214f3aa9176c8f04',
    '00ee17b1b120f8907c537bb73879a6020f0f32aca9942a4402cb399d137b52ee',
    'b9dbc7f4f69d9bde52d84e8c96b50e0519c33245b4d2de304ca021740f609db3',
    '06852ebd4ab501e51704f8df7d5709063a4e8a1d675b3c018eb39226f0ce2df8',
    '513dd6421d52e745bb3ba54daaa79eb4c05cfa0d1bd464c27cb03997969245e6',
    '8323d9cc07a099a8234f6b2fda34b1250b78f7df9ffcbcb8ab66ec2e3fd90cb4',
)
ROW_HASHES = (
    'c89f8ac7430f4e5342fbffb23cd5ce4aa54f2151e38b3e46af7035aea13fc6c3',
    'ff98c12644fed8ba786a453ae49fde0ba7648160e8a2c1bf7ab75fc07d3c898d',
    'f287fea597ca4fbe7c875b7678c92f3a27be08066712d8cb2be70bf1c474498b',
    '3636c3aec938363dd71350cafbce79434fa852463e7c2733fa30deaa4cb36bbd',
    'c5f318d16964e88df19e41544d5bf73920542ed138c587681e2771d15c015a0b',
    '890320b6c6608fc53e356268bce7cb8890d144b8c4d8151cf2fc6dfc8c730db6',
    '6ccf671ffe56b9fc5625317761f5e2a437be89d8d58ad77dca301c3fb610071f',
)


class CustodyError(ValueError):
    """Finite NOTRUN for this selector; never authorize a replacement request."""


def digest(value: str | bytes) -> str:
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def native_recipes() -> list[dict]:
    """Import the unchanged module and call only its pure serviceRecipe export."""
    if digest(BUILDER.read_bytes()) != BUILDER_SHA256:
        raise CustodyError('builder hash mismatch')
    program = """
import { serviceRecipe } from 'file:///home/user/work/app/scripts/testing/d66-plain-stack.mjs';
let input=''; for await (const part of process.stdin) input+=part;
const {sources,selectors}=JSON.parse(input);
const pins=Object.fromEntries(Object.entries(sources).map(([r,s])=>[r,{checkout:`/home/user/work/${r}`,head:s.sha,tree:s.tree}]));
const checkouts=Object.fromEntries(Object.entries(sources).map(([r,s])=>[r,s.checkout]));
console.log(JSON.stringify(selectors.map(name=>({name,pins,checkouts,recipes:{
  preflight:serviceRecipe({name,pins,checkouts,preflight:true}),
  normal:serviceRecipe({name,pins,checkouts})
}}))));
"""
    output = subprocess.run([NODE, '--input-type=module', '-e', program],
                            input=json.dumps({'sources': SOURCE_TUPLE, 'selectors': SELECTORS}),
                            text=True, capture_output=True, check=True, timeout=20)
    result = []
    for index, row in enumerate(json.loads(output.stdout)):
        selector = row.pop('name')
        suffix = '-popup-retry-1' if selector == 'p2-popup-add' else ''
        suite = f'full-d141-{selector}-82e9e13d-submit{suffix}'
        row.update(selector=selector, attempt_scope='popup-retry-1' if suffix else 'original',
                   target=TARGET, suites={'normal': suite, 'preflight': f'{suite}-preflight'})
        row['rows'] = {phase: f'app {row["suites"][phase]} {command}\n'
                       for phase, command in row['recipes'].items()}
        row['command_sha256'] = {phase: digest(command) for phase, command in row['recipes'].items()}
        row['row_sha256'] = {phase: digest(text) for phase, text in row['rows'].items()}
        if row['command_sha256']['normal'] != COMMAND_HASHES[index] or row['row_sha256']['normal'] != ROW_HASHES[index]:
            raise CustodyError(f'genuine recipe conservation failed: {selector}')
        root = EVIDENCE / 'future-native' / suite
        row['output_path'] = str(root / 'output')
        row['plan_path'] = str(root / 'submit-plan.json')
        row['lock_path'] = row['plan_path'] + '.lock'
        row['environment'] = {
            f'D66_{role.upper()}_{part.upper()}': source[part]
            for role, source in SOURCE_TUPLE.items() for part in ('sha', 'tree', 'checkout')
        }
        row['environment'].update(D66_SUBMIT_TARGET=TARGET, D66_SUBMIT_SUITE=suite,
                                  D66_SUBMIT_PLAN_PATH=row['plan_path'], D66_OUTPUT_DIR=row['output_path'])
        row['argv'] = [NODE, '--max-old-space-size=6144', '--import', 'tsx', str(BUILDER), selector, '--submit']
        row['cwd'] = '/home/user/work/app'
        result.append(row)
    return result


def validate_recipe(recipe: dict) -> None:
    index = SELECTORS.index(recipe['selector'])
    if recipe['target'] != TARGET or recipe['pins'] != {
        role: {'checkout': f'/home/user/work/{role}', 'head': source['sha'], 'tree': source['tree']}
        for role, source in SOURCE_TUPLE.items()
    } or recipe['checkouts'] != {role: source['checkout'] for role, source in SOURCE_TUPLE.items()}:
        raise CustodyError('recipe source tuple mismatch')
    if recipe['command_sha256']['normal'] != COMMAND_HASHES[index] or recipe['row_sha256']['normal'] != ROW_HASHES[index]:
        raise CustodyError('recipe differs from genuine builder bindings')
    for phase in ('normal', 'preflight'):
        command = recipe['recipes'][phase]
        row = recipe['rows'][phase]
        if digest(command) != recipe['command_sha256'][phase] or digest(row) != recipe['row_sha256'][phase]:
            raise CustodyError('inconsistent command/row hash versus bytes')
        if row != f'app {recipe["suites"][phase]} {command}\n':
            raise CustodyError('row/command binding mismatch')


def read_regular(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise CustodyError(f'missing or non-regular native file: {path}')
    return path.read_bytes()


def assignments(path: Path) -> dict[str, str]:
    """Parse native %q assignment files as data, never source shell content."""
    result = {}
    for line in read_regular(path).decode().splitlines():
        tokens = shlex.split(line)
        if len(tokens) != 1 or '=' not in tokens[0]:
            raise CustodyError(f'invalid native assignment: {path}')
        key, value = tokens[0].split('=', 1)
        if key in result:
            raise CustodyError(f'duplicate native assignment: {path}')
        result[key] = value
    return result


def native_key(recipe: dict, phase: str, external: str = '') -> str:
    # test-run uses echo "$repo $TREE $suite $files $CMD $EXT" | sha256sum.
    value = f'app {SOURCE_TUPLE["app"]["tree"]} {recipe["suites"][phase]}  {recipe["recipes"][phase]} {external}\n'
    return digest(value)[:32]


def authenticate_request(recipe: dict, phase: str, directory: Path) -> dict:
    if not directory.name.startswith(f'{TARGET}-{recipe["suites"][phase]}-'):
        raise CustodyError(f'native request ID namespace mismatch: {directory}')
    request = assignments(directory / 'request')
    expected = {'target': TARGET, 'repo': 'app', 'suite': recipe['suites'][phase], 'files': '', 'nocache': '1'}
    if set(request) != set(expected) | {'requested'} or any(request.get(key) != value for key, value in expected.items()):
        raise CustodyError(f'request target/suite/argv mismatch: {directory}')
    snap = assignments(directory / 'snap')
    if set(snap) != {'tree', 'key', 'worktree'} or snap.get('tree') != SOURCE_TUPLE['app']['tree'] or snap.get('worktree') != SOURCE_TUPLE['app']['checkout']:
        raise CustodyError(f'request source mismatch: {directory}')
    external = ''
    if (directory / 'ext').exists():
        raw = read_regular(directory / 'ext').decode()
        lines = raw.splitlines()
        # Admission retries append the same native external binding repeatedly.
        if not lines or len(set(lines)) != 1 or not lines[0].startswith('external=') or not raw.endswith('\n'):
            raise CustodyError(f'unknown native ext format: {directory}')
        external = lines[0][len('external='):]
    if snap.get('key') != native_key(recipe, phase, external):
        raise CustodyError(f'request command/row/source key mismatch: {directory}')
    if (directory / 'summary').exists():
        commands = [line[5:] for line in read_regular(directory / 'summary').decode().splitlines() if line.startswith('cmd: ')]
        if commands and commands != [recipe['recipes'][phase]]:
            raise CustodyError(f'request command mismatch in summary: {directory}')
    status = read_regular(directory / 'status').decode().strip()
    if status not in {'queued', 'running', 'pass', 'fail', 'timeout', 'error', 'cancelled'}:
        raise CustodyError(f'unknown native request status: {directory}')
    return {'id': directory.name, 'resultDir': str(directory), 'status': status,
            'phase': phase, 'request_sha256': digest(read_regular(directory / 'request')),
            'snap_sha256': digest(read_regular(directory / 'snap'))}


def inspect_native(recipe: dict, *, tests_root: Path, registry: Path, artifact_path: Path,
                   owner_state: str, tool_session: str | None = None) -> dict:
    """Read native state once. Caller repeats immediately before FIRST invocation.

    owner_state is the existing tool owner's knowledge, not PID liveness inferred
    from another sandbox. 'active' must retain the actual tool session. Unknown
    provenance never becomes permission merely because a lock disappeared.
    """
    validate_recipe(recipe)
    if owner_state not in {'not-started', 'active', 'ended', 'unknown'}:
        raise CustodyError('unknown owner state')
    live_owner = owner_state == 'active' and bool(tool_session)
    rows = read_regular(registry).decode().splitlines(keepends=True)
    registered = {}
    for phase in ('normal', 'preflight'):
        suite = recipe['suites'][phase]
        matching = [line for line in rows if line.split()[:2] == ['app', suite]]
        if matching and matching != [recipe['rows'][phase]]:
            raise CustodyError(f'same-suite command/row mismatch or duplicate: {suite}')
        registered[phase] = bool(matching)
    records = {phase: [] for phase in ('normal', 'preflight')}
    for directory in sorted(tests_root.iterdir()):
        if not directory.is_dir() or directory.name == 'cache':
            continue
        request_path = directory / 'request'
        # Names select potentially torn requests too; incomplete files fail closed.
        named = next((p for p in ('preflight', 'normal')
                      if directory.name.startswith(f'{TARGET}-{recipe["suites"][p]}-')
                      and (p == 'preflight' or not directory.name.startswith(f'{TARGET}-{recipe["suites"]["preflight"]}-'))), None)
        if not request_path.exists() and not request_path.is_symlink():
            if named:
                raise CustodyError(f'torn native request: {directory}')
            continue
        try:
            request = assignments(request_path)
        except (ValueError, UnicodeError):
            if named:
                raise CustodyError(f'unreadable native request: {directory}') from None
            continue
        phase = next((p for p in records if request.get('suite') == recipe['suites'][p]
                      and request.get('target') == TARGET), None)
        if named and phase != named:
            raise CustodyError(f'ID/request suite mismatch: {directory}')
        if phase:
            if directory.is_symlink():
                raise CustodyError(f'native request directory is a symlink: {directory}')
            if not registered[phase]:
                raise CustodyError('existing request without its exact native row')
            records[phase].append(authenticate_request(recipe, phase, directory))
    if any(len(values) > 1 for values in records.values()):
        raise CustodyError('ambiguous multiple native request IDs')
    artifact = None
    if artifact_path.exists() or artifact_path.is_symlink():
        artifact = json.loads(read_regular(artifact_path))
        if not isinstance(artifact, dict):
            raise CustodyError('native artifact is not an object')
        expected = {'version': 1, 'suite': recipe['selector'], 'pins': recipe['pins'],
                    'checkouts': recipe['checkouts'], 'target': TARGET,
                    'suites': recipe['suites'], 'recipes': recipe['recipes']}
        if set(artifact) != set(expected) | {'normal', 'preflight'} or any(artifact.get(key) != value for key, value in expected.items()):
            raise CustodyError('native artifact source/command/row mismatch')
        for phase in records:
            entry = artifact.get(phase)
            if entry is not None:
                if not isinstance(entry, dict) or not records[phase] or entry.get('id') != records[phase][0]['id'] or entry.get('resultDir') != str(ORCH / 'tests' / entry['id']):
                    raise CustodyError('native artifact ID/result path mismatch')
    lock_exists = Path(str(artifact_path) + '.lock').exists() or Path(str(artifact_path) + '.lock').is_symlink()
    if records['normal']:
        normal = records['normal'][0]
        return {'action': 'ADOPT', 'request': normal, 'native_submit_allowed': False,
                'body_verdict': 'UNVERIFIED', 'owner_session': tool_session if live_owner else None}
    if live_owner:
        return {'action': 'WAIT_EXISTING_TOOL_SESSION', 'tool_session': tool_session,
                'native_submit_allowed': False, 'preflight': records['preflight']}
    if owner_state != 'not-started' or artifact is not None or lock_exists or any(records.values()) or any(registered.values()):
        return {'action': 'NOTRUN', 'reason': 'incomplete or prior native custody; never resume by invoking submit again',
                'native_submit_allowed': False, 'preflight': records['preflight']}
    return {'action': 'FIRST_NATIVE_INVOCATION_ONLY', 'first_invocation_candidate': True, 'live_admission': 'UNVERIFIED',
            'condition': 'same sole owner; repeat inspection immediately before exec, measure >5.2GB once, retain tool session'}


def disk_decision(request_id: str, available_bytes: int) -> dict:
    return {'action': 'STOP_EXACT_EXISTING_ID' if available_bytes <= STOP_BYTES else 'OBSERVE',
            'request_id': request_id, 'available_bytes': available_bytes}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('selector', choices=SELECTORS)
    parser.add_argument('--owner-state', required=True, choices=('not-started', 'active', 'ended', 'unknown'))
    parser.add_argument('--tool-session')
    args = parser.parse_args()
    try:
        recipe = next(row for row in native_recipes() if row['selector'] == args.selector)
        decision = inspect_native(recipe, tests_root=ORCH / 'tests', registry=ORCH / 'tests/suites.conf',
                                  artifact_path=Path(recipe['plan_path']), owner_state=args.owner_state,
                                  tool_session=args.tool_session)
    except (CustodyError, OSError, ValueError, subprocess.SubprocessError) as error:
        decision = {'action': 'NOTRUN', 'native_submit_allowed': False, 'reason': str(error)}
    print(json.dumps(decision, indent=2))


if __name__ == '__main__':
    main()
