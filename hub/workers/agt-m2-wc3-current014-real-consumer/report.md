Implemented WC3 native media replacement on current014.

- Composed donor `76c6c591` onto current014 `e86f44d0`.
- Added exact five-field pin guards; malformed/unrelated pending swaps refuse without POST or outbox changes.
- Preserved native session/outbox/history behavior and added exact replay receipt assertions.
- Updated real-provider parent-media conformance coverage.

Tests:

- Targeted replacement/replay: 22 passed.
- Native/conformance suite: 154 passed.
- a0 Runtime integration: 22 passed.
- Ruff and `git diff --check`: passed.
- Central named suite stopped during collection due missing `vibecomfy` imports; no full suite requested.

Handoff, commit message, and `DONE` marker written.