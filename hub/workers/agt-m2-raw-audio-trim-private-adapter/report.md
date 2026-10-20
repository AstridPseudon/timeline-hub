Implemented Agent’s private raw-audio trim adapter.

- Added exact base media-pin discovery and request-scoped `media_info` consumption.
- Preserved existing trim timing, hold/speed, dependency, inverse, and zero-write semantics.
- Added nonauthoritative WAV-header authoring preflight.
- Added focused tests and documentation: [agent-raw-audio-trim-private-adapter.md](/home/user/work/wt/agt-m2-raw-audio-trim-private-adapter/docs/agent-raw-audio-trim-private-adapter.md).

Tests:

- `test_recipe_m2_clip_trim.py`: 121 passed
- CLI/provider lanes: 126 passed
- Compile check and `git diff --check`: passed

Runtime counterpart is not committed, so end-to-end pairing remains intentionally unverified. `DONE`, report, and commit-message artifacts were created.