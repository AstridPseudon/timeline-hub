# Receiving handoff

The stale missing-Agent prerequisite is cleared by the done receipt
`checkout-agent-2eca9a1da94eb35bb969540e150192ff920ce326` and the clean
checkout `/home/user/work/wt/agt-pin-2eca9a1d` at commit `2eca…`, tree
`888c…`. Do not gate on the old `22bf…` source.

The smallest next step is to repair the candidate code before installation:

1. Make `dry-check.sh` validate the actual launcher manifest format consumed
   by `p4-d73-pinned-launch.sh` (or explicitly separate a JSON receipt from the
   key/value launcher manifest).
2. Make the bounded control either invoke the supported production `run --`
   argv or state accurately that it only covers `dry`; preserve the focused
   positive-17 one-call and poisoned zero-call behavior.
3. Render one genuine four-repository manifest and bind both exact source rows
   to it. Install the two rows only through the existing central route.
4. Run each exact `--files` request once, preserving `D66_OUTPUT_DIR`, XML,
   raw runner output, and receipt artifacts per central request ID.

No source-body, request/reply-shape, Runtime, App, or Composition product
change is requested by this review. Functional readiness must be reported
separately from source review after the receiving run exists.
