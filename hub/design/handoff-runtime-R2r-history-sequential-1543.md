# R2r historical sequential verification — 1543

Implemented against HELD/unmerged Runtime `85b2feeb58bc54174ac7b89fda4805883865d3b2`. No integration, branch, ref, commit, pin or dependency mutation. Computed final source tree (without writing Git objects): `5a8594a623dc07c0cb61c45000523eac427d3a7a`.

## Result and scope

The unchanged real Agent `67ba416bca813f4931b557f6f2ca2abf935d7d35` original nine now pass: four current/moved × declared/no-read positives and all five strict negatives. Real moved history and exact retry succeed. The required Runtime nine-file selection passes **366 tests**: the prior 353 plus 13 narrow regressions. Ruff22/Pyright80 retain exactly the same diagnostic identities, none added or removed.

Only three worktree paths changed: `runtime_protocol/timeline_commit_store.py`, `runtime_protocol/timeline_commit_port.py`, and `tests/test_timeline_commit_sequential_verifier.py`. The entire authentication module, including atomic scope and inverse-stage helpers, is byte-identical to 85b2. All 78 entries actually present in `contract/artifacts.json` match their hashes and HEAD bytes (the brief's count was 77). All schemas, generated clients, contracts, locks and pins remain unchanged. Original Agent test bytes and AST remain unchanged.

## Correction and retained-fact justification

Before this change, acceptance consumed the private original/landing proof, then discarded it. `_verify_accepted` subsequently validated only landed records against previous HEAD; it did not have the authenticated original BASE or original sequential context. Original submitted second-step refs/read claims still named the legitimate unlanded original intermediate, which differed from landing after the peer edit. Existing authenticated history correctly contained only the real peer edge. The old verifier raised `provider alias is outside its authenticated boundary`, wrapped as `accepted commit record is corrupt`.

Retaining private facts is necessary for this implementation: the accepted landing records/document do not retain the original execution's records, original intermediate images, and complete original-to-landing replay map. Original content-derived physical identities depend on BASE; landing identities include the peer change. A submitted ref string cannot reconstruct its complete original image. Those originals must not be installed as accepted revisions or invented ancestry edges. No old receipt is rewritten or backfilled.

The private port returns the already detached and successfully authenticated capture with its verifier result. After the full normal acceptance validation succeeds, the store carries that capture plus exact PreparedCommit into `_publish`, in the same acceptance transaction. They are stored under one private key in the **existing history metadata JSON**. Preview drops the private retention value. Public history removes that key, and canonical data/receipts/wire schemas are unchanged. This adds no table, ledger, executor or public field.

On every historical read/retry, the store validates retained CommitContext and PreparedCommit schemas; authenticates realm, publisher, key, request hash, invocation operation/path/body, project/timeline/base and non-dry-run status; compares prepared document/records/head/digests/id map/versions/metadata/effective merge against accepted facts; and checks the retained semantic-event sequence against accepted event IDs/payloads. It then calls the unchanged `validate_sequential_capture` and `validate` against independently loaded immutable BASE and previous HEAD, actual accepted continuation edges and inverse history. Thus retained snapshots remain claims: BASE plus preceding original actual effects/materialization and HEAD plus preceding landed effects independently reconstruct them. Full prepared digest, complete map, unique consumption, owner edges, pins/digests, ordinals, submitted patches/reads, ABA and forgery checks are retained. Missing private proof for a moved staged alias fails closed. Existing old rows without the proof are not repaired by inventing data.

## Exact commands and results

Commands run from `/home/user/work/wt/rt-R2r-history-sequential-1543` unless stated. `W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-history-sequential-1543` below is only an abbreviation for the absolute evidence directory.

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_commit_inputs.py tests/test_timeline_commit_port.py tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_sequential_verifier.py
```

**Exit 0, 366 passed in 89.36s.** `evidence/runtime-final.log`. An earlier pre-final-test run passed 365 in 96.61s. No tests were weakened, skipped or marked xfail.

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_sequential_verifier.py
```

**Exit 0, 57 passed in 11.65s**, `evidence/sequential-final.log`. Includes a real service close/reopen with no provider registered, exact retry/history equality and unchanged database rows; 11 retained-proof tamper cases exercising retry and history with no writes; and the moved historical regression. Initial tamper assertions expected the store exception directly, but the public coordinator intentionally wraps it as outcome-unknown; the tests were corrected to assert its ProtocolError cause and direct history rejection. The initial 11 assertion failures are preserved in `history-targeted.log`.

For meaningful **old RED**, a private baseline copy was made from HEAD without checking out or modifying any shared repo. The exact same new moved regression was run with the old Runtime module pre-imported before pytest (necessary because pytest's path setup otherwise selected the candidate):

```bash
# cwd=/tmp/w-070f2ea023/baseline
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=/tmp/w-070f2ea023/baseline:/home/user/work/agent /home/user/work/venv-runtime/bin/python -c 'import runtime_protocol.timeline_commit_store as store; print(store.__file__, flush=True); assert store.__file__.startswith("/tmp/w-070f2ea023/baseline/"); import pytest; raise SystemExit(pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", "/home/user/work/wt/rt-R2r-history-sequential-1543/tests/test_timeline_commit_sequential_verifier.py::test_moved_history_replays_authenticated_original_and_landing"]))'
```

**Exit 1, 1 failed in 1.39s**, `moved-old-red-confirmed.log`: original outside-boundary failure wrapped by old store line297. The regression uses real captured BASE, HEAD, original/landing executions and preceding edge; it constructs only its enclosing receipt/event using an in-memory SQLite fixture. It passes on the candidate and also verifies removal of required private proof is refused. Real-store qualification is the separate original nine. Two earlier baseline attempts inadvertently loaded the candidate and passed; their logs are preserved and are not counted as old RED.

The **one original Agent nine** was run only after the meaningful product correction and moved old RED/new GREEN:

```bash
PYTHONDONTWRITEBYTECODE=1 ORIGINAL9_EVIDENCE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-history-sequential-1543/evidence/original9 ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-67ba416b PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-history-sequential-1543:/home/user/work/wt/agt-pin-67ba416b:$PWD:$PWD/packages/python /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p original9_observer /home/user/work/wt/agt-pin-67ba416b/tests/editing_conformance/test_doc_patch_sequential_rebase.py
```

**Exit 0, 9 passed in 17.45s.** The bounded observer saves full private inputs **before validation**, outcomes, no-write hashes, and all **27 per-node setup/call/teardown reports immediately**, including full longrepr fields and actual before/after origin stdout. Four previews preserve database bytes; all five unchanged strict-negative assertions execute. There are 23 complete prevalidation/outcome records. Credential-key scan is clean. Report metadata keys `credential_clean`/`credential_keys` are excluded from the scan itself.

A central request `request-test rt-R2r-history-sequential-1543 targeted --files <absolute worker/test_original9_runner.py> --no-cache` was rejected by its **relative-path argument validation before snapshot or execution** (`tests/rt-R2r-history-sequential-1543-targeted-1023155417-56/summary`). Inspection of unchanged `saved_source` confirms this nine is in-process direct service transport, with no sockets/browser/daemon. Therefore the exact targeted command above was permitted directly. No Agent test body was run by that rejected request; there was only one actual original-nine run.

```bash
/root/.local/bin/ruff check runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py tests/test_timeline_commit_sequential_verifier.py --output-format json
/root/.local/bin/pyright runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py --outputjson
git diff --check
```

Ruff **exit1, 22 existing diagnostics**; Pyright **exit1, 80 existing diagnostics**; both exact normalized identities have **0 added, 0 removed**, auth diagnostics0. Whitespace exit0. Baseline/final JSON, source-line identity comparisons and stderr are durable in evidence. An initial new test import formatting diagnostic was fixed; the final comparisons are exact.

## Durable evidence and hashes

Manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/runtime-R2r-history-1543-manifest.json`. It maps **80** source/log/report/capture files to absolute flat design exports, with SHA256 and byte sizes. Named current-only patch: `runtime-R2r-history-1543-current-only.patch`. Sources also have named flat copies. Original 1534/1512 evidence was not modified.

Final changed-file SHA256:

- port: `0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859`
- store: `b1cfdceefc533220ea9a5478f61a971109d1cc2d70fa2c7a76341ffa977f2246`
- tests: `35451bda9486c042fa907454b41e7b90439fa1964ec9a68ad3936acc25a22800`
- Original Agent test bytes: `75ccd026898b241d2241f5c058342aeb728e3a70f039a8701343b55f6fc648f6`; AST `be9a7dce79a3fbe8be453a0dcb8f4c0a8d33eb35cbe8fd6e34d0194bfe5206ea`.

## Limits and next step

No full suite, native14/40/281/58, browser, journey, benchmark, provisioning, host or daemon run. No deletion. No shared dependency/caches edited. The real Runtime reopen regression uses a current accepted private capture; moved real-store history/retry are proved by the original nine, but a separate moved-service-reopen scenario was not executed. Deep multi-hop positive coverage remains the prior verifier's limitation. Pre-fix accepted moved rows lacking original private facts remain fail-closed; no fabricated recovery/backfill is claimed.

Keep 85b2 ancestry **HELD/unmerged**. Independent review should inspect the private metadata retention/verification and public field exclusion, then decide a current-only port alongside the separate atomic and inverse-stage workers. Nothing here authorizes merging the held ancestor or changes those workers' helpers.
