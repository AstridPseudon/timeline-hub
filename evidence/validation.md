# Validation

Read-only validation only, as required by D141 P4.

## Commands and results

- `git -C /home/user/peteromallet/astrid-agent rev-parse 28e56cac...` and `^{tree}`: Agent `28e56cac...`, tree `2ebe2ddf...`.
- Equivalent `git rev-parse` checks for Runtime, App, and Composition: Runtime `6a011d58...`/`ac5b8627...`; actual App pin `867cb273...`/`2b44a46c...`; Composition `635f4de0...`/`5ab5191a...`.
- `git diff --name-status 867cb273... 5fe3e4de...`: exactly five modified App files, listed in `source-map.json`.
- `git -C /home/user/banodoco/reigh-app rev-parse tl/app-P2-D141-materialization-expectation-0225`: exactly `5fe3e4de...`; tree exactly `af51793b...`.
- Git blob reads (`git show`, `git rev-parse <commit>:<path>`) and SHA-256 hashing of all five candidate App blobs: all match `review.json`.
- Git blob reads and numbered line inspection of launcher, three selectors, ingress fixture, Runtime helper, Runtime server/service/execution, and changed App files: results recorded in `source-map.json`.
- `test -f` for the recorded XML and stale alternate XML: both absent in this sandbox.

## Explicitly not run

`pytest`, Vitest, npm tests, imports, tsc, lint, browser journeys, localhost/live sockets, the P4 launcher, Runtime execution, body parsing, and kit/registry checks: **NOT APPLICABLE / prohibited for this read-only path review**.

No source, test, registry, queue, body, or kit files were edited.
