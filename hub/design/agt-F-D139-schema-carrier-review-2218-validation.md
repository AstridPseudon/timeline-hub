# D139 independent carrier review

Verdict: `FAIL` for the required portable pinned source carrier. The 2214 `EXACTMISSING` disposition is supported.

## Static checks

- `python3 -m json.tool` on `review.json` and `source-manifest.json`: PASS.
- Read-only RECORD/direct URL verification against `/home/user/work/venv-agent/lib/python3.13/site-packages`: PASS.
  - 18 RECORD rows; 12 hashed rows.
  - All 12 hashed rows matched bytes and recorded sizes.
  - All RECORD files were regular `0644` files.
  - RECORD SHA-256: `50be781bec3546ca9995ce2f0aaa1284fa68198735866c0f00a601bb3ce9c3a1`.
  - direct_url SHA-256: `b7a0a4f90218d54bc1fb118609d40a381f5762650f8e5863ec39098ec269165e`.
- Bounded exact-path availability check across the four integration worktrees and four named repository roots: the expected `packages/timeline-schema/python` directory was absent in all checked locations.
- Bounded carrier-name check under the named roots: no authorized schema carrier archive was present.
- `git -C /home/user/work/runtime grep -n -E 'ASTRID_TIMELINE_SCHEMA_PYTHONPATH|banodoco_timeline_schema|packages/timeline-schema/python' HEAD -- '*.py' '*.sh' '*.md' '*.json`: only provenance metadata matched; no Runtime 2153 recipe/source matched.
- Candidate source inspection: PASS for the narrow D137 runner; applicability to Runtime 2153 remains `UNKNOWN`.
- `git -C /home/user/work/wt/agt-F-D139-schema-carrier-review-2218 diff --check`: PASS; no worktree product changes.

## Provenance boundary

The installed distribution’s direct URL and RECORD establish a qualified installed input and its byte-level integrity. They do not establish physical availability of the original ArtAgents source tree, portable source completeness, or permission to republish installed files as a source carrier.

The retained D137 runner at `/home/user/work/agent/tools/run-discovery-original-0603.py:45,379,394-398` explicitly binds and checks the installed site-packages root. That is a real, narrow candidate proof. The frozen R4 SDK candidate at `origin/codex/handover-timeline-r4-20261019-candidate-sdk` instead derives the schema from `project/node_modules/@banodoco/timeline-schema/python` (`astrid/core/execution/generic_host.py:1699-1715` and `astrid/sdk/host_bootstrap.py:422-433`). Neither source proves that Runtime 2153’s production recipe consumes this installed input; that candidate applicability is therefore not promoted from inference.

No acquisition, retry, transfer, install, import execution, child request, Store/provider/runtime execution, archive creation, source copy, product write, Git mutation, or test/typecheck/lint/full-suite run occurred. The prior 403 stop is preserved.
