# D135 validation

## Controls implemented

- `ops-delivery-d135/delivery-build` was copied from the installed builder (`f25dfab...2270`) before the private D135 changes.
- `--source-tuple` (or `TIMELINE_DELIVERY_SOURCE_TUPLE`) is required. The tuple must contain exactly `agent`, `runtime`, `app`, and `composition`; every entry must contain exactly `root`, `sha`, and `tree`.
- Each source root is checked clean, each pinned commit/tree is resolved directly, and each selected repository resolves its own `origin/main` before `git merge-base --is-ancestor origin/main tip`.
- All selected ancestry checks finish before delivery or verifier directories are created. A failed check reports the exact repository, base, and tip and exits nonzero.
- Squash/bundle input comes from the resolved tuple SHA. Temporary refs are created only in an alternates-backed private verifier repository; the source checkout is not mutated.
- Delivery, verifier work, README template, and gate-results locations are explicit CLI inputs or environment overrides. Existing installed defaults remain the fallback values.

## Commands and results

| Command | Result |
|---|---|
| `python3 -m py_compile ops-delivery-d135/delivery-build` | PASS |
| `python3 -B -m unittest -v ops-delivery-d135/tests/test_delivery_build.py` | PASS — 7 tests |
| `git diff --check` | PASS |
| Production-main preflight with the committed tuple and private roots | PASS control — exit 2 before writes; Agent, Runtime, and App report exact repo/base/tip ancestry refusals; Composition passes ancestry |
| `sha256sum ops-delivery-d135/evidence/d59-source-tuple.json` | PASS — `ce3d06b41014bcd5cd42454c62828c7d240d3beb0a570467be0375109b1c4338` |

The tests are source/unit mock controls. They honestly do not claim a real Git fixture, ZIP, bundle, browser, socket, heavy clone, or production delivery qualification. The committed D59 tuple is the current authoritative Agent-home capture (`a30e74e9`); its ancestry is intentionally not claimed positive here because the farm report records Agent/Runtime/App upstream-only divergence. A later manager cut must provide a successor tuple after forward integration and rerun the actual caller.

## Not run by this worker

No full ZIP, real clone, heavy bundle, core/E2E/browser/network/acquisition run, live install, or production request was run. No shared repo, live script, delivery root, branch, ref, credential, or generated pin was changed.

## Independent review

- Candidate commit/tree: `799cf268a1c28cc461d099cf67324e2987a1f1a4` / `663f5e926370d7a9a6bc65a6abbc6f26b8be172d`.
- Candidate script/test SHA256: `afd7625ca64a13eda1f4506e69cb6d1103bd28053b9cde09a1a752dc77b9b84e` / `a91ab4c9de2b212d3e47dd165a08f21ae4bf8d6486e906228ccd2f7f8eeff103`.
- Independent real-main probes confirmed non-ancestor, stale Agent `547e1045`, malformed tuple, later-repository failure, and symlinked private-root refusals before delivery/work writes.
- One review finding remains open: delivery/work/template/gate path `Refused` exceptions are raised before the parser-error try block, so a symlinked delivery root emits a traceback/exit 1 instead of the normal exit-2 CLI refusal. See `evidence/review.json` (`D135-REV-1`).
- The positive build remains intentionally unrun until a successor D59 tuple is a real upstream descendant for every selected repository.
