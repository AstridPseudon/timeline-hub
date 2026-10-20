Implemented WC5 repair.

- Restored all original 22 voiceover tests/fixtures exactly.
- Preserved legacy `TargetBound.publish` for ripple, regeneration, and unqualified native cases.
- Native activation now requires real managed output selection/producer authority; normal speech output fails closed without fabrication.
- Added separate regression tests.

Evidence:

- Voiceover tests: **26 passed**
- Adjacent SDK tests: **26 passed**
- `git diff --check`: passed
- No full suite run.
- Native activation remains held pending Runtime carrier qualification.

Report, commit message, and `DONE` were written under the assigned worker directory.