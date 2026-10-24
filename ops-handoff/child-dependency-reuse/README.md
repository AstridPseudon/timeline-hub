# Verified child dependency seed

This packet is a private review/install kit for the Runtime child-venv route. It does not modify the live ORCH scripts.

The live baseline `candidate/make-child-venv.baseline` is byte-exact from the reviewed source before this packet. `candidate/request-child-venv` and `candidate/bench_store.py` are carried alongside it so the packet can be reviewed as one route; their baseline hashes are in `manifest.json`.

## Supported input

For a normal request, set `CHILD_VENV_DEPENDENCY_WHEELHOUSE` only in the requester environment. `request-child-venv` validates the absolute physical path and serializes it as an explicit `--dependency-wheelhouse` queue argument; the daemon/maker does not depend on inheriting the requester shell environment. The queued path must contain only the exact compatible wheel artifacts for the active `requirements/proof.lock` after the existing Agent/Runtime exclusions. The maker then:

1. checks the wheelhouse path and every artifact;
2. evaluates lock markers for the maker interpreter/platform;
3. verifies each wheel filename, compatibility tag, SHA-256, exact pinned version, complete one-wheel-per-active-package set, and one unambiguous `.dist-info` directory whose complete distribution identity matches after the packaging library's standard name canonicalization;
4. retains a read-only, stage-owned snapshot of the validated lock bytes and original wheel bytes;
5. reads the committed lock again, checks its approved SHA-256 and the retained filtered lock, and reauthenticates the retained wheels;
6. installs with `pip --no-index --find-links <open snapshot directory> --require-hashes --no-deps -r <kernel-sealed lock>`;
7. checks installed dependencies before local source installs and relocation, then checks every active dependency again at the final path before publishing a passing registration, using its original authenticated wheel and installed RECORD integrity and ownership.

Seeded reuse follows the same committed-lock, original-wheel and installed-byte checks, including when the current Store reuse request does not repeat `--dependency-wheelhouse`: the helper pin, approved lock and retained original snapshot are reauthenticated before return. A Store reuse request explicitly asking for seeded verification without retained original wheels refuses with `seeded child reuse requires Store custody and retained original wheels`; no provenance is inferred from an old RECORD or version. Top-level legacy children refuse seeded reuse because they have no Store custody. Ordinary unseeded legacy and Store reuse retain their existing exact Agent/Runtime/client verification, without claiming original-wheel verification. Parsing preserves the original argument array when the maker delegates an existing target back to the requester.

The sealed-lock install uses Linux `memfd` seals and `/proc/self/fd`; missing support refuses within the existing stage budget. The open directory survives parent renames, while pip's enforced hashes prevent substituted wheel bytes from gaining authority. Read-only modes are not a boundary against a hostile process with the same UID. The existing private-owner Store model and its leases/ownership checks remain the custody boundary; this packet adds no stronger same-UID or global Store guarantee.

Installed verification reconciles every file and directory in the entire physical child root against verified ownership, including foreign metadata, hidden files and unowned executables. No installed RECORD row can extend an active wheel’s file set. The only bootstrap executable exception is a physical, owner-owned interpreter copy whose bytes match the external maker interpreter; aliases are limited to python, python3 and the maker’s exact python3.N basename. Agent/Runtime ownership comes from the existing committed-source verifier, narrowed to exact committed bytes, validated bytecode, finite installer metadata and canonical console scripts declared in committed pyproject.toml. Its inventory is passed directly between authenticated verifier processes; it is not loaded from an installed allowlist. Creation checks again before relocation writes, then final verification and both seeded Store reuse routes perform the same complete inventory.

The seeded normal maker consumes the independently reviewed input0932/publication0940 archive at `$CHILD_VENV_ORCH_ROOT/artifacts/bootstrap-wheel-input-0932-443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548.tgz`. The archive SHA-256, three original wheel hashes and exact bootstrap lock are pinned in the helper. Only pip 26.2.1, setuptools 80.9.0 and wheel 0.46.3 enter the bootstrap snapshot; xdist and execnet remain separate Farm inputs. Missing or altered genuine input refuses explicitly.

Before any wheel runs, venv uses `--copies --without-pip --without-scm-ignore-files --prompt child`. The helper authenticates activation scripts against immutable root-owned host Python venv source/templates, writes deterministic `pyvenv.cfg`, verifies interpreter copies, and closes the initial root inventory. Pip launches directly from the authenticated retained original pip wheel, with `--ignore-installed` so that importing its wheel cannot make pip appear already installed. Installation still uses the sealed hash lock and open snapshot directory. The complete inventory is rechecked after bootstrap, active dependencies, local source installation, relocation, final publication and every seeded reuse.

The bootstrap authority digest binds the whole-root inventory format, archive, exact lock, wheel hashes, maker interpreter path/bytes/version, and trusted host venv source/template paths and bytes into the existing Store child key. Old incomplete entries are not adopted or relabeled. All bootstrap inputs are retained and reauthenticated, including reuse without a new wheelhouse argument. The one structural symlink allowance is the owner-owned `lib64 -> lib` link; structural directories are limited to authenticated file ancestors and the exact empty venv include/site layout. Files do not gain ownership from those directories.

