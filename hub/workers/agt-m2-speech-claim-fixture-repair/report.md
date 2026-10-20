Implemented and validated the WC5 speech fixture repair.

- Fixed SDK speech capability metadata to declare primary `audio`.
- Added fixture `manifest.json` result receipt and bounded diagnostics/waiting.
- Updated audio output selection compatibility.
- Preserved all required assertions and test-double authoring boundary.

Tests:

- Local targeted suite: `58 passed`
- Central `native014-sockets-integration`: `2 passed in 36.34s`
- Tree: `83f16e907286f0a33b92a15a9df42277b4188264`

No Runtime/API/schema/generator/pin changes. No full/D13/WC5 retirement claim. `commit-msg` and `DONE` were created.