# Runtime parent `clip.swap-media` exact 014 proof

## Result

The existing strengthened native parent-clip positive passes when run with the
exact immutable Runtime `a0dca169` KEEP checkout and the exact Agent `310e548`
snapshot. It was run with `--runxfail`, so the pass is not an xfail being
reported as success:

```text
.                                                                        [100%]
1 passed in 4.40s
```

This proves the already-existing bounded parent carrier is executable on the
matching 014 candidate pair. It does not authorize changing the current
public-013 integration schema or test marker.

## Exact provenance

Runtime was imported from the KEEP checkout:

- checkout: `/home/user/work/wt/rt-m2-pin-a0dca169-b`
- commit: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
- tree: `4b7dd0fe44be973c344bab3de568eaf0bdd28476`
- `runtime_protocol.__file__`:
  `/home/user/work/wt/rt-m2-pin-a0dca169-b/runtime_protocol/__init__.py`
- commit-provider module:
  `/home/user/work/wt/rt-m2-pin-a0dca169-b/runtime_protocol/timeline_commit_provider.py`
- bundle:
  `/home/user/work/wt/rt-m2-pin-a0dca169-b/runtime_protocol/schemas/timeline-commit-bundle.json`
- bundle SHA-256:
  `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`

Agent was materialized privately with `git archive` from the exact frozen
source commit (the frozen repository and object were not checked out over any
worktree):

- commit: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`
- tree: `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`
- raw schema SHA-256:
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- imported provider source: `astrid/sdk/timeline/commit.py`
- imported parent media source:
  `astrid/sdk/timeline/native_occurrence_media_commands.py`
- provider source SHA-256:
  `ed20be6e514efe6a5b0e671a7ed92fa333847b0d77b62994ba0f6f68d950a75b`
- parent media source SHA-256:
  `6aaa6c167c3dbad0783c095d04868c8a67e88f7f7b698178596160b06e781442`

The corrected provenance probe reported Runtime first on `sys.path`:

```text
['', '/home/user/work/wt/rt-m2-pin-a0dca169-b',
 '/home/user/work/wt/rt-m2-parent-clip014-exact-proof/tests',
 '<private archived Agent 310 source>', ...]
```

No public-013 Runtime checkout was used. The first attempted probe referenced
a prepared Agent directory that had already been cleaned up; it failed setup
before importing or running the test. The successful run above rebuilt the
private overlay directly from the exact 310 Git object.

## Exact command and evidence

From the exact Runtime KEEP checkout, with `PYTHONDONTWRITEBYTECODE=1`, no
pytest cache, and the exact Agent overlay selected by `ASTRID_CHECKOUT`:

```sh
PYTHONPATH="$RUNTIME:$TESTS:$AGENT" \
ASTRID_CHECKOUT="$AGENT" \
PYTHONDONTWRITEBYTECODE=1 \
/home/user/work/venv-runtime/bin/python -m pytest -q \
  --runxfail --import-mode=importlib -o addopts= -p no:cacheprovider \
  "$TESTS/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media"
```

where `RUNTIME` was `/home/user/work/wt/rt-m2-pin-a0dca169-b`, `TESTS` was
`/home/user/work/wt/rt-m2-parent-clip014-exact-proof/tests`, and `AGENT` was a
private archive of Agent commit `310e548…`. Result: **1 passed in 4.40s**.

The test exercised Runtime's real service/provider path, real imported old/new
media, the bounded parent selector, and the accepted canonical parent asset.
No test body, xfail, schema, command body, frozen artifact, or product source
was changed.

## Decision and handoff

The previous parent-path report was correct only for the current public-013
integration pair: that Runtime validator rejects `ownership: parent` before
provider execution. This exact 014 run proves that rejection is not evidence
that Agent 310 lacks the carrier or that the operation is semantically
invalid. The existing marker remains valid for public 013 until the 014
generated schema is adopted.

Retirement of the marker requires qualification of the same 014 cohort (Agent
source/schema and Runtime generated bundle together), followed by the normal
integration/release decision. Do not widen `clip.set`, use add-then-delete,
invent an endpoint/DTO, or rewrite the frozen artifact.

No full suite was run or requested.
