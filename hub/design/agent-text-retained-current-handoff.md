# Agent next-text candidate on current S2 — private qualification

Both original retained legacy `text/plain` positives passed with `--runxfail` against current committed Runtime source, before either expected-failure marker was removed. Final native service tests pass **21/21**, with exact inverse/redo and no remaining text xfails. The reviewed native text command/capture/state/inverse changes are prepared on Agent `9cb10904`; the public release and App writers remain held.

## Exact candidate

| Item | Identity |
| --- | --- |
| Agent base | `9cb1090458428fb09067e359be92cdbb6608a206` |
| Reviewed native source | `cb1e907c6846341997e50d7f51aed65a84b6c335` |
| Original strict positives | `9bf654387c8c1aaa2bc3ef74210fa4a6825956ad` |
| Current committed Runtime producer base | `129493b2aff614560d9b7ac2577957e799cf30ec` |
| Committed Runtime base tree | `330ea3969cb9cce77271404f31793c21abd5993f` |
| Approved retained correction / merge | `e41f3d1e` / `a51267ec3dd94ea465a3161e3b4d8fbcd061009e` |
| Private generated Runtime content tree | `fbca3c2fc63a2244370aacb9c7ec2c17eaa01406` |
| Authored command schema SHA256 | `b2dcbec7e212c1bccc7ea662367b98b973e6308c9b7a2f9aead42c6a9d807a78` |
| Normally generated schema digest | `sha256:7cc26d125d3e16bebb3694bf724c7e1e3fd7ada0398ef1fc3020dde245e494bf` |
| Private artifact version (75 entries) | `sha256:b8b5e14cb2b53b27ff07745b264c5d59e703fa7bc52dfb3e63c5bb6d58361d8c` |
| Complete Agent source/test patch SHA256 | `e7c092dda52fe60de5b98fda30dedd14559cc72820094dff7a4107e0dd841410` |

The private tree is calculated in Git tree format without writing Git objects; it is not an invented commit or published producer. Runtime base `129493b2` is a verified `a51267ec` descendant including reviewed retained correction `e41f3d1e`/tree `de8f95b2`. Private source is an archive of that exact committed source, with only the authored command schema plus 12 normal generated outputs differing. Runtime product source is unchanged. `runtime-candidate/` and `agent.patch` live in this worker directory; the harness assigns the Agent commit on exit.

All **48 S2 definitions / 22 operation clauses** survive; the candidate has **49 / 23**. The only additions are reviewed native `TextBindingSetArgs`, `text-binding.set` and complete additive legacy/S2/native branches for `ScopedId`, `EntityRef`, `TargetKey`. The closed new-input descriptor remains canonical UTF-8 (including EMPTY); arbitrary legacy MIME is not admitted as a new selection. All five normal generation compatibility floors and Python/TypeScript conformance/artifact checks pass. Agent source and private Runtime command schema bytes are identical.

Private contract input still says `0.2.13`; it is an unpublished experiment, **not permission to release changed bytes at that existing version**. Public producer `2c4ac180...` / client `0.2.13` and Agent lock/client/artifact files remain frozen. This handoff prepares the next schema source; it does not publish or repin it.

## Qualified

- Real main-API film backup, managed project CAS, actual Agent provider and normal port, accepted history, atomic projection, restart and exact retry. No schema override, fake Prepared/history/provider, positive SQL write, new endpoint/table or inline text authoring.
- Exact original legacy `text/plain` document, descriptor/order and bytes after canonical replacement/restart/inverse, then exact redo.
- Exact legacy clear, absent GET/list, restart/retry, inverse to original MIME/bytes/document and redo to absence. Only new text selections use `text_selection`.
- First-birth undo to absence; EMPTY as present; whole clear/inverse at original row position; historical pins/events; V1 through V2/removal/restart/group inverse and deep reachability.
- Same-field and unchanged-value authorship guards; different-field rebase; exclusive ownership; closed input, wrong project/hash/size/MIME/UTF-8 and atomic corruption refusals. Retained opaque authored values remain literal.

Exact commands and logs: [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-text-retained-current-pair/notes/report.md). Final targeted results:

- Original two strict legacy positives with `--runxfail`: **2 passed** before marker promotion.
- Native actual service: **21 passed** (the old 19 positive + 2 strict-gap cases).
- Original affected Agent unit subset: **450 passed / 1 integration-only deselected**.
- Native unit + current union/golden schema: **54 passed** (includes the prior 25 native cases; overlaps the 450 lane).
- Current duplicate/trim/unplace/selected-schema neighbors: **245 passed**.
- Current private Runtime clear/selection/legacy/schema neighbors: **199 passed**; artifact tests: **3 passed**.
- Ruff, diff check, normal generation and all final generation/conformance/artifact `--check` commands: **exit 0**.

An initial pre-correction schema fingerprint assertion failed because serialization changed old compact formatting. Final checks fingerprint the entire approved S2 object after removing exactly the text delta; all affected lanes were rerun. Details and the initial failure log are retained in the report.

## Gaps and release boundary

**Destructive media GC is unverified.** Current Runtime CAS is append-only and provides no media collector. The positive V1 test checks deep reachable/non-orphan status and exact bytes/inverse after removal and restart; it does not claim an actual collection cycle. PLAN.md defers retention/purge. A future GC claim needs its owner's actual collector path and journey.

No full/full* request, socket/browser/App journey, public package build/install/public TypeScript compile or public-tuple qualification occurred. No writer deletion or native public completion is marked. App text/candidate writers stay held.

Next: Runtime owner takes this full S2+text source through an authorized fresh public release and normal client generation; owners coordinate consumer pins, qualify that exact tuple and run the actual App journeys before writer cutover. Preserve the two promoted strict legacy positives and all source/golden expectations. A later GC owner must supply a real collector qualification path before claiming destructive-GC survival.
