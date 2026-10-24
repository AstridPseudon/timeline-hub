# Report

**Actual receipt: PASS** — artifact/publication only.

Verified read-only:

- ORCH archive: `3,002,878` bytes, SHA-256 `443977b004381bf3dd23cdcc7558335913256dc438198ed6478259d2f98cb548`.
- Byte-identical to normal hub archive and committed blob `bf4d0f53…`.
- Hub sidecar and committed sidecar contain the matching digest.
- Archive has exactly 10 safe, unique members; no traversal, links, or duplicates.
- Five wheels and full hashes/metadata verified:
  - pip 26.2.1 — `71138adf…0384ed3e`
  - setuptools 80.9.0 — `062d3422…9f306922`
  - wheel 0.46.3 — `4b399d56…15d8bc4d`
  - pytest-xdist 3.8.0 — `202ca578…10f0b88`
  - execnet 2.1.2 — `67fba928…79e296ec`
- Bootstrap role: pip/setuptools/wheel (3). Test role: pytest-xdist/execnet (2).
- Lock SHA-256: `62bf0f1e…70af6b8`.
- `requirements/proof.lock` unchanged: `236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778`.

Commands/results:

- Inline `tarfile`/`zipfile` validator: **PASS**.
- Hub/commit byte and sidecar comparisons: **PASS**.
- `git diff --check HEAD`: **PASS**; worktree clean.
- Product tests/static/type checks: not applicable; no source changes.

Missing facts:

- ORCH has no separate `.sha256` sidecar; this was reported absent, not inferred.
- No installation, Agent child readiness, remote owner receipt, or 67-wheel byte credit claimed.
- No downloads, provisioning, publication, or manual sync performed.

Recorded commit message and empty `DONE` marker.