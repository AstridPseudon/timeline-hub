# D132a source-trace commands and results

- `sed -n '1,240p' PLAN.md` and `sed -n '1,260p' AGENTS.md` — PASS; governing plan and repo guidance read first.
- Read-only source inspection of the graph fixture, graph RuntimeRealm caller, Agent command/recording/commit/preview modules, frozen Runtime service/port/store/auth modules, edit-command schema, and C0 contract — PASS; complete path traced.
- `git rev-parse HEAD HEAD^{tree}` — PASS; Agent `136c8ae6c6159285c066e4347c881dd4e4a39bb2`, tree `aabbe60c220768dc4beee25146d4342cff98525e`.
- Frozen Runtime custody — PASS; commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, tree `de2954a0ceadb4455903d9abdfec3b773318a50f`, clean.
- Read-only hash comparison of all cited Agent/Runtime source files — PASS; hashes are in `source-custody.json`.
- AST parse plus `compile(source, filename, 'exec')` for 10 cited Python files — PASS; no bytecode or source writes.
- JSON parse of Agent edit-command schema and frozen Runtime bundle schema — PASS; 2 files.
- `git diff --check`; Agent and Runtime-pinned clean status checks — PASS; no worktree changes.
- No pytest, own9 rerun, native/full/family/profile/browser/service suite, collector, recovery, SWAP inspection, or source fix was run.

## Source citations

1. `tests/editing_conformance/test_recorded_graph_roots.py:21-30,55-57`: test-only registered `test.create-roots` handler and submitted command envelope; no `created` claim.
2. `tests/editing_conformance/test_recorded_graph_roots.py:184-208`: `create_entity` validates and records each root allocation in order.
3. `astrid/sdk/timeline/_recording.py:85-87,249-273`: recorder starts from the submitted command and capture finish writes the authoritative `created` list.
4. `astrid/sdk/timeline/commands.py:222-304`: validation, registered handler execution, capture finish, and submitted-claim checks.
5. `astrid/sdk/timeline/_commit_preview.py:7-22,25-91`: prepared records and private sequential capture carry the provider-produced record; no record patching is introduced.
6. `/home/user/work/wt/rt-pin-5e9ad1c6/runtime_protocol/service.py:2469-2483,2528-2559`: canonical `commitTimeline` request validation, authenticated context, registered provider/coordinator dispatch.
7. `/home/user/work/wt/rt-pin-5e9ad1c6/runtime_protocol/timeline_commit_port.py:677-712`: Runtime preview/acceptance and request-bound capture validation seam.
8. `/home/user/work/wt/rt-pin-5e9ad1c6/runtime_protocol/timeline_commit_store.py:1491-1538`: prepared-record, v2 step, sequential proof, and auth validation order.
9. `/home/user/work/wt/rt-pin-5e9ad1c6/runtime_protocol/timeline_commit_auth.py:328-338,2873-2888`: first differing claim and exact refusal.
10. `astrid/core/timeline/schema/edit-command.schema.json:894-900`, `/home/user/work/wt/rt-pin-5e9ad1c6/contract/commit-v2.md:569-572`: `created` is an allowed command claim and C0 requires it for creation.
11. `tests/editing_conformance/test_recorded_graph_roots.py:123-139` and `tests/sdk/test_timeline_commit_graph_roots.py:345-360`: comparison custom operations allocate nothing; omitted `created` therefore remains an empty recorded list.
