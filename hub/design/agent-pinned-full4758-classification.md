# Pinned Agent full4758 classification

Date: 2026-10-20

## Source identities

- Pinned full: commit `13a05d553a50d62538db3cd6bc1f09da6983b3d5`, tree
  `a5e00ca29a72ba00d34c0d8b1bcea67132a8e954`.
- Current source before this worker's test-only edit: commit
  `8e3107853d17453758a933d1f47215cc1c002660`, tree
  `7b395a0165b00808b9b554213ff015838e813e51`.
- Final central targeted snapshot including the edit below: tree
  `bd36b27861808a19f1e0895be947de629667ef65`.

The pinned run `agent-full-remotion12-s2-integration-1020122457-4758` was not
rerun, cancelled, or relabelled. Its recorded result remains 14,577 passed,
6 failed, 452 skipped, 4 xfailed, 565 subtests passed in 4,905.65 seconds.

## Six-node evidence

| Exact node | Pinned traceback / cause | Current targeted result and classification |
|---|---|---|
| `tests/packs/timeline/test_cli_media.py::test_trim_and_slip_keep_the_film_span` | `tests/packs/timeline/test_cli_media.py:27` passed `object()` to `build_parser`; native trim reached `astrid/sdk/timeline/store.py:590`, `c.timelines.open_composition(...)`, and raised `AttributeError: 'object' object has no attribute 'timelines'`. | First current run: failed with the same traceback. The detached test helper now builds with `client=None`, so native dispatch is not asked to inspect Runtime before the patched checkout path. Final targeted run: passed. **Old test-setup defect; fixed current.** |
| `tests/packs/timeline/test_cli_media.py::test_a_trimmed_bed_is_extended_to_the_film_end_under_keep_end` | Same exact `store.py:590` `AttributeError` from the opaque parser client, before the keep-end edit or assertion. | First current run: failed identically. Final targeted run: passed after the same bounded fixture correction; trim and film-end semantic assertions were retained. **Old test-setup defect; fixed current.** |
| `tests/sdk/test_timeline_persistence.py::test_a_live_holder_that_never_exits_is_waited_for_then_refused_by_name` | The holder owned `.main.json.lock`; pinned line 379 called `Checkout.load(path)` while it was held. `store.py:148` first got `BlockingIOError: [Errno 11] Resource temporarily unavailable`, then `store.py:155` raised `TimelineEditError: another writer (pid 13471) has held ... for 0.5 s`. | Current `ce363f6d` setup loads the checkout before starting the holder, preserving the positive timeout/refusal-by-PID assertion. Final targeted run: passed. **Historical test-setup defect; fixed current.** |
| `tests/stage1/test_zero_shim_execution_pack_deletion.py::test_external_executor_command_always_crosses_subprocess_boundary` | The pinned full exported VibeComfy variables. Its fake `runner.subprocess.run` returned `CompletedProcess(..., returncode=0)` with `stdout=None`; the ambient identity check reached `vibecomfy_dependency.py:106`, `result.stdout.strip()`, and raised `AttributeError: 'NoneType' object has no attribute 'strip'` before the executor boundary assertion. | Current `ce363f6d` clears the VibeComfy selection/candidate/attestation variables in this test. Final targeted run: passed. The subprocess-boundary assertion remains intact. **Old environment/test-isolation defect; fixed current.** |
| `tests/test_generic_host.py::test_launch_worker_projection_matches_fixed_execution_context` | The pinned test computed expected paths with ambient `_dependency_pythonpath()`, while the launch candidates used the explicit `environment`. Assertion differed by `/home/user/work/fixtures/vibecomfy`. | Current `ce363f6d` computes expected paths with `dependency_pythonpath(environment)`. Final targeted run: passed. **Old environment/test-isolation defect; fixed current.** |
| `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale` | Pinned inventory stopped at `astrid/core/execution/generic_host.py`: rationale 13,798 vs on-disk 13,860, a 62-line drift beyond the ±50 tolerance. | First current run no longer failed on `generic_host.py`; current source is 13,816, within 18 lines of the rationale, consistent with the extraction. It now fails on Viewing-owned `astrid/core/rendering/service.py`: rationale 2,314 vs on-disk 2,367, a 53-line drift. Final targeted result: failed. **Historical host drift fixed by extraction; current structural inventory regression belongs to Viewing.** Do not loosen threshold/tolerance or edit this inventory here. |

## Changes made

One test-only change in `tests/packs/timeline/test_cli_media.py`: the detached
working-copy helper now passes `None` rather than an opaque `object()` as its
parser client. This uses the existing detached path seam and changes no
product code or semantic assertion.

## Verification

- Central targeted, before the edit: `3 failed, 3 passed in 11.37s`; the two
  CLI nodes and the giant-file node failed.
- Central targeted, after the edit, exact six node IDs: **1 failed, 5 passed
  in 13.01s**; only the Viewing `service.py` inventory drift failed.
- Direct local targeted edited tests, with private/no pytest cache:
  `env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/timeline/test_cli_media.py::test_trim_and_slip_keep_the_film_span tests/packs/timeline/test_cli_media.py::test_a_trimmed_bed_is_extended_to_the_film_end_under_keep_end`
  -> **2 passed in 2.70s**.

No full suite, full-remotion suite, browser, localhost, live-socket, or
subprocess qualification suite was run or requested by this worker. The six
historical full-run artifacts (`request`, `ext`, `log.txt`, `summary`, and
status/exit) and `agent-full797-classification.md` plus
`agent-baseline-109-cutlist.md` were read. No shared dependency, runtime,
fixture, integration worktree, branch, or ref was modified.
