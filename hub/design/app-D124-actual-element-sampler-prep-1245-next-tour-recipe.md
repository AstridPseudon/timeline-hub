# Next tagged P2 recipe

## Gate

**Do not run or submit until the Runtime publisher supplies the exact current
tuple handoff.** The current handoff file is only a request. The source-only
normal D66 command is retained in `next-tour-recipe.json`, with the exact
App/Agent/Runtime/Composition pins and the existing `p2` selector. It must be
bound to detached, clean checkout receipts by the controller.

The worker does not submit, retry, run a browser/native/service/full suite, or
change the D66 suite registry.

## Required sampler activation

The approved D111a method must be loaded into the actual `runtime_protocol.cli`
daemon handling the hosted browser request. The private marker lifecycle is:

1. Create a mode-0700 private output directory and mode-0600 idle marker.
2. Arm the browser response waiter for the element commit, then activate the
   marker immediately before the real `AM Burst` Apply gesture.
3. Mark done immediately after the browser response is captured. Keep the
   private profile/result until Runtime teardown completes.
4. Select exactly one request using the supported private correlation/hash and
   bind it to Runtime PID plus Linux birth ticks. Use the browser POST wall
   interval as the denominator.
5. Run the offline control. It refuses ambiguous selection, PID/birth drift,
   missing handler timing, broad input permissions, or missing wall timing.

This lifecycle is a control specification, not an assertion that the current
D66 launcher supports the attachment. Current `runtimeEnv()` overwrites
`PYTHONPATH`, and the existing D111a source has no safe per-request correlation
hash. A wrapper, overlay, header injection, or modified harness is not an
approved substitute.

## Safety/accounting

Per-sample safe-frame identity is deduplicated. Inclusive frame shares overlap
and are not additive. `lost_samples` remains explicitly process-lifetime
observer gap, never request loss. Observer CPU remains process-lifetime, never
claimed as request overhead. Calibration uses the fixed 20 ms interval only as
nominal metadata; request wall time is the true denominator.
