# Automatic placement reads + current fixture trim

Completed on `tl/agt-m2-auto-fixture-gate`, base `df2739f9`. Product changes are
exactly the approved `db98206f` `_consume` change: seven literal timing/lane
field reads (`at`, `at_ms`, `track`, `hold`, `from`, `to`, `speed`), retaining
membership, pool, legacy and ownership guards. The approved `540d37b0` known-path
loader and ten fixture consumer adaptations are composed with those semantics.
No schema, dependency pin, other product logic, integration or ledger changes.

## Data and decisions

The brief says four changed narrow fixtures. Read-only `git diff --name-only
 df2739f9 db98206f` establishes four changed files, **two** of which are fixtures:
`recipe_m2_auto_placement.json` and `recipe_m2_shared_auto_placement.json`.
Neither overlaps the ten compact fixture files. Intended expanded data therefore
uses `db98206f` for those two and `df2739f9` for the other ten; no old whole-clip
reads replace the seven-field semantic reads. This follows the approved source,
rather than inventing changes to two additional fixtures.

Applied the approved factoring algorithm to that intended data: remove only
record fields equal to the same command's `created`/`reads`/`selections`, share
identical inputs/media at named locations, and reuse create output as unplace
input. Ten reconstructed fixtures exactly equal intended data; all 15 compact
cases survive. The two auto goldens retain all eight cases and differ from base
only by whole consumed-row reads becoming the seven field reads. All 23 cases
across 12 changed fixtures remain. Ordinary expanded handoffs for all 12 are
byte-identical to their intended source blobs at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agent-expanded-<stem>.json`

App consumes those expanded JSON files, never the Python private encoding.
The repo loader/tests have no Git metadata prerequisite. The one-off composition
and scope audit scripts use only read-only Git operations to compare approved
sources. Source provenance, individual source/handoff/compact SHA-256 hashes,
unchanged schema hash and sizes/case counts are documented in
`docs/design/agent-fixture-trim-current.md`.

The loader never recursively interprets authored payload keys. Input/output
opaque `records`, `command`, `reads`, nested created metadata, Unicode and newline
values survive with equal UTF-8 JSON bytes. Kept the original input test and added
an output parameter; no assertions were removed or weakened. AST audit confirms
182 existing consumer/helper functions match the approved trim apart from
imports, and explicitly confirms current positive equal-state delete replay and
three D07 timing proof bodies are unchanged. Initial scoped Ruff found four
import-format issues in the approved trim files; import sorting fixed them.

## Size: current integration → after

Counts include one logical line for an already-flat JSON file; there is no new
minification, opaque compression or general fixture language.

| Scope | Bytes before → after (net) | Lines before → after (net) |
| --- | ---: | ---: |
| Ten compact fixtures | 917,833 → 740,101 (-177,732) | 32,338 → 25,775 (-6,563) |
| All twelve changed fixtures | 1,018,059 → 857,785 (-160,274) | 36,275 → 30,546 (-5,729) |
| All 27 source/test/fixture/design paths, excluding this report | 1,181,467 → 1,043,506 (-137,961) | 39,452 → 34,142 (-5,310) |

## Exact commands and results

Working directory for all commands:
`/home/user/work/wt/agt-m2-auto-fixture-gate`.
Shared dependency environments remained read-only. No full suite was requested.

Original narrow acceptance suite, unchanged set: **571 passed in 54.62s**, exit 0.
Includes eight-mode image/video guard matrix, consumed-claim tampering, stale
native moves, ownership/membership/order/timing refusals, pool/legacy guards,
media/manifest inverses and positive unrelated params/volume/opaque rebases.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-auto-fixture-gate/pytest-narrow tests/editing_conformance/test_recipe_auto_placement_reads.py tests/editing_conformance/test_recipe_m2_auto_placement.py tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/editing_conformance/test_recipe_m2_placement_create_unplace.py
```

Original trim acceptance suite plus the new opaque-output case: **556 passed in
41.78s**, exit 0 (original 555 nodes retained). This overlaps the narrow suite;
these totals must not be added as distinct coverage. The only Python changes
after the narrow run were import sorting; the subsequent trim suite exercises
the final loader and consumer imports.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-auto-fixture-gate/pytest-trim tests/editing_conformance/test_fixture_loader.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/editing_conformance/test_recipe_m2_clip_split.py tests/editing_conformance/test_recipe_m2_clip_trim.py tests/editing_conformance/test_recipe_m2_placement.py tests/editing_conformance/test_recipe_m2_placement_create_unplace.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_recipe_occurrence_delete.py tests/editing_conformance/test_recipe_occurrence_duplicate.py tests/editing_conformance/test_recipe_occurrence_media.py
```

Reconstruction and source comparison: **10/10 exact**, **15/15 compact cases**;
**2/2 narrow-only semantic fixtures**, **8/8 auto cases**; **12/12 byte-exact
expanded exports**, exit 0.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-auto-fixture-gate/compose_fixtures.py
```

Scope/AST/schema audit: **passed**, exit 0. Approved paths only; sole product
change exactly `_consume`; existing positive delete and D07 proofs unchanged;
EditCommand schema byte-unchanged.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-auto-fixture-gate/check_scope.py
```

Scoped lint and whitespace: **passed**, exit 0.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/fixture_loader.py tests/editing_conformance/test_fixture_loader.py tests/editing_conformance/test_recipe_auto_placement_reads.py tests/editing_conformance/test_recipe_clip_scalar_fields.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/editing_conformance/test_recipe_m2_clip_split.py tests/editing_conformance/test_recipe_m2_clip_trim.py tests/editing_conformance/test_recipe_m2_placement.py tests/editing_conformance/test_recipe_m2_placement_create_unplace.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_recipe_occurrence_delete.py tests/editing_conformance/test_recipe_occurrence_duplicate.py tests/editing_conformance/test_recipe_occurrence_media.py
git diff --check
```

## Holds, blockers and next steps

No blocker to this bounded source/test unit. Actual Runtime/App qualification,
live/socket/browser journeys, `make check`, and full suites were not run or
claimed. Keep production activation held pending Runtime schema/provider
regeneration and normal regeneration/attempt-fence qualification, and App's
original-approval/outbox journey using the expanded exports. Existing fixed
occurrence-window bounds, parent-owned completion, video-unplace and legacy
migration restrictions are unchanged; this unit does not resolve those holds.

Recommended next step: orchestrator review and integrate this single composed
unit, then coordinate Runtime/App consumers with these expanded vectors under
their existing qualification gates. No commit/merge/rebase/checkout/push was
performed. Commit message and DONE are supplied for the harness; test temp files
and worktree bytecode were removed.
