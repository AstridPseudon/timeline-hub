# PASS — OPS Farm metadata protected source review (SOURCE_ONLY)

Exact narrow ownership fix: PASS. Live root applicability: SOURCE_ONLY because the actual failed Farm `RECORD` is absent. See the worker evidence summary for commands, hashes, controls, and the installation gate.

Candidate SHA-256: `d2da4aecd759999fe1d7c929b82403533746df746c50b9928f97d083605b2a3a`.
Installed kit baseline: PREIMAGE_MATCH, SHA-256 `ff8dbf0ecb615a665e346b36d9d179526a58127d09749748990ea0fa885cf8f8`.

The candidate's only functional change is the private embedded `STORE_VERIFY` ownership predicate. It admits exactly `licenses/LICENSE` when its bytes equal authenticated committed source `LICENSE`; all other unowned metadata remains refused. Bounded production-caller tests pass old-red/new-green, valid authenticated inventory, extra/altered/renamed metadata, wrong/missing source license, RECORD traversal, and symlink negatives. Compile, `bash -n`, focused controls, and normalized Ruff/mypy no-new checks pass against the retained baseline.

The refused Farm log does not contain the installed inventory. `<distribution>.dist-info/licenses/LICENSE` is therefore inferred, not observed. Required before any install or retry: the failed distribution `RECORD`, matching `licenses/LICENSE` bytes/hash, matching `METADATA` Name/Version, and matching `direct_url.json`/`WHEEL` rows. No installation, child retry, registration, live-kit mutation, or C0 wire/product change was made.
