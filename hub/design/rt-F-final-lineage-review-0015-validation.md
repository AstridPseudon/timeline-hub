# Validation record

All checks were read-only against the private candidate or used temporary stub inputs. No production body, service, browser, provider, profile, render, build, ZIP, live install, tuple capture, network, package, or full-suite flow ran.

## Exact commands and results

- `PYTHONPYCACHEPREFIX=/tmp/rt-F-final-lineage-review-0015-checks/pycache python3 -m py_compile <all 19 candidate Python files>` — **PASS** (`compile19=PASS`).
- `python3 -c 'json.loads(...)' <the 7 candidate JSON files>` — **PASS** (`JSON7=PASS`).
- `bash -n <the 3 candidate shell files>` — **PASS** (`Bash3=PASS`).
- `RUFF_CACHE_DIR=/tmp/rt-F-final-lineage-review-0015-checks/ruff /root/.local/bin/ruff check --select F <the 19 candidate Python files>` — **PASS**, `All checks passed!`.
- `/root/.local/bin/mypy --ignore-missing-imports --follow-imports=skip --explicit-package-bases --cache-dir /tmp/rt-F-final-lineage-review-0015-checks/mypy <the 13 active Python files>` — **PASS**, `Success: no issues found in 13 source files`.
- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/rt-F-final-lineage-review-0015-checks python3 candidate/install-final-services.py --registry .../orch/tests/suites.conf --candidate .../lineage-return-0000/evidence/candidate/runtime-final-service-rows.txt --builder .../orch/bin/delivery-build` — **PASS**, `no installation requested`.
- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/rt-F-final-lineage-review-0015-checks python3 candidate/acceptance-d73.py` — **PASS**, one capture/four receipts and drift refusal before request-test.
- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/rt-F-final-lineage-review-0015-checks python3 candidate/d59-final-matrix/stubcontrols.py` — **PASS**, positive dispatch count 1 and poisoned dispatch count 0.
- Read-only Python CAS control loading `install-final-services.py` and calling `validate_registry` on the current snapshot, plus in-memory three-row replacement, own-target drift, and unrelated/global drift — **PASS**; no registry write.
- Read-only Python custody/path control comparing the candidate to `rt-F-final-route-return-sol-2349/evidence/candidate` — **PASS**, 66/66 files byte-exact, 41 matrix/inventory files unchanged, active paths regular/non-symlink/absolute.

An initial static invocation attempted to use the assigned worker `tmpdir`, but that path is a file in this environment rather than a directory; its cache-dependent result was not counted. The commands above were rerun with the private `/tmp/rt-F-final-lineage-review-0015-checks` cache root and are the evidence.

## Inherited source evidence rechecked

- D135 install and independent install review: PASS for reviewed `ef9` source, installed bytes/mode, exact `f25` backup, wrapper/caller receipt, and no second install.
- Independent runner review/route return: PASS after the earlier obsolete-runner finding was resolved; active pins are `8aea497…` core, `45a5063…` delivery caller, and `774aafc…` rows.
- D141 Runtime source review: PASS; C0 request/reply fields remain present and the cut remains frozen. Full-suite and live-service items remain intentionally unverified here.

## Not run

Real service/test bodies, localhost/live sockets, full suites, delivery build, ZIP, live installation, normal tuple movement, network/package acquisition, Store, child/browser/provider/profile/render, original9, D130, credentials, hub, and Git ref mutation.
