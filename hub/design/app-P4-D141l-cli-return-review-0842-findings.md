# Findings

## SOURCE_QUALIFIED

The operational source-coordinate correction independently passes. The reviewer-local byte copy of the author checker and writable inputs differs only by the absolute author-worker-root relocation. Normalized diffs for checker logic/assertions, positive input, poison input, production input, and the copied control profile are empty.

The exact reviewer-local checker `prepare` and `check` both exited `0`. Git directly authenticated four clean detached stable pins with full commit, tree, and parent tuples:

- Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, tree `d362fe9d`, parents `ecdc242e`, `432f9dcb`, `00ec0f2f`.
- Runtime `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d6`, parents `95d98f03`, `857e4c3b`, `012889c1`.
- App `82e9e13ddf1d7ec6c736521b2eb091dca9877598`, tree `6a6e49eb`, parents `82e9e13d`, `4de54db1`, `4937203f`.
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a`, parents `635f4de0`, `7a95a40b`, `c05fdb17`.

All four are clean and detached. The target selector, launcher, installer, restricted environment, `run -- -m pytest`, integration marker, timeout, cache setting, JUnit path, and existing test predicates remain unchanged. The source-only checker did not run pytest or collection.

## CONTROLS

Through the unchanged production launcher in `run` mode, the harmless positive stub returned exit `17` with exactly one call. The Agent-SHA-only poison returned nonzero (exit `1`) with zero calls and the expected SHA mismatch. The reviewer packet preserves the author packet; the author selected evidence/input/control-profile hash set is unchanged after replay.

Static AST, Bash syntax, and `git diff --check` checks passed. Product typecheck/lint are N/A because this review changed no product source, tests, pins, profiles, or generated files.

## PRODUCTION_INPUT_MISSING

The App venue’s supported `.astrid-registry-state.json` and historical profile are absent. Consequently the production body-evidence directory, future runmanifest, and body JUnit XML are prospective receiving inputs. This remains an ordinary receiving gap, not Agent-host absence and not an authorization refusal. No profile was created, no registry or CAS was changed, and no service request or row install was made.

No behavioral P4 GO, REG0, build, ZIP, or body credit is claimed. The old `8585ed9c` App pointer remains D141v metadata only. D130 remains held; 8912 is refused/stopped; 19479 remains held/unstarted; raw KEEP is retained. Future production runmanifest/body XML are not pre-body proof requirements.

## TRACE GAP

The reviewer trace began before the local replay, sampled at 5-second intervals, stayed above the 4,000,000,000-byte stop threshold, and was explicitly SIGTERM-stopped, waited, and reaped. It contains two samples over this short source-only review. This is honest lifecycle evidence, not a claim of continuous full-time 4GB coverage for the future heavy Agent run. The author trace’s 08:40:01Z start and one sample are likewise not upgraded into continuous coverage.
