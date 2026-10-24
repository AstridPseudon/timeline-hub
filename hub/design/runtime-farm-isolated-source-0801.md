## Result

The blocker is genuine for the current Farm row’s direct `-I` subprocesses, but not for GenericHost’s managed child route.

- Current v2 row uses source imports via `PYTHONPATH="$PWD:<Runtime>"` and `/home/user/work/venv-agent/bin/python`.
- `python -I` ignores that `PYTHONPATH`; the bare `runtime_protocol` probe therefore fails.
- The real Agent test `tests/packs/h3_av/test_character_swap_cpu_boundary.py:87-96` also launches `sys.executable -I -c` after removing `PYTHONPATH`; retained Farm output shows the same class of failure (`ModuleNotFoundError: astrid`).
- GenericHost has an explicit supported carrier: `generic_host.py:2221-2304` injects validated roots through `-I -c` bootstrap code; captured source uses inherited descriptors (`generic_host_worker.py:26-90`). A bare `-I` import is not its production contract.

## Exact source facts

Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26`, tree `57f0231da0d7904ecd8778169973d6384e0ae141`:

- `generic_host.py` SHA256 `b5ad2c6494064ecb5e1c1c1c251b411a39f8b59de3358ddc783a1b1ec6765fd6`
- `generic_host_worker.py` SHA256 `0fd735fad6312aa0dc9be3e84da697a5810711f8ae5fadba66deb2a7550b4a49`
- `host_bootstrap.py` SHA256 `50e73b1a9b95528dc06192e0102caad55ec7192b5369ff8a6698cb14c70a0b07`
- `subprocess_env.py` SHA256 `ae1aefbdec52e7db70b2ddfe7b2f75698bfc5aece1b5506030bc30569a3ee42b`

Runtime D40 source:

- `runtime_protocol/external_pack_sources.py` SHA256 `8931d2ae530ff1d6eccbb28dadec4349641fd4e1c19f231dba2616b93be2234e`
- Owner-authenticated capture/descriptor contract: `external_pack_sources.py:53-65`, `160-224`, `227-273`.

Reviewed packet: commit `471712f15fc14da5439fdab1da10e43259d18435`, tree `11eddad56372ff0fe955799f8e57a1f9a599f01a`. Independent review `0632` was source PASS only; Farm READY remained unverified.

The genuine installed child `3b5cb98c...` imports from private site-packages and carries markers for Agent `ba8f0bc8`, Runtime `f3208b26`, client tuple, custody owner/key, and RECORD files. It proves the installed-profile route, but is the wrong tuple and cannot qualify Agent `9cd`/Runtime `1d9`.

## Required Farm input

Use one normal authenticated managed child built for:

- Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26`
- Runtime `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree `f56c396c4495547680b46e832565278d2c375e69`
- Runtime D40 hash above and the packet’s canonical client hashes
- Installed, non-editable Agent/Runtime origins in the managed child
- Exact marker, RECORD, custody-owner/key, lock, and normal maker receipt

The Farm row must invoke that authenticated child interpreter with `PYTHONPATH` absent, while retaining the approved Node20/Remotion bindings. Farm must return the rendered row, receipt/profile path and key, marker/RECORD hashes, and parent plus `-I` child import origins before requesting any checkpoint.

No source edits, provisioning, package installation, live actions, or tests were run. `git diff --check` passed; worktree is unchanged. Commit message and `DONE` marker were written.