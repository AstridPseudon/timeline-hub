# Validation

Candidate: `1b709a79658e5c553281a4fe66d388fe284b6dd0` / tree
`040c17724799aa53bda05775b88d0aac8db11289`; compared with 0032
`ba8bec724fb2f348a4d2fdb4389025138060d1d5`.

| Command | Result |
| --- | --- |
| `pytest -q -p no:cacheprovider ops-d140-farm/test_recipe.py::test_receiver_is_check_only_and_contains_current_tuple ops-d140-farm/test_recipe.py::test_phase_census_does_not_admit_future_inputs_or_start_routes ops-d140-farm/test_recipe.py::test_import_failure_stops_before_controls_and_core ops-d140-farm/test_recipe.py::test_core_selector_has_exactly_22_unfiltered_roots` | PASS — 4 passed in 1.14s |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-d140-farm/test_recipe.py` | PASS |
| in-memory `ast.parse` of `ops-d140-farm/test_recipe.py` | PASS |
| `bash -n ops-d140-farm/receive-farm.sh` | PASS |
| `python -m json.tool` on existing source/controls manifests | PASS |
| `git diff --check ba8bec724 1b709a796` | PASS |
| changed-path census `git diff --name-status ba8bec724 1b709a796` | PASS — four expected ops-d140-farm files only |
| unchanged-file diff for receipts.py, D139a kit sources and manifest | PASS |
| exact tuple checkout/tree/origin/object and source blob/SHA readback | PASS |
| Runtime lock 15-entry source-hash comparison against exact 6a011d58 tree | PASS |
| C0 schema SHA comparison between f103 and 6a011d58 | PASS — byte-identical |

## Independent no-request census

The exact four clean local checkouts were supplied to the production
`receive-farm.sh --check-only` caller before any request, child, import, dry
control, or core action. It returned exit 1, JSON status `NOT_READY`, 66 checks
(24 PASS, 42 non-PASS), and SHA-256
`b0a1ee1337a2a89f52de5ff7124f61d7421e2ea23a60ea43314e93213dc108d2`.
All 20 source checkout/object/origin/blob checks passed. Every side-effect
field was false: child, pytest, installer, import, Store, queue, acquisition.
The non-PASS rows name all current missing/unbound venue owners; no first-error
short circuit or fictional receipt was used.

The prior independent ordinary review's `pytest` result (`97 passed`) is
reused as directed; the 97-test suite was not repeated because ordinary logic
did not change. No full suite, Runtime full/pristine, Farm import/body, D134
body, D124 core, package, network, Store, service, or ZIP run was performed.

