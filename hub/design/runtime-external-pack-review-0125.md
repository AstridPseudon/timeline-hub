## Result

**UNKNOWN — end-to-end external-pack authority remains unproven.**

The prior report’s core conclusion stands, but its “no Runtime byte observation” statement was too broad.

- **FAIL (overbroad prior finding):** Runtime does have private live byte observation for profile-declared extra roots. `local_worker_composition.py` compares `_pack_inventory()` before launch and during retained observation, rejecting changes or mismatches. [`local_worker_composition.py:361`](/home/user/work/wt/rt-R2r-external-pack-review-0125/runtime_protocol/local_worker_composition.py:361), [`:1063`](/home/user/work/wt/rt-R2r-external-pack-review-0125/runtime_protocol/local_worker_composition.py:1063), [`:1284`](/home/user/work/wt/rt-R2r-external-pack-review-0125/runtime_protocol/local_worker_composition.py:1284)

- **PASS (core prior finding):** No Runtime-owned authenticated provenance/definition authority exists for the actual Agent production host path. Runtime’s retained installed-release verifier inventories Runtime/Agent installation roots, not external pack roots. [`local_worker_composition.py:1323`](/home/user/work/wt/rt-R2r-external-pack-review-0125/runtime_protocol/local_worker_composition.py:1323)

- **PASS, Agent-local only:** Agent source setup validates repository, exact revision, manifest/tree digests, and managed roots. [`source_setup.py:318`](/home/user/work/agent/astrid/core/pack/source_setup.py:318)

- **UNKNOWN:** Agent admission computes selected definitions, capability digests, and source digests, then rechecks source bytes before execution; however, these remain Agent-owned claims. Runtime registration stores claimed aggregate digests/descriptors without independently binding them to external-pack bytes, provenance, or selected definition origins. [`generic_host.py:6010`](/home/user/work/agent/astrid/core/execution/generic_host.py:6010), [`generic_host.py:4269`](/home/user/work/agent/astrid/core/execution/generic_host.py:4269), [`host_bootstrap.py:1368`](/home/user/work/agent/astrid/sdk/host_bootstrap.py:1368)

## Exact missing trust fact

A Runtime-owned, owner-authenticated binding is missing that connects the exact launched external root to:

- canonical root and symlink-free complete file/byte inventory;
- pack identity, repository origin, exact revision, subpath, manifest/tree digests;
- selected definition origin/bytes and capability digest;
- launch/executor identity and an immutable lifetime or protection lease.

Current Runtime inventory is filesystem observation against profile-supplied expected files. Current Agent source setup provides provenance, but the production caller passes roots and an identity string into `generic_host`; it does not provide Runtime-authoritative provenance or definition evidence.

## Smallest private seam

Runtime manager owns the producer: extend the existing private host-preparation/launch custody boundary to capture and retain the authenticated external-pack binding.

Agent manager owns the consumer: `ensure_pack_host()` and `generic_host` must consume that private binding before discovery/admission and reject foreign roots, collisions, symlinks, mismatched definition/capability digests, and any post-capture mutation.

This should remain a private owner-bound artifact/FD/sidecar keyed to the existing launch custody identity—not a new public API, schema, tuple, or client route. `source_setup` remains provenance validation, not Runtime authorization.

## Scope and verification

Runtime:

- HEAD: `458595850c354f4403dabc58a72b98bebbc2c3a3`
- Tree: `703b1aac733ad3c977399e67cd4e23d6ae85e7bb`
- Clean worktree.
- Key module hashes recorded for `local_worker_composition.py`, `verified_host_launch.py`, `service.py`, and `store.py`.

Agent:

- HEAD: `940b54d60b217df6b55cd5454bb896acfbf8f455`
- Tree: `128187be31dd61d9cadcd5b4482007b1204bf8a8`
- Clean worktree.
- Key module hashes recorded for `host_bootstrap.py`, `generic_host.py`, `source_setup.py`, and `source_identity.py`.

Exact source checks used included `git rev-parse`, `git status`, `sha256sum`, and targeted `rg` source inspection. Tests, installation, live sockets, child launches, process probes, full suites, and browser journeys were **not run** per the task limits.

No product files, schemas, generated clients, tuples, or v2 contract behavior were changed. The full v2 request/reply behavior—including request fields, accepted/merged/conflict/invalid replies, dry-run preview, authority/tamper/ABA/no-write guards, revisions/digests, records/effects/bindings/dependencies/history/undo steps, and conflict/error details—remains untouched.

No blockers.