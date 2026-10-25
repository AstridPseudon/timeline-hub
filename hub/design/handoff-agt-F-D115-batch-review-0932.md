# D115 protected batch review

Reviewed the three disjoint Agent fixture commits against parent `f3c0bc72898e59e8f8b87c60cb0a47cf247d8c9e`, immutable source blobs, the retained authenticated archive, the actual Runtime commit provider path, and the retained worker XML.

## Verdicts

| Diff | Verdict | Candidate commit/tree | File SHA-256 | Exact evidence |
|---|---|---|---|---|
| A pair16 | `PASS_SOURCE` | `7d85895ba18637231adc12fc0130f51f8be96608` | `6a0787475f0b032500e769379a2e3f556a4ba5cabc07fa3996350200083a1284` | 16/16 passed; cluster XML SHA-256 `9637d97ba0baa7b2400de55bd586e201a004ed9efaab9a3740391cd6a13e22b4` |
| B legacy27 | `PASS_SOURCE` | `a089532e2bc9a0a014a73047d3cc70b051d8215e` | `c25ec5b116d712d2abdbc316bd5f22be91392435217461ce49d4f4204fa1f374` | 26 passed, 1 distinct Runtime refusal; cluster XML SHA-256 `f2e132895754f39a21d9724cb2d9112be3e984057b274ffbe6340cc5a3a6c209` |
| C native54 | `PASS_SOURCE` | `45daf7d872ab39c91a1a0d3360d5ec7b15f38b3a` | `e0b170149fa08cd2bd5655af505b4b96cc0faccc5dceba51c50ee2cbdcb1c91a8` | source-only correction; sample remains red; no exact-54 rerun |

### A — pair16

Only `test_current_pair_reader.py` changed (8 insertions/1 deletion). The optional `ASTRID_AUTHENTIC_LEGACY_ARCHIVE` override remains active; unset uses the already-published archive. The archive bytes hash exactly `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`; no history, pins, IDs, assertions, auth guards, or provider callers changed. The seven test function ASTs and 22 test assertions are byte/AST-equivalent to the parent. All 16 selectors pass.

### B — legacy27

Only `test_authenticated_legacy_restore.py` changed (6 insertions/20 deletions). It reuses A's genuine `reader` fixture, so archive extraction, SHA-256 check, backup verification, Runtime setup, provider registration, and teardown are shared rather than duplicated. Baseline head and canonical content-digest checks remain in `case`; the four test function ASTs and 19 test assertions are unchanged. The original 27 selectors are collected. The one `[True]` stale-merge case reaches the unchanged production caller and is refused as `invalid_records: sequential command metadata differs from the prepared candidate`; this is a remaining Runtime/provider metadata issue, not a source-fixture pass. Invalid/unauthenticated negative guards remain intact.

The setup AST assertion count falls from 25 to 23 because the duplicate archive assertion and explicit `ASTRID_RUNTIME_CHECKOUT == use_runtime()` assertion are moved/covered by the shared reader path (the shared reader retains the exact archive hash/head/authenticated restore checks). This is the only setup assertion delta; test bodies are unchanged.

### C — native54

Only `native_word_anchor_fixture.py` changed (12 insertions/2 deletions). The semantic/source inputs remain unchanged: authored declaration, word text/times, rational FPS, occurrence duration/window, opaque pin graph, media admission, and all negative guards. The corrections are: `occurrence_id:occ` address, complete ordered v2 request metadata/steps, and provider-visible internal timeline FPS equal to authored `30000/1001`. `test_native_word_anchor.py` remains byte-identical (SHA-256 `ab07f5b9cda3a42d0c9273917b46d9486c39b453b979d2ad5d39df5528d4179f`, 122 assertions); `test_word_binding_recipe.py` remains byte-identical (SHA-256 `f23e227bce165d3c7ada70d9742c1e6f36159823c845df9903903f71575228bd`, 87 assertions). The corrected seed still refuses before selector bodies with `candidate.timing: legacy word anchor is missing`; the short-occurrence sample separately retains the `[1,3)` media interval against the authored `[0,0.1)` occurrence. No source-only result is a behavior pass, and the exact 54-cluster run remains open pending the orchestrator's seed/scope decision.

## Shared caller/static audit

All three use the unchanged production route: fixture `RuntimeService.commit_timeline` → `runtime_protocol.timeline_commit_port.route_path` → registered `astrid-v1` Agent `create_runtime_commit_service()` provider; C0 request metadata uses `steps[].reads` (not an invented field). Candidate source copies passed Ruff, mypy, py_compile, and `git diff --check` with the normal Agent environments/config. No product, Runtime, pin, registry, generated, ledger, or test-body edits were introduced.

## Proposed D72 entries

`A PASS_SOURCE`: faithful authenticated archive-path setup correction; behavior qualification remains the retained 16-node evidence only.

`B PASS_SOURCE`: faithful shared authenticated-reader setup correction; record the 26/27 retained proof and keep the sequential-command-metadata refusal as a distinct open Runtime/provider item.

`C PASS_SOURCE`: faithful address/envelope/internal-FPS setup correction; record source-only qualification, keep all 54 selectors and the legacy-seed/short-containment scope question open, and do not claim behavior qualification or rerun unchanged 54/27 clusters.

