# Agent receiving invocation

Status: source/unit qualification only. Independent exact-final review is next. The Agent's existing receiving service is the sole actual venue; installer1826 stays held until the genuine E2E and its result review pass. No service, Git creation, receiving Store initialization, install, or genuine body was submitted by this worker.

## Exact source binding

The worker's Git HEAD is the **base** `2fffe593175338ffb8144705bb70c9542fa4459f` (tree `516da69731401037b6845f1e14ea11b4c9135628`), not a final commit. The harness assigns the final commit after exit. Its SHA is currently EXACTMISSING and must be resolved by the receiving reviewer; never use historical parent674d as final. The final two-file working source has calculated Git tree `dd4347a933103bbfc17c3e3237d52ea13ac1f677`, runner SHA-256 `1498a1597c058f92176a0d447b372b4791e6af345c479445b9027e0521d75085`, and test SHA-256 `eeeddb0fcac8863a364c4814fac82830f3fb70b7505a311eb10acc954fdd0137`. Verify the harness final commit's actual tree and runner hash against those values before changing the existing receiving source binding. Source tree calculation was validated against Git's base tree and writes no Git objects/index/refs.

Use the complete exact source tree, including `ops-child-custody/tests/support.py`, the tiny manifest/all 15 source files, and both frozen makers. Keep the normal service's source-carrier Git history creation: it materializes exactly the manifest's Agent/Runtime files into **two fresh private receiving checkouts**, commits them normally, then authenticates the clean HEAD/file set/modes/blob hashes. This worker creates no fixture Git history or substitute service/process files. The inherited 1816 source1747 wrapper binding is historical, not this final source.

## Inputs to stage in the admitted Agent service

Start only after independent final PASS and normal service admission with at least `5905580032` available bytes. Preserve the `4000000000` stop line, sourcefloor4.6/noheavy/default180 controls, all installed benches and production helpers. Main is below reserve: no genuine E2E here.

- Runner/build Python: `/home/user/work/venv-agent/bin/python` (Python 3.13.16; build 1.4.0, setuptools 80.9.0, wheel 0.46.3). Preserve the venv invocation spelling even though its interpreter is a symlink; resolving it would select the system environment.
- Child Python: physical `/usr/bin/python3.13`. Do not select missing venv-runtime or use system Python as the offline build environment.
- Protected helper: `$ORCH/bin/bench_store.py`, SHA-256 `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`.
- Bootstrap archive: `$ORCH/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz`, SHA-256 `443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548`. Its basename is required by the unchanged maker.
- Existing receiving source-Git service supplies clean Agent/Runtime tiny carriers under this run's TMPDIR. The source-only CLI `--write-inputs "$TMPDIR/source-inputs"` can materialize manifested files; it creates no Git history. The service, not this worker, performs its ordinary fixture commits.
- Existing offline staging supplies all five wheels, authenticated by the manifest/bootstrap pins: pip 26.2.1, setuptools 80.9.0, wheel 0.46.3, custody_b 0.1.0, custody_a 0.1.0. If necessary the existing `--build-wheels "$TMPDIR/tiny-wheelhouse" --build-python /home/user/work/venv-agent/bin/python` command builds only the two tiny dependencies offline, without isolation/acquisition; stage the three bootstrap wheels using the normal receiving service. Never write shared dependencies or introduce a new installer.
- All carrier/wheelhouse/orchestration/work/output paths below are fresh private paths. Setup roots must be disjoint, writable, outside the input directories, with existing writable parents. Ambient `python3` and the enumerated shell commands must exist. No production index/credentials/provider/core/profile/network is involved.

## Complete census, then unchanged private setup, then one body

These commands are for the existing Agent service **after** final source review/admission and input staging. SOURCE names the service's complete exact final source tree, not this worker's branch tip or a historical archive. ROOT/TMPDIR are supplied by that service, not newly allocated here.

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

`set -e` stops on nonzero census/preparation. Preparation itself now repeats the complete nonmutating census before the unchanged setup function. It still writes empty private `tests/suites.conf` before the two existing `Store.initialize` calls, and never changes their API. The last command is exactly one parent-RED/candidate-GREEN whole-maker run, authentic report/registration equality, unchanged sealed verifier and existing adversarial assertions. Never reuse a venue or retry automatically; stop at first unexpected refusal or floor crossing, retain the result, and obtain the existing result review. No actual body is authorized by this document alone.
