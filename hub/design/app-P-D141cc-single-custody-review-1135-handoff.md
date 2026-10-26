# Handoff

P2 D141cc `p2-transition-none-single@original` is **FAIL_CUSTODY / NOTRUN**.

The sole native submit returned exit 1 before request/row/artifact creation because of the manually typed agent SHA mismatch. The receipt additionally records integration checkout paths instead of the accepted detached paths; the worker log renders conflicting detached values, so custody is not qualified. Preserve the exact stderr and raw hashes. Do not retry, repair, substitute a selector, infer a body verdict, or call this a product PASS/FAIL.

Current source pins, trees, builder hashes, and the Composition worktree remain unchanged. D141ff and other selectors are separate scopes.
