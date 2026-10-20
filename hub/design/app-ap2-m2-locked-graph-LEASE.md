# App M2 locked graph lease

- Lease owner: `ap2-m2-locked-app-test-graph`
- Created: `2026-10-20T17:03:43Z`
- Source: App `48576cfa2783331f2c7c8309ff4069162a3afd11`, tree `126983e329d1ab85a59d7a62ebb96676f8aab622`
- Graph: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph/`
- Wrapper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-wrapper.sh`
- Source archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar`
- Source archive SHA-256: `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- Locked Composition artifact SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`

Lease rules:

1. Downstream consumers may read the graph and invoke the wrapper, but must not write inside the graph or shared dependency targets.
2. Each invocation must use its own private source-run and cache paths. The published wrapper enforces this under `/tmp/app-ap2-m2-locked-run.*`.
3. This lease remains valid only while the graph, wrapper, source archive, and hashes above are unchanged and the App source identity remains the recorded HEAD/tree.
4. If a dependency changes, rebuild a new private graph and lease; do not patch this graph in place.

