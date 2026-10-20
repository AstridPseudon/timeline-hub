# Owner-film differences scanner extension

## Result

Prepared an ORCH-only readonly extension of the predecessor
`owner_film_cliplook_scan.py`. It reports the three approved hard-stop
categories:

- `curve_honoured`
- `element_clip_look_overlap`
- `continuous_audio_fade`

No owner-film canonical closure was supplied or found. The current result is
therefore **incomplete / unverified**, with `clean_claim: false`; it is not a
no-differences or no-overlap claim. The predecessor report and predecessor
JSON were not edited.

## Files

- `owner_film_differences_scan.py` — new ORCH scanner.
- `test_owner_film_differences_scan.py` — synthetic direct smokes only.
- `owner-film-differences-scan.json` — current bounded-search output from this
  extension; it contains no owner-film data.

The scanner imports and reuses only the predecessor's loader/search helpers
plus the current Agent's existing canonical parent projector, clip-field
codec/public fade-curve registry, element registry, rational-FPS resolver,
and half-open clip timing helpers. It performs no product writes, database or
credential search, media access, render, network, socket, browser, install,
package-pin, or source-provider operation.

Audio-fade findings are known only when the projected compiled track has an
audio role and the registered asset has an audio type. Missing or invalid
role/asset/track metadata is emitted as `unknown`. Curves use the exact
`clip_fields.describe` and `params.fadeInCurve` / `params.fadeOutCurve`
contract; no clip-name, suffix, or shape heuristic is used. Element overlap
uses existing registered-element metadata and existing projected half-open
intervals; it adds no clock or timing implementation.

The public finding payload is limited to project/timeline/revision IDs,
clip/occurrence/shot/internal-revision pins, source kind/path, named
properties/source paths, existing half-open frame ranges, semantic category,
known/unknown, and compile availability. It does not emit scripts, captions,
raw payloads, or look values.

## Current bounded search

Command:

```sh
PYTHONPATH=/home/user/work/wt/vw-m3-owner-film-differences-scan-prep \
/home/user/work/venv-agent/bin/python -B \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/\
scratchpad/orch/workers/vw-m3-owner-film-differences-scan-prep/owner_film_differences_scan.py \
  --search \
  --json-out /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/\
scratchpad/orch/workers/vw-m3-owner-film-differences-scan-prep/owner-film-differences-scan.json
```

Result: zero matching canonical-document paths in the predecessor's named
roots; `status: incomplete`, `owner_film_present: false`, and
`clean_claim: false`. The search excluded credentials, `.aws`, `.git`,
`node_modules`, tests, fixtures, examples, databases, and arbitrary user
directories.

## Exact command when the orchestrator supplies one duplicate

Run once, after the orchestrator provides the exact readonly Runtime
canonical-document duplicate:

```sh
PYTHONPATH=/home/user/work/wt/vw-m3-owner-film-differences-scan-prep \
/home/user/work/venv-agent/bin/python -B \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/\
scratchpad/orch/workers/vw-m3-owner-film-differences-scan-prep/owner_film_differences_scan.py \
  --input /OWNER-PROVIDED/canonical_document.json \
  --json-out /tmp/owner-film-differences-scan.json
```

The required input is one immutable canonical closure with
`parent_revision.payload`, pinned `shot_revisions`, pinned
`internal_timeline_revisions`, and `dependency_manifest`. A missing or
unprojectable closure remains `incomplete` and `clean_claim: false`.

## Tests and checks

- `PYTHONPATH=/home/user/work/wt/vw-m3-owner-film-differences-scan-prep /home/user/work/venv-agent/bin/python -m pytest -q /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-owner-film-differences-scan-prep/test_owner_film_differences_scan.py` — **8 passed**.
- `/home/user/work/venv-agent/bin/ruff check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-owner-film-differences-scan-prep/owner_film_differences_scan.py /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-owner-film-differences-scan-prep/test_owner_film_differences_scan.py` — **passed**.
- `python3 -B -m py_compile owner_film_differences_scan.py test_owner_film_differences_scan.py` — **passed**.
- `git diff --check` in the Agent worktree — **passed; no product/repo files changed**.
- Full/browser/network/live-socket/service tests — **not run** by design.

Synthetic cases are explicitly non-owner evidence. They cover all three
categories, rational FPS, occurrence pins, known/default/invalid curves,
unresolvable audio metadata, registered versus unknown elements, same-track
scope, cross-track exclusion, output redaction, and closure failures.

## Review / next step

Agent canonical-policy review remains the appropriate next review: confirm
the supplied duplicate is the exact readonly Runtime closure before any real
owner-film run. No product integration or shared single-list edit is included.
