# Agent canonical-policy review file list

Candidate review scope for the scanner package. These are files in the
current Agent integration checkout at review time; the owner or manager must
reconfirm that the extracted Agent checkout matches the Runtime closure before
any owner-film run or publication.

| Path | Review purpose |
| --- | --- |
| `AGENTS.md` | Repository setup boundary and canonical documentation pointers. |
| `docs/getting-started.md` | Qualified Agent environment and installed/source boundary context. |
| `docs/setup/README.md` | Maintained setup path and explicit workspace/setup constraints. |
| `docs/setup/release-recipe.md` | Paired environment and artifact qualification requirements. |
| `docs/reference/timeline-offline-inspection.md` | Render-free, bounded inspection and pinned-closure policy. |
| `astrid/core/timeline/shot_composition_projection.py` | Canonical parent/shot/internal projection seam. |
| `astrid/core/timeline/clip_fields.py` | Declared clip-look field descriptions; no suffix/shape guessing. |
| `astrid/core/timeline/clip_fields.yaml` | Source declaration for public clip-look fields. |
| `astrid/core/timeline/audio_curves.py` | Public audio-curve registry and validation. |
| `astrid/core/timeline/audio_curves.json` | Source registry for supported audio curves. |
| `astrid/core/timeline/duration.py` | Existing half-open clip timing helpers. |
| `astrid/core/element/registry.py` | Registered element lookup and source availability. |
| `astrid/core/rendering/profile.py` | Existing render-profile FPS resolution fallback. |
| `astrid/sdk/timeline/capture.py` | Existing rational FPS parser. |

The package scanner imports only the existing Agent helper seams listed above
and emits bounded IDs, pins, properties, source paths, ranges and
known/unknown classifications. It does not change these files.
