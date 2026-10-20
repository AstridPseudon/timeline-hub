# Runtime carrier cd0 marker carry

Date: 2026-10-20 UTC

## Status

**Private test-only successor.** This carries the exact owner 16:17 `cd0` test
delta onto Runtime private carrier `0511`. It does not change Runtime product
code, schema, provider imports, DTOs, public artifacts, pinning, adoption, or
native qualification.

## Exact source tuple

- Base commit: `0511ba84d846f451111db628c52d25cf203c615a`
- Base tree: `0a5bd960862875eac265deeedb543611675ca577`
- Working successor tree (the harness will create the commit):
  `22762a43df52c32d907e46a349a3f8e52d50cc65`
- Successor commit SHA: harness-assigned after worker exit; no SHA is invented
  for the uncommitted worker tree.
- Exact `tests/test_timeline_clip_replacement.py` blob:
  `65f5c22d40da230b368f3c7d3b77bb9ca127aafc`, identical to
  `cd0b0dcbea57c2a140e970eda59bea1161d6ff06`.

The only product-tree change is that test blob. The prior `6ab` clip
strengthening and the private carrier's helper, join, ownership, and artifact
contents remain inherited from `0511`; the accidental product design document
remains absent.

## Test contract

The old imperative/non-strict marker is replaced by the exact `cd0` split:

1. `test_native_parent_clip_swap_route_refuses_parent_ownership_on_current_schema`
   validates the real request against current public-013 and asserts the
   `ValidationError` that `parent` is not in `['shared', 'occurrence']`.
2. `test_native_parent_clip_swap_route_replaces_parent_media` retains its full
   acceptance body under strict `ValidationError` xfail with reason
   `needs schema 0.2.14 parent ownership; ledger D04`.

The private S2/current-013 schema still does not accept parent ownership. No
schema/provider/SDK hack was added to force the positive case.

## Evidence and boundary

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/packages/python:$AGENT" \
ASTRID_CHECKOUT="$AGENT" /home/user/work/venv-runtime/bin/python -m pytest \
-q --collect-only -p no:cacheprovider -m integration \
-k 'native_parent_clip_swap_route' tests/test_timeline_clip_replacement.py
2 tests collected (23 deselected)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/packages/python:$AGENT" \
ASTRID_CHECKOUT="$AGENT" /home/user/work/venv-runtime/bin/python -m pytest \
-q --import-mode=importlib -o addopts= -p no:cacheprovider -m integration \
-k 'native_parent_clip_swap_route' tests/test_timeline_clip_replacement.py
1 passed, 23 deselected, 1 xfailed

git diff --check
PASS
```

The prepared Agent factory was available and used. Agent private paired source
`3730` does not expose `capture_parent_swap_media`; that is a source-feature
separation, not native acceptance proof. No duplicate `3730` pair, broad suite,
full suite, or public adoption was run or claimed. The exact native pair is
coordinated by Agent only after this committed successor is independently
reviewed.
