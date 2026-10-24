Updated only the five allowed evidence artifacts: exactly nine closures, yielding **211 closed / 56 open / 267 total**, with **69 mappings**. Active owner and family counts independently sum to 56.

The other 258 nodes, prior proof records, 60 mapping rows, historical counts, and D40 installed `ba8f/f320` limits remain preserved.

Census SHA-256:
`6422ec5cd2f310a118b8d9e88f6ac3fe3cbb55d916655c7921e933c91235d07c`

Validation passed:

- `python3 /tmp/w-55f691c167/validate-sdk9.py` — exact delta, counts, phases, preservation, CSV/JSON agreement, and 14 retained report/log hashes.
- `sha256sum -c agent-D32-current-node-reconciliation-H30-corrected.sha256` — OK.
- `git diff --check` — clean.
- Retained AST-prefix comparison against independent 0603 output — all nine match.

Used corrected 0619 membership: both schema cases and all 24 unqualified SDK selectors remain excluded. Recorded AST prefixes explicitly; no unavailable full hashes invented. Historical helper packet hashes remain reported evidence because its temporary packet is unavailable.

No behavior/full/browser/gate reruns or broader v2 acceptance credit. No blockers. `commit-msg` and `DONE` written; ready for independent package review and harness commit.