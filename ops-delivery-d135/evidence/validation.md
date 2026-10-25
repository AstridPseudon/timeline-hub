# D135 validation

Candidate status: **PASS_WITH_FINDING** (`D135-REV-1`, Luna/high/default180). The finding was
that private delivery/work/template/gate path refusals escaped the caller's `argparse.error`
boundary (a symlink delivery root could traceback with exit 1). The caller now places all private
path and source-tuple validation in that existing structured refusal boundary; guards and the
all-repository ancestry preflight remain unchanged.

## Controls implemented

- `ops-delivery-d135/delivery-build` was copied from the installed builder (`f25dfab...2270`) before the private D135 changes.
- `--source-tuple` (or `TIMELINE_DELIVERY_SOURCE_TUPLE`) is required. The tuple must contain exactly `agent`, `runtime`, `app`, and `composition`; every entry must contain exactly `root`, `sha`, and `tree`.
- Each source root is checked clean, each pinned commit/tree is resolved directly, and each selected repository resolves its own `origin/main` before `git merge-base --is-ancestor origin/main tip`.
- All selected ancestry checks finish before delivery or verifier directories are created. A failed check reports the exact repository, base, and tip and exits nonzero.
- Squash/bundle input comes from the resolved tuple SHA. Temporary refs are created only in an alternates-backed private verifier repository; the source checkout is not mutated.
- Delivery, verifier work, README template, and gate-results locations are explicit CLI inputs or environment overrides. Existing installed defaults remain the fallback values.
- Invalid private paths now produce an `argparse` error with exit 2 before any delivery or verifier output is created; no broad exception catch was added.

## Commands and results

| Command | Result |
|---|---|
| `python3 -m py_compile ops-delivery-d135/delivery-build` | PASS |
| `python3 -B -m unittest -v ops-delivery-d135/tests/test_delivery_build.py` | PASS — 8 tests (original 7 plus private-input caller probe) |
| `ruff check ops-delivery-d135/delivery-build ops-delivery-d135/tests/test_delivery_build.py` | PASS |
| `python3 -m compileall -q ops-delivery-d135/delivery-build ops-delivery-d135/tests/test_delivery_build.py` | PASS |
| `git diff --check` | PASS |
| Production-main preflight with the committed tuple and private roots | PASS control — exit 2 before writes; Agent, Runtime, and App report exact repo/base/tip ancestry refusals; Composition passes ancestry |
| `sha256sum ops-delivery-d135/evidence/d59-source-tuple.json` | PASS — `ce3d06b41014bcd5cd42454c62828c7d240d3beb0a570467be0375109b1c4338` |
| Candidate script SHA/mode | PASS — `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`, `0755` |
| Candidate source/test tree | `f51f996895497d90f10e1c62b5a6585f83ac2514` (HEAD tree with candidate delivery script and focused test blobs; final harness commit tree assigned after exit) |
| Protected installed reference SHA/mode | PASS unchanged — `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708`, `0755` |

The tests are source/unit mock controls. They honestly do not claim a real Git fixture, ZIP, bundle, browser, socket, heavy clone, or production delivery qualification. The committed D59 tuple is the current authoritative Agent-home capture (`a30e74e9`); its ancestry is intentionally not claimed positive here because the farm report records Agent/Runtime/App upstream-only divergence. A later manager cut must provide a successor tuple after forward integration and rerun the actual caller.

## Not run by this worker

No full ZIP, positive build, real clone, heavy bundle, core/E2E/browser/network/acquisition run, live install, or production request was run. The existing current-production non-ancestor refusal control is retained; it was not replaced by a positive fallback. No shared repo, installed script, delivery root, branch, ref, credential, or generated pin was changed.
