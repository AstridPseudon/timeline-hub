# D141jj finite whole-path findings

## Verdict

`READ_ONLY_FINITE_NOT_READY`. The earlier isolation repair was valid but incomplete. No production-source defect was found, and no source qualification PASS is assigned.

## Blocking findings

1. **Stale fixture does not encode stale upstream.** `check_jj.py:439-448` creates `stale_base`, commits `stale_head`, and records `upstream_base=stale_base`, but leaves `refs/heads/origin/main` at `stale_base`. D68 compares that recorded base with current `origin/main` at `delivery_gate_build.py:228-241`; equality means the intended non-App refusal is false. The observed D68 PASS receipt is a false-positive control result.

   Minimal purpose-preserving fixture adaptation: advance the fixture's `origin/main` to `stale_head` while retaining `upstream_base=stale_base` and `gated_tip=stale_base`. This is the relationship already expressed by the low helper at `check_jj.py:248-256`; the main helper omitted its `update-ref`.

2. **Checker observes the wrong refusal channel.** `check_jj.py:112-117` returns only caught `OSError`/`ValueError` and discards `caller.main(args)`'s integer. A genuine D68 source refusal is converted to a nonzero child exit, returned through `delivery_lifecycle` and `run_wrapper`, recorded as a FAIL diagnostic by D68 (`delivery_gate_build.py:457-464`), then wrapped in the caller's FAIL receipt and returned by `run-final-delivery.py:287-306`. The preserved `assert failure is not None` and `assert not target.exists()` therefore do not describe the current contract.

   Minimal purpose-preserving entrypoint adaptation: capture the caller return code; for this control accept only the documented nonzero refusal, assert the D68/caller diagnostic receipt status is FAIL and contains the stale-upstream reason, and assert the stub builder/positive output was not produced. Do not turn a nonzero return into a Python exception and do not require the caller receipt to be absent.

3. **Stage-owner and stage-mode controls stop too early.** `wrong-stage-owner` monkeypatches `caller.os.geteuid`, which mutates the shared `os` module and makes caller source identity fail at `run-final-delivery.py:58-71,107` before D68. `wrong-stage-mode` supplies the 0775 directory as `service_tmp`, so caller `run_wrapper` rejects it at `run-final-delivery.py:211-213` before D68's private `stage_parent` check at `delivery_gate_build.py:409-415`.

   Minimal purpose-preserving adaptation: keep a valid 0700 outer service root and perturb only the D68 stage-parent ownership/mode after caller validation, through a private harness seam or stage-parent fixture. Isolate any source-owner perturbation from the shared `os` module. The stage controls must still traverse caller -> lifecycle -> D68.

## Earlier collision and route comparison

The original failed log (`ce9e0532`, preserved at the prior evidence path) shows positive D68 PASS, then a `delivery trace already exists` failure, then the stale-upstream assertion. The first isolation derivative gave each no-explicit-root refusal a fresh 0700 service root, eliminating this collision. That repair did not correct the stale fixture or refusal observation.

The prior positive and same33 both exercise the real caller -> lifecycle -> D68 -> bounded stub route. Same33 gives each case a separate TMPDIR and therefore avoids the fixed `timeline-delivery-KEEP/disk-trace.tsv` collision. Its low-floor, trace, sampler, and source checks remain lifecycle/entry validation; none is a semantic PASS for a later D68 source guard.

## Unverified

The seven controls were not re-executed by this task. No staging, builder, service, installer, source authoring, product import, or full suite was run. Same33's retained actual PASS remains retained and was not duplicated.
