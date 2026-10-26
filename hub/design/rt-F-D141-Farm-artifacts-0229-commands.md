# F D141i Farm artifact publication commands

All commands were read-only except creation of this packet's seven evidence
files. The repository remained clean.

## Physical schema, census, and receipt validation

```bash
python - <<'PY'
import base64,csv,hashlib,json,stat
from pathlib import Path
root=Path('/home/user/work/venv-agent/lib/python3.13/site-packages')
dist=root/'banodoco_timeline_schema-0.0.2.dist-info'
record=dist/'RECORD'
assert dist.is_dir() and not dist.is_symlink()
assert hashlib.sha256(record.read_bytes()).hexdigest() == '844b2a2e1ee19d7a1656d57cb49c2bc8febf67295e653f93ff8f96217a0c7220'
rows=list(csv.reader(record.open(newline='')))
assert len(rows) == 18 and len({r[0] for r in rows}) == 18
assert sum(bool(r[1]) for r in rows) == 12
for rel, encoded, size in rows:
    p=root/rel
    st=p.stat(follow_symlinks=False)
    assert p.is_file() and not p.is_symlink() and stat.S_ISREG(st.st_mode)
    if size:
        assert st.st_size == int(size)
    if encoded:
        algo, value=encoded.split('=',1)
        assert algo == 'sha256'
        assert hashlib.sha256(p.read_bytes()).digest() == base64.urlsafe_b64decode(value+'=')
direct=dist/'direct_url.json'
assert hashlib.sha256(direct.read_bytes()).hexdigest() == 'b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e'
metadata=json.loads(direct.read_text())
assert metadata['url'] == 'https://github.com/banodoco/ArtAgents.git'
assert metadata['subdirectory'] == 'packages/timeline-schema/python'
assert metadata['vcs_info']['commit_id'] == '242f9c4306bf3b501222cb041a9eb246ef47bc85'
census=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-D139-import-input-census-2149-input-census.json')
assert census.is_file() and not census.is_symlink() and census.stat(follow_symlinks=False).st_size == 10686270
assert hashlib.sha256(census.read_bytes()).hexdigest() == 'be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30'
c=json.loads(census.read_text())
assert c['schema'] == 'timeline.d139.input-census/v1' and c['summary']['unique_import_requirements'] == 1146
install=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-OPS-D139a-install-2309-installation.json')
assert install.is_file() and not install.is_symlink()
assert hashlib.sha256(install.read_bytes()).hexdigest() == '82bdfab2c3ec483261126b3446aacf7d1ee9df6d38e1c2491b33e3927c60f5a4'
assert json.loads(install.read_text())['result'] == 'PASS_INSTALL_COMBINED'
print('PASS: schema physical RECORD closure 18/18, hashed 12/12, direct_url binding, census hash/summary, and D139a install receipt')
PY
```

Result: `PASS`.

The raw `direct_url.json` content was inspected only on its private source path;
the packet records its path, mode, size, hash, and safe pinned identity.

## Existing-source syntax and whitespace checks

```bash
bash -n ops-d140-farm/receive-farm.sh ops-child-custody/request-child-venv ops-child-custody/make-child-venv
python - <<'PY'
import ast
for p in ['ops-d140-farm/receipts.py','ops-d140-farm/test_recipe.py']:
    ast.parse(open(p, encoding='utf-8').read(), filename=p)
print('PASS: Python AST parse for receipts.py and test_recipe.py')
PY
git diff --check
```

Result: `PASS` for bash syntax, Python AST parsing, and `git diff --check`.

## Packet JSON checks

```bash
E=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141-Farm-artifact-publication-0229/evidence
python -m json.tool "$E/artifact-index.json" >/dev/null
python -m json.tool "$E/publication.json" >/dev/null
python -m json.tool "$E/source-manifest.json" >/dev/null
python - <<'PY'
import json
from pathlib import Path
E=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141-Farm-artifact-publication-0229/evidence')
def no_dupes(pairs):
    keys=[k for k,_ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError('duplicate JSON keys')
    return dict(pairs)
for p in [E/'artifact-index.json', E/'publication.json', E/'source-manifest.json']:
    json.loads(p.read_text(), object_pairs_hook=no_dupes)
print('PASS: recursive JSON duplicate-key checks')
PY
git status --short --untracked-files=all
```

Result: `PASS` for JSON parsing and recursive duplicate-key checks after the
packet was authored; the worktree status remained clean because the packet is
in the worker evidence directory outside the repo.

## Deliberately not run

No `receive-farm.sh --check-only` run was attempted because the required Farm
venue bindings are absent. No full suite, localhost/browser/live-socket suite,
97-control suite, acquisition, prior-403 retry, venv creation, package install,
network access, hub write, or product/kit test was run.
