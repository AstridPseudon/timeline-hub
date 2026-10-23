# OPS bench store interface 1850 (core source contract, 18:51Z)

Staged source: `handoff-runtime-OPS-bench-store-core-1850-bench_store.py`.
Install name (lead only after review): `ORCH/bin/bench_store.py`. Python 3 stdlib, Linux flock. No installation by this worker.

## Adapter API (frozen now)

Import with importlib.util.spec_from_file_location. `Store(root, tests_dir)`; root is a NEW, dedicated physical directory (proposed `/home/user/work/bench-store`), tests_dir is exact ORCH/tests. `Store.initialize(root, tests_dir)` explicitly initializes an ABSENT root; existing/legacy paths are never adopted. Constructor requires existing owned store. No automatic legacy migration.

`child_key(agent_sha, backend_sha, client_tuple)` -> hex SHA256; all exact 40-lowercase-hex commits; client_tuple is a nonempty JSON object supplied by verified creator (all generated client custody identities, no omitted backend). `runtime_key(remotion_tree)` -> hex SHA256 of exact remotion tree SHA. Runtime backend/requested Agent origin is registration data, not key input.

`store.ensure(component, identity, registration, build, verify)` -> entry dict with `key`, `path`, `identity`, `reused`. component `child` or `runtime`; identity child `{agent_sha, backend_sha, client_tuple}`; runtime `{remotion_tree}`. registration `{name, env, suite, requires}`; name safe `[A-Za-z0-9][A-Za-z0-9_-]*`, env/suite exact STRINGS (suite is one full suites.conf row ending newline). requires list of `{component,key}` for other already-managed dependencies, normally empty. The current entry is automatically included. env/suite strings may contain literal `{bench_path}` replaced with final path. Preserve exact requested tuples/origin metadata in those bytes. Registration names are immutable; exact same bytes/dependencies may repeat idempotently.

Callbacks: `build(stage_path, final_path)` builds ONLY at stage_path; no publication or ORCH registration. `verify(path)` MUST run existing full verified creator custody, raises on failure. Called on both newly built stage and reused entry. Existing child1839 and Remotion f63a validation remain mandatory. Callback return values ignored. Core does no installer/network/source resolution itself. Core owns rename/publication/registration. Maker must render final paths (venv relocation remains adapter responsibility).

`store.acquire(names)` is a context manager yielding list of entry dicts. names are exact registered env base names (e.g. tuple), NOT paths. It resolves metadata and acquires all stable shared flocks atomically under store mutex, verifies exact suite/env bytes and entry identity. Python context holder must keep alive through setup and command. `store.run(names, argv)` executes actual command with lease FDs explicitly inherited by child/descendants and returns exit status. Ordinary unregistered legacy names must be classified by adapter and retain existing semantics; they are never eviction targets. `store.registered(name)` returns bool (malformed metadata/pending txn raises).

CLI: `python3 bench_store.py --root ROOT --tests-dir TESTS run --name NAME [--name NAME] -- COMMAND...`; `... recover`; `... key child --identity JSON` or `... key runtime --identity JSON`. Creation uses Python API to preserve trusted callbacks. CLI exit 2 for refusal; run exit mirrors child. No caller-provided paths become deletion authority.

## Transactions and capacity

Two slots per component, oldest unleased removed BEFORE build; if both held, refuse before callback. Store mutex serializes creators and lease acquisition/eviction; independent builds are deliberately serialized for simplicity. Stable locks are outside entry directories and NEVER removed/replaced. Leases inherited through subprocess chain survive holder death.

One journal covers build, immutable publication, index and exact suite/env projection. Any pending/crash journal blocks ordinary API. Explicit `recover()` rolls back to previous index and exact registration bytes, deleting only positively owned new stage/publication. No unknown directory adoption or sweeping. Old registrations remain exact when live; registrations referencing an evicted tuple fail closed (their suite/env bytes remain untouched). Prior suite/env bytes are never rewritten for eviction.

Store owner UID, physical path chain, exact schemas, canonical keys/paths, entry ownership markers and lock identities are checked. No /proc. Existing benches untouched. Dedicated store is the only eviction authority; old benches protected pending separate explicit trustworthy adoption (not implemented here).

Limits: staged core alone is not production-wired acceptance; creator and test-run adapter owners supply actual caller seams and combined private proof before install. Pending journal recovery is explicit, never silent. No public C0v2 changes.
