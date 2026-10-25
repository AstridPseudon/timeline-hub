# F-D86 source review — projection9

Verdict: `PASS_SOURCE`

## Exact source

- Repository: Agent (`/home/user/peteromallet/astrid-agent`), read-only.
- Captured base: `tl/integration` = `657bc2e8dba066df1c7d21851315bdb6b0f16a3a`.
- Parent: `657bc2e8dba066df1c7d21851315bdb6b0f16a3a`.
- Candidate: `tl/agt-F-projection9-source-0325` = `b8dbb40a3c038634f232f4b10dad4eaf9ddef4ba`.
- Candidate parent is exactly the captured base; the candidate changes only the assigned test file.
- File: `tests/sdk/test_timeline_capture_projection.py`.
- Parent blob SHA-256: `91047638576673c9cbb65780d7364b9a4d5245ec40b19cbd52af5c3381a41105`.
- Candidate blob SHA-256: `90c4625a7481fdcd570ec8b85bbe95325f4d3c57f0a3a26017dd405b8269b638`.

Exact diff:

1. Remove the fallback that fabricated an `items[0]` entry from an internal clip when the genuine source payload had no items.
2. Before the two existing `duplicate_authoring_shot` calls, copy the explicitly authored current `source_payload` and `source_internal` into `source["base_payload"]` and `source["base_internal_timeline"]`.

No assertion, decorator, parameter, test selector, refusal expectation, no-write guard, topology expectation, or production file changed.

## Static conservation and payload review

- All 11 `test_*` function ASTs are identical parent/candidate.
- All 45 `assert`/`raise` AST nodes are identical parent/candidate.
- The fixture still begins from `_saved_document(runtime)` and `open_authoring_bundle(...)`, preserves the same parent/placement/source shot, media identity, authored parent fields, occurrence fields, payload fields, internal effects/audio/layout/assets/opaque registry/track/clip fields, duplicate IDs (`shot-z`/`occ-z`, `shot-a`/`occ-a`), start times, removal of the original source, authored metadata, writer, idempotency key, canonical document extraction, and all nine original projection/canonical-image/opener cases.
- The removed fallback was synthetic data, not a source input. The candidate now requires `source_payload["items"][0]` from the genuine opened Runtime image, so it does not invent an item, media identity, history, receipt, custody fact, registry binding, or default timeline payload.
- The added copies preserve the complete authored payload—including `opaque_timeline`—as the duplicate helper's explicit current baseline. `duplicate_authoring_shot` already copies `base_payload`/`base_internal_timeline`, remaps only schema-owned item references, and preserves arbitrary opaque/provenance values. The source mapping remains separate and is still removed only by the existing `remove_authoring_shot` operation.

## Mounted production trace

The duplicate and publication are real current API paths:

1. The test calls `duplicate_authoring_shot` twice, which calls the existing `add_authoring_shot` helper and records `occurrence.duplicate` reservations.
2. `publish_authoring_candidate` compiles the candidate, calls `authoring_commit_request`, and uses `_materialize_duplicates` to validate each exact occurrence owner, materialize the registered semantic duplicate, and produce commands.
3. The test's `_RuntimeAuthoringWriter.commit_timeline` delegates to the mounted `RuntimeService.commit_timeline` with the real registered Python commit provider, exact scope, publisher, invocation path, and idempotency key.
4. The resulting canonical document is then consumed by the unchanged projection, full-expansion, authored-field/pin/order/read-row, and SDK-opener predicates.

No direct lookup, unsupported registry, synthetic revision/history, fabricated custody, or retired writer route was introduced.

## Checks run

Source-only checks, with no pytest collection, fixture/helper/function execution, probe, service, render, browser, or package install:

- In-memory `ast.parse` + `compile(..., "exec")` for parent and candidate: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check` on parent and candidate extracted source: PASS for both.
- `/home/user/work/venv-agent/bin/python -m mypy` on parent and candidate extracted source: PASS for both (`Success: no issues found in 1 source file`).
- `git diff --check 657bc2e8dba066df1c7d21851315bdb6b0f16a3a..tl/agt-F-projection9-source-0325 -- tests/sdk/test_timeline_capture_projection.py`: PASS.

Behavioral qualification is intentionally unverified here; MAIN9 remains required after merge.
