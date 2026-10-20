# Portable owner-film clip-look scanner

Version: `1.0.8` (HELD pending independent and Agent canonical-policy review)

This delivery contains `owner_film_cliplook_scan.py`, a credential-free,
read-only scanner for one exact Runtime canonical-document JSON closure. The
tool adds no package-install step, but it is not a fresh-Python standalone
program: it imports the Agent projectors, registry and timeline policy from a
normal qualified Agent Python environment and a matching extracted Agent
checkout. It reports the three hard-stop review categories:

- `curve_honoured`
- `element_clip_look_overlap`
- `continuous_audio_fade`

The result also includes bounded `media_look_inventory` entries for media
entrance/exit declarations and `transition_boundaries` entries for canonical
incoming transition declarations. `transition_conversion`,
`media_clip_look_overlap`, and renderer presence/alpha/pixel coverage are
explicitly listed in `not_covered`; an empty inventory is not evidence that
those semantics are absent.

The scanner reports only bounded IDs and pins, named properties and source
paths, existing half-open frame ranges, compile availability, and
`known`/`unknown` classifications. It never claims an owner-film result is
clean: `clean_claim` is always `false`. Missing or incomplete closure data is
`status: incomplete`. Unsupported or unresolvable metadata is `unknown`.
Malformed required scope and emitted-reference containers are omitted from
reports and produce bounded type errors; valid string IDs and pins are kept
exactly as supplied. Optional authored null/clear values are left to the
Agent projector and are not rejected merely because their field resembles a
reference. There is no whole-document reference validator. Asset IDs appear in
`projected.registry.assets[...]` source paths; authored transition IDs and
types are free-form strings included unchanged in the inventory. Audio fade
and curve paths point into the input parent or internal revision, while
track and asset context paths start with `projected.`. Unreadable transition
declarations make the scan incomplete with bounded errors. Duplicate internal
revision IDs are incomplete through the Agent projector; the source-path
helper also refuses an ambiguous list index rather than selecting a row. An
invalid declared stored look or audio-fade value makes the scan incomplete,
reports only the bounded authored source path, and retains affected
inventory/findings as `unknown`; exception text and authored values are never
copied into output. Each declared `FieldSpec.stored_at` and `stored_at_audio`
path is checked before projection, using the Agent's per-field Draft-07 schema
and strict `FieldSpec.to_stored` codec. Shared visual fade aliases use the
general entrance/exit animation spec, preserving non-fade animations and open
animation params. This checks stored types as well as codec values without
normalizing or rewriting the input. It uses the one Agent projector and no
whole-document validator or copied field bounds/catalogs.

Null/missing declarations remain explicit clears. Audio curve values use the
Agent curve registry; an unknown string curve remains `unknown` under the
existing scanner policy, while a non-string curve makes the scan incomplete.
A non-object audio `params` container produces a bounded error at `.params`
and unknown fade observations pointing to that openable container. If malformed
speed prevents a frame range, the unknown single-clip finding retains an empty
`interval_frames` list; no overlap range is invented. If the Agent projector
refuses the closure, findings remain empty with `status: incomplete`.

## Owner run

Before running, use the existing Agent setup documentation in the extracted
checkout: `docs/setup/README.md` and its maintained
`docs/setup/release-recipe.md`. Supply the already-qualified Python
interpreter/environment from that normal setup and an extracted Agent
checkout matching the Runtime canonical closure. This delivery does not
create Python, install Agent dependencies, or claim that a bare fresh Python
environment is sufficient. The owner keeps the film and canonical closure
local; do not upload either to this delivery or to the orchestration
workspace. The candidate was exercised on Linux; no macOS claim is made.

From the extracted delivery directory, with an immutable copy of the exact
canonical closure and an extracted Agent checkout:

```sh
OWNER_AGENT_PYTHON=/path/to/qualified/Agentenv/bin/python
AGENT_ROOT=/path/to/extracted/astrid-agent
OWNER_FILM_INPUT=/path/to/owner-provided/canonical_document.json
OWNER_SCAN_OUTPUT=/path/to/local/owner-film-cliplook-scan.json
PYTHONPATH="$AGENT_ROOT" "$OWNER_AGENT_PYTHON" -B owner_film_cliplook_scan.py \
  --agent-root "$AGENT_ROOT" \
  --input "$OWNER_FILM_INPUT" \
  --json-out "$OWNER_SCAN_OUTPUT"
```

`--input` must be a regular JSON file containing the Runtime canonical
closure: `parent_revision.payload`, pinned `shot_revisions`, pinned
`internal_timeline_revisions`, and `dependency_manifest`. The input is never
written or mutated. `--json-out` is optional; the bounded report is also
printed to stdout. The output is rejected before writing if it is the input,
a symlink, or a hardlink to the input.

The closure must be a read-only duplicate, not credentials, a database/table
dump, media, or a production upload. Review `status`, `closure_errors`, and
every `unknown` finding before drawing conclusions. No owner film data is
included in this candidate, and the absence of owner input does not block
delivery preparation: without the exact closure the scanner must remain
`incomplete` with `clean_claim: false`. This is scan preparation for the
owner hard stop, not a production approval or a replacement for the Agent
canonical-policy review.

## Synthetic checks

Run from any directory with the same qualified interpreter; `--agent-root` is
explicit and no orchestration environment variable or search root is used:

```sh
"$OWNER_AGENT_PYTHON" -m pytest -q \
  /path/to/delivery/tests/test_owner_film_cliplook_scan.py \
  --agent-root "$AGENT_ROOT"
```

The tests use synthetic data only. They cover rational FPS, opaque-field
redaction, occurrence/shot/internal revision pins, all three categories,
single-element and cross-track overlap, crop/speed look inventory, media
entrance/exit, incoming transition inventory, malformed/unreadable transitions,
duplicate revision refusal, malformed stored number/animation/audio-fade/curve
shapes with unknown inventory, numeric booleans, both audio directions at parent,
config and occurrence-child paths, malformed audio params, authored values before
placement overrides, one projector call, explicit optional clears and unknown
extension preservation,
malformed scope/caption sentinels, known/unknown
metadata, relocated CLI execution, incomplete closures, and
same-path/symlink/hardlink input protection.

This is unpublished and held pending manager review and Agent canonical-policy
review. It has not been run against owner-film data.
