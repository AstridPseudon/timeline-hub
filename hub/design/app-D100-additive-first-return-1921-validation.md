# D100 additive first return validation

## Scope

Only `tests/sdk/test_d100_item_birth_boundary.py` changed. The protected
`astrid/sdk/timeline/_command_state.py` SHA-256 remains
`018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`.

The direct shared-owner fixture now authors `source_offset: 0` and recomputes
the authored parent `content_digest` with the existing `_digest` helper. The
two overbroad source-mapping assertions were replaced with exact equality for
`shots`, `placements`, and `_runtime_document`, an exact allowed-key check,
and an exact `_doc_patch_images` projection assertion. Existing item identity,
opaque payload, canonical document, internal revision, wrong-pair, digest,
no-write, and original-bundle predicates remain unchanged.

## Static checks

- `PYTHONPYCACHEPREFIX=<private task tmp>/pycache python3.11 -m py_compile tests/sdk/test_d100_item_birth_boundary.py` — PASS.
- Python 3.11 `ast.parse` plus `compile` of the exact test file with the same private cache root — PASS.
- `ruff check tests/sdk/test_d100_item_birth_boundary.py` — PASS (`All checks passed!`).
- `mypy tests/sdk/test_d100_item_birth_boundary.py` — PASS (`Success: no issues found in 1 source file`).
- `git diff --check` — PASS.

## Runtime and test status

The registered production route was verified by read-only source inspection:
the test helper registers the existing Astrid provider and submits through
`service.commit_timeline`; Runtime's pinned `ab1e4f61` source enforces the
canonical route and startup-only provider registration. No unmounted helper
was used as behavior credit. The mounted App save wiring was also inspected:
`useTimelineSave` passes `commit.commitData` into
`useTimelinePersistence`, whose mutation calls the provider's
`saveTimelineAtHead` path. This worker did not claim an App runtime result
from source inspection alone. The ordinary D66 diagnostic hook is not relevant
to this physical item-birth assertion, so no diagnostic credit was claimed.

Current free space was 4,843,577,344 bytes, below the genuine 5 GB unit-body
threshold and above the 4.6 GB source-admission floor. Unit bodies are
therefore **NOTRUN**. The corrected own27 and unchanged original9 are also
**NOTRUN** by instruction. No full, browser, socket, acquisition, native,
fixture-receiving, or D130 run was requested.

The later normal acceptance request is:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-D100-additive-first-return-1921 targeted --files "tests/sdk/test_d100_item_birth_boundary.py") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

It must run only after the required independent purpose review and genuine
source admission; unchanged original9 follows separately.
