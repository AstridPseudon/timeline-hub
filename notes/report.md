# agt-m2-text-binding-native

Implemented additive native `text-binding.set`, closed schema and capture helper, real provider `text_selection` capture, stable kind/slot rows, exclusive source-occurrence ownership, ordered append/clear with guarded exact inverse, concurrent disjoint-key rebase, same-value/ABA guards and opaque preservation. Old writers remain. No integration checkout, shared dependency, ledger, producer/element/capture-hook/word-hunk path was edited.

Agent base: `ba5f2756f50a84f570aa9699ef621873f7521abc`; Runtime observed: `8609333456b9537339ee1a5dfc7ffd9609242de8`. Contract and gaps: `design/agent-text-binding-native.md`.

## Verification

Run from `/home/user/work/wt/agt-m2-text-binding-native`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_text_binding_native.py tests/editing_conformance/test_recipe_text_binding_spike.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_recipe_occurrence_media.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_shot_text_bindings.py --tb=short
```

**414 passed, 1 deselected.** The historical spike remains isolated from the new ordered collection; its former Runtime-presence xfail is now an integration-lane positive because P1 exists.

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_text_binding.py -x --tb=short
```

**1 failed** at first-use preview: unchanged Runtime's frozen TargetKey pattern rejects `occurrence:occurrence-1/text-binding:voiceover_script::` in PreparedCommit; reason `invalid_prepared`. No schema monkeypatch or Runtime source edit was used.

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_text_binding.py -k 'exact_project_text_selection_refuses_before_writes or runtime_declares_and_captures_exact_text_port' --tb=short
```

**9 passed, 11 deselected.** Actual P1 rejects foreign/missing CAS, wrong descriptor/hash/size/MIME, invalid UTF-8 and oversized objects without publication or live binding changes.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-text-binding-native/prepare-runtime-overlay.py
ASTRID_RUNTIME_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-text-binding-native/runtime-schema-overlay PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_text_binding.py tests/editing_conformance/test_recipe_text_binding_spike.py::test_runtime_port_declares_exact_text_selection --tb=short
```

**17 passed, 4 strict xfailed.** This private overlay uses current Runtime code unchanged; only its contract input and normally generated schema bundle are extended. It preserves Runtime's other operation clauses and does not publish a partial schema. The script checks that the only changed `runtime_protocol` file is `schemas/timeline-commit-bundle.json`. Tests use real main-API backup/CAS, native provider and RuntimeService, without sockets, SQL writes or fake PreparedProvider. They cover exact nonempty/Unicode/CRLF/EMPTY bytes, first-use capture, live projection, restart retry, V1 retention after rebind/restart and exact inverse/redo, original guards, disjoint births/rebinds, same-value authorship, and acceptance-time CAS re-verification.

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/native_text_binding.py astrid/sdk/timeline/_command_state.py astrid/sdk/timeline/_collections.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/inverse.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py tests/editing_conformance/test_recipe_text_binding_native.py tests/editing_conformance/test_recipe_text_binding_spike.py tests/editing_conformance/test_commit_runtime_text_binding.py

git diff --check
```

Both passed. No full suite requested or run.

## Decisions and remaining pairing

- Used actual existing P1 MIME `text/plain; charset=utf-8` (space included), exact descriptor fields and existing media dependency lane.
- Used source-aware exclusive ownership; shared source aliases refuse rather than writing a sibling's live binding.
- Preserved collection order, using the existing include-concurrent policy for append; no canonical sort. Accepted records capture actual rebased membership while the original public command stays unchanged.
- Kept all clear/first-birth undo/V1-after-clear positive assertions as strict xfails for the exact `text_binding_clear_unsupported` refusal. No EMPTY-as-clear encoding.
- Found an additional genuine retained-main gap: undoing a rebind of the backup's existing `text/plain` transcript fails Runtime's strict MIME verifier. A separate narrow strict xfail preserves exact restoration rather than normalizing immutable history.

Recommended next steps: manager composes the operation into the current full public schema superset and runs normal generation; Runtime owner resolves removal and legacy exact MIME restoration; rerun the positive integration tests against that pair (strict xfails must then flip); retain old writers until all positives qualify. App/wire/browser journeys, public client generation and full suites are unverified.
