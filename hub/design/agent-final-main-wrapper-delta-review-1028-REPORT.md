# Agent final MAIN wrapper delta review — 2026-10-21

## Verdict

**APPROVE.** The final wrapper at `scripts/full_coherent_public_current_integration.sh`
is approved for the exact b3c96a758 Agent source tuple. The `run-on-main-agent-coherent-public-current.md`
handoff is a concrete releasable MAIN request, conditional on its stated HOLD:
publish this wrapper commit/blob, materialize and verify the exact private profile,
then make the one exact `env -i` request. This review did not authorize or run that
MAIN execution.

## Exact identities

- Wrapper commit: `297fbe0e5cf9bc37c7115dae294838f96df95f16`
- Wrapper tree: `a4fdb4a28b9d7a88267105f8261518336a18047e`
- Wrapper blob: `aa8dda3e9cf81301c163294ceec805d97be0d5c8`
- Wrapper file SHA-256: `09822614697e50a0764c2a125bfd0575baadeeb2f87661b4b3a4a10551e96438`
- Expected Agent source: commit `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`,
  tree `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857`
- `hub/tl/integration` and `hub/timeline/agent/tl/integration` both resolved to
  that exact Agent commit/tree during review.

## Review scope and results

- The final delta from the repaired 1014 wrapper is exactly the two Agent
  commit/tree constants and the three `c4b` → `b3c` diagnostic labels. No
  namespace-mapping, closure, origin, exit, or pytest lines changed.
- The repaired source-to-wheel maps are explicit and exact:
  `astrid/` → `astrid/`, `astrid_runtime_client/` → `astrid_runtime_client/`;
  Runtime `astrid_runtime/` and `runtime_protocol/` remain explicit; public
  client `packages/python/astrid_runtime_client/` → `astrid_runtime_client/`.
- The mapper and outer guards reject traversal, duplicate canonical members,
  extra roots, missing members, wrong bytes, duplicate raw wheel names, unsafe
  wheel members, and unexpected/multiple dist-info roots. The actual b3, b92,
  and 95bd Git archives mapped cleanly: 1,438 Agent files, 75 Runtime files,
  and 4 client files. Agent and public-client source payloads matched byte for
  byte across all 4 client files.
- The unchanged wrapper still contains the exact 164-pin and 166-distribution/
  166-RECORD checks, complete RECORD closure, symlink/traversal checks, private
  site origin checks for the schema and eight execution origins, and source
  Agent import separation.
- The unchanged final execution remains a direct
  `exec "$PROFILE_PY" -m pytest -q -n 3 "$@"`; collection, child exit status,
  and SIGTERM propagation assertions remain present.

## Commands and results

Passed:

```text
bash -n scripts/full_coherent_public_current_integration.sh
git diff --check HEAD^ HEAD -- scripts/full_coherent_public_current_integration.sh
compact AST/mapper synthetic positive + traversal/duplicate/extra/missing/wrong-byte guards
compact exact-source archive mapping guard for Agent b3 / Runtime b92 / client 95bd
compact static 164/166 closure and private-origin guard
compact direct pytest/collection/SIGTERM-preservation guard
```

The wrapper was also run with deliberately missing setup inputs. It returned
exit `2`, listed all setup failures, and invoked no pytest body. The refusal was
expected; no profile, build, install, renderer, browser, socket, or full suite
was run.

## Remaining MAIN conditions

The handoff correctly remains HOLD until harness publication confirms this exact
wrapper blob in the durable runner path and MAIN has a newly materialized,
private, symlink-free 164-pin/166-RECORD profile. The absent profile is not
claimed as present, and no full-suite result is claimed here.
