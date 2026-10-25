# Runtime D112a release — RELEASED

Published from the actual clean normal Runtime head after exact-tree verification.

## Identity

- Normal branch: `tl/integration`
- Actual normal HEAD: `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e`
- Actual normal tree: `6283b5fbb128447f1b333e0e6af334d35637cf69`
- Reviewed candidate: `32c22795de890818eb8abeae6e644685098cbf30`, exact tree match.
- Normal receipts: `8b3895cf141f5b7359cceacefde62c9a9475eabf` followed by `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e`.
- `git diff --exit-code 32c22795de890818eb8abeae6e644685098cbf30 -- .`: clean.
- Home status: clean.

The original product-semantic identity is `be828d92cba9200a6ae0ded3a2e968dc3f6ac383` (tree `08ea7479d3709a915a51e17ade13453eee914da5`). The final integrated tree adds only the reviewed type-only correction and preserves the disjoint D108 snapshot-test merge; no client, schema, pin, registry, or product semantic change was introduced by publication.

## Exact source custody

| Path | Git blob | SHA-256 |
| --- | --- | --- |
| `runtime_protocol/timeline_commit_store.py` | `6e29f654710649bd1110d5c5a4be04dbfde198c8` | `f0867b6bf083aef2ca280c3f1bcbbbc926c7dfc448c519836e286022f5e3d59a` |
| `tests/test_timeline_history_state.py` | `098eee4efb4236e45dda2b0742295aece56f50e9` | `788e1280c61cbee6817595544495ba462365d956d0cd85499923328dedba838b` |
| `tests/test_timeline_render_publication.py` | `88ff0a9d94af99d28e58b935de946f9ca1ffc7c2` | `7de21278fa27582e7b6d4d47a2fac69468c9466931f4f2c44923d8e44977e6a2` |

The current store/history source-pair digest is `639afa0d321ce071552724248ca49a33522118c0d0573ba781c56da121024d9d`. The original `be828` pair digest was `0fa2ad93606210d29538b6be4265e0175dc994f23919325dd496b21b5aa897d4`.

The `32c22795` correction is strictly typing-only: one `typing.cast` import and typed local connection aliases at five existing uses. Normalized runtime AST is equal after removing those casts/aliases, with SHA-256 `d6c9b5d449530c541236d95c6122382ce83cf4a27d82c970e5864b262b23678d` on both sides. No tests changed in that commit.

The 15 canonical client/schema paths were checked against `be828d92`; all are byte-identical. Their exact git blobs and SHA-256 values are recorded in the companion JSON packet.

## Proof register

- `rt-D112a-warm-release-check-0927`: 53 history-state tests passed on the reviewed `be828` source, including warm forward/read controls.
- `rt-D112a-type-narrowing-0940`: 53 history-state tests and 2 real Agent provider smoke tests passed on the corrected source.
- `rt-D112a-typing-review-0945`: independent PASS; Pyright parent/candidate both 55 diagnostics with zero added or removed identities; normalized AST, Ruff E9/F, compile, and diff checks passed.
- `rt-D112a-home-release-0931`: prior hold was solely the five diagnostics later corrected by `32c22795`; it is superseded by the merged correction and independent final review.
- `rt-D112-security-review-0827`: identity-fallback controls PASS; the two `PRAGMA data_version` authorizer failures are parent-identical and disclosed.
- `rt-D112-native-acceptance-0827-targeted-1025084336-23116` and `...1025084443-11165`: real registered-provider seed/SWAP/native-undo positives.
- `rt-D112-acceptance-return-0850`: identity controls RED3/GREEN3 and tamper controls qualified; no flat-curve claim.
- `rt-D112-curve-return-sol-0907` / `rt-D112-curve-wholepath-0907`: baseline and candidate verification counters and payload sizes matched under the accepted identical-lifecycle comparison; both retained flatness flags are false, so no broader performance claim is made.
- `e6b669b98d8eeb349c311741cdfd8cfbfe5e5486`: preserved D108 snapshot tests.

Retained XML/artifact hashes, including native smoke, security JUnit, identity summary, curve result, AST conservation, and Pyright identity comparison, are in `runtime-D112a-release-0952.json`.

## Commands and results

- `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_history_state.py` — 53 passed in 24.95s.
- `ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e PYTHONDONTWRITEBYTECODE=1 bash scripts/check-before-push --native-provider-smoke` — 2 passed, exit 0; provider origin verified.
- `/root/.local/bin/pyright --outputjson runtime_protocol/timeline_commit_store.py tests/test_timeline_history_state.py` — parent 55, candidate 55, zero identity delta; exit 1 on both for inherited diagnostics.
- `/root/.local/bin/ruff check --no-cache --select E9,F runtime_protocol/timeline_commit_store.py tests/test_timeline_history_state.py` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-d75051f122/d112a-review/pycache /home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/timeline_commit_store.py tests/test_timeline_history_state.py` — PASS.
- `git diff --check` — PASS.

## Release scope and handoff

The production caller is the normal coordinator through `TimelineCommitStore` recovery and history verification. Identity changes now drop memo, re-establish the connection, reset the physical baseline, and full-verify. Tampered state remains refused without writes. Public C0/auth/freshness and full C0v2 request/reply §§1/4 remain unchanged.

This is a Runtime core product release. It does not claim the original tour SWAP GO. D59 final gates remain owed. D111b remains held until genuine source-doc read-wall, independent review, and real-provider acceptance; no cache candidate is adopted.

No new test stage, core change, semantic review, product/test pin, generated-file, kit, registry, hub, upstream push, or git write was performed by this publication worker.
