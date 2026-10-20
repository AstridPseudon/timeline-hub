# WC6 reload inverse repair

Status: **implementation and local guards pass; required real HTTP proof is blocked by test-lane classification**. No completion or commit message is claimed.

Agent worktree: `/home/user/work/wt/agt-m2-wc6-reload-inverse-repair`, base `53742bcab1d5ea53157fd65bf9ed99117f4738bf`, with the changes described below uncommitted. Runtime reference remains `7f6dd8920e1ceec41b137358df5e7fecc304888d`. No Runtime, schema, DTO, identity seed, fixture matrix, public package, integration tree, or shared dependency was changed.

## Cause and repair

The prior report's Runtime-ownership explanation was incorrect. Runtime's `timeline_commit_provider.py:79` imports `astrid.sdk.timeline.commit` in process. A direct loader check using `tests.helpers.runtime.use_runtime(commit='7f6dd89')` and `load_timeline_commit_provider('astrid')` resolved:

```text
Runtime loader: /tmp/astrid-runtime-archive-f48s2zg2/runtime_protocol/timeline_commit_provider.py
Agent provider module: /home/user/work/wt/agt-m2-wc6-reload-inverse-repair/astrid/sdk/timeline/commit.py
Agent inverse module: /home/user/work/wt/agt-m2-wc6-reload-inverse-repair/astrid/sdk/timeline/inverse.py
Provider implementation: /home/user/work/wt/agt-m2-wc6-reload-inverse-repair/astrid/sdk/timeline/commit.py
```

Two Agent mismatches were reproduced independently of sockets:

1. The recorded whole-payload read contains the original internal revision link. Reversing media leaves on a reloaded accepted document leaves the compiler's new link in that payload. For shared shots, its declared item identities also remain materialized. In the existing occurrence-media fixture, the expected read has `internal_timeline_revision_id: internal-1` and `item_id: item-1`; after reversal on the reloaded document, actual values are `authoring-timeline-revision-41af98ff86bc8a370d0608ce6c1d090b1d36672555b4b8f988f8d1b6fe5c9f2a` and `shot-item-placement-cb1bf5d05853ca0713af2d9450cfbb2f3d41bbda49e6b17c2d62b854e0b1c993`. The media value is restored correctly. The previous absent-ancestor exemption cannot fix this present-payload mismatch and is unsafe independently.
2. After fixing that read, accepted inverse media-pin validation fails with `unproven media boundary scope`. Its exact physical replay already equals the accepted document, but `_collect_media` sees only tagged scalar after-values, without their `media_id` address. In a same-alias rebind, introduced media is `{sha256:2222…2222}`, while media extracted from those writes was the empty set.

`inverse.py` now removes `own_materialized_read` completely. Its replacement applies only to present whole-payload reads backed by `AcceptedRecords`. It finds the authenticated accepted input closure, requires the same occurrence-owned shot, converts only declared item references with that closure's exact item map, and admits only the exact internal revision link verified by the original and current closure provenance. It then compares the **entire physical payload** with strict JSON equality. It never treats an unchanged child as proof of an absent ancestor, strips namespaces, or accepts arbitrary compiler links.

`commit.py` now retains the final recorded address token when collecting media from scalar after-values. Whole-value writes still use their original structure. The existing before-value guards, complete replay, physical parent/shot/internal comparisons, source document pins, introduced-pin scope, surviving-dependent checks, and accepted-history authority remain required.

## Guards and current F1

- New direct regression proves that one matching child cannot satisfy an absent ancestor read.
- New accepted same-alias regression proves exact reload undo and inverse redo across shared-shot materialization.
- Focused neighboring damage checks reject opaque `True` → numeric `1`, an unknown item identity, an unverified internal link, and an invalid source identity, preserving inputs/head/history.
- Existing alias, selection, membership, opaque preservation, source pins, exact media restoration, corrupt-boundary and ABA assertions remain unchanged. Portable fixture goldens remain unchanged and pass.
- This task's base predates F1. The narrow `fa156464` change was ported exactly: `commands.execute` supplies `staged_records=records`; `apply_inverse` checks them with `check_intervening` before any reversal. Its three scalar regressions were also ported unchanged: same-value refusal, ABA refusal, and disjoint prior/later explicit write plus composed reversal success.
- No whole historical files were copied. P1/current provider authority was retained; the only provider change is scalar media extraction inside its existing boundary proof.

## Tests

All commands below run from the assigned worktree, using read-only shared dependencies and no pytest cache.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_media.py -m 'not integration'
# 62 passed in 6.70s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_recipe_scalar_commands.py tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py -m 'not integration'
# 299 passed in 35.65s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_feedback.py tests/timeline/test_authoring_media.py -k 'not real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba' -m 'not integration'
# 88 passed, 2 deselected in 4.80s; socket proof reserved for central service

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/commands.py astrid/sdk/timeline/inverse.py astrid/sdk/timeline/commit.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_recipe_scalar_commands.py
# All checks passed!

git diff --check
# passed
```

An intermediate combined local run had `2 failed, 281 passed`: one exposed the scalar media-pin issue fixed above; the other was a new damage test using a nonexistent physical shot (raising KeyError before the intended guard). That test now corrupts the source identity of an existing shot and verifies CommandError. Both failures pass in the final runs above.

No full suite, browser test, or local socket suite was run.

## Required central proof remains unverified

The original HTTP test is entirely unchanged, including every positive/negative assertion. It has **no integration marker**, unlike the neighboring older HTTP test. The brief requires the integration lane and also prohibits new markers.

```sh
$ORCH/bin/request-test agt-m2-wc6-reload-inverse-repair registered-native-render-integration --files tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba
$ORCH/bin/wait-test agt-m2-wc6-reload-inverse-repair-registered-native-render-integration-1020144028-12846
```

Result: exit 5, `1 deselected in 1.04s`; source tree `790ac7f00fe9d0c1886a9dab3f12a8263deaf4ef`. The named suite explicitly runs `-m integration`, so no HTTP behavior ran. Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-wc6-reload-inverse-repair-registered-native-render-integration-1020144028-12846/`.

A second exact-node request attempted to preserve the unmarked test with `--files "tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba -m 'integration or not integration'"`. The service rejected it before execution: `bad file arg -m (relative path/glob/node-id, no ..)`. Request/result: `agt-m2-wc6-reload-inverse-repair-registered-native-render-integration-1020144421-8823`.

The classification question is pending with the orchestrator. Recommended next step: allow only the existing test's `@pytest.mark.integration` classification (no xfail/skip and no assertion edits), or register a central exact-node command that selects the unmarked test. Then run the required real script → normal clients/provider → reload → exact undo/restart retry/disjoint edit/redo/opaque refusal/ABA assertions, resolve any further exposed failure, and only then create commit-msg and DONE. This is a test-lane blocker, **not a Runtime defect**, and the required HTTP success is not claimed.
