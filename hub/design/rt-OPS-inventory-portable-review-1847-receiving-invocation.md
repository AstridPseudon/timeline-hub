# Normal receiving invocation

The normal receiving service must first materialize the exact Agent and
Runtime tiny source files from `ops-child-custody/e2e-fixtures/tiny/{agent,runtime}`
into clean dedicated checkouts and create their ordinary fixture commits. The
worker does not create those Git histories. It must stage the two pinned tiny
dependency wheels and the three bootstrap wheels into the private wheelhouse
using the already-qualified offline inputs.

After those inputs exist, run the non-mutating census first. This is the exact
receiving-side command; all paths are explicit so the maker defaults cannot
redirect the run to production:

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

Admission rule: continue only if that command exits 0 and the receiving
filesystem has at least `5905580032` bytes available. Then prepare the two
private Stores through the unchanged API, and run exactly one genuine body:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
  ops-child-custody/tests/e2e_inventory.py --prepare-venue \
  "$TMPDIR/tiny-venue.json" \
  --helper "$ORCH/bin/bench_store.py" --orch-root "$ORCH_ROOT" \
  --python /usr/bin/python3.13 --wheelhouse "$WHEELHOUSE" \
  --agent "$AGENT_CHECKOUT" --runtime "$RUNTIME_CHECKOUT" \
  --parent-work "$PARENT_WORK" --candidate-work "$CANDIDATE_WORK"

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python \
  ops-child-custody/tests/e2e_inventory.py \
  --venue-manifest "$TMPDIR/tiny-venue.json" \
  --result "$TMPDIR/tiny-e2e-result.json"
```

The final command is one bounded parent-RED/candidate-GREEN run followed by
the unchanged sealed verifier and adversarial checks. Never use
`/home/user/work` as the fixture work root, never reuse either private Store,
and stop at the unchanged 4 GiB floor (`4000000000`) or on the first
unexpected refusal. This source review authorizes no run while the review is
FAIL.
