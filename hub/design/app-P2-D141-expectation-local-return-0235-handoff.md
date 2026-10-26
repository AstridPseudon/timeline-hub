# D141d handoff

The rejected shared `assertNativeHistoryEntry` candidate was repaired. The shared helper and all non-placement gestures are restored to the 5fe baseline. The automatic-placement Undo expectation now has a callback-local exact composition for the D124 materialization family: two bindings, 22 approved structural paths, canonical source/successor derivation, and no fallback if the family is absent.

Static validation is green: App and node TypeScript, scoped ESLint, and `git diff --check`. Collection listed the three tests and exited 1 on the repository guard without running bodies. Browser/full acceptance remains unverified and is for the later central service.

The manager may review and merge this one-file change. No upstream ledger row or new ledger is requested.
