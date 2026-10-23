# Agent G4 render current-resolution review

**Result: PASS for the G4 render delta.** Reviewed merge
`737df3dbfd567943e7d21f085b2d290c31087449` (`d4b212572482c56d974c28ac564e97f0287a7fe6`
plus current `ecea7d8563c93059283ef9475ecb41a37e628a38`). The true delta onto
`ecea` is limited to the requester render publication handoff, requester
RemoteTasks adapter, settled assembly commit helper, production wrapper, one
native CLI output correction, their tests, and the Ruff baseline metadata.

Requester render sources match `d4b` byte-for-byte. All six approved V4
live-scenes deletions remain absent. Protected G3/R2/R3/meta source, generated
client, Runtime lock, and tests remain unchanged from `ecea`. The requester
path retains exact producer/requester scope and fence checks, outbox/restart
replay, full v2 commit fields and structured replies, exact canonical render
pinning, and no old worker-authority publication route.

Evidence: requester publication **13 passed**; v2/error/meta/open-commit
neighbors **48 passed**; render/assembly/producer neighbors **221 passed**;
Runtime 780 lock (**15 mappings**) and artifact manifest passed; scoped Ruff
and private targeted mypy passed; normal ratchets are Ruff **2149/2149** and
mypy **1915/1915**. Worktree clean; diff check and conflict-marker scan clean.
No full/browser/farm/render-heavy/live-socket suite was run.

Inherited separately: G3 `inverse.steps` schema drop (`a51678…` vs required
`d106dfe8…`) remains the already-known FAIL0304 / repair0314 block and was not
edited or waived. Runtime's malformed partial receipt / missing
`preview.would_status` hold also remains separate and Runtime-owned.
