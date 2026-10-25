# GO — P2 single5678

Verified the genuine portable packet for request `rt-P2-native-reply-resume-0217-p2-native-reply-resume-0217-single-1025022644-5678`.

Recorded tuple:

- App `24865fa212148e9bc149a1285936372656037e55`, tree `741333cebfb2b6505a080507bb6c9789df494d43`
- Agent `6386c700ee56264aebe12da4558ac74dda0d60ca`, tree `4f157f4445968ca625017a7e20bd7ca317fa0d5d`
- Runtime `6634a17f3ffd885567ba3c91b6c7a560df7375a4`, tree `47b376717ce7a919a697c62133de3e74dc9f6d3a`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`

Evidence checks:

- Reconstructed packet files in private `/tmp`; declared SHA-256 list matched exactly.
- Service/preflight manifests agree on heads, trees, clean detached checkouts, versions, imports, command, and test membership.
- Original XML: `43e81d9b…b3869b`; readiness XML: `273b9b26…a6018`.
- Original: 1 pass, 0 failures/skips/errors.
- Readiness: 1 pass, 0 failures/skips/errors.
- Source hashes and Git blobs matched; profile hashes matched origin commit `5671cd8dbef709fb9068d6db11eef28313b4b102`.
- Pinned source test asserts exact v2 clear request, canonical/field delta, history, reload, guarded Undo, and zero legacy traffic.

Commands/results included packet hash comparison, four-checkout `git rev-parse HEAD`/tree checks, protected-source hash checks, and manifest predicate checks; all passed. No functional/browser/service tests were rerun per brief.

The private central raw log and attachment bodies remain intentionally unexported; under D66, the ordinary run manifest plus exact XML/source identity is sufficient. No product or test files changed. `DONE` and the required commit message were created.