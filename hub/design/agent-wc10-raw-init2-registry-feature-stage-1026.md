# Agent WC10 raw init v2 registry stage

Status: **NOOP — registration already exists exactly** (2026-10-21).

The assigned base is already the approved source commit:

- commit: `3dfdb1fa8c51b51f142cf6630816b313dc212cbd`
- tree: `20f436e18f6291eb5e38e3e5e058d02bac0f3fb5`
- parent: `7c9ef2ed5e70da1a13e89278496c74321453955a`
- Agent schema SHA-256: `d6aa2a9e76544cf3c58b313830b0fce7ce767577a0073192ff26dc88a2e97f7c`
- pre-feature/floor schema SHA-256: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

I did not duplicate or amend the registration. The existing commit contains the
exact approved future tuple:

- closed `timeline.init@2` args: `name`, `slug`, `config`; only `config` is an
  open semantic-JSON object;
- the existing `timeline.init` operation and deterministic `initialize` handler,
  with v1's `TimelineInitArgs` and fixed defaults unchanged;
- ordinal-zero, exact authenticated pristine-parent, empty placements/shots,
  and absent parent name/slug checks before any write;
- empty-only structural paths for tracks, clips, occurrences, placements,
  shots, groups, pinned shot groups, media, references, reference, assets, and
  `registry.assets`, plus the existing created-claim refusal;
- exactly scoped raw `parent.config`, `parent.name`, and `parent.slug` writes,
  with mirrored-clips suppression for v2; no registry-assets injection or
  structural birth;
- raw custom-canvas/null/absence/opaque-member/array-order preservation and
  guarded inverse coverage;
- provider history tests proving that undo back to empty does not permit a
  second initialization.

## Live callers and boundaries

There is no production v2 caller. `capture_initialize_raw` is the source helper
used by focused tests; the production `RemoteTimelines.create_empty` and the
duplicate workflow remain existing callers and were not migrated. The existing
v1 capture helper and v1 behavior remain unchanged. The commit changes no
Runtime/client generated files, public pins, endpoints, DTOs, stores, journals,
or release artifacts.

## Evidence

Focused source/schema/provider lane:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" PYTHONDONTWRITEBYTECODE=1 \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_pristine_raw_initialize.py \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/sdk/test_timeline_pristine_initialize_provider.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_composed_schema.py
=> 75 passed in 161.78s
```

The same command without `/home/user/work/runtime` on `PYTHONPATH` failed at
test collection with `ModuleNotFoundError: runtime_protocol`; the rerun above
uses the read-only shared Runtime source as required. Targeted Ruff also passed:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check \
  astrid/sdk/timeline/native_initialize.py astrid/sdk/timeline/commands.py \
  astrid/sdk/timeline/_recording.py \
  tests/editing_conformance/test_pristine_raw_initialize.py \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/sdk/test_timeline_pristine_initialize_provider.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_composed_schema.py
=> All checks passed!
```

No full, HTTP, native, installed-pair, renderer, browser, profile, generation,
pin, or consumer-activation run was performed.

## Next normal-generation dependency

The next step is an explicitly authorized reciprocal review of this exact
source/schema tuple and floor reconstruction, followed by one normal generated
Runtime/client counterpart and paired qualification in a containing private
release cohort. That generation must preserve the existing generated surfaces
and pins until the containing release is approved; no caller activation or
public release follows from this source-only stage.
