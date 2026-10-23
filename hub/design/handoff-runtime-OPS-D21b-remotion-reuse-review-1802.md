# Runtime handoff: OPS-D21b Remotion reuse independent review

Status: FAIL; do not install or merge.

The private same-tree matrix does reuse one physical synthetic graph across different Agent and Runtime source IDs, and the request writer preserves 2/3/7 argument payloads. That evidence is not production qualification.

Blocking facts:

1. Reuse runs before verify_node. With the author's own RUNTIME_NODE_BIN=/does/not/exist, the candidate returns success and writes ASTRID_NODE_EXECUTABLE=/does/not/exist/node. The current Node 20.19.4/npm 10.8.2 host guard is therefore bypassed.
2. The candidate accepts the fixture's fabricated build-origin marker 1111111111111111111111111111111111111111; it checks only hexadecimal shape and does not authenticate source custody or the origin Remotion tree.
3. Existing agent-remotion, agent-remotion-0013, and agent-remotion-current graphs use the old layout and lack the candidate markers. They are future-only partials for this reuse protocol; no actual 5.1 GB graph PASS is claimed.
4. The author positive does not vary requested Agent/Runtime source identities. An independent private synthetic pair did, but it still hit item 1 and cannot certify a real graph.

Checks: bash -n PASS; scoped Python compile PASS; hashmanifest PASS; assigned Runtime worktree clean against 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d; author offline matrix PASS; private request-writer 2/3/7 queue-shape smoke PASS. No dispatcher/daemon/provision/network/install/build/host publication was run.

Required owner follow-up: validate/select the actual Node/npm toolchain before reuse, bind it into the reused env/suite, authenticate or conservatively refuse unproven build-origin markers, and add real-layout plus engine/origin/profile/template/manifest/partial/dirty/source-ID negatives. Preserve the old graphs as future-only until a compatible authenticated receipt exists. No consumer-identity waiver.

