# D118d own9 command results

Admission:

```text
df -B1 /home/user/work/wt/app-D118d-projection-own9-final-1646
admission: 5094088704 bytes available
post-run: 5092470784 bytes available
floor: 5000000000 bytes
stop: 4000000000 bytes
```

Source custody checks passed: the worktree was clean; `tests/sdk/test_timeline_capture_projection.py` had SHA-256 `6e41a5bba04666275b9e252d7aeb30247a145207da3f9ed14f06b338563a1436` and Git blob `16954294f9f70018e4bbd1012083f51594f6cb19`, matching the reviewed source. The Runtime pin was clean at commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.

Exact command run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=evidence/own9.xml tests/sdk/test_timeline_capture_projection.py::test_real_saved_projection_config_registry_and_full_pins_golden tests/sdk/test_timeline_capture_projection.py::test_real_saved_entire_expansion_golden tests/sdk/test_timeline_capture_projection.py::test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[parent]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[child]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[new_shot]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[duplicate]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[remove]' 'tests/sdk/test_timeline_capture_projection.py::test_real_candidate_matches_sdk_opener_exactly[sdk_bundle]'
```

Result: exit 1; 9 tests collected, 9 setup errors, 0 failures, 0 skipped, 16.26s. JUnit XML records `errors="9" failures="0" skipped="0" tests="9"`.

First safe exact failure: `tests/sdk/test_timeline_capture_projection.py:311` calls the real commit path; `astrid/sdk/timeline/_command_state.py:369` raises `astrid.sdk.timeline._command_state.CommandError` with kind `identity_conflict` and message `shot item correspondence changed`. It surfaces as `runtime_protocol.errors.RuntimeErrorBase: shot item correspondence changed`. All nine nodes hit the same setup error. No source fix or retry was made.
