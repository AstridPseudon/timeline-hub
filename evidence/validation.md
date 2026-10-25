# D139 independent validation

## Targeted controls

All commands were run against the candidate worktree. No full suite, live
socket, browser, package installation, child request, Store mutation, or body
was run.

| command | result |
|---|---|
| `bash -n ops-child-custody/make-child-venv` | PASS |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v` | PASS, 44 tests |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/check-child-imports` | PASS |
| `bash -n ops-child-custody/install-prep/apply-reviewed-maker.sh` | PASS |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/install-prep ops-child-custody/check-child-imports` | PASS |
| seven embedded Python blocks compiled in memory | PASS |
| `git diff --check` | PASS |
| `python3 -m json.tool ops-child-custody/source-manifest.json` | PASS |
| `.../install-prep/dry_run_controls.py` | PASS, private offline CAS controls |

Embedded block hashes observed: `STORE_PY`
`d0a00a6d8577d340a5733cf64488b3ba3524b8f01492cb094e3b3c4f2afa636a`,
`STORE_VERIFY`
`a5d0ddd7074561537fcb2721c96d9ce3f6cef861c44fb0d403fd0d02934023f0`.

## Check-only controls

The author’s retained evidence reports the real D73 preflight set as six
modules with only `banodoco_timeline_schema` missing, plus missing-one and
missing-many controls that list all failures. It also reports a static census
of 21,752 rows / 1,191 applicable non-stdlib modules / 602 probe failures.
Those results are bounded evidence, not registered-child proof.

The reviewer ran the executable against `/usr/bin/python3.13` with the real
launcher path and six requested names using `-I -B -P`; it exited 1 and listed
all six missing modules. This difference is expected evidence of the absent
current registered child and is not used to relabel the author’s historical
result. The checker does not execute the launcher subprocess.

Input2149 independently reports 431 root Python files, 1,146 unique import
requirements, 1,001 reachable source modules, 17 dynamic records, 12 missing
categories, and zero parse errors. It explicitly excludes execution and does
not authorize installation. Relative import and `typing_extensions`
classification defects are recorded in `review.json`.

## Source and call-path audit

The candidate serializes the maker context, then calls `Store.ensure` with
`build`, `verify`, `seal`, and `registration`. The build installs the pinned
requirements and schema/Agent/Runtime archives; verification invokes the
embedded verifier; registration projects the verified report. The ordering is
present in source, but no actual Store/child receipt exists.

Schema identity is hashed before the live schema directory is archived and
installed. There is no authenticated D73 source-tree comparison and no
schema-input recheck. This is the decisive FAIL finding.
