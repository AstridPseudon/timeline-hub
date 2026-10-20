Implemented the reviewed Composition 0.0.13 adoption onto current `c73b1ab1`.

- Added exact 58,477-byte/77-member archive with SHA-256 `9412ae25…d54738`.
- Updated package, lockfile, runtime pin, and focused admission tests.
- Preserved 0.0.12 compatibility artifacts and current behavior.
- Central journey tests: 85 passed, 2 deselected.
- Capture/static Node tests: 20 passed.
- `git diff --check`: passed.
- No full suite or physical PCM/frame-parity claim made.

Local socket tests were sandbox-blocked, but passed via the central service. Report and commit message are written; `DONE` created.