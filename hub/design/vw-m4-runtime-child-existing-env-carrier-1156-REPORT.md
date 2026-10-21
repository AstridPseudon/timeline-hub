# Unapplied child-runtime env carrier successor 1156

## Result

Prepared the unapplied successor packet:

- Patch: `vw-m4-runtime-child-existing-env-carrier-1156.patch`
- Source-only fixture: `vw-m4-runtime-child-existing-env-carrier-1156-source-fixture.mjs`
- Commands: `vw-m4-runtime-child-existing-env-carrier-1156-COMMANDS.txt`
- File list: `vw-m4-runtime-child-existing-env-carrier-1156-FILES.txt`

The Composition worktree is based on `tl/integration` at
`df7b86308902fae90eda1dc3080d17d8fc30ea78` and remains product-clean. The
patch is not applied to the ORCH toolkit or any product repository.

## Change carried by the patch

The patch updates only the unapplied `bin/make-runtime` and
`bin/make-child-venv` kit scripts.

`make-runtime` now refuses before `$D.partial`, archive, or `npm ci` allocation
when either authoritative legacy prerequisite is absent:

- `$ORCH/tests/agent-remotion-0012.env`
- the `agent remotion-0012-nodes` row in `$ORCH/tests/suites.conf`

The refusal lists every missing prerequisite. It also rejects an env template
with a missing/duplicate, foreign, or broken `ASTRID_REMOTION_PROJECT_DIR`.
The generated new-runtime env and suite replace the selected runtime root with
`$D/remotion`, while preserving the nested `$D/remotion` project and sibling
`$D/astrid` source layout from 1144. Existing runtime/env/suite entries are
not edited.

`make-child-venv` now refuses before Python venv allocation/install when its
selected generated env or base suite row is absent. It reads the existing
`tests/$RT.env` `ASTRID_REMOTION_PROJECT_DIR` value and carries that exact
value into the child suite; it does not reconstruct a project path from `RT`
or retry another root. Both established values are accepted:

- old flat: `/home/user/work/runtimes/$RT`
- new nested: `/home/user/work/runtimes/$RT/remotion`

The child path, Agent SHA/source archive, lock, immutable venv destination,
and generated suite remain under the existing custody contract. No CLI,
DTO/store/authority, source factory, alternate-root detection, or old-runtime
copy was added.

## Fixture evidence

The fixture creates one task-owned temporary root, records it, and removes that
exact root in `finally`. It proves:

- an old flat env value selects the flat project and its in-project Remotion CLI;
- a new nested env value selects `$D/remotion` and its in-project CLI;
- missing env, foreign env, broken relative env, and a suite without the
  required env carrier refuse.

The fixture does not require a runtime, package install, source copy, browser,
server, socket, or test service.

## Prerequisite status / HOLD

The current machine still lacks the authoritative legacy env template and
`agent remotion-0012-nodes` suite row. This is not repaired by inventing a
baseline. The lead/main kit owner must restore or deliberately re-establish
those exact inputs, record their bytes, and independently review any changed
contract before application. The proposal remains **HOLD** until that review
and the real prerequisites are satisfied.

Before application, the lead also needs the existing Agent commit and exact
lock SHA, Node 20.19.4 toolchain, Python 3.13/pinned child requirements,
network access for the normal `npm ci`/PyPI steps, writable new runtime and
ORCH output destinations, and enough storage. No installation was attempted
here.

## Checks

Passed:

- `node --check` on the source-only fixture.
- Fixture execution: flat, nested, and all refusal cases passed.
- Patch dry-run and apply in a private task-owned copy of the two kit scripts.
- `bash -n` on both patched scripts.
- Patched-script refusal probes: both missing-baseline calls exited 2 and
  listed the absent env and suite row before allocation/install.
- `git diff --check`; Composition worktree status is clean.

Not run by instruction: test service, package install/`npm ci`, venv creation,
runtime build, source/graph copy, browser/helper, Runtime/server/socket,
render, full, or physical proof. The prior 1149 nested source-layout evidence
remains unchanged and is not re-claimed as new execution here.
