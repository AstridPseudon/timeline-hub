# Supported D66 external-helper activation

The supported normal route is the existing D66 `p2-element` service recipe, not
a synthetic launcher:

```text
D66_OUTPUT_DIR=<private worker submission directory> \
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node \
  --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-element --submit
```

The recipe's source is App `scripts/testing/d66-plain-stack.mjs`: the canonical
helper is `tests/helpers/p2_commit_phase_capture.py` (constant at line 76), the
external helper path and SHA are validated before the normal recipe is emitted
(lines 365-380), and `p2-element` selects the single original test by its exact
grep descriptor (lines 21-24). The Runtime child receives the helper through
the normal harness environment (`harness.ts` lines 722-731), and the existing
`sitecustomize.py` loads only the canonical basename after the normal Runtime
CLI starts.

The previously reviewed external helper blob was
`4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e` at the
Runtime `e319fdb...` parent. This first-return candidate's helper SHA is
`a92122c24afc581f71687d25ffc6a4bd8bb7c2e7381e5b47a6be861d23594a1c`; normal
D66 adoption must use that new SHA only after the required independent review.

Selection remains source-local and body-safe: actual
`runtime_protocol.server.RuntimeHandler._timeline_commit`, POST to the exact
commit route with existing `_prefetched_body`, API v1, non-dry-run, and exactly
one `clip.set-element` command. A mixed command, retry/second element request,
wrong route/method/query/request, or unselected handler is not profiled.
Setup/native non-element commits do not consume the one-shot element selection.
No readiness/bootstrap/native setup or full process is profiled. No mounted
element body was run in this worker, so this is an attachment recipe and source
guard, not production-run qualification.
