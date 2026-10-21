# Runtime source review: occurrence trim ownership repair

**Verdict: SOURCE ACK (bounded source only); activation and qualification remain HOLD.**

## Exact candidate

- Agent commit: `9c35f4a18c65ec09d567f58839590f44b6d3997d`
- Agent tree: `64a25c3a5f374a1598d97a555266ad4351e41b63`
- Changed source: `astrid/sdk/timeline/_trim_commands.py`, blob
  `7ac448d8b7e46a43083b854e865c5ef21fbe6b57`
- Changed test: `tests/sdk/test_timeline_occurrence_trim_source_spike.py`
- Scope: dormant, unregistered `clip.trim@2`, raw selector
  `occurrence:<id>/clip:<id>`, unchanged args `{in_s, out_s}`, no live caller.
- Agent schema raw SHA-256: `ca55d74acbeef104be3a4a1ef57e2b4b2d7d1859d5194873a0fdf76a879ad6e3`
- Agent schema canonical SHA-256: `b19161c0881d7496e65e3cb52dcf57b35e661b780a608bd8fabba062d7bc495f`
- Frozen public ordinary floor: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

## Source checks

The repaired `_clip_trim_v2` calls `_owner(ctx, ref, child=True)` and then
`_exclusive(ctx, owner)` before the target membership select, clip reads,
registry/source reads, timing checks, dependency recording, or writes. The
existing `_exclusive` policy refuses unless `placement.owners` is exactly the
single requested occurrence. The repaired source test therefore gives both
required outcomes: a sole-owner positive records the existing source-only
recipe and inverse, while a shared-shot bundle refuses with
`unsupported_ownership` and leaves the bundle byte-for-byte unchanged.

The original occurrence guards remain in the source: literal raw child identity;
active translation-only occurrence; no source offset or time map; matching
parent/child rate; positive occurrence duration; existing child membership;
video media and exact verified-media identity; existing source-window/hold
consistency; in-range half-open source seconds; interior rounding through
`trim_source_interval`; and the existing `_clip` timing/track guards. The
positive writes remain limited to the selected child’s `from`, `to`, and
`hold`, with only the existing trim-intent cleanup when present. No parent,
shared shot, sibling, registry identity, or source bytes are written.

## Runtime carrier fit and boundary

Runtime’s existing generic carrier is sufficient at the record/receipt level:
`EditCommand` already carries `op`, `version`, `select`, `args`, and recorded
metadata; `CommandRecord` carries the command, writes, reads, selections,
bindings, dependencies, and derived writes; `PreparedCommit` carries the
`Recorder`; and the existing commit store persists it in timeline history beside
the generic idempotent mutation receipt. This requires no Runtime DTO, port,
endpoint, persistence, retention, generation, or pin expansion for the source
review.

The current Runtime published schema intentionally remains parent-only for live
`clip.trim@1`; it does not admit the dormant occurrence v2 selector today.
That is a later coordinated activation/generated-schema decision, not a defect
in this source-only repair. Frozen017 excludes this candidate. No generation,
version/pin, schema mutation, native/live execution, or caller activation is
claimed here.

## Evidence and limits

Reused the author’s bounded evidence from the exact candidate: **8** ownership
spike tests, **204** direct occurrence-media/trim/commit neighbors, and **104**
parent trim/sheet/occurrence-media neighbors; the handoff also records Ruff and
`git diff --check` passing. This Runtime review ran only the following compact
non-HTTP probes:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_commit_contract.py::test_schema_pin_and_generated_dtos_are_identical \
  tests/test_timeline_commit_contract.py::test_recorders_retain_execution_ordinal_and_all_leaf_families \
  tests/test_timeline_commit_validation.py::test_bundle_matches_canonical_resources_and_generator \
  tests/test_command_schema_compatibility.py::test_current_canonical_schema_preserves_latest_ordinary_publication \
  tests/test_command_schema_compatibility.py::test_withdrawn_exact_10c_schema_reports_every_lost_definition_and_operation \
  tests/test_command_schema_compatibility.py::test_widening_the_envelope_does_not_preserve_supported_operations
7 passed, 1 warning in 3.37s
```

No full suite, HTTP, native, generation, pin, registration, activation, or
audio/sound-window qualification was run. The original occurrence sound-window
positive for the sound path therefore remains **unqualified**; this ACK does
not convert that open qualification into a refusal or claim it passed.
