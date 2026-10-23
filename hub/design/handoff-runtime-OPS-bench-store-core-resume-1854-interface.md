# OPS bench store interface 1850 (corrected by core-precondition-1858)

Staged source: `handoff-runtime-OPS-bench-store-core-precondition-1858-bench_store.py`.
Install name (lead only after review): `ORCH/bin/bench_store.py`. Python 3 stdlib, Linux flock. No installation by this worker.

## Adapter API (frozen now)

Import with importlib.util.spec_from_file_location. `Store(root, tests_dir)`; root is a NEW, dedicated physical directory (proposed `/home/user/work/bench-store`), tests_dir is exact ORCH/tests. `Store.initialize(root, tests_dir)` explicitly initializes an ABSENT root; existing/legacy paths are never adopted. Constructor requires existing owned store. No automatic legacy migration.

`child_key(agent_sha, backend_sha, client_tuple)` -> hex SHA256; all exact 40-lowercase-hex commits; client_tuple is a nonempty JSON object supplied by verified creator (all generated client custody identities, no omitted backend). `runtime_key(remotion_tree)` -> hex SHA256 of exact remotion tree SHA. Runtime backend/requested Agent origin is registration data, not key input.

`store.ensure(component, identity, registration, build, verify)` -> entry dict with `key`, `path`, `identity`, `reused`. component `child` or `runtime`; identity child `{agent_sha, backend_sha, client_tuple}`; runtime `{remotion_tree}`. registration `{name, env, suite, requires}`; name safe `[A-Za-z0-9][A-Za-z0-9_-]*`, env/suite exact STRINGS (suite is one full suites.conf row ending newline). requires list of `{component,key}` for other already-managed dependencies, normally empty. The current entry is automatically included. env/suite strings may contain literal `{bench_path}` replaced with final path. Preserve exact requested tuples/origin metadata in those bytes. Registration names are immutable; exact same bytes/dependencies may repeat idempotently.

Callbacks: `build(stage_path, final_path)` builds ONLY at stage_path; no publication or ORCH registration. `verify(path)` MUST run existing full verified creator custody, raises on failure. Called at the final path for both newly published and reused entries before index/registration commit. Existing child1839 and Remotion f63a validation remain mandatory. Callback return values ignored. Core does no installer/network/source resolution itself. Core owns rename/publication/registration. Maker must render final paths (venv relocation remains adapter responsibility).

`store.acquire(names)` is a context manager yielding list of entry dicts. names are exact registered env base names (e.g. tuple), NOT paths. It resolves metadata and acquires all stable shared flocks atomically under store mutex, verifies exact suite/env bytes and entry identity. Python context holder must keep alive through setup and command. `store.run(names, argv)` executes actual command with lease FDs explicitly inherited by child/descendants and returns exit status. Ordinary unregistered legacy names must be classified by adapter and retain existing semantics; they are never eviction targets. `store.registered(name)` returns bool (malformed metadata/pending txn raises).

CLI: `python3 bench_store.py --root ROOT --tests-dir TESTS run --name NAME [--name NAME] -- COMMAND...`; `... recover`; `... key child --identity JSON` or `... key runtime --identity JSON`. Creation uses Python API to preserve trusted callbacks. CLI exit 2 for refusal; run exit mirrors child. No caller-provided paths become deletion authority.

## Transactions and capacity

Fixed policy: latest TWO tuples per component PLUS ANY older leased tuples. Before a new tuple build, retain the newest existing tuple and the incoming tuple plus all leases; remove superseded unleased entries. A reuse/policy transaction retains latest two existing plus leases and reaps older released entries. Two held tuples never imply capacity refusal by themselves; the fixed 8 GiB free-space reserve still applies. No count override. Store mutex serializes creators and acquisition/eviction; stable lease lock inodes are never replaced or removed.

Eviction is a separate durable journal transaction that completes BEFORE any new build callback. It validates directory ownership/key/path/lock identity and ALL exact owned suite/env registration hashes before deletion, removes those registrations and index references, and ACTUALLY deletes the owned bench contents. It does not quarantine/copy old benches for rollback. Pending eviction recovery rolls FORWARD deletion and projection/index removal; a failure leaves an explicit pending refusal. No installer runs with any pending journal. Completed eviction remains valid if a subsequent build fails.

Only after completed reclamation and reserve verification does a separate creation journal cover stage/build, verified final-path publication, new index and exact owned suite/env projection. Creation failure/recovery rolls BACK only that creation to its post-eviction baseline. No false success or stale managed registrations. All unrelated/current/leased/unmanaged/template bytes remain exact. Evicting any dependency removes its complete owned registration; leased registrations protect every dependency. No unknown directory adoption or sweeping.

Store owner UID, physical path chain, exact schemas, canonical keys/paths, entry ownership markers and lock identities are checked. No /proc. Existing benches untouched. Dedicated store is the only eviction authority; old benches protected pending separate explicit trustworthy adoption (not implemented here).

Limits: staged core alone is not production-wired acceptance; creator and test-run adapter owners supply actual caller seams and combined private proof before install. Pending journal recovery is explicit, never silent. No public C0v2 changes.

## Compatible adapter extensions (1854)

`registration` may also be a callable `(path, final_path, reused) -> dict`, evaluated after strict verification at final path. New entries are renamed under pending journal before `verify(final_path)` so existing relocation-sensitive custody checks remain strict; no public index/registration is committed until verification succeeds. A callable must not mutate public registration files. Empty env/suite strings mean no projection file/row (metadata still owned). `require_names` may additionally name existing managed registrations; core resolves and records their complete dependencies under its mutex.

`names_for_suite(repo, suite, command)` matches the exact stored `repo suite command` row (command before appended --files); it returns managed names, [] for unmanaged rows, and refuses tampered managed projection. `registration_entries(name)` resolves immutable metadata under mutex for creator use, with no lease implied. Acquire yields entries with inheritable `lease_fd`; adapters must pass those FDs to their supervised actual command. `run` explicitly inherits these FDs. The adapter owns waiting for descendants; flock protection survives direct parent death while any inheriting descendant retains the FD.

Eviction and creation have distinct journal kinds and recovery directions as above. No quarantine is credited as freed space. This corrects the earlier rollback requirement, which is withdrawn. Public API signatures and compatible extensions remain unchanged. Migration coverage remains dedicated-store entries only; existing unknown benches are protected and their space is not reclaimed automatically.

1858 source is now exported. The 1854 source basename is an identical compatibility copy for the existing adapter fixtures. Ownership marker is written before build, included unchanged through publication and verification. No prior core source/WIP survived either stopped worker; implementation follows their settled interface.

Private source-only proof: 1858 core tests exercise real reclamation/crashes; lease adapter fixtures pass. Creator runtime fixture passed creation/reuse; child fixture is BLOCKED by sandbox PermissionError renaming an already-readonly stage and deleting readonly contents on rollback. That journal remains pending, with no success. No chmod/retry of refused fixture paths; production install is NOT approved by this packet.
