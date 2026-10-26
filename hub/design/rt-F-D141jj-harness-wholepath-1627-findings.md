# F D141jj whole-path findings

## Result

The failed complete `check_jj.py` run is a control-harness failure, not a
production guard failure. The positive caller -> D68 path passed, then the
later stale-nonapp-upstream refusal did not reach its intended source guard.
No source qualification PASS is assigned.

## Exact collision

The positive invocation created the private checker work directory
`.../d141jj-check-5gzvtnl9/service-tmp`. `run-final-delivery.py:211-232`
created a unique D68 stage parent below it, but passed the *outer*
`service_tmp` to `run_delivery`. The lifecycle therefore intentionally wrote
its retained evidence at:

`.../service-tmp/timeline-delivery-KEEP/disk-trace.tsv`

and returned PASS. The exact positive log records D68 PASS, the positive
receipt, the stale-manifest refusal, the no-install/preimage controls, and the
gate/source-root refusal before the later negative.

The later `stale-nonapp-upstream` call used `check_jj.py:402-432`'s refusal
helper without a `service_root`, so the process environment still pointed at
that same outer `service-tmp`. D68 lifecycle code
`delivery_lifecycle.py:290-337` reused the fixed `timeline-delivery-KEEP`
path, saw the retained `disk-trace.tsv`, and correctly failed closed with
`delivery trace already exists`. Consequently the child never reached
`delivery_gate_build.py:221-242`, where the stale non-App `origin/main` guard
would have refused the fixture. The checker then asserted at
`check_jj.py:448` that a refusal exception existed.

## Complete finite defect set

1. **Isolation defect (blocking):** the checker has one shared lifecycle
   `service_tmp` for the positive call and negatives. Give every caller
   invocation its own mode-700 service root, while preserving explicit
   `service_root` fixtures for the stage-owner/mode negatives. The smallest
   correction is to create a fresh `work/<label>-service-tmp` inside the
   refusal helper when no explicit root is supplied, and use it for
   `TMPDIR`, `TMP`, and `TEMP`. Do not remove or overwrite retained traces.

2. **Refusal-observation defect (would remain after isolation):**
   `check_jj.py:112-117` ignores the integer returned by `caller.main`; it
   reports only Python exceptions. The real stale guard is raised in the
   child D68 wrapper, converted to a nonzero child exit, and propagated as a
   nonzero caller return. After isolation, the refusal assertion would still
   fail unless the private helper treats a nonzero return as refusal (for
   example, return a local `ValueError` sentinel while preserving the existing
   `failure is not None` assertion). This is checker-only; do not alter the
   caller or D68 return contract.

No other finite isolation defect was found: the checker `work` directory is
per-invocation, receipt names are label-specific, the positive D68 stage parent
is unique, and SAME33 assigns each case its own `TMPDIR` case directory.

## Comparisons

- SAME33/lifecycle controls passed because `candidate/check.sh` sets a fresh
  case directory as `TMPDIR` for each case; each case gets its own retained
  `timeline-delivery-KEEP` and trace.
- Earlier negatives passed because stale-manifest validation and the
  source/gate-root binding fail before D68 lifecycle entry.
- The current caller/D68/lifecycle path is byte-exact to the supplied manifest:
  the caller invokes lifecycle around the D68 wrapper; lifecycle retains and
  rejects a pre-existing trace; D68 performs source snapshot validation inside
  that lifecycle. This ordering is intentional production behavior. The
  collision is caused by the checker reusing the lifecycle root.

