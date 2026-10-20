Implemented the approved seven-file managed-audio port.

- Preserved five-field `MediaSelection` and existing media command carriers.
- Added verified `audio/*` admission and bounded duration handling.
- Added real PCM WAV CAS lifecycle coverage through reload, retry, inverse, and redo.
- Identified the existing child-scope gap: `draft_voiceover.py` directly mutates internal timelines instead of capturing `track.create` + `occurrence.add-media`; no new writer/proposal layer or `bound.publish` deletion was added.
- Wrote [REPORT.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-managed-audio-current014-source/REPORT.md), commit messages, shared handoff, and DONE marker.

Tests:

- 275 passed, 48 deselected targeted conformance tests.
- Real managed WAV: 1 passed, 36 deselected.
- Voiceover tests: 22 passed.
- Ruff and `git diff --check`: passed.

No full suite run.