Committed source snapshots retain only exact Git archive files. Seeded local builds consume retained exact Git archives under `.source-inputs` to keep setuptools output outside the retained source namespace. Their truthful PEP 610 archive URLs and SHA-256 hashes are checked against fresh Git archive bytes during every source verification, then relocated with the existing direct-url/RECORD transformation. Source/client markers, import origins, exact distribution metadata, provision report, provision requirements, original snapshots, and canonical Store ownership metadata receive narrowly validated ownership. The committed-source verifier passes this finite inventory directly as the reserved `__root__` member alongside `astrid` and `astrid-runtime` ownership; there is no installed manifest or command-line allowlist. Private tests materialize genuine wheel bytes and mock installation; actual guarded installation still requires independent cumulative review.

Installed verification deliberately refuses unsupported wheel `.data` relocation layouts and unexpected generated files. It accepts ordinary package/dist-info layouts, including standards-equivalent dotted/underscore/dash distribution spellings, and validates generated bytecode against authenticated source. Physical child, metadata and RECORD ownership are checked before importlib reads the installed file list. Installer bookkeeping accepts only pip's exact `INSTALLER` and `REQUESTED` bytes. POSIX console-entrypoint scripts are the one supported installer transformation: their authenticated wheel entry-point metadata determines the exact `bin/` path and wrapper bytes, including pip's simple shebang and long-path shell trampoline after relocation, while the installed RECORD hash/size and physical containment/ownership checks remain mandatory. Relocation preflights all RECORD paths before target reads or metadata writes and rehashes only launchers and local direct URLs, preserving all other installed hashes. A refusal needs a separately reviewed layout implementation or the required original artifacts; it is never permission to relabel an old bench.

The input is opt-in. Without it, the existing pip route and its bootstrap behavior are unchanged. The existing exclusions for Agent and pip/setuptools/wheel remain. Seeded bootstrap uses the separately authenticated retained archive described above; the unseeded legacy route retains its existing behavior. No stage timeout is increased.

## Atomic install procedure

Review `manifest.json`, compare each live path with the listed `live_sha256`, verify every candidate hash (including the exact `verify_dependency_seed.py` hash pinned by `make-child-venv`), and review the candidate diff against `candidate/make-child-venv.baseline`. After independent approval, copy the candidate files atomically into the ORCH `bin` directory during a UTC-named backup window. Create the backup first, preserve modes/ownership, install the helper adjacent to the maker, and verify every destination hash before exposing the new kit:

```text
make-child-venv
request-child-venv
bench_store.py
verify_dependency_seed.py
```

Configure the private environment input only after the wheelhouse itself has been independently authenticated. The deployed helper is accepted only when it is the nonsymlink file with the manifest-pinned bytes; a helper found in the wheelhouse is never used. Do not claim a seed is authenticated from an existing child `RECORD`; retained original wheel bytes and their lock hashes are required. This packet makes no AgentREADY or actual-cache qualification claim; an independently authenticated same-lock wheelhouse is still required.

The existing Store child identity is `(agent_sha, backend_sha, client_tuple)` for legacy requests and additionally binds `bootstrap_authority` for authenticated seeded children, with its lease, ownership, path and transaction guards. This packet does not alter those guards or registration semantics.

## Bounded failure observability

The normal maker now carries a finite failure marker from its existing `build(stage, final)` boundary before Store rollback removes the staging directory. Stage subprocess output is discarded at that boundary; it is never copied into a receipt. The retained record is written only after a successful rollback at:

```text
$CHILD_VENV_ORCH_ROOT/tests/provision-failures/<child-name>.txt
```

It contains only the validated `status`, stage, return code, elapsed seconds, exact Agent/Runtime identities, the committed lock path and digest, and the fixed diagnostic `stage-command-failed`. The record and its directory are physical, owner-owned, finite-size, private-mode files. Unsafe, oversized, malformed, symlinked or path-escaping records refuse. A failed build still returns refusal, leaves no Store entry or pending journal, and does not change the successful source/provenance path.

The supported normal artifact input remains the existing opt-in contract: set `CHILD_VENV_DEPENDENCY_WHEELHOUSE` to an independently authenticated absolute physical wheelhouse containing the exact compatible `requirements/proof.lock` artifacts, then invoke `request-child-venv` with the existing source carrier. This packet does not acquire, probe or qualify that wheelhouse.


## Component join seam

Farm component0946 owns `candidate/verify_farm_distribution_inputs.py`, `tests/test_farm_distribution_inputs.py` and its standalone interface. This packet does not author or wire schema support. The exact component API is `validate_farm_distribution_inputs(*, schema_source: Path, wheelhouse: Path, additional_wheels: Sequence[WheelInput] = ()) -> dict`; it returns `schema_source`, `wheel_inputs` and `component_identity`. The future maker hook belongs beside `bootstrap_key()` before Store identity selection/`store.ensure`, with final and reuse checks at `verify(path)` and the staging inventory boundary. A later reviewed join must validate Farm inputs before installation, keep test2 separate from bootstrap3, include any newly authenticated component identity in the Store key, retain its original inputs, and pass only authenticated file ownership into the existing final/root verifier. Adding a distribution to a wheel dictionary or a namespace to an exemption is not a supported join. The current production caller remains the normal requester → maker → Store creation/final/reuse path; no component0946 readiness is claimed here.
