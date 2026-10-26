# Validation

- Exact controls: `TMPDIR=/tmp/w-d0794e7d6a/d141-controls-final PYTHONDONTWRITEBYTECODE=1 python3 -I ops-d141-measured-floor/controls/real-controls.py` — PASS, exit 0, 73 purposes; `SEC001=PASS`, `SEC002=PASS`, `freeze2=NEEDS`, `release=NOT_READY`.
- `bash -n ops-d141-measured-floor/bin/test-run` — PASS.
- Python AST parse with `PYTHONDONTWRITEBYTECODE=1` over all five scoped Python files — PASS; no bytecode written.
- `python3 -m json.tool ops-d141-measured-floor/install-manifest.json` — PASS.
- Manifest SHA-256, mode, regular-file and single-link source checks — PASS for all five files.
- `git diff --check` — PASS.
- `/home/user/work/venv-runtime/bin/ruff check --no-cache ...` — NOT RUN successfully: the prescribed executable is absent; shared runtime Python also reports `No module named ruff`. No dependency was installed.

The controls covered direct USR1/TERM, mounted request-stop-test child-only semantics, timeout-child reap, frozen sampler failure/125, first/periodic/final KEEP traces, seven custody attacks, paired refusal attacks, normal success, P5 6934, floors, cache/source/snapshot/leases, held IDs and one-heavy protection. No full suite, live service, browser, installation/CAS, receipt attachment, App freeze-2 registration, build, ZIP or release was run.
