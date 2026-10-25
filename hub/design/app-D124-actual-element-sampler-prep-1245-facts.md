# D124 actual element sampler prep

Status: **blocked on the exact supported attach handoff; no tour body created or submitted.**

## What is reusable

The existing Runtime diagnostic source is the D111a/native1218 method from
Runtime commit `a0b3eac1a2126c6bf2e77f06ab5d0a9312ef4328`, tested against its
`7070f1378d1917fcce69857ebd33cd2b3015568b` parent. The source-byte SHA-256
values are recorded in `facts.json` and the private reuse manifest. It uses the
Runtime daemon's normal `runtime_protocol.cli` process, passive Python tracing,
20 ms sampling, per-sample frame deduplication, handler/read timing, and
PID/birth-tick identity. It does not alter Runtime product code.

The App already has a supported D66 private lifecycle sink. D66 configures it
before `DirectHarness` construction; the normal daemon and the Agent-authoring
restart inherit the selected private sink; ordinal-specific directories avoid
reusing a sink; teardown retains bounded mode-0600 streams. This is the only
currently verified normal startup/teardown path.

## Concrete missing seam

The requested flat Runtime handoff is not a handoff yet: the file contains the
Runtime publisher's request, not source bytes or an invocation. D66's
`runtimeEnv()` in `tests/e2e/local/support/harness.ts:692-706` overwrites
`PYTHONPATH` with the App phase bootstrap, selected Runtime checkout, and Agent
checkout. Therefore setting `D111A_*` variables cannot load D111a's
`sitecustomize_d111a.py` into the actual D66 daemon. The existing D66 hook loads
only the phase helper named by `ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER` and is not
the D111a sampler.

There is a second qualification gap: the retained D111a launcher measures a
synthetic direct Node POST. It does not select the browser-originated element
POST from the tagged next tour. Its `lost_samples` and observer CPU values are
process-lifetime counters, and its displayed sample share uses a nominal
sample interval rather than the selected browser request wall denominator.

No body is safe until Runtime supplies a current-tuple source handoff and a
supported attachment/correlation method. A wrapper executable, PYTHONPATH
overlay, modified harness, new HTTP header, or speculative collector would be
an unsupported seam and was not invented here.

The prior retained `11:50:14.905Z` trace remains unusable because it lacks the
App receive marker and Runtime UTC anchor. It is not reused.
