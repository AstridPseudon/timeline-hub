# Agent private392 pin review

Decision: **APPROVE**.

This is an independent PRIVATE pin/reload review only. It is not an
integration, public-release, adoption, activation, or native-pair claim.

## Exact candidate

- Agent commit: `1303ce6be32e7bd96ed5c6b35afcb15819e81b50`
- Agent tree: `2f2685d85c3f65b458795100a8045371eb19ee06`
- Frozen Agent base: `e010e6a3868e963471244491bb6672c3e4a5135e`
- Frozen Agent base tree: `70414cf6875d2c97c45f33e0a5158c80bd7391d9`
- Runtime producer commit: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`
- Runtime producer tree: `8be43e13acb436120f8a63b1a178d64c49422461`

The candidate has six changed paths from the frozen base: the Runtime lock,
four generated Python client files, and `astrid/sdk/remote.py`. The source
hunk is byte-identical to approved `909bfad8`.

## Identity and byte review

- The Runtime manifest contains 75 artifacts; all 75 exist at `f8da4b6d` and
  match their declared hashes.
- All 15 locked consumer paths match both the lock hashes and the exact
  producer bytes at `f8da4b6d`.
- Runtime identity is `astrid-runtime`, protocol `workspace.v1`, package
  `0.2.13`, health/schema digest
  `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`,
  raw bundle digest
  `sha256:fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`,
  and artifact version
  `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`.
- The Agent command schema is unchanged from `e010`: 56 definitions, 30
  operations, schema digest
  `sha256:39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`.
- No `e63` incomplete source, old `952` source commit, or `0.2.14` package
  identity appears in the candidate pin files.

## Source/reload review

The sole extra source change is the approved `_source_closure` conversion:
Runtime read envelopes are projected through the existing canonical image
field sets before `open_authoring_bundle`, while raw GET rows remain available
to callers. It preserves payload/authored fields, revision pins, identity,
collection order, and the existing schema. It adds no DTO, authority,
normalization, or current/future feature semantics. This retains the actual
`909bfad8` reload fix and does not alter the accepted-history or materialization
authority paths.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q tests/test_vendor_lock.py tests/stage1/test_vendored_workspace_client_parity_luna.py tests/sdk/test_timeline_materialization_schema_union.py` — **47 passed**.
- Pinned-client import identity check for package `0.2.13`, health digest,
  and `ProjectDataWriteArgs` — PASS.
- `git diff --check` — PASS.
- Reused the unchanged pin worker proof: **98 passed, 9 deselected**;
  no broad matrix, full suite, localhost rerun, or native pair was run for
  this review.

The next step remains the manager’s separately bounded new project-data/carrier
lifecycle Door case; this review makes no claim about that case.
