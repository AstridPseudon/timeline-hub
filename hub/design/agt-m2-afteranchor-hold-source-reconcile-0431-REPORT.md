# Agent after-anchor hold/source successor — source report

Date: 2026-10-21 UTC

## Result

Prepared a new private Agent successor for the App2 after-anchor source
discrepancy. The source remains dormant: no App caller, Provider/session path,
Runtime source, pin, generation, activation, publication, or public artifact
was changed.

The current worktree is based on Agent `a905fa29b1bb47739df438f4203ed987be588e46`
(tree `5871915b4ed820e1a9c17a44f20ffd683f05df8c`). The approved complete floor
is Agent `5672d2b7deee2bfe2ab375fd6db5fc35a192591d` (tree
`6dd13b552c4f07fff5586b1fa772bdbdf64accba`). The harness will assign the
successor commit after worker exit; no commit SHA is claimed here.

Changed paths are exactly:

- `astrid/core/timeline/schema/edit-command.schema.json`
- `astrid/sdk/timeline/native_parent_media_commands.py`
- `tests/editing_conformance/test_recipe_m2_parent_media.py`
- `tests/sdk/test_timeline_materialization_schema_union.py`

## Closed contract correction

`ClipAddMediaArgs.row` now accepts the existing positive-hold row or the
minimal after-anchor-compatible row with `hold` absent or explicit `null`.
Explicit zero remains invalid in both alternatives. `clip.add` and its
positive-hold `ClipAddArgs` schema are unchanged. The parent handler sets
`raw_window` only for a non-replacement raw `parent/clip:<id>` selection and
rejects missing/null hold for ordinary append/replacement before `_clip`; only
the after-anchor video path reaches the existing `to - from` source-window
derivation. No `afterClipId` wire alias was added.

The existing two parent mirror compilations remain in place. The compact
regression asserts both derived mirror writes, final mirror equality, source
seconds, speed-aware placement, and the `max(0.05, timeline_duration)` floor.

## Exact identity and goldens

Changed-file SHA-256:

```text
astrid/core/timeline/schema/edit-command.schema.json        e161e18e7feda1d206db54a76d682887a742d82b8aee6d53d456d1e1002684da
astrid/sdk/timeline/native_parent_media_commands.py         935fab0dac38b4d6f4b16cb7f3254d1624496931e6425b93e07e6b9f0e367f16
tests/editing_conformance/test_recipe_m2_parent_media.py    f1860f7bb447438de52981fc70ab833c686d4b94b5adcfdfc8519554671e6c9d
tests/sdk/test_timeline_materialization_schema_union.py     8b12ba5b7b64c11dbebc55452c819dab7dee3387a84482558b2fe9c2c720ba82
```

Schema identity:

```text
raw SHA-256:       e161e18e7feda1d206db54a76d682887a742d82b8aee6d53d456d1e1002684da
canonical SHA-256: 0e4e3e78e3c80dafd79bc47ccf98100525c72c98ecb4c189d19b8ac6bcc46314
inventory:         62 definitions / 36 closed operation clauses
```

Unchanged fixture goldens:

```text
tests/editing_conformance/fixtures/recipe_m2_parent_media.json  22f1d1e94f3fbfada8cfc37519c30cfc96024a5a9a03a927a79a8ffcc85415b5
tests/editing_conformance/fixtures/recipe_m2_clip_add.json      cebe45dbf6806c2fb772665ad2c3a416eae172df48d1b0cc48d023cbc80345ff
```

The prior frozen floor hashes are reconstructed by the existing schema-floor
helpers; no frozen fixture or frozen schema was edited.

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_m2_clip_add.py
150 passed in 21.73s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py
59 passed in 180.37s

git diff --check
passed
```

The focused Python compilation check also passed and its generated caches
were removed. No full suite, Runtime/App acceptance, browser, live socket,
native Door, pin, activation, or generation qualification was run.
