# Agent receiving invocation

The receiving service must materialize `--write-inputs` into two dedicated
clean fixture checkouts and commit the exact emitted files through its normal
receiving path. The worker does not initialize Git or Stores.

```sh
export TMPDIR=/target-private-tmp
python ops-child-custody/tests/e2e_inventory.py --check-only \
  --helper "$TMPDIR/bench_store.py" --bootstrap-artifact "$TMPDIR/bootstrap-wheel-input.tgz" \
  --wheelhouse "$TMPDIR/tiny-wheelhouse" \
  --agent "$TMPDIR/tiny-agent-fixture" --runtime "$TMPDIR/tiny-runtime-fixture" \
  --orch-root "$TMPDIR/tiny-orch" --parent-work "$TMPDIR/tiny-parent-work" \
  --candidate-work "$TMPDIR/tiny-candidate-work" --result "$TMPDIR/check-only.json"
```

Only after check-only exits 0 and the unchanged reserve is admitted:

```sh
python ops-child-custody/tests/e2e_inventory.py --prepare-venue "$TMPDIR/tiny-venue.json" \
  --helper "$TMPDIR/bench_store.py" \
  --bootstrap-artifact "$TMPDIR/bootstrap-wheel-input.tgz" \
  --orch-root "$TMPDIR/tiny-orch" --python /usr/bin/python3.13 \
  --wheelhouse "$TMPDIR/tiny-wheelhouse" --agent "$TMPDIR/tiny-agent-fixture" \
  --runtime "$TMPDIR/tiny-runtime-fixture" --parent-work "$TMPDIR/tiny-parent-work" \
  --candidate-work "$TMPDIR/tiny-candidate-work"
python ops-child-custody/tests/e2e_inventory.py --venue-manifest "$TMPDIR/tiny-venue.json" \
  --result "$TMPDIR/tiny-e2e-result.json"
```

The first command is exhaustive and non-mutating. The second creates only the
two private Stores through the unchanged Store API, with `tests/suites.conf`
created first. The final command is the one genuine parent-RED/candidate-GREEN
path; do not run it when the reserve is below `5905580032` bytes or rerun a
failed venue.
