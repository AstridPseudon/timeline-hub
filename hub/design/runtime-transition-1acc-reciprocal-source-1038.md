# Runtime reciprocal transition source review — 1acc

Date: 2026-10-21 UTC

## Result

**SOURCE ACK — bounded source/schema review.**

The exact Agent candidate `1acc64610019cd13e344a4a4d75e84280b8b7f16` /
tree `b51829d29f5eb22e6cae524b1df66bf0febd1de9` fits the settled Main
transition semantics for this source slice. The final delta is the requested
raw-params safety correction; it does not weaken the earlier b7 presence,
revision, authority, adjacency, fit, owner, or media guards.

This ACK is not complete-source approval, generation, Runtime publication,
pinning, caller activation, or a claim that this source-only shape runs under
the current Runtime schema. Agent1024 owns the later complete composition on
approved6c.

## Exact identities

| Item | Exact identity |
| --- | --- |
| ca9 feature provenance | commit `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`, tree `87b432d48b0e1a5e0410c630ca76150095075eff` |
| b7 Main-presence repair | commit `b7c58a5fbc98a886444110b22aa897cc3ba1dda6`, tree `d69b461aa386f0b2247862bbfd2f9a5dfd569a55` |
| reviewed Agent candidate | commit `1acc64610019cd13e344a4a4d75e84280b8b7f16`, tree `b51829d29f5eb22e6cae524b1df66bf0febd1de9` |
| candidate source, `_clip_scalar_commands.py` | blob `8267b26d126cd5dc1acf76f1a54b4908b1162603`; SHA-256 `e842d696a575b86a3b33feb5d4033b70815d037de3fef878c94e71e0889a08e7` |
| retained authority source, `_selected_param_authority.py` | blob `da3cb86c6a90290ca5f712ab23610e6cc743aa19`; SHA-256 `8b19d56d2c28f1dc9e003f1a578e361397e0f73845319ee76cd60456ba211fdf` |
| candidate schema, `edit-command.schema.json` | blob `5a7e89214b1f94378e908f996bb3428c1e6d5474`; SHA-256 `27b76296a6c1a81495a1cdd80b13d765ebf7952af1967eb839d2fd3606413eab` |
| Runtime review base | commit `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d` |
| Runtime current edit-command schema | blob `8cedcd2506e5408e8e96a74adca5abd036d03f7e`; SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Runtime bundle schema | blob `cf5dfbda604f7337f8fc155f811cb67fbfa4dfc9`; SHA-256 `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3` |
| Runtime generated timeline DTO | blob `e4605ad9dca1733bc9547fdfa8ef5e80e00ce008`; SHA-256 `4b23c46311210f5fa3a5684eceeab2772b30c40b61c623eacf0fcd1183d45457` |

The `1acc` commit changes only
`astrid/sdk/timeline/_clip_scalar_commands.py` and its focused test. The
schema and the b7 presence repair are inherited, not regenerated here.

## Exact source/schema fit

- Reference presence and revision identity remain the b7 behavior previously
  reviewed. The no-reference legacy path is admitted only for an existing
  transition with both reference spellings absent and an exact tagged
  `(revision key present, revision value)` match. A present canonical or
  legacy reference, including null/empty/malformed data, is not absence. A
  selected path requires a transition reference with exact kind/id/revision;
  `ElementRef.revision` is schema-required. No new delta changes these guards.
  Source: `_clip_scalar_commands.py:120-164`; schema:
  `edit-command.schema.json:595-617,1716-1807`.
- The built-in descriptor remains the literal `cross-fade`; there is no
  Runtime alias normalization. Selected `elementRef.id` and transition
  `type` must match literally. Authored duration remains seconds in the raw
  transition; the frame product is used only for safe positive-frame and
  shortest-neighbor-fit checks. Main integer-frame input remains a caller
  mapping concern. Source: `_clip_scalar_commands.py:131-135,190-221`.
- Incoming adjacency and shortest-fit, owning-track, occurrence/map, and
  neighbor asset/media reads remain in the inherited b7 source. Existing raw
  transition keys are copied and merged, so unknown opaque fields survive.
  Source: `_clip_scalar_commands.py:165-234`.
- The final `1acc` delta closes the only new safety issue. At
  `_clip_scalar_commands.py:167-182`, incoming params absent preserves the
  existing raw presence/value; incoming literal null writes literal null when
  the prior value is absent, null, or an empty object; a non-empty object or
  other existing non-null value refuses atomically instead of silently
  retaining or discarding supplied intent. Object input still merges only
  supplied keys, including opaque keys. This preserves explicit-clear and
  changed-known-key validation boundaries.
- The candidate schema admits `params` as exactly object or null and retains
  the existing `clip.set` carrier, optional selected `elementRef`, exact
  `schema_source` pin shape, and paired `transition`/`elementRef` clear
  vocabulary. No DTO, endpoint, store, operation, or authority shape was
  added.

## Runtime carrier boundary

Runtime b92 stores accepted commands and `CommandRecord.command` as the
existing generic command/record carriers (`timeline_commit_store.py:128-179,
555-592`; bundle schema `CommandRecord` at `:3572-3637`). Those carriers can
retain the source command and inverse record shape without a new endpoint or
store field.

The currently published Runtime command schema is intentionally not the
transition source schema: `runtime_protocol/schemas/timeline-commit-bundle.json:659-707`
and `runtime_protocol/timeline_commit_types.py:118-129` admit only the
hold-shaped `clip.set` values, and the embedded `edit-command` resource is the
ordinary `6ba` schema. I did not override that schema, change the generated
DTO, or claim that `1acc` executes under it. A later normal Runtime schema
publication/qualification is required before activation; that is outside
this bounded source ACK.

## Evidence

Pure source/schema probe, run against the exact git object (no checkout or
product mutation):

```text
PYTHONDONTWRITEBYTECODE=1 python -B - <<'PY' ... Draft202012Validator ... git show 1acc... ... PY
```

Result: **passed** — four schema-valid carrier shapes were checked: selected
`cross-fade` with matching revision and `schema_source`, a legacy-shaped
literal-null transition, opaque object params, and paired
transition/reference clear. The probe also verified `params` object|null and
the paired-clear schema clauses. It does not authenticate a live legacy row.

Reused prior evidence without rerunning the passing Agent suites, as required:

- `agent-transition-main-presence-correction-1007-REPORT.md`: reported 178
  focused tests passed, 5 composed-schema tests passed, py_compile, JSON parse,
  Ruff, and `git diff --check` passed.
- `agent-review-transition-b7-raw-intent-no-normalize-1017-REPORT.md`:
  reported the focused transition-schema lane **5 passed**, the focused
  conformance selection **13 passed / 109 deselected**, Ruff, and
  `git diff --check` passed.

No Runtime pytest, full suite, HTTP/body, browser, renderer, live socket,
install, generation, pin, or native replay was run. No Runtime or product file
was changed; the Runtime worktree is clean.

## Decisions and next steps

I issued SOURCE ACK because the exact new delta is a conservative atomic
refusal/preservation correction and introduces no new source/schema mismatch.
The current Runtime hold-only schema is recorded as an activation boundary,
not silently treated as compatible. Agent1024 should compose the complete
source on approved6c, after which the normal Runtime schema/public artifact
review and App caller review can proceed. No complete-source freeze, public
allocation, qualification, or caller activation is claimed here.
