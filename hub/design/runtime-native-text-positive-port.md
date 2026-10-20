# RT02 Runtime native text positive port

## Scope and frozen pair

This worker added Runtime-owned integration coverage for the ordinary native
`text-binding.set` path. The test uses the frozen ordinary Agent source from
commit `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3` (content tree
`c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`) and the staging Runtime 0.2.14
candidate described by `runtime-next-ordinary-official-candidate.md`:

- contract version `0.2.14`;
- schema digest `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`;
- artifact version `sha256:8023c665f0e32835cf06b793c6f5ffa0a278a7ca5aadbfe971d52d163d66c7a3`;
- 55 definitions / 29 operations, including `text-binding.set`.

The public Runtime 0.2.13 tuple and the four retired endpoint controls were
not changed.

## Original assertion -> native replacement

| Retired original | Runtime-owned positive replacement |
| --- | --- |
| `tests/test_shot_text_bindings.py::test_set_is_deterministic_project_scoped_and_replays` | `tests/test_timeline_text_native_positive.py::test_native_first_use_is_project_scoped_deterministic_and_replays` (UTF-8 and empty first use, exact retry, digest/size/MIME readback, project-owned object) |
| `tests/test_shot_text_bindings.py::test_set_rebind_and_event_order` | `tests/test_timeline_text_native_positive.py::test_native_rebind_preserves_event_order_and_exact_inverse_after_restart` (native rebind, ordered events, restart, inverse and redo) |
| `tests/test_shot_text_bindings.py::test_invalid_utf8_and_size_are_zero_write` | `tests/test_timeline_text_native_positive.py::test_native_invalid_text_selection_is_zero_write[utf8]` and `[limit]`, plus the project/digest/size/MIME guard cases |
| `tests/test_shot_text_bindings.py::test_identity_digest_is_sha256` | `tests/test_timeline_text_native_positive.py::test_native_identity_digest_and_empty_present_clear_inverse` (SHA-256 identity, empty PRESENT row, explicit clear, inverse restoration) |

The new test creates a project and timeline through the normal Runtime
bootstrap, initializes the visual output track with the Agent command, births
`occurrence:occurrence-1` with `occurrence.create`, then submits the real
Agent-captured `text-binding.set` command through Runtime acceptance. It does
not call a retired writer, manufacture accepted history, or write SQL.

The additional `test_unplaced_project_shot_target_is_not_claimed_by_occurrence_command`
proves the ownership boundary: a `shot:unplaced` target is refused with no
writes. This is not claimed as a replacement for the original unplaced
project-shot capability. Its positive promotion remains open with the
project-library owner / `rt-m2-unplaced-shot-promotion-carrier` pending the
owner decision on an authorized carrier.

## Evidence

Actual new native count: **11 passed, 0 failed** (two first-use data cases,
six exact-selection refusal cases, and the three lifecycle/boundary cases).

Candidate command:

```text
PYTHONDONTWRITEBYTECODE=1 \
ASTRID_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source \
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/candidate-0.2.14:/home/user/work/wt/rt-m2-native-text-positive-port/tests:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source \
/home/user/work/venv-runtime/bin/python -m pytest -q --import-mode=importlib -o addopts= -p no:cacheprovider \
/home/user/work/wt/rt-m2-native-text-positive-port/tests/test_timeline_text_native_positive.py
```

Result: `11 passed in 6.32s`.

Also passed: `git diff --check` and bytecode compilation of the new test.

The required central exact-file Runtime request
`rt-m2-native-text-positive-port-targeted-1020143622-13964` passed with
`69 passed, 11 deselected, 4 xfailed in 21.27s`. The 11 new cases are marked
integration and were therefore deselected by the central default targeted
lane; the four xfails are the unchanged retired endpoint controls. The
candidate run above is the authoritative native qualification for this
bounded staging pair.

## Remaining qualification boundary

RT02 is not public-schema deletion or publication. The four original tests
remain strict-xfail refusal controls. This change qualifies occurrence-owned
native positives only; it does not silently retarget the old unplaced
project-shot writer. Public schema union, authorized release, and consumer
qualification remain required before promoting the native command onto the
public tuple.
