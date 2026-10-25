# Normal receiving invocation

The normal receiving service must materialize the exact manifest-declared Agent and Runtime tiny source files into clean dedicated checkouts and create their ordinary fixture commits. It must stage the two pinned dependency wheels and the three pinned bootstrap wheels into the private offline wheelhouse. The review worker does not create those Git histories, Stores, or installs.

All paths below are explicit and must be under the admitted private run directory:

```sh
set -eu
export TMPDIR=/the-admitted-run-tmpdir
export ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
export AGENT_CHECKOUT=/the-normal-receiver/tiny-agent
export RUNTIME_CHECKOUT=/the-normal-receiver/tiny-runtime
export WHEELHOUSE="$TMPDIR/tiny-wheelhouse"
export ORCH_ROOT="$TMPDIR/tiny-orch"
export PARENT_WORK="$TMPDIR/tiny-parent-work"
export CANDIDATE_WORK="$TMPDIR/tiny-candidate-work"
export CHECK_RESULT="$TMPDIR/check-only.json"

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
  ops-child-custody/tests/e2e_inventory.py --check-only \
  --helper "$ORCH/bin/bench_store.py" \
  --bootstrap-artifact "$ORCH/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz" \
  --runner-python /home/user/work/venv-agent/bin/python \
  --build-python /home/user/work/venv-agent/bin/python \
  --python /usr/bin/python3.13 \
  --wheelhouse "$WHEELHOUSE" \
  --agent "$AGENT_CHECKOUT" --runtime "$RUNTIME_CHECKOUT" \
  --orch-root "$ORCH_ROOT" --parent-work "$PARENT_WORK" \
  --candidate-work "$CANDIDATE_WORK" --result "$CHECK_RESULT"
```

Continue only when this exits `0` and the receiver has at least `5905580032` bytes available. Then run the unchanged private preparation API exactly once:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
  ops-child-custody/tests/e2e_inventory.py --prepare-venue \
  "$TMPDIR/tiny-venue.json" \
  --helper "$ORCH/bin/bench_store.py" \
  --bootstrap-artifact "$ORCH/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz" \
  --orch-root "$ORCH_ROOT" --python /usr/bin/python3.13 \
  --wheelhouse "$WHEELHOUSE" --agent "$AGENT_CHECKOUT" \
  --runtime "$RUNTIME_CHECKOUT" --parent-work "$PARENT_WORK" \
  --candidate-work "$CANDIDATE_WORK"
```

Only after successful preparation may the receiving service run one genuine body:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
  ops-child-custody/tests/e2e_inventory.py \
  --venue-manifest "$TMPDIR/tiny-venue.json" \
  --result "$TMPDIR/tiny-e2e-result.json"
```

That body is the single bounded parent-RED/candidate-GREEN run followed by the unchanged sealed verifier, report/registration equality, and adversarial checks. Never reuse a private Store or venue, and stop at the unchanged `4000000000`-byte floor or the first unexpected refusal. This review authorizes no actual body while the source verdict is FAIL.
