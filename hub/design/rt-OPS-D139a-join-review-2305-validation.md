# D139a joined-source validation

## Exact custody

Base: `bae2ba5ec66e6fb4115c2f79299f82f535e68bb1`.

Maker review: `e9fdcfe299a20f1a137e0c87d2c0bf2de49f9e45`, candidate
`fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5`,
111171 bytes, mode 0755. Shared installed preimage:
`f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`,
75541 bytes, mode 0755.

The five imported blobs and the two protected checker/canonical-test blobs
were compared directly with `git show`/`cmp`; all matched their required
source commits. The product delta was censused against the base: exactly the
five maker files plus `ops-child-custody/source-manifest.json`; no outside
product bytes were found.

## Commands and results

All controls below were run once on the joined source with the specified
binaries/configuration. Scratch fixtures and the canonical result were placed
under the harness private `/tmp/w-…` directory. The assigned worker `tmpdir`
was a regular file, so it could not host fixtures; this was an environment
limitation only and did not alter the source tree.

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m unittest discover -s ops-child-custody/tests -p 'test_*.py' -v` | PASS — 63/63 |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/check-child-imports` | PASS |
| `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` | PASS |
| Seven embedded Python `compile()` blocks using `/home/user/work/venv-agent/bin/python` (`STORE_PY`, `STORE_VERIFY`, `STAGING_INVENTORY`, `RELOCATE`, `PROVENANCE_SCRIPT`, `DIST_METADATA_SCRIPT`, `IDENTITY_SCRIPT`) | PASS — 7/7 |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B ops-child-custody/install-prep/dry_run_controls.py` | PASS — private candidate/preimage/CAS/helper/shape controls |
| `/usr/bin/python3.13 ops-child-custody/check-child-imports --child /usr/bin/python3.13 --launcher /home/user/work/agent/tools/p4-d73-pinned-launch.sh --census-file /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agt-F-D139-import-input-census-2149-input-census.json --output <private result>` | Expected exit 1 — 1146 rows, 22 attempted modules, 12 canonical missing names, 12 failures, zero missing installed distributions |
| `/home/user/work/venv-agent/bin/python -m json.tool ops-child-custody/source-manifest.json` | PASS |
| `git diff --check` | PASS |

The canonical command consumed the authenticated 1146-row Agent2149 packet
(`be9e8bc9c6d2411809da2d99126a9b3eef72678de2066bb6ad196d5d16ebcd30`) and
used `/usr/bin/python3.13` only as the supporting system probe. Its all-missing
diagnostic is not registered-child, install, Store, provider, or core evidence.

## Scope boundary

The maker source admits the pinned installed `banodoco-timeline-schema` 0.0.2
RECORD closure and binds its immutable identity through the existing internal
verification/Store route. The live outer request caller remains `NOT_READY`
because it has not yet gained the two schema transport flags; no dead-helper
claim or alternate route is made here.

No installation, package acquisition, child request, Store/registry mutation,
provider, browser, full suite, live socket, or body run was performed. The
D137 whole-make fixture gate remains withdrawn, and the real child/core result
remains `NOTRUN`.
