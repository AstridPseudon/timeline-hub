# Runtime ordinary014 a020 final candidate

## Result

Forwarded the exact test-only delta from `5988a3b38293a82175052e84a2717ae5578b61dd`
onto committed candidate `616d2111f35937f311330ffebc8610d21bf80f74`.
No product, schema, generator, artifact, release, pin, or adoption changes were
made. The only worktree change is the appended test in
`tests/test_timeline_clip_replacement.py`.

## Identity

- Committed candidate SHA: `616d2111f35937f311330ffebc8610d21bf80f74`
- Committed candidate tree: `8e7b22f073b4ff3f21e684af9cf853b07672ea2a`
- Current-base SHA: `a020a1c77a07aa657efb60b0442450209e55e470`
- Current-base tree: `9243cb9227d97515bf87a46bd694a7c72c520c04`
- Forwarded snapshot tree: `69abf4e2a8340d7d39a955d71d08afbf3a311a35`
- Current-base parent: `d1ea66bb749ce4f696fec440eb6dc0b5ad86bd87`

The final tree is the central test-service snapshot tree for the exact three
requested nodes; the local worktree remains intentionally uncommitted for the
harness.

## Exact qualification

Named suite: `ordinary014-parent-agent7b3-integration`

```text
env ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-7b3e1205 PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-7b3e1205 PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_replaces_parent_media tests/test_timeline_clip_replacement.py::test_native_parent_clip_swap_route_refuses_parent_ownership_on_public013_schema tests/test_timeline_clip_replacement.py::test_rt02_project_shot_crud_native_replacement_retries_after_restart
```

Result: **3 passed in 3.11s**.

Executed nodes:

- `test_native_parent_clip_swap_route_replaces_parent_media`
- `test_native_parent_clip_swap_route_refuses_parent_ownership_on_public013_schema`
- `test_rt02_project_shot_crud_native_replacement_retries_after_restart`

Agent checkout identity: `7b3e1205a374443c46bad6b18753ef146e1e42c6`.
Normal Runtime14a0 checkout identity: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`. The Agent lock reads the same
14a0 source commit and producer version.

## Byte and artifact checks

- Outside `tests/test_timeline_clip_replacement.py`, the worktree is byte-identical to committed candidate `616d2111`.
- Runtime guard/history files are byte-identical between candidate `616d2111` and merged current `a020a1c`.
- `contract/artifacts.json`: 75 entries, 0 declared-byte/hash mismatches.
- Artifact version read from the manifest: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`.
- `contract/artifacts.json` file digest: `sha256:ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- Generated release metadata: contract version `0.2.14`.
- Generated client metadata schema digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Shared command schema file digest: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Runtime bundle schema file digest: `sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`.
- Normal14 client `__init__.py` and `contract_metadata.py` are byte-identical to the Runtime candidate.
- `git diff --check`: passed.

No renderer, App browser, 64-schema, 143-cohort, full-suite, release, pin, or
integration-adoption operation was run. Owner decision remains after handoff.

