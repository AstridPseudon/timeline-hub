# Portable owner-film clip-look scanner

Version: `1.0.2`

This delivery contains `owner_film_cliplook_scan.py`, a credential-free,
read-only scanner for one exact Runtime canonical-document JSON closure. The
tool adds no package-install step, but it is not a fresh-Python standalone
program: it imports the Agent projectors, registry and timeline policy from a
normal qualified Agent Python environment and a matching extracted Agent
checkout. It reports the three hard-stop review categories:

- `curve_honoured`
- `element_clip_look_overlap`
- `continuous_audio_fade`

The scanner reports only bounded IDs and pins, named properties and source
paths, existing half-open frame ranges, compile availability, and
`known`/`unknown` classifications. It never claims an owner-film result is
clean: `clean_claim` is always `false`. Missing or incomplete closure data is
`status: incomplete`. Unsupported or unresolvable metadata is `unknown`.
Malformed required scope and emitted-reference containers are omitted from
reports and produce bounded type errors; valid string IDs and pins are kept
exactly as supplied. Optional authored null/clear values are left to the
Agent projector and are not rejected merely because their field resembles a
reference.

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
known/unknown metadata, relocated CLI execution, incomplete closures, and
same-path/symlink/hardlink input protection.
