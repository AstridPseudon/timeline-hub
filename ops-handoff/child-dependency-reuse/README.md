# Verified child dependency seed

This packet is a private review/install kit for the Runtime child-venv route. It does not modify the live ORCH scripts.

The live baseline `candidate/make-child-venv.baseline` is byte-exact from the reviewed source before this packet. `candidate/request-child-venv` and `candidate/bench_store.py` are carried alongside it so the packet can be reviewed as one route; their baseline hashes are in `manifest.json`.

## Supported input

For a normal request, set `CHILD_VENV_DEPENDENCY_WHEELHOUSE` only in the requester environment. `request-child-venv` validates the absolute physical path and serializes it as an explicit `--dependency-wheelhouse` queue argument; the daemon/maker does not depend on inheriting the requester shell environment. The queued path must contain only the exact compatible wheel artifacts for the active `requirements/proof.lock` after the existing Agent/Runtime exclusions. The maker then:

1. checks the wheelhouse path and every artifact;
2. evaluates lock markers for the maker interpreter/platform;
3. verifies each wheel filename, compatibility tag, SHA-256, exact pinned version, and complete one-wheel-per-active-package set;
4. writes an immutable, stage-owned snapshot of the validated lock bytes and original wheel bytes;
5. installs with `pip --no-index --find-links <stage snapshot> --require-hashes --no-deps -r <stage snapshot>/requirements.txt`.

The input is opt-in. Without it, the existing pip route and its bootstrap behavior are unchanged. A verified dependency seed does not prove that pip/setuptools/wheel bootstrap is available offline: bootstrap remains the existing separate stage.

## Atomic install procedure

Review `manifest.json`, compare each live path with the listed `live_sha256`, verify every candidate hash (including the exact `verify_dependency_seed.py` hash pinned by `make-child-venv`), and review the candidate diff against `candidate/make-child-venv.baseline`. After independent approval, copy the candidate files atomically into the ORCH `bin` directory during a UTC-named backup window. Create the backup first, preserve modes/ownership, install the helper adjacent to the maker, and verify every destination hash before exposing the new kit:

```text
make-child-venv
request-child-venv
bench_store.py
verify_dependency_seed.py
```

Configure the private environment input only after the wheelhouse itself has been independently authenticated. The deployed helper is accepted only when it is the nonsymlink file with the manifest-pinned bytes; a helper found in the wheelhouse is never used. Do not claim a seed is authenticated from an existing child `RECORD`; retained original wheel bytes and their lock hashes are required. This packet makes no AgentREADY or actual-cache qualification claim; an independently authenticated same-lock wheelhouse is still required.

The existing exact Store child identity remains `(agent_sha, backend_sha, client_tuple)`, with its lease, ownership, path and transaction guards. This packet does not alter those guards or registration semantics.
