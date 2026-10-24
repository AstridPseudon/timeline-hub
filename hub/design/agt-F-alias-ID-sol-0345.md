**BLOCKED. No source or test changes.** Wrote `BLOCKED` and the required `commit-msg`; no `DONE`.

The required identity predicates conflict for equivalent candidates:

- `compile_authoring_candidate` materializes **both** shared occurrences under their `shot-placement-*` IDs. Original11 requires those exact persisted IDs.
- Existing alias controls require the untouched sibling to retain **`shot-shared` / `shot-rev-1`**, including its exact physical occurrence.
- `_fork_shared_aliases` currently creates an `authoring-fork-*` destination only for the edited occurrence.
- Removing `_runtime_document` and `publication_id` produces identical commands after hydration. Introducing different behavior based on those markers would invent a publication policy.

Runtime’s `_check_shot_destinations` accepts recorded fresh IDs without imposing an ID prefix, while retaining existing, foreign, item, and historical reservation guards. Native `capture_occurrence_fork` currently refuses the compiler alias because its virtual slot/item identities are occupied. A projection seam could address that allocation collision, but cannot satisfy the contradictory sibling predicates.

**Exact decision needed:** Should publication materialize every compiler alias, including the untouched sibling, or preserve that sibling’s exact physical identity? If both are required for different callers, what established semantic distinction separates them?

Production tracing confirmed `TargetBoundAuthoringBundle` → `publish_authoring_candidate` → `authoring_commit_request` → Runtime commit.

Complete source, candidate, compilation/mapping, request, prepared-before-validation, history, and accepted results for both selected occurrences are captured in [identity-evidence](/tmp/w-8239c7de87/identity-evidence/sha256.json), totaling **1.38 MB**. For the first occurrence:

```text
compiler:  shot-placement-eb955f5f43724e2b0418580853406379e7f8f8cd241a72730f9880ef23f926c0
persisted: authoring-fork-8c07eceddff02f1e177f04aa3e7f206cca27f5be870d7d5380fefae4e8bca1ed
sibling:   shot-shared / shot-rev-1
```

All pytest commands used this exact prefix, with separate scratch `--basetemp` directories:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f \
ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f \
/home/user/work/venv-agent/bin/python -m pytest \
-q -oaddopts= -p no:cacheprovider --timeout=45 --tb=short
```

Executed selectors and results:

- `test_authoring_shared_alias_commit.py`, public shared-alias refusal, removed-occurrence sibling preservation, and unplaced-copy filtering: **24 passed**.
- `test_authoring_publication_migrations.py` plus the seven specified compiler/open/reopen/mapping/group-move/opaque-field neighbors: **18 passed**.
- `tests/timeline/test_authoring_commit_media.py`: **6 passed**.
- Original FIRST real media round-trip plus `test_publication_data_projects_accepted_parent_revision_without_rewriting_reply`: **2 passed**.

Static commands passed:

```bash
/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/authoring_commit.py
/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/authoring_commit.py --cache-dir /tmp/w-8239c7de87/mypy --hide-error-context --no-color-output --no-pretty --show-error-codes
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-45c3a7f4
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Original fixture and integration-test body remain exact against `d7390a90d4`; **all 11 assertions retained**. Original11 was **not rerun**, because no genuine source change was made. No newGREEN claim, full suite, browser run, shared dependency mutation, or Git mutation.

Recommended next step: reconcile the sibling identity requirements before assigning the projection implementation.