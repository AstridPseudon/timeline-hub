"""Render private caller drafts; never install rows or submit work.

This is a preparation artifact, not qualification. Supply manager-published exact
identities, then independently qualify source, receipts, imports and controls.

READY needs the cumulative merged App SHA/tree, D42-on-37eb Runtime SHA/tree,
independent review and the same 145-case qualification, normal exact checkout,
new backend-keyed child, and normal matching-tree Remotion receipts. Agent079
and the approved 819acf graph remain fixed. Agent4151's 145-case result is
separate from Agent079's historical transcript failure. Daemon/provider imports
and the historical browser failure cause remain UNKNOWN.

The manager owns these normal routes (commands are documentation only):
  "$O/bin/request-checkout" runtime "$QUALIFIED_D42_RUNTIME_SHA" 'D42 exact proof pin'
  "$O/bin/request-runtime" "$RN" "$AGENT" "$LOCK_SHA256" "$AGENT_CHECKOUT" \
      "$RUNTIME_CHECKOUT" "$QUALIFIED_D42_RUNTIME_SHA" remotion-env-nodes
  "$O/bin/request-child-venv" "$CN" "$AGENT" remotion-env-nodes "$REMOTION_GRAPH" \
      --source-carrier "$AGENT_CHECKOUT" "$RUNTIME_CHECKOUT" "$QUALIFIED_D42_RUNTIME_SHA"
Use only published identities and actual resulting registrations. After source,
custody and control qualification, fresh-read suites.conf, compare both old rows,
replace the pair atomically and assert every outside byte unchanged. The manager
alone submits the ONE actual P2/P3 pair after READY. This program has no installer
or submission path.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
OLD_APP = '804134d74782d40855146aa568ff289200b79142'
OLD_TREE = '8437e47666853b62e03a58af3716235346316fba'
OLD_PARENT = '22efcda3da4005f8663c078439ff0edbfade69be 42db156ede0d0192ec4176a2edd29b366b552a8d'
BASE = 'f90e708b379145ac456924742cc51c187ed6e0c6'
AGENT = '079580ca46af77e0292d49dc34386b25c8391f99'
RUNTIME = '37eb6c7bdb79dcae2523883e66b5cea5be721ffd'
RUNTIME_TREE = 'be4114705127f9ee9e86b26cd6de3f467e771c01'
SUITES = ('full-e2e-three-products', 'ap2-P3-gate5-h6-0348')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app-source', required=True)
    parser.add_argument('--runtime-source', required=True)
    parser.add_argument('--runtime-checkout', required=True, type=Path)
    parser.add_argument('--child', required=True)
    parser.add_argument('--remotion', required=True)
    args = parser.parse_args()
    app = Path(__file__).resolve().parent
    out = Path(os.environ['TMPDIR']).resolve()
    assert out != app and not out.is_relative_to(app), 'drafts belong in private TMPDIR'
    for value in (args.app_source, args.runtime_source):
        assert re.fullmatch('[0-9a-f]{40}', value), 'exact commit required'
    for value in (args.child, args.remotion):
        assert re.fullmatch('[a-z0-9-]+', value), 'normal registration name required'
    runtime = args.runtime_checkout
    assert runtime.resolve() == runtime
    assert git(runtime, 'rev-parse', 'HEAD').decode().strip() == args.runtime_source
    assert not git(runtime, 'status', '--porcelain=v1', '--untracked-files=all').strip()
    subprocess.run(['git', '-C', str(app), 'merge-base', '--is-ancestor', BASE, args.app_source], check=True)
    subprocess.run(['git', '-C', str(runtime), 'merge-base', '--is-ancestor', RUNTIME, args.runtime_source], check=True)
    tree = git(app, 'rev-parse', args.app_source + '^{tree}').decode().strip()
    parent = git(app, 'show', '-s', '--format=%P', args.app_source).decode().strip()
    rt_tree = git(runtime, 'rev-parse', 'HEAD^{tree}').decode().strip()
    runtime_changes = git(runtime, 'diff', '--name-only', RUNTIME, args.runtime_source).decode().splitlines()
    assert all(path == 'runtime_protocol/timeline_commit_store.py' or path.startswith('tests/')
               for path in runtime_changes), 'backport changed protected source/contracts/clients/schema/locks'
    paths = git(runtime, 'ls-tree', '-r', '--name-only', args.runtime_source, 'packages/python/astrid_runtime_client/').decode().splitlines()
    assert len(paths) == 4
    client = {}
    for path in paths:
        data = git(runtime, 'show', args.runtime_source + ':' + path)
        assert data == git(runtime, 'show', RUNTIME + ':' + path), 'client drift'
        assert data == git('/home/user/work/wt/agt-pin-079580ca', 'show', AGENT + ':' + path.removeprefix('packages/python/')), 'Agent client mismatch'
        client[path] = sha(data)
    replacements = {OLD_APP: args.app_source, OLD_TREE: tree, OLD_PARENT: parent,
                    RUNTIME: args.runtime_source, RUNTIME_TREE: rt_tree,
                    '/home/user/work/wt/rt-pin-37eb6c7b': str(runtime),
                    'venv-agent-child-app-ready-079-37eb-0256': args.child,
                    'agent-remotion-app-ready-079-37eb-0258': args.remotion}
    changes = git(app, 'diff', '--name-only', '--diff-filter=M', OLD_APP, args.app_source).decode().splitlines()
    for path in changes:
        old = git(app, 'show', OLD_APP + ':' + path)
        new = git(app, 'show', args.app_source + ':' + path)
        if path in ('tests/e2e/local/three-products.spec.ts',
                    'tests/e2e/local/three-products.p2-tour.spec.ts',
                    'tests/e2e/local/three-products.p2-elements-assets.spec.ts',
                    'tests/e2e/local/three-products.p2-popup.spec.ts'):
            assert old == new, 'original body changed'
        for before, after in ((blob(old), blob(new)), (sha(old), sha(new))):
            assert before not in replacements or replacements[before] == after
            replacements[before] = after
    raw = (ORCH / 'tests/suites.conf').read_bytes()
    lines = raw.splitlines(keepends=True)
    rows = {line.split(None, 2)[1].decode(): line for line in lines
            if line.split()[:2] in [[b'app', name.encode()] for name in SUITES]}
    assert tuple(rows) == SUITES, 'expected exactly the existing pair'
    outside = b''.join(line for line in lines if line not in rows.values())
    result = {}
    for n, (name, line) in enumerate(rows.items(), 2):
        outer = line.decode().split(None, 2)[2].rstrip('\n')
        a = outer.index('$(bash -c ') + len('$(bash -c ')
        b = outer.index(')" && eval', a)
        decoded = shlex.split(outer[a:b])
        assert len(decoded) == 1
        inner = decoded[0]
        updated = inner
        tail = outer[b:]
        for before, after in replacements.items():
            updated = updated.replace(before, after)
            tail = tail.replace(before, after)
        original_native = inner[inner.index('import { expect }'):inner.index('finally { await harness.stop(); }')]
        assert original_native == updated[updated.index('import { expect }'):updated.index('finally { await harness.stop(); }')]
        new_outer = outer[:a] + shlex.quote(updated) + tail
        for label, data in [('inner', inner), ('outer', outer), ('new-inner', updated), ('new-outer', new_outer)]:
            path = out / f'p{n}-{label}.sh'
            path.write_text(data)
            subprocess.run(['/bin/bash', '-n', str(path)], check=True)
        result[name] = 'app ' + name + ' ' + new_outer
    (out / 'before.json').write_text(json.dumps({k: v.decode().rstrip('\n') for k, v in rows.items()}))
    (out / 'after.json').write_text(json.dumps(result))
    (out / 'd42-draft.rows').write_text(''.join(row + '\n' for row in result.values()))
    (out / 'outside.before').write_bytes(outside)
    key = sha(json.dumps(['child', AGENT, args.runtime_source, client], sort_keys=True, separators=(',', ':')).encode())
    manifest = {'status': 'PREPARED_ONLY', 'app_source': args.app_source, 'app_tree': tree,
                'app_parent': parent, 'runtime_source': args.runtime_source, 'runtime_tree': rt_tree,
                'child_key': key, 'client_tuple': client, 'replacements': replacements,
                'live_row_sha256': {name: sha(row) for name, row in rows.items()},
                'draft_row_sha256': {name: sha((row + '\n').encode()) for name, row in result.items()},
                'outside_sha256': sha(outside), 'outside_lines': len(lines) - 2}
    (out / 'prepared.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: v for k, v in manifest.items() if k not in ('replacements', 'client_tuple')}, indent=2))


if __name__ == '__main__':
    main()
