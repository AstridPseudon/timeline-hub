# D136b validation

Result: PASS. Static-only acceptance; no tests, collection, product imports/execution, typecheck, lint, browser/service/profile or comparison run.

The exact final static validation command was:

```bash
python3 - <<'PY'
import ast, hashlib, json, pathlib, subprocess
root = pathlib.Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
out = root / 'workers/app-D136b-observation-producer-sol-2231/evidence'
m, p, c = [json.loads((out / n).read_text()) for n in ('source-manifest.json', 'producer-map.json', 'classification.json')]
def sha(data):
    return hashlib.sha256(data).hexdigest()
def git(*args):
    return subprocess.check_output(['git', *args])
trees, hashes = {}, {}
for f in m['files']:
    path = f['path']
    data = git('-C', m['runtime']['repository'], 'show', m['runtime']['commit'] + ':' + path) if f['repo'] == 'runtime' else pathlib.Path(path).read_bytes()
    assert sha(data) == f['sha256'], path
    assert len(data.splitlines()) == f['line_count'], path
    if f['repo'] == 'agent':
        assert data == git('show', m['agent']['joined_source_commit'] + ':' + path), path
    if path.endswith('.py'):
        trees[path] = ast.parse(data)
    hashes[path] = sha(data)
assert git('-C', m['runtime']['repository'], 'rev-parse', m['runtime']['commit'] + '^{tree}').decode().strip() == m['runtime']['tree']
for item in m['inputs'] + m['prior_safe_packets_hash_verified']:
    assert sha(pathlib.Path(item['path']).read_bytes()) == item['sha256'], item['path']
def definitions(tree):
    result = {}
    def visit(node, owners):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = '.'.join(owners + [child.name])
                result[name] = child
                visit(child, owners + [child.name])
            else:
                visit(child, owners)
    visit(tree, [])
    return result
defs = {path: definitions(tree) for path, tree in trees.items()}
def check_citation(s):
    n = defs[s['path']][s['qualified_name']]
    assert (n.lineno, n.end_lineno) == (s['start_line'], s['end_line'])
    assert n.lineno <= s['span_start'] <= s['span_end'] <= n.end_lineno
    assert s['source_sha256'] == hashes[s['path']]
nodes = {n['id']: n for n in p['nodes']}
assert len(nodes) == 52 and len(p['call_edges']) == 43
for n in nodes.values():
    check_citation(n['source'])
for e in p['call_edges']:
    owner = nodes[e['from']]['source']
    calls = [n for n in ast.walk(trees[owner['path']]) if isinstance(n, ast.Call) and n.lineno == e['line'] and ast.unparse(n.func) == e['callee']]
    assert len(calls) == 1 and calls[0].end_lineno == e['end_line']
    assert owner['start_line'] <= e['line'] <= e['end_line'] <= owner['end_line']
    assert e['to'] in nodes
    for guard in e['lexical_control_ancestors']:
        assert any(type(n).__name__ == guard['kind'] and n.lineno == guard['line'] and sha(ast.dump(n, include_attributes=False).encode()) == guard['ast_sha256'] for n in ast.walk(trees[owner['path']]) if hasattr(n, 'lineno'))
assert len(c['rows']) == 15 and [r['boundary'] for r in c['rows']] == ['B%03d' % n for n in range(22, 37)]
assert len(c['cases']) == 9 and sum(len(x['boundaries']) for x in c['cases']) == 135
assert all(r['classification'] == 'UNKNOWN' and r['required_missing_facts'] for r in c['rows'])
assert all(set(x['boundaries'].values()) == {'UNKNOWN'} for x in c['cases'])
assert len(c['original_predicates']) == 43 and len(c['test_bodies']) == 11
for item in c['original_predicates'] + c['test_bodies']:
    check_citation(item['source'])
    s = item['source']
    n = defs[s['path']][s['qualified_name']]
    if 'predicate_ast_sha256' in item:
        n = next(x for x in ast.walk(n) if isinstance(x, ast.Assert) and x.lineno == s['span_start'])
        expected = item['predicate_ast_sha256']
    else:
        expected = item['body_ast_sha256']
    assert sha(ast.dump(n, include_attributes=False).encode()) == expected
prior = json.loads((root / 'design/app-D136a-boundary-custody-sol-2211-table.json').read_text())
old = {r['id']: r for r in prior['boundaries']}
assert [x['selector'] for x in c['cases']] == prior['original_inputs']['selectors']
for r in c['rows']:
    assert r['source_spans'] == old[r['boundary']]['source_spans']
    assert r['actual_status_retained'] == old[r['boundary']]['actual_status']
changes = git('diff', m['agent']['joined_source_commit'], '--name-only').decode().splitlines()
assert all(path.startswith('evidence/') for path in changes)
assert not git('status', '--porcelain').strip()
for name in ('classification.json', 'producer-map.json', 'source-manifest.json', 'findings.md', 'handoff.md'):
    data = (out / name).read_bytes()
    assert data and b'https://' not in data and b'http://' not in data, name
print('PASS: 25 source/document hashes; 24 Python ASTs; 13 input and 37 prior SAFE hashes; 52 citations; 43 call edges; 43 predicates; 11 bodies; 135 UNKNOWN classifications; source unchanged.')
PY
```

Result:

```text
PASS: 25 source/document hashes; 24 Python ASTs; 13 input and 37 prior SAFE hashes; 52 citations; 43 call edges; 43 predicates; 11 bodies; 135 UNKNOWN classifications; source unchanged.
```

The evidence generator also verifies every added Agent source byte against immutable joined source and reuses approved prior AST identities where present. New spans are mechanically bound to exact full definitions and call sites. Existing final2220 inventory is retained, without reopening closed generic range findings.

An initial enrichment-only assertion used an unqualified method name for store preview and stopped before writing output; it was corrected to AST identity TimelineCommitStore.preview. The final complete validation above passed. No product action was refused, retried or requalified.

Final ancillary commands: `git diff --check` and `git status --short --branch`. Results and all six evidence SHA-256 values are recorded by the final tool output. Validation does not self-embed its hash. The harness writes report.md from the final message after exit; that report existence/hash is necessarily a harness check, and no worker report.md write is attempted.

