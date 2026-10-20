# Runtime visibility/auth final review

Verdict: **REJECT pending one-line correction**.

The candidate `ecd63784a8e2ba19939b4da14966b059f36fde8b` (tree `36061d5fa887a47864eef077bd596718649c91ec`) cleanly applies to current integration `3b900c377e7126e14eeb92dc2ce73114cbda5a0e`; hypothetical merged tree: `3fb300766b0dde3f5fa72548489ed562bd43cb09`.

The archive/recover HTTP matrix covers unauthenticated and read-only reader credentials with `401`, unchanged snapshots, and zero writes. Historical recover covers tracked/fresh/unused and installs the replay trap before the call. Existing visibility-positive assertions remain. The strict xfail is scoped to the post-setup timeline-update call through `_RetiredTimelineUpdate`, so setup or unrelated `ApiError` failures cannot satisfy it.

Required correction: in `tests/test_runtime_domains.py:28-33`, also require the exact message `legacy timeline writes are retired; submit EditCommands through commitTimeline`, matching `runtime_protocol/service.py:1629-1633`. The current sentinel guard checks status/code/reason only, so a wrong message with matching metadata could still satisfy the xfail.

Evidence was inherited as requested: central exact lane `78 passed, 3 xfailed` on tree `36061d5...`; service-only historical lane `3 passed, 56 deselected`. Review-time `git diff --check`, patch-apply check, and clean merge-tree checks passed. No rerun/full/socket test was performed.
