# P2 SWAP3250 native preparation handoff

Source-only handoff for manager publication. Exact native replay is not
admissible from the safe 3250 packet: the packet retains the exact tuple and
terminal predicates, but not the original request body, authentic pre-SWAP
history/base state, exact media custody, or private realm/auth inputs.

Use the existing registered acceptance command only after a receiving
diagnostic source is bound to Runtime `5e9ad1c6` and light admission is at
least 5 GB:

```text
env ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-070dfc5e PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -o addopts= --junitxml="$D66_OUTPUT_DIR/p2-swap-native.xml" diagnostics/test_p2_swap_native.py::test_p2_swap_native_replay_and_d112_control
```

Registered suite: `full-p2-swap-native-1055`. This worker did not execute it.
The full source-preparation report and JSON manifest are in this worker's
evidence directory. The source-faithful App recipe and D112 positive differ
precisely in setup history, fork placement, command grouping, merge mode,
target clip, caller path, and separate Undo; those differences must not be
collapsed into a replay claim or a Runtime root claim.

Exact tuple: App `fe3309db` / Agent `070dfc` / Runtime `5e9ad1c6` /
Composition `635f4de0`, with the pinned trees recorded in the JSON manifest.
