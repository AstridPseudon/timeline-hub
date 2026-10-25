# D139a reviewed join validation

## Source custody

The worktree started exactly at bae2ba5ec66e6fb4115c2f79299f82f535e68bb1.
Only the five paths from e9fdcfe299a20f1a137e0c87d2c0bf2de49f9e45 were
imported. Each is byte-identical to the maker commit. The bae2 checker and
`test_canonical_census.py` remain byte-identical. The final product source
manifest is the only shared manifest update.

Candidate: `fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5`,
111171 bytes, mode 0755. Required installed preimage:
`f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`,
75541 bytes, mode 0755.

## Commands and results

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-child-custody/tests -p 'test_*.py' -v` | PASS — 63 tests |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/check-child-imports` | PASS — all checks passed |
| `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` | PASS |
| seven embedded Python compile blocks with `/home/user/work/venv-agent/bin/python` | PASS — 7/7 |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B ops-child-custody/install-prep/dry_run_controls.py` | PASS — private candidate/preimage/CAS/helper/shape controls |
| exact canonical 1146-row CLI with `/home/user/work/venv-agent/bin/python` | EXPECTED status 1 — 1146 census rows, 22 attempted modules, 12 canonical missing names, 12 failures; no installed-distribution or child claim |
| `/home/user/work/venv-agent/bin/python -m json.tool ops-child-custody/source-manifest.json` | PASS |
| `git diff --check` | PASS |

The focused unittest command was run once on the joined source. The canonical
CLI used the authenticated Agent2149 packet and `/usr/bin/python3.13` only as a
supporting system probe; its all-missing result is intentionally not genuine
child acceptance.

No install, package acquisition, child request, provider, browser, Store,
registry, suite, full suite, or Git mutation was run.
