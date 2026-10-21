# Agent current5c full-suite preflight

Date: 2026-10-21 UTC

## Result

**READY** for the manager to submit exactly one full suite. No full suite was
requested or run by this worker.

The suite is `full-c13-5c5173dc-integration`. It contains both `full` and
`integration`, so the central service includes the other repositories' current
integration heads in its cache key.

## Exact source identities

- Agent source: commit `5c5173dcb57669a9d43e5add2674543333f1c6d2`, tree
  `8626f868a3869b23baaca9814adb930e8952e4c7`, branch `tl/integration`.
- Runtime source: commit `9d1c43c647301da48a6e86ad82e466b501bd2418`, tree
  `50e74e3243c5da4cf77b6e6cc76605fae8aeb649`.
- Immutable Runtime checkout: `/home/user/work/wt/rt-pin-9d1c43c6`, detached
  at the exact Runtime commit above. It was created through
  `request-checkout`; the mutable `/home/user/work/runtime` checkout is not
  used by the suite.

## Installed environment

- Child Python profile: `/home/user/work/venv-agent-child-c13-5c5173dc`.
  The provisioning record says it was built from Agent `5c5173dc`, read-only,
  with 164 pins; `.astrid-source-commit` contains the full Agent SHA.
- Child lock/profile hash:
  `.provision-requirements.txt` SHA-256
  `25be6fc3e797ac8518f597037d34123c13b9a4171dc4b78f9605bfe3dd50437c`.
- Installed schema source is
  `/home/user/work/venv-agent-child-c13-5c5173dc/lib/python3.13/site-packages`;
  `banodoco-timeline-schema` imports from that path and is version `0.0.2`.
- Node executable: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`
  (`v20.19.4`); npm is `10.8.2`.
- Remotion project: `/home/user/work/runtimes/agent-remotion-0013`.
  Its package uses Remotion `4.0.509` and Composition `0.0.13`.
- `ASTRID_TEST_NODE_MODULES` is exactly
  `/home/user/work/runtimes/agent-remotion-0013/node_modules`; its installed
  `@banodoco/timeline-composition` is `0.0.13`.
- Current Agent public13 artifact SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Current Agent `remotion/package-lock.json` SHA-256:
  `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.
  The lock resolves `file:artifacts/banodoco-timeline-composition-0.0.13.tgz`
  with integrity
  `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`.
- VibeComfy fixture: `/home/user/work/fixtures/vibecomfy`, detached commit
  `31f90bb03d330283b76e7dbdda51197be787090d`.
- No old `a8a40afd` child, generated pin, health override, or Main014 profile
  is referenced by this suite. No Main014 adoption was made.

## Exact registered command

The central suite allow-list entry is:

```text
agent full-c13-5c5173dc-integration env -i HOME=/root LANG=C.UTF-8 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-9d1c43c6" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-5c5173dc/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9d1c43c6 ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-c13-5c5173dc/bin/python -m pytest -q -n 3
```

The command uses the current source snapshot supplied by the central test
service, the exact installed child profile, the immutable Runtime checkout,
the pinned Node 20 toolchain, public13 node modules, the installed schema path,
and the required VibeComfy fixture.

## Preflight evidence

The exact suite environment was probed without pytest. It successfully
imported `astrid.sdk.timeline` from the current Agent worktree,
`runtime_protocol.server`, `runtime_protocol.timeline_commit_provider`,
`astrid_runtime`, and `astrid_runtime.cli` from the immutable Runtime checkout,
and `banodoco_timeline_schema` from the child venv's installed site-packages.

The previous suite, `full-c13-a8a40afd-integration`, ran on the older Agent
tree `b614c4d7036ad8b93517969fc595e9f43c9f8ff4` with child venv
`venv-agent-child-c13-a8a40afd` and mutable Runtime `/home/user/work/runtime`.
It ended with 19 failed, 14,813 passed, 452 skipped, 4 xfailed, and 565
subtests passed. Its failures are classified in
`agent-full4555-classification.md`; this preflight does not rerun or
reclassify them.

No product source, test assertion, generated pin, health override, or Main014
source was changed. The only setup change is the new named suite entry above.

