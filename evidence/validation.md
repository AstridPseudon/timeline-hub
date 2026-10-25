# D139 bounded independent disposition validation

Result: `PASS_ASSESSMENT`; source disposition: `FAIL_SOURCE/NOTREADY` with
`UNAPPLIED_HOLD`. The exact author `controls.py` is missing from the author's
worker tmpdir, so its complete RED harness was not claimed or re-executed.
Small independent probes below used only temporary private fixtures.

## Author commands, rerun on the exact candidate

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-d131 -p 'test*.py' -v
```

PASS: 18 tests, including all 14 unchanged baseline tests.

```sh
RUFF_CACHE_DIR=/tmp/w-5e1c59c475/d139-review/ruff-cache /home/user/work/venv-agent/bin/ruff check ops-d131/bench_store.py ops-d131/retire_entry.py ops-d131/test_retire_entry.py
RUFF_CACHE_DIR=/tmp/w-5e1c59c475/d139-review/ruff-cache /home/user/work/venv-agent/bin/ruff check ops-d131/bench_store.py ops-d131/retire_entry.py ops-d131/test_retire_entry.py --ignore EXE002,BLE001
```

PASS: both invocations, zero diagnostics.

```sh
/home/user/work/venv-agent/bin/python -B - <<'PYCOMPILE'
from pathlib import Path
for name in ('bench_store.py', 'retire_entry.py', 'test_reserve.py', 'test_retire_entry.py'):
    path = Path('ops-d131') / name
    compile(path.read_bytes(), str(path), 'exec')
    print('PASS:', path)
PYCOMPILE
sh -n ops-d131/install-prep/check-cas.sh
ops-d131/install-prep/check-cas.sh "$PWD" tl/rt-OPS-D131-kind-reserve-1558
git diff --check
git diff --check tl/rt-OPS-D131-kind-reserve-1558..HEAD
```

PASS: four private in-memory compiles; shell syntax; exact `123bb` preimage
and mode `0755` CAS preflight with no installation; both diff checks. The
candidate-to-return-base diff check was also run and passed:
`git diff --check tl/rt-OPS-store-retire-return-2235..HEAD`.

## Independent private probes

The one-shot Python probe used `TMPDIR=/tmp/w-5e1c59c475/d139-review` and the
existing `RetirementTests.make_entry()` fixture only:

- F1: referenced activity → `REFUSED: retirement activity reference: workers`;
  erased valid self-hash → `retired`.
- F2: process started on the third process scan → `retired`, process alive
  afterward, 3 scans.
- F3: late activity reference and late `KEEP` → `retired` in both cases.

These results independently confirm the three `UNAPPLIED` findings. They are
synthetic source controls, not real Store or child acceptance. The missing
author `controls.py` means no claim is made that all of the author's original
RED matrix was re-executed.

## Prohibited operations not performed

No install, queue admission, real Store/registry/metadata access or mutation,
eviction, child/body, suite, browser, provider, acquisition, D130 work, or
full suite occurred. No protocol, historical field, cleanup route, generated
file, product test, pin, Git internal, hub, or design file was changed.
