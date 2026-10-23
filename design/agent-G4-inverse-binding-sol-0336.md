# R2/G4 inverse physical-binding preservation

Bounded repair: PASS. Independent Luna review: PASS (read-only review; it did not run tests). The original provider file contributes 112 passing cases, with four additional boundary controls passing. The real Runtime script remains unverified here.

Base: `9fcb72397db25cf92f0e4046584a5d4aa29a18c6`, tree `ae34f53a72a311931f556d59f6f5dacf76d6c50e`. Read PLAN §3 R2/G4, contract §§2/5, author0332 report/log and independent0324 report (the latter's full design report was read with `git show tl/agt-G4-bootstrap-current-review-0324:design/agent-G4-bootstrap-current-review-0324.md`; its worktree was already recycled).

## Cause and correction

`inverse.py:_validate_inputs` unconditionally continued for every binding containing `physical_ref`. The restored original test gives this helper a plain record list with a timeline scope read and deliberately mismatched binding revision. Its read still matches the input pin, so the unconditional binding skip caused `DID NOT RAISE`. This was reproduced before editing: **1 failed**.

The correction restricts that skip to `isinstance(records, AcceptedRecords)` and removes the second redundant `physical_ref` exclusion from entity validation. Plain helper inputs therefore retain the existing scope read/binding consistency check; the deliberate mismatch reaches the original `unsupported entity reference 'timeline'` refusal. A matching scope binding avoids `State.entity` exactly as before. No error assertion was changed.

The production boundary matters: this helper failure alone does **not** establish a caller-forged physical binding accepted by the provider. `commit.py:commit` obtains target records through the Runtime port, verifies closure scope and complete ancestry with `_load`, `_history`, and `_records`, and constructs `AcceptedRecords` using verified before/after closures. `select_inverse_records` checks the selected records against the complete accepted history. `inverse_address_resolver` constructs historical contexts and authenticated successor mappings before `execute` calls `apply_inverse`. `apply_inverse` refuses physical bindings unless records are `AcceptedRecords` and an address resolver exists, before historical reversal reaches `_validate_inputs`. The new raw-record controls exercise that real execution gate, with both matching and deliberately mismatched scope pins; both remain `history_unavailable` without mutation.

Accepted physical bindings must keep using that resolver, rather than re-resolving old aliases through `State.entity` after reversal. In particular, a timeline scope captures parent, shot and internal images, whose pins need not equal the parent scope read pin. Restricting every accepted binding to that single pin or comparing historical revisions with the current head would incorrectly refuse valid multi-image scope undo and revision turnover. No resolver, successor, input-read, selection, previous-value, later-history, ABA, allocation or root-restoration guard was removed or changed.

Contract mapping: §2 persists scope's complete physical image set and permits only authenticated continuation; §5 uses accepted physical bindings for inverse/redo, preserves scope dependencies after landing, and refuses later overlapping writes including equal-valued writes. The change preserves those paths while restoring the original raw-helper mismatch check. No contract decision changed.

## Source and test mapping

- `astrid/sdk/timeline/inverse.py`: two existing conditions plus their explanatory comment; no new abstraction.
- `tests/sdk/test_timeline_inverse_binding.py`: four compact cases. Two reject raw physical records at `execute`/`apply_inverse`; two exercise `create_runtime_commit_service().commit` with a three-image timeline scope, prohibit timeline entity dispatch, prove undo/redo across revision turnover, or refuse an equal-valued later write without partial acceptance.
- `tests/sdk/test_timeline_commit_provider.py` and `tests/timeline/test_authoring_media.py` are byte-identical to base0332. The original scope function is also byte-identical to the exact 33 lines from `a8c2b5b88533c7b58207f0b77d179a1dc523c0d2` (compared AST source spans). Thus both 0332 changes remain: the restored original test and G3's exact two guarded patch effects. All original film/reload/history/retry/ABA assertions remain unchanged.
- Existing neighboring suites cover per-step selection, raw accepted-record requirements, selected-view mutation refusal, physical owner replacement, missing/corrupt materialization proofs, disjoint successors, transient roots and restoration/redo.

## Commands and results

Commands ran from `/home/user/work/wt/agt-G4-inverse-binding-sol-0336`. Each pytest command below used this exact prefix:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-780da6d6" ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-780da6d6 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider
```

| Arguments after the prefix | Result |
| --- | --- |
| `tests/sdk/test_timeline_commit_provider.py::test_timeline_scope_inverse_binding_skips_entity_dispatch_but_keeps_guards` | Before repair: **1 failed**, `DID NOT RAISE`, 0.47s. After repair: **1 passed**, 0.39s. |
| `tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_commit_provider.py` | **116 passed**, 30.06s: all **112 original provider cases + 4 new controls**, no exclusions, including no-renderer coverage. |
| `tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_doc_patch_v2.py` | **155 passed**, 13.95s. |
| `tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/timeline/test_authoring_media.py -m 'not integration'` | **118 passed, 2 deselected**, 5.28s; the two real Runtime integration tests were not executed locally. |

Static and preservation checks:

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/inverse.py tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_commit_provider.py tests/timeline/test_authoring_media.py
env PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-73698d9217/mypy /tmp/astrid-u2-typecheck/bin/python -m mypy astrid/sdk/timeline/inverse.py tests/sdk/test_timeline_inverse_binding.py --follow-imports=skip
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" RUFF_NO_CACHE=true /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" MYPY_CACHE_DIR=/tmp/w-73698d9217/mypy-normal /tmp/astrid-u2-typecheck/bin/python -m scripts.reshape.compare_mypy_baseline
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-780da6d6
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

All passed: scoped mypy **2 source files** clean; Ruff **2150/2150**; normal mypy **1915/1915**. The brief's Ruff no-growth ceiling was 2151; this base's committed and observed count is 2150, with no baseline edit. All **15** locked producer artifacts match `780da6d605033ca71dbe2ad48c10ec2870ea4865`; `artifacts.json` is current. `sha256sum` of Agent and producer edit-command schemas is exactly `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. Entire original test-file byte comparisons against base passed.

Two initial lint invocations had setup errors, corrected without source/dependency changes: the harness's `workers/.../tmpdir` is a text pointer to `/tmp/w-73698d9217`, not a directory, so a Ruff cache path beneath that pointer failed; `RUFF_NO_CACHE=1` was invalid for Ruff and was replaced with `true`. Final Ruff used no cache; mypy caches used the private resolved scratch directory.

## Limits and handoff

No broad full suite, browser/socket suite, farm, native14, P4 HTTP or render journey was requested or run. The exact real Runtime script test at `test_authoring_media.py:649` hardcodes `use_runtime(commit='a0dca16975dfe8f5e762703b99d9791a16cf7fd7')` and overrides the checkout to `/home/user/work/runtime`; prior central attempts also failed collection/health before its assertion. The generic central targeted suite does not supply the required 780 import environment. A safe, coherent 780-source invocation was not established here, so no live G4 script PASS is claimed and no known-broken central request was repeated. Its source and strengthened exact effect assertions remain intact.

No schemas, fixtures, generated clients, pins, locks, protocol shapes or writer flows changed. Nothing was deleted; no skip/xfail/assertion weakening, dependency/shared-cache write, git write or push occurred. Independent Luna review passed the final product/test diff and traced the accepted-record boundary; it supplied review evidence only.

Recommended next steps: queue this bounded R2/G4 repair after the completed independent review; have the orchestrator supply a coherent sanctioned Runtime780 service configuration for the unchanged exact G4 integration script before claiming that separate journey qualified. No product blocker remains for this bounded repair.
