# Receiving invocation after final source PASS

This review authorizes no E2E execution by this worker. After independent
review PASS, the Agent is the sole actual venue. Use the exact final source
tree, a fresh private TMPDIR, an admitted private source-carrier service, and
at least `5905580032` available bytes. Preserve the `4000000000` stop line,
source floor4.6GB, no-heavy/default180 controls, existing benches and helpers.
Do not reuse a venue or retry a failed body.

```sh
set -eu
export TMPDIR=/the-admitted-agent-service-private-run
export ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
SOURCE=/the-service-exact-final-source-tree
RUNNER="$SOURCE/ops-child-custody/tests/e2e_inventory.py"
PY=/home/user/work/venv-agent/bin/python
BOOTSTRAP="$ORCH/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz"
AGENT_CHECKOUT="$TMPDIR/tiny-agent"
RUNTIME_CHECKOUT="$TMPDIR/tiny-runtime"
WHEELHOUSE="$TMPDIR/tiny-wheelhouse"
ORCH_ROOT="$TMPDIR/tiny-orch"
PARENT_WORK="$TMPDIR/tiny-parent-work"
CANDIDATE_WORK="$TMPDIR/tiny-candidate-work"

PYTHONDONTWRITEBYTECODE=1 "$PY" "$RUNNER" --check-only \
  --helper "$ORCH/bin/bench_store.py" --bootstrap-artifact "$BOOTSTRAP" \
  --runner-python "$PY" --build-python "$PY" --python /usr/bin/python3.13 \
  --wheelhouse "$WHEELHOUSE" --agent "$AGENT_CHECKOUT" --runtime "$RUNTIME_CHECKOUT" \
  --orch-root "$ORCH_ROOT" --parent-work "$PARENT_WORK" \
  --candidate-work "$CANDIDATE_WORK" --result "$TMPDIR/check-only.json"

PYTHONDONTWRITEBYTECODE=1 "$PY" "$RUNNER" --prepare-venue "$TMPDIR/tiny-venue.json" \
  --helper "$ORCH/bin/bench_store.py" --bootstrap-artifact "$BOOTSTRAP" \
  --runner-python "$PY" --build-python "$PY" --python /usr/bin/python3.13 \
  --wheelhouse "$WHEELHOUSE" --agent "$AGENT_CHECKOUT" --runtime "$RUNTIME_CHECKOUT" \
  --orch-root "$ORCH_ROOT" --parent-work "$PARENT_WORK" --candidate-work "$CANDIDATE_WORK"

PYTHONDONTWRITEBYTECODE=1 "$PY" "$RUNNER" \
  --venue-manifest "$TMPDIR/tiny-venue.json" --result "$TMPDIR/tiny-e2e-result.json"
```

The first command must exit0 with no missing entries before preparation. The
second performs only the unchanged private setup after the complete census,
including empty `tests/suites.conf` before the normal Store initialization.
The third is exactly one parent-RED/candidate-GREEN whole-maker run, followed
by authentic report/registration equality, unchanged sealed verification and
the original adversarial checks. Stop at the first unexpected refusal or
reserve crossing and obtain the independent result review. A source PASS is
not an E2E GREEN claim; installer1826 remains held until the final result
passes.
