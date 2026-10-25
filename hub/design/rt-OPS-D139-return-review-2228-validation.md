# D139 return validation

## Exact author commands

All commands ran against the clean candidate worktree
`4e0fa7afeeee5ee380c6e063c09bc1c63aa98aee`.

| command | result |
|---|---|
| `python3 -m json.tool ops-child-custody/source-manifest.json` | PASS |
| `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` | PASS |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/check-child-imports` | PASS — All checks passed |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ops-child-custody/tests -p 'test_*.py'` | PASS — 51 tests |
| `PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py` | PASS — private candidate/preimage/CAS controls |
| `git diff --check` | PASS |

## Additional focused commands

Embedded Python compile, exact command:

```sh
python3 - <<'PY'
import re
from pathlib import Path
text=Path('ops-child-custody/make-child-venv').read_text()
def block(text, name):
    return text.split(f'# {name}_BEGIN\n',1)[1].split(f'# {name}_END',1)[0]
def store_python(text):
    return text.split("<<'STORE_PY'\n",1)[1].split('\nSTORE_PY\n',1)[0]
blocks={'STORE_PY': store_python(text), 'STORE_VERIFY': block(text,'STORE_VERIFY')}
for name in ('STAGING_INVENTORY','RELOCATE'):
    blocks[name]=text.split("<<'"+name+"'\n",1)[1].split('\n'+name+'\n',1)[0]
for name, code in re.findall(r"(?m)^(\w+_SCRIPT)='(.*?)'\nrun_stage", text, re.S):
    blocks[name]=code
expected={'STORE_PY','STORE_VERIFY','STAGING_INVENTORY','RELOCATE','PROVENANCE_SCRIPT','DIST_METADATA_SCRIPT','IDENTITY_SCRIPT'}
assert set(blocks)==expected, sorted(set(blocks)^expected)
for name, code in blocks.items():
    compile(code,name,'exec')
print('PASS: compiled 7 embedded Python blocks')
PY
```

Result: PASS for `DIST_METADATA_SCRIPT`, `IDENTITY_SCRIPT`,
`PROVENANCE_SCRIPT`, `RELOCATE`, `STAGING_INVENTORY`, `STORE_PY`, and
`STORE_VERIFY`.

Canonical missing-census command, exact input, exact command:

```sh
python3 ops-child-custody/check-child-imports --child /usr/bin/python3.13 --launcher /home/user/work/agent/tools/p4-d73-pinned-launch.sh --census-file /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-D139-import-input-census-2149-input-census.json --output /tmp/d139-return-2228-canonical.Nu9pTm/result.json
```

Result: FAIL/exit 2, `census rows require a string name`. This is the open
CENSUS-005 finding.

For diagnosis only, a private temporary normalization of the same 1,146 rows
was accepted by the checker and probed with `/usr/bin/python3.13`: 1,146 census
rows, 22 unique attempted modules, 12 missing names, exit 1. This is not
canonical acceptance and not genuine-child evidence.

Private classification control with a temporary package fixture:

- relative import → `relative_source`, not probed;
- `typing_extensions` → `installed_distribution`, probed;
- platform branch → `static_conditional`, not probed;
- `try/except` `cv2` → `platform_optional`, not probed.

The private system probe is supporting evidence only. It did not execute the
D73 launcher, install anything, mutate Store, register/adopt a child, or run a
body/suite.

## Independent identity checks

- Candidate maker: SHA-256 `5b6bfa01…`, 93,300 bytes, 0755; Git blob
  `5546173f…`.
- f07 preimage: SHA-256 `f07b8093…`, 75,541 bytes, 0755; Git blob
  `898b5879…` at parent `cf80cfcb…`.
- Current maker and baseline custody/inventory test hashes match
  `source-manifest.json`; the baseline `test_custody.py` and
  `test_inventory.py` are byte-identical to the prior candidate.
- No full suite was requested or run.
