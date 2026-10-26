# D141h validation

Result: **FAIL** for the bounded closure check. Source remains unchanged.

## Exact checks

- `TMPDIR=/tmp/d141h-verify-0402-controls-2 PYTHONDONTWRITEBYTECODE=1 python3 -I privateops-d141-measured-floor/controls/real-controls.py` — **FAIL**, exit 1 at `real-controls.py:478`; `body-cancel` stayed running, with only the first trace sample and no `trace-validation`. The script therefore did not reach the seven new trace-custody attacks. It was not rerun.
- `bash -n privateops-d141-measured-floor/bin/test-run` — **PASS**.
- Python AST compilation of `privateops-d141-measured-floor/bin/*.py` and `controls/real-controls.py` — **PASS**, 5 files.
- `ruff check --no-cache privateops-d141-measured-floor/bin/*.py privateops-d141-measured-floor/controls/real-controls.py` — **PASS**, all checks passed.
- `python3 -m json.tool privateops-d141-measured-floor/install-manifest.json` — **PASS**.
- Exact five-file hash/mode manifest verification — **PASS**; direct regular 0755 files only, controls excluded from publication.
- `git diff --quiet HEAD^ HEAD -- ops-d141-measured-floor` — **PASS**; parent route unchanged.
- `git diff --check` — **PASS**.
- Isolated installed → published → received-bin smoke using `cp -p`, atomic temporary receiver replacement, SHA-256 comparison, and mode checks — **PASS** for all five files; no controls sibling.

## Source-only limits

No full suite, live dispatcher, actual P5/target15 service receipt, product test/import/collection, queue, installation/CAS, body qualification, network, package, build, ZIP, or release gate was run. The C0 v2 request/reply contract remains unchanged and is not requalified by this task.
