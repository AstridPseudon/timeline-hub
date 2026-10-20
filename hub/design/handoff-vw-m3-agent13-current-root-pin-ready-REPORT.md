# Agent public13 current-root normal-pin prep

## Decision

Prepared and verified a held Agent public13 normal pin on the current
`tl/integration` root (`2f8b9cc53648a392da8684016c6ee15e589ea060`). This is
branch preparation only. App-FIRST qualification remains a prerequisite; no
adoption or integration request was made.

## Scoped changes

Only the normal-pin seam was changed:

- `astrid/core/rendering/remotion_runtime.py`: required Composition package
  version `0.0.12` -> `0.0.13`;
- `remotion/package.json` and `remotion/package-lock.json`: local artifact path,
  package version, and exact lock integrity;
- immutable public13 artifact and bare SHA sidecar;
- direct current-pin tests for package identity, 77-member safety, public
  evaluation admission/four forged-source refusals, capture hash admission, and
  readiness fixture version.

No Runtime client/schema/artifact tuple changes, source/render service/SDK/core
changes, policy/default/theme changes, Node/toolchain changes, install, npm ci,
network, registry publication, or shared dependency/cache writes.

## Exact release identity

- package: `@banodoco/timeline-composition@0.0.13`
- artifact: `58477` bytes, `77` regular members
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- lock SRI: `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`
- public12 SHA-256 retained: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`
- public11 SHA-256 retained in the handoff archive: `dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601`

The public13 artifact compares byte-for-byte with prior reviewed Agent13
commit `5ef483ce14f76fec18e3d8fe2543421de06dca6f` and the orchestrator
handoff artifact. Its sorted archive member list matches the supplied 77-file
manifest. Public12 bytes compare unchanged with the current root.

## Tests and checks

All commands were run from the worker worktree with the verified Node binary
first in `PATH`:

```text
PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep:$PATH
ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python3 -B -m pytest -q tests/packs/rendering/test_composition_package.py -m 'not integration'
# 6 passed, 1 deselected

PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python3 -B -m pytest -q tests/core/timeline/test_clip_fields.py::test_render_status_defaults_to_pinned_union_composition tests/journeys/test_journey_plumbing.py::test_renderer_install_problem_names_the_missing_install_and_the_fix
# 2 passed

node --test <private extracted public13 scope>/remotion/tests/normal-audio-sources.test.mjs
# 5 passed, 0 failed; Node v20.19.4, private scope only

git diff --check
# passed
```

The direct audio test used only a private temporary extracted package scope;
it did not install or modify shared `node_modules`. No full, browser, socket,
renderer, npm install, or network suite was run.

## Hold / next step

Keep this branch held until the App owner lands and qualifies the exact public13
consumer source. Then the owner may provision an isolated Agent13 leaf, repeat
the byte/lock/member/readiness checks, and decide adoption. This report does
not claim App consumer qualification or physical frame parity.
