# Agent private392 native/Door pair qualification

Status: **PASS for the bounded qualification only.** This report does not
claim public release, integration adoption, or broad private matrix coverage.

## Exact source and tuple

- Agent committed source: `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`
- Agent source tree: `2f2685d85c3f65b458795100a8045371eb19ee06`
- Central snapshot test tree (uncommitted worker edits captured by the test
  service): `56032756ed07b4424b912c1b3ea06b90fb51c1f6`
- Runtime producer: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`
- Runtime producer tree: `8be43e13acb436120f8a63b1a178d64c49422461`
- Runtime package: `0.2.13`; identity `astrid-runtime`; protocol `workspace.v1`
- Runtime health/schema digest:
  `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`
- Raw timeline commit bundle:
  `sha256:fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`
- Producer artifact manifest:
  `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`
- Agent schema: `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
  (`56` definitions, `30` operations, schema v2).

The exact imported module identity was checked before the live Door writes:

- Agent client: `/home/user/work/wt/.test-agt-m2-private392-matched-native-door-pair-private392-native-door-integration-1020210828-10824/astrid_runtime_client/__init__.py`, SHA-256 `7cbab37a442875664633520ac337823d19d8371ee3607e3213747b435e4677c5`.
- Runtime protocol: `/tmp/astrid-runtime-archive-sh5wyi44/runtime_protocol/__init__.py`, SHA-256 `ab861f37552e1a27a706ffc1499a720ef8274248be3e4cb7e18dcbc8526261b1`.

The test also compared the imported Runtime protocol bytes to the exact
`rt-pin-f8da4b6d` checkout and checked the authenticated health response.

## New behavior: one native/Door case

Added `tests/editing_conformance/test_commit_runtime_private392_native_door.py`.
It uses the real startup factory, authenticated Door, exact captured source
inputs, and the immutable `agent-remotion-0013` fixture. The single test
covered:

1. `project-data.write` commit and direct readback for target
   `com.example.private392`, key
   `__dsl__:dsl://com.example.private392/main.json`, including an opaque
   `__proto__` value.
2. `timeline.inverse` and inverse-of-inverse readback.
3. An original same-leaf stale request refusing with no history change
   (zero-write guard).
4. An original-head disjoint source-map write rebasing successfully while
   preserving the opaque source value and adding the source-map value.

## Existing representative control

The named suite reused exactly one existing shared-occurrence control:
`tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_occurrence_retry_own_move_and_historical_restore`.
It covers the existing shared-occurrence v2 allocation/own-slot path,
readback after Runtime restart, simulated lost acknowledgement, exact retry
without provider/projection persistence, own subsequent move, historical
restore, and rematerialization. It passed as one test; no new lifecycle matrix
or old44 replay was added.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_project_data.py` — **17 passed**.
- Central named suite `private392-native-door-integration`, with explicit
  `--files "tests/editing_conformance/test_commit_runtime_private392_native_door.py tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_occurrence_retry_own_move_and_historical_restore"` — **2 passed in 5.32s**.

The local live-socket attempt was not used as qualification because the
sandbox rejected socket creation with `PermissionError`; the central test
service supplied the live evidence above. No full suite, public release,
integration adoption, future-group/audio/provenance/transition/opacity work,
SQL setup, fabricated history, or authority override was used.

## Limits

This is one new project-data Door behavior and one existing representative
carrier lifecycle control. It does not establish the excluded broad matrices,
full-suite status, or any product behavior outside the listed keys and
fixture.
