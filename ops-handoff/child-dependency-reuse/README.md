# Verified child dependency seed

This packet is a private review/install kit for the Runtime child-venv route. It does not modify the live ORCH scripts.

The live baseline `candidate/make-child-venv.baseline` is byte-exact from the reviewed source before this packet. `candidate/request-child-venv` and `candidate/bench_store.py` are carried alongside it so the packet can be reviewed as one route; their baseline hashes are in `manifest.json`.

## Supported input

Set `CHILD_VENV_DEPENDENCY_WHEELHOUSE` in the dispatcher/maker environment to an existing, absolute, physical directory containing only the exact compatible wheel artifacts for the active `requirements/proof.lock` after the existing Agent/Runtime exclusions. The maker then:

1. checks the wheelhouse path and every artifact;
2. evaluates lock markers for the maker interpreter/platform;
3. verifies each wheel filename, compatibility tag, SHA-256, exact pinned version, and complete one-wheel-per-active-package set;
4. installs with `pip --no-index --find-links <wheelhouse> --require-hashes --no-deps`.

The input is opt-in. Without it, the existing pip route and its bootstrap behavior are unchanged. A verified dependency seed does not prove that pip/setuptools/wheel bootstrap is available offline: bootstrap remains the existing separate stage.

## Atomic install procedure

Review `manifest.json`, compare each live path with the listed `live_sha256`, and review the candidate diff against `candidate/make-child-venv.baseline`. After independent approval, copy the candidate files atomically into the ORCH `bin` directory during a UTC-named backup window:

```text
make-child-venv
request-child-venv
bench_store.py
verify_dependency_seed.py
```

Install the helper adjacent to `make-child-venv`, preserve executable bits on the two shell entry points, and verify the manifest candidate hashes after the copy. Configure the private environment input only after the wheelhouse itself has been independently authenticated. Do not claim a seed is authenticated from an existing child `RECORD`; retained original wheel bytes and their lock hashes are required.

The existing exact Store child identity remains `(agent_sha, backend_sha, client_tuple)`, with its lease, ownership, path and transaction guards. This packet does not alter those guards or registration semantics.
