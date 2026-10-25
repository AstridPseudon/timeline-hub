# D116 NEW4 commands and results

## Admission and custody

```text
df -B1 --output=source,avail,target . /tmp
PASS before launch: /dev/vda 5005950976 /home/user/work/wt/app-D116-native4-own-proof-1711
PASS before launch: /dev/vda 5005950976 /tmp

git rev-parse HEAD
795608e1b9d8077487b26eea50b65c1e79c3f522

git status --porcelain=v1
PASS: empty

git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse HEAD
5e9ad1c6f74241d8771d3284fdd2ce7a214fd344

git -C /home/user/work/wt/rt-pin-5e9ad1c6 rev-parse 'HEAD^{tree}'
de2954a0ceadb4455903d9abdfec3b773318a50f

git -C /home/user/work/wt/rt-pin-5e9ad1c6 status --porcelain=v1
PASS: empty
```

The required admission record was persisted immediately before launch in `body-admission.json` with decimal availability `5005950976`, above the `5000000000` floor.

## Exact functional launch

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=<own evidence>/own4.xml <EXACT4NEWnodeIDs>
```

Expanded selectors were exactly:

```text
tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_move_trim_lost_ack_restart_and_guarded_undo[disjoint-peer]
tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_move_trim_lost_ack_restart_and_guarded_undo[touching-peer-conflict]
tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_commands_file_preserves_opaque_unchanged_write_and_undo
tests/editing_conformance/test_native_checkout_current_equivalent.py::test_current_checkout_gate3_reload_undo_and_visualize_report_unavailable
```

Result:

```text
3 failed, 1 error in 28.85s
```

The three failures report `TimingCompileError: exact transcript pin is missing or revoked or ambiguous` at `astrid/sdk/timeline/native_word_anchor.py:100`, wrapped at line 381 as `CommandError kind=invalid_anchor`. The gate3 case errors in setup at `tests/editing_conformance/native_checkout_current_fixture.py:90` with `RuntimeErrorBase: closure membership and edges require semantic commands`.

No retry, source fix, broader collection, central test request, or unrelated test was run. Raw XML/log remain private worker artifacts; hashes are recorded in `facts.json`.
