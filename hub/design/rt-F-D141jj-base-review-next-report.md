# F D141jj independent source review

## Verdict

FAIL. The positive source caller path and the no-install/receiving controls passed, but the completed source resume is not independently qualified.

The required lifecycle command did not complete: it stopped at `caller-parent-death` because the candidate correctly refused staging after available space fell to `4,959,588,352` bytes, below its `4,960,000,000` pre-stage admission. No threshold was bypassed and no rerun was attempted.

## Findings

1. `source-manifest.json` is stale. It pins `candidate/receiving_controls.py` to `a5d20f98…`, while the delivered file hashes to `fd8c1a24…`. The only observed content difference from the predecessor is a blank line, but the manifest/hash closure is still false.
2. `run-final-delivery.py:67-145` validates the source tuple and gate tuple independently but never requires each gate tuple `root` to equal the corresponding source tuple `root`. The wrapper stages from gate roots, so a valid-but-different checkout can be built while the source tuple names another checkout.
3. `delivery_gate_build.py:213-223` does not require the recorded `upstream_base` to equal the current `origin/main` for Agent, Runtime, and Composition. It stages from current `origin/main` while applying the recorded base-to-gated delta, leaving the claimed current-upstream identity underconstrained.
4. `run-final-delivery.py:81-99` and `delivery_gate_build.py:187-193,390-393` check source/stage directories for directory/non-symlink status but not owner and mode. The required wrong-owner/wrong-mode refusal is therefore not demonstrated or enforced at these boundaries.

## Passed evidence

- `python3 .../base-resume-next/evidence/check_jj.py`: PASS for actual caller → D68 → stub, frozen App base/tree, current other-three selection, source cleanliness/ref identity, no-install/preimage/outside-row controls, and five refusal fixtures.
- Separate `receiving_controls.py`: PASS.
- Separate installer no-install/preimage invocation: PASS.
- `ruff check --isolated --select F` on `check_jj.py` and candidate Python: PASS.
- AST parse, private `compileall`, JSON parse, and `bash -n candidate/check.sh`: PASS.
- Candidate source worktrees were clean and their refs/trees were readable; no source worktree or registry mutation was observed.
- Positive staging receipt measured `1,126,663` bytes, with alternates-backed private staging and `4,967,452,672` bytes free after staging. The review sampler recorded real five-second available-byte observations.

Full Ruff was not used as a gate: it reports three non-F findings in the inherited candidate (`PLW1510`, `EXE001`, and import ordering in `run-final-services.py`).

## Explicitly unexecuted or deferred

- The remainder of `candidate/check.sh` after the admission refusal, including the final lifecycle/control-pipe/guard summary, is unexecuted in this review run.
- Genuine Main dispatcher admission, Agent REG0, D141v final metadata successor applicability, final delivery build/install, activation, ZIP, and canonical writes remain outside this source-only review.
- No repair, installation, merge, package, bundle, service action, syscall tracing, or full unrelated matrix suite was performed.

