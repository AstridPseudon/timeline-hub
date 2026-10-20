# Agent ordinary014 normal consumer-pin candidate

Status: NORMAL STAGING CANDIDATE; consumer qualification passed. This is not an
integration pin, release, activation, or App/browser qualification.

## Exact tuple

| Item | Value |
| --- | --- |
| Agent source HEAD | `ee896821b502ee4e51211b19d064fa44915f5777` |
| Agent HEAD tree | `aa0b15850d4b777b77f54faec189cf7e4c60a7b6` |
| Central qualification snapshot tree | `5b4ec03d6d3081f9a3b96676f10ca051c4e9775e` |
| Runtime producer checkout | `/home/user/work/wt/rt-pin-a0dca169` |
| Runtime producer commit | `a0dca16975dfe8f5e762703b99d9791a16cf7fd7` |
| Runtime producer tree | `4b7dd0fe44be973c344bab3de568eaf0bdd28476` |
| Runtime package | `0.2.14` (unpublished) |
| Frozen raw schema source | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Runtime schema digest | `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59` |
| Artifact version | `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0` |
| `contract/artifacts.json` SHA-256 | `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815` |
| Producer manifest entries | 75 |

The producer checkout was detached, clean, and verified at the exact requested
commit/tree. All 75 manifest source bytes hash exactly to their committed
manifest entries. The 15 selected vendored consumer files hash exactly to the
producer source bytes and manifest entries.

## Pin and changed paths

I set only `runtime.lock.json`'s `source_commit` to the exact Runtime SHA, then
ran the normal updater. The generated consumer changes are limited to:

```text
astrid_runtime_client/__init__.py
astrid_runtime_client/contract_metadata.py
astrid_runtime_client/generated.py
astrid_runtime_client/timeline_commit_types.py
runtime.lock.json
```

The schema consumer byte was unchanged because the candidate supplied the same
schema bytes; unchanged response fixtures were not rewritten. No hand-edited
generated file, manifest bypass, raw-schema override, pip install, shared
dependency write, or Agent artifact-manifest refresh was needed. The normal
vendor lock check passes.

## Qualification evidence

Local targeted lane, with bytecode and pytest cache writes disabled:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/test_vendor_lock.py \
  tests/stage1/test_vendored_workspace_client_parity_luna.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_pristine_initialize_provider.py \
  tests/editing_conformance/test_native_word_anchor_vectors.py \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/editing_conformance/test_recipe_occurrence_create.py \
  tests/editing_conformance/test_recipe_parent_media.py \
  tests/editing_conformance/test_recipe_text_binding_native.py \
  tests/editing_conformance/test_recipe_parent_auto_completion.py
```

Result: **279 passed in 190.54s**.

Central named actual-provider lane (HTTP/socket-capable test service), with
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169` and
`ASTRID_PARENT_MEDIA_SEED_RUNTIME=/home/user/work/runtime`:

```text
python -m pytest -q -m integration \
  tests/sdk/test_timeline_pristine_initialize_runtime.py \
  tests/editing_conformance/test_commit_runtime_occurrence_create.py \
  tests/editing_conformance/test_commit_runtime_parent_media.py \
  tests/editing_conformance/test_commit_runtime_text_binding.py \
  tests/editing_conformance/test_native_word_anchor.py \
  tests/editing_conformance/test_next_command_cohort_runtime.py \
  tests/editing_conformance/test_commit_runtime_m1.py \
  tests/editing_conformance/test_commit_runtime_identity.py \
  tests/sdk/test_timeline_producer_guard_runtime.py \
  tests/sdk/test_timeline_native_frontends.py
```

Result: **143 passed, 10 deselected in 214.10s**. This covers representative
`timeline.init`, `occurrence.create`, parent media add, text binding, word
anchor, S2 move/undo/retry, P1 authority, F1 identity, and normal CLI/Python/
native frontend/session paths against the exact producer. Renderer-off save
fences, original request bodies/keys/receipts, reload/restart, guarded undo,
and exact retry assertions were retained by the existing tests. No App browser
journey or renderer/audio claim is made.

Final checks:

```text
python3 scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-a0dca169
git diff --check
```

Both passed.

## Remaining gates and boundaries

- App must complete its own normal-owned pin and actual consumer proof against
  this exact Runtime candidate as the same cohort.
- Manager independent review and peer App cohort review remain required.
- No public `0.2.14` release, Runtime integration bump, activation, or release
  claim is authorized here. Public Runtime `0.2.13` (`2c4ac180…`) remains
  untouched.
- Composition 0.0.12 archive/lock remains untouched.
- No carrier, audio, WC3, WC5, WC6, or D13 changes were included or reviewed.
- No full or full-* suite was run.
