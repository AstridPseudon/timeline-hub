# Agent review: owner-film clip-look scanner 1.0.8

Reviewer: Agent worker `agt-review-scanner-108` (2026-10-20). Review only; no
product repository files changed, nothing was published, pushed, merged, or
integrated.

## Verdict

**APPROVE** the exact immutable 1.0.8 archive for policy review completion and
delivery preparation.

The prior 1.0.7 rejection remains in force. This approval does not relabel
1.0.7 or approve owner-film data, renderer behavior, macOS, or the full Agent
suite.

## Exact artifact and four-member integrity

- Archive: `design/handoff-vw-m4-scanner108-codec-repair-1.0.8.tgz`
- Size: `18116` bytes
- SHA-256: `e87e88705679e320bc83b6c72dff31fe23bbd0122981f314b5890411d6449cfb`
- Archive sidecar, metadata archive entry, and computed archive hash agree.
- The archive contains exactly four regular USTAR members, sorted and mode
  `0644`, with uid/gid/mtime zero and empty owner names.
- Every member was extracted to a private scratch directory and compared
  byte-for-byte with its flat `design/handoff-vw-m4-scanner108-codec-repair-1.0.8-*`
  copy and with the metadata hash:

  | member | bytes | SHA-256 | flat/metadata |
  | --- | ---: | --- | --- |
  | `README.md` | 7033 | `72f5c5ccb029ff6a9fe815c14ee2334e7913432eb9a4a03187eb43bef245c037` | agree |
  | `owner_film_cliplook_scan.py` | 38074 | `66fadbd930d8af88ceb06a5e40b9e4cb4a8a90d42175b6b630309eec72aeffed` | agree |
  | `tests/conftest.py` | 385 | `ea7d84927b97d78e2eb17fa87180ce2b7591f2c53645d1799b99f2c34197e430` | agree |
  | `tests/test_owner_film_cliplook_scan.py` | 36197 | `5160c0d2c6f8728125383cde832a6a9e59297bab952ec8263d98266261e7baf4` | agree |

The archive metadata identifies this exact 1.0.8 source and keeps 1.0.7 as
separate historical provenance.

## Exact tests and results

All commands used the exact extracted archive and the assigned clean Agent
worktree `/home/user/work/wt/agt-review-scanner-108` as `--agent-root`. The
qualified shared Agent venv was used read-only; no dependency or cache files
were changed.

```text
cd <private exact-1.0.8 extraction>
/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider \
  --basetemp <private pytest directory> \
  --agent-root /home/user/work/wt/agt-review-scanner-108 -q tests
```

Result: **124 passed in 12.36s**, exit 0. This is the shipped extracted
archive suite.

The focused replay of the old rejected surface used the exact archive's
tests for malformed look values, entrance/exit strings and lists, numeric
booleans, audio fade strings/lists/objects/booleans in parent/config/child
paths, malformed curve containers, non-object params, child values hidden by
placement, and openable source paths:

```text
/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider \
  --basetemp <private pytest directory> \
  --agent-root /home/user/work/wt/agt-review-scanner-108 -q \
  tests/test_owner_film_cliplook_scan.py::test_malformed_look_fails_closed_and_retains_unknown_inventory \
  tests/test_owner_film_cliplook_scan.py::test_declared_stored_numbers_fail_closed \
  tests/test_owner_film_cliplook_scan.py::test_stored_animation_shapes_fail_closed \
  tests/test_owner_film_cliplook_scan.py::test_stored_audio_fades_fail_closed_at_authored_paths \
  tests/test_owner_film_cliplook_scan.py::test_stored_audio_curve_containers_fail_closed \
  tests/test_owner_film_cliplook_scan.py::test_audio_params_non_objects_fail_closed \
  tests/test_owner_film_cliplook_scan.py::test_audio_error_source_paths_are_openable \
  tests/test_owner_film_cliplook_scan.py::test_stored_child_value_checked_before_placement_can_replace_it
```

Result: **84 passed in 7.00s**, exit 0. The 1.0.7 fail-open cases now yield
`status: incomplete`, bounded `... is unreadable` errors, and affected
`knowledge: unknown` inventory/findings. Malformed values and exception text
are not copied into output.

The existing Agent codec lane was run directly:

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/home/user/work/wt/agt-review-scanner-108 \
/home/user/work/venv-agent/bin/python -I -B -m pytest -p no:cacheprovider \
  --basetemp <private pytest directory> -q tests/core/timeline/test_clip_fields.py
```

Result: **102 passed in 2.61s**, exit 0.

## Policy checks

- The scanner uses one `project_runtime_parent_composition` projector call;
  the shipped regression test guards this directly.
- Declared `FieldSpec.stored_at` values are checked with the Agent Draft-07
  field schema and strict codec before presentation; `stored_at_audio` is
  included. Shared visual fade aliases use the general entrance/exit codec.
- Audio curve containers are shape-checked. Unknown string curve IDs retain
  the settled policy of `complete` with `knowledge: unknown`; non-string
  malformed curve values fail closed.
- Errors and source paths remain openable and bounded to authored closure
  paths, IDs, pins, properties, and existing ranges. No malformed authored
  value, exception text, credential, or owner-film data is emitted.
- Explicit `None` clears remain accepted. Opaque extension/animation data is
  preserved through the Agent projector and does not appear in bounded output.
- Free-form transition IDs/types remain accepted under the settled transition
  policy; malformed transition containers fail closed.
- `clean_claim` remains false, and missing/incomplete closure data is honest
  `incomplete`; no owner-film canonical closure was supplied or scanned.

## Limits and next steps

No owner data, full Agent suite, browser, renderer, playback, network,
installation, macOS, product-repository mutation, ZIP publishing, or
integration was performed. The independent 130-case matrix approval is
supporting evidence only; this report independently reran the exact archive,
the historical negative surface, and the existing codec lane.

Recommended next step: retain 1.0.7 as rejected, and allow the orchestrator to
use this approved 1.0.8 artifact in delivery preparation subject to the owner
hard-stop process and the stated limitations.
