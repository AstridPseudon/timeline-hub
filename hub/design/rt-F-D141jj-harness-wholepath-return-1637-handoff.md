# D141jj handoff: finite read-only NOT_READY

The earlier private isolation derivative correctly separated refusal service TMP roots, but it did not clear the gate. The remaining correction is harness-only and has two independent pieces:

1. Advance the stale fixture's `origin/main` to its new `stale_head` while retaining the recorded `upstream_base=stale_base`.
2. Observe the real caller's nonzero return and FAIL diagnostic receipt for D68 refusal; do not require a Python exception or absent caller receipt.

Before any future control run, repair stage-owner/mode fixtures so service TMP validation succeeds and only D68's private stage-parent check is perturbed. Do not call the current false-positive controls semantic PASS. No product/source merge follows this handoff.
