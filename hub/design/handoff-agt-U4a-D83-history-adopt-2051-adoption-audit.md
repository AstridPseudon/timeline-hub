# U4a D83 normal-tool adoption audit

Status: PREPARED pending publication of the independently PASS `rt-D83-history-security-2037` report. No Runtime security PASS is inferred from the source merge.

## Exact Runtime release

- Checkout: `/home/user/work/runtime`
- `git status --porcelain=v1 --branch`: `## tl/integration...hub/tl/integration` (clean)
- `git rev-parse HEAD`: `dc55b8bc6e638acd9e5031ff6b51b50cd2e2b63c`
- `git rev-parse HEAD^{tree}`: `0f941b27dc3396adbf41683e8ae30d77fc8b8768`
- Exact delta over `4351b9f91ee5adfc7d8e6e6b544a9ee6256a774a`: only
  `runtime_protocol/timeline_commit_auth.py` and
  `tests/test_timeline_capture_projection.py`.
- Both current blobs equal the reviewed source `57df943ecd3355a891d0229aecca7e645c58f4b6`:
  - `runtime_protocol/timeline_commit_auth.py`: `dddabb1a11e7c9b010d294f9db3765f771cd8cd8`
  - `tests/test_timeline_capture_projection.py`: `7486b460b999a3ee4d44d412e625434ef1152059`
- Full authorized source diff was inspected with:
  `git -C /home/user/work/runtime diff --no-ext-diff 4351b9f91ee5adfc7d8e6e6b544a9ee6256a774a dc55b8bc6e638acd9e5031ff6b51b50cd2e2b63c -- runtime_protocol/timeline_commit_auth.py tests/test_timeline_capture_projection.py`

## Retained reviewed identities

- `runtime_protocol/timeline_commit_validation.py`: e745/release blob `e896fcc8f44822ba6e8a7a6566b35657b0678283`
- `tests/test_timeline_schema_resolution.py`: e745/release blob `68674055692137706e5531b765196b6303b09df3`
- Runtime schema `contract/schemas/timeline-config.schema.json`: e745/current SHA-256 `4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`
- Runtime artifact manifest SHA-256: `9bbce65e5b8dd4fd7ca1f24105ffb88d341e5d5beb10348e555dda79145c4dd3`
- Popup owner fix `4dab564` is an ancestor of `dc55…` (exit 0).
- Inverse/range fix `1bae0e8` is an ancestor of `dc55…` (exit 0).

## Normal-tool adoption

Commands and exits:

1. `/home/user/work/venv-agent/bin/python scripts/refresh_runtime_client.py --producer /home/user/work/runtime` — exit 0; refreshed from `dc55b8bc6e63`.
2. `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/runtime` — exit 0; `ok runtime.lock.json (matches producer manifest)`.
3. `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — exit 0; `artifacts.json is current`.
4. `git diff --check` — exit 0.

Agent adoption diff:

```diff
diff --git a/runtime.lock.json b/runtime.lock.json
@@
-  "source_commit": "4351b9f91ee5adfc7d8e6e6b544a9ee6256a774a"
+  "source_commit": "dc55b8bc6e638acd9e5031ff6b51b50cd2e2b63c"
```

- Before lock SHA-256: `21c27ddd8ec6e10b3ed4b5af6f786837b8459439b6efc1ba6ec659492739703f`
- After lock SHA-256: `cd8afc023a0396199250b3aec24a8897bd4c2fc9e454fe9856e74416481ac7b9`
- Before Git blob: `05dbc24a0554bf35e3d20c7f4a4315f9da691865`
- After Git blob: `dc544f7983e92856f5afd4b28ec28c74f96d4e72`
- Working tree diff: one file, two lines (`runtime.lock.json` only).
- All 15 lock mappings have equal lock/consumer/producer SHA-256 values; `source_commit` is the exact `dc55…` release.

## Security receipt gate

At the final lookup, the exact independently PASS `rt-D83-history-security-2037` report was not present in the received normal hub/design paths. The local Runtime ref `refs/remotes/hub/tl/rt-D83-history-security-2037` points to the source `57df943…`, not to a security verdict. Therefore this worker does not claim qualified-source PASS, does not run originals, and does not release the PARAM candidate or five held original scopes.
