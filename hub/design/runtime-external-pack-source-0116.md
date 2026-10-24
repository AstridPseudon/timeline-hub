## Result

**UNKNOWN — no Runtime-owned external-pack source capture/authority route exists in Runtime `458595850`.** The production path accepts profile-declared external roots, but their inventory remains caller/profile data.

### Evidence

- Runtime loads the configured worker profile and passes it into `RuntimeDaemon`: [runtime_boundary.py:1152](/home/user/work/wt/rt-R2r-external-pack-source-0116/astrid_runtime/runtime_boundary.py:1152).
- Host-only launch forwards `additional_pack_roots` and compares live files against profile-supplied `files`: [local_worker_composition.py:361](/home/user/work/wt/rt-R2r-external-pack-source-0116/runtime_protocol/local_worker_composition.py:361).
- Runtime’s retained installed-release capture inventories only the installed source, Python runtime, stdlib, and native library roots; external pack roots are absent: [local_worker_composition.py:1323](/home/user/work/wt/rt-R2r-external-pack-source-0116/runtime_protocol/local_worker_composition.py:1323).
- The verifier’s strong source/inventory binding therefore covers Astrid/Runtime installation, not external-pack definition/module origins: [verified_host_launch.py:340](/home/user/work/wt/rt-R2r-external-pack-source-0116/runtime_protocol/verified_host_launch.py:340).

Agent does have a separate managed-source inventory:

- Repository/revision, manifest digest, tree digest, and root are validated by Agent: [source_setup.py:318](/home/user/work/agent/astrid/core/pack/source_setup.py:318).
- GenericHost derives admitted source roots, capability digest, and source digest: [generic_host.py:5937](/home/user/work/agent/astrid/core/execution/generic_host.py:5937).
- It rechecks the admitted source digest immediately before execution: [generic_host.py:4269](/home/user/work/agent/astrid/core/execution/generic_host.py:4269).

These are Agent-owned facts, not Runtime authority. Agent’s `source_inventory_identity` and CLI/source mappings cannot authorize Runtime loading.

### Missing private seam

Smallest proposed seam, not implemented:

- Producer: Runtime private capture during [local_worker_composition.py:1170](/home/user/work/wt/rt-R2r-external-pack-source-0116/runtime_protocol/local_worker_composition.py:1170), independently recording canonical root, authenticated origin/revision, symlink-free inventory, per-module bytes digests, and selected definition/capability digest.
- Consumer: private launch binding through [verified_host_launch.py:289](/home/user/work/wt/rt-R2r-external-pack-source-0116/runtime_protocol/verified_host_launch.py:289), consumed by Agent admission in [generic_host.py:6010](/home/user/work/agent/astrid/core/execution/generic_host.py:6010).

It must reject foreign roots/digests, parent or descendant symlinks, `astrid`/`runtime_protocol` collisions, source mutation, and mismatched definition bindings; retain `-I`/`-S`; and never use `PYTHONPATH` or caller claims as authority.

### Scope and verification

- Runtime HEAD/tree: `458595850c354f4403dabc58a72b98bebbc2c3a3`, clean.
- Agent HEAD/tree: `3059ba95860886d9a79f62abadbd27120bf41853`, clean.
- Key file hashes recorded; no tracked edits made.
- Requested design files were absent at the stated Astrid path; equivalent copies were read from `/home/user/timeline-hub/hub/design/`.
- C0 v2 §§1–7 unchanged (`contract/commit-v2.md`, hash `257024df6fa93be767f0c74ee10014a6770c4fcb`).
- Tests/lint/typechecks: **NOT RUN**; this was a bounded readonly source assessment. No host-liveness claim made.
- Wrote the required commit message and `DONE` marker.