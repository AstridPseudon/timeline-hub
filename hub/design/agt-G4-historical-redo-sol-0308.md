Implemented **G4 historical redo source authority**, preserving `975dd47157` and `69dca6af52`.

- Undo/repeated redo recover the original selected forward record and revalidate its exact source, physical pins, media, documents, and access through Runtime.
- Extended physical-owner normalization to redo and fixed transcript dependency kinds.
- Changed only `native_occurrence_shared.py`, two `commit.py` capture seams, and one new test file. Reserved files remain untouched.

Tests used the prescribed environment:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f
export ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f
P=/home/user/work/venv-agent/bin/python

$P /tmp/w-3c34d22610/predecessor_red.py
```

**3 expected failures** against predecessor source `69dca6af52`: redo normalization, access loss after forward, and transcript custody.

```bash
$P -m pytest -q -oaddopts= -p no:cacheprovider --timeout=45 --tb=short \
 tests/editing_conformance/test_historical_shared_redo_authority.py \
 tests/editing_conformance/test_historical_shared_inverse_owners.py::test_inverse_retains_existing_destination_owner \
 tests/editing_conformance/test_historical_shared_inverse_owners.py::test_inverse_guards_later_destination_consumer \
 tests/editing_conformance/test_occurrence_shared_historical.py::test_historical_shared_exact_physical_retry_preview \
 tests/editing_conformance/test_occurrence_shared_historical.py::test_historical_shared_media_and_opaque_fidelity \
 tests/editing_conformance/test_occurrence_shared_historical.py::test_historical_shared_rejects_inconsistent_port_images
```

**28 passed**, including production-session restart/redo and genuine registered-provider document history.

Also passed:

```bash
$P -m ruff check --no-cache astrid/sdk/timeline/native_occurrence_shared.py astrid/sdk/timeline/commit.py tests/editing_conformance/test_historical_shared_redo_authority.py
$P -m mypy --cache-dir /tmp/w-3c34d22610/mypy-final --hide-error-context --no-color-output --no-pretty --show-error-codes astrid/sdk/timeline/native_occurrence_shared.py astrid/sdk/timeline/commit.py
$P scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
$P scripts/artifact_manifest.py --check
git diff --check
```

Decision: follow accepted history recursively rather than trust stored source digests. No guard waiver or wire change.

Limits: denial/image-substitution controls inject failures; public redo proof uses the in-process registered provider with a transport stub. The known last-owner test `test_historical_shared_undo_redo_retains_physical_source` was deliberately excluded. Its Runtime boundary remains unresolved; no full suite ran.

Next: port this focused diff onto current HOME, then qualify the original last-owner case after Runtime review. Wrote `commit-msg` and `DONE`; no commit or push.