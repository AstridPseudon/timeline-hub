# OPS-child kit live review evidence

Observed UTC: 2026-10-24T07:39:43Z
Runtime review base: `33fc06bbd5b0a778517ac6f7c161b2a556ab80c4`
Runtime worktree: `/home/user/work/wt/rt-OPS-child-kit-live-review-0739`
ORCH root: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`

## Reviewed manifest

```json
{
  "packet": "OPS-child-dependency-reuse",
  "base_runtime": "1d9ddba546f8fb1300f55ff62607ed492719cbaa",
  "lock_sha256": "236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778",
  "live_baseline": {
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv": "c887a1bef4831f2ca5a43372ee28430000b2f20b9d290bffb237f27ffc404ff2",
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-child-venv": "3b771253b465a6ba06b57ab16d6049273114dc75f491ce81d0132fedb3c8aa33",
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py": "6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8"
  },
  "candidate_sha256": {
    "candidate/bench_store.py": "ba31adcf5dfbad179dfe08b048c48052cee2083026ec62790659c8cdbbc903bd",
    "candidate/make-child-venv.baseline": "c887a1bef4831f2ca5a43372ee28430000b2f20b9d290bffb237f27ffc404ff2",
    "candidate/make-child-venv": "6b3e34f9d8abecb7dd0a62f448e8863a76271d273815e1ec82e6c25f94665dbd",
    "candidate/request-child-venv": "08f1b00a716456ba328ff42ee96f3df60d0dfa5470b36eeafb5d299b3df22fde",
    "candidate/verify_dependency_seed.py": "8f95cdaee258b87dde8e859e99fb955e9cde91dfeec9e7191f4837a5ced6714f",
    "tests/test_dependency_reuse.py": "e582b9dfd17460a9a047afa92d865159e01d40b0fa8f91b5f269dccc2b83f2cb",
    "README.md": "09feab2bef22de6d06dc5733e362509476586d7d86c30114ea096453f4a893a3"
  }
}
```

## Full hash and metadata table

All four live files and all three existing backups are regular, non-symlink, root-owned (`uid=0 gid=0`), mode `0755`.

| location | file | size | SHA-256 |
|---|---|---:|---|
| LIVE/bin | `bench_store.py` | 42323 | `ba31adcf5dfbad179dfe08b048c48052cee2083026ec62790659c8cdbbc903bd` |
| LIVE/bin | `verify_dependency_seed.py` | 17162 | `8f95cdaee258b87dde8e859e99fb955e9cde91dfeec9e7191f4837a5ced6714f` |
| LIVE/bin | `make-child-venv` | 39611 | `6b3e34f9d8abecb7dd0a62f448e8863a76271d273815e1ec82e6c25f94665dbd` |
| LIVE/bin | `request-child-venv` | 14380 | `08f1b00a716456ba328ff42ee96f3df60d0dfa5470b36eeafb5d299b3df22fde` |
| UTC backup | `bench_store.py.20261024T073341Z.bak` | 38921 | `6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8` |
| UTC backup | `make-child-venv.20261024T073341Z.bak` | 33373 | `c887a1bef4831f2ca5a43372ee28430000b2f20b9d290bffb237f27ffc404ff2` |
| UTC backup | `request-child-venv.20261024T073341Z.bak` | 13326 | `3b771253b465a6ba06b57ab16d6049273114dc75f491ce81d0132fedb3c8aa33` |
| publication `hub/kit/bin` | `bench_store.py` | 42323 | `ba31adcf5dfbad179dfe08b048c48052cee2083026ec62790659c8cdbbc903bd` |
| publication `hub/kit/bin` | `verify_dependency_seed.py` | 17162 | `8f95cdaee258b87dde8e859e99fb955e9cde91dfeec9e7191f4837a5ced6714f` |
| publication `hub/kit/bin` | `make-child-venv` | 39611 | `6b3e34f9d8abecb7dd0a62f448e8863a76271d273815e1ec82e6c25f94665dbd` |
| publication `hub/kit/bin` | `request-child-venv` | 14380 | `08f1b00a716456ba328ff42ee96f3df60d0dfa5470b36eeafb5d299b3df22fde` |
| committed hub `HEAD` | `hub/kit/bin/bench_store.py` | — | `ba31adcf5dfbad179dfe08b048c48052cee2083026ec62790659c8cdbbc903bd` |
| committed hub `HEAD` | `hub/kit/bin/verify_dependency_seed.py` | — | `8f95cdaee258b87dde8e859e99fb955e9cde91dfeec9e7191f4837a5ced6714f` |
| committed hub `HEAD` | `hub/kit/bin/make-child-venv` | — | `6b3e34f9d8abecb7dd0a62f448e8863a76271d273815e1ec82e6c25f94665dbd` |
| committed hub `HEAD` | `hub/kit/bin/request-child-venv` | — | `08f1b00a716456ba328ff42ee96f3df60d0dfa5470b36eeafb5d299b3df22fde` |

`verify_dependency_seed.py` had no pre-existing live file and therefore no helper backup. The three backups are byte-exact against the manifest's three `live_baseline` hashes.

## Protected files

Current live hashes match both sides of the authentic installation receipt:

| file | before/after/current SHA-256 |
|---|---|
| `dispatcher-daemon` | `d5c6753312e485f2368ab61d34161f0853b27aa6c5e2b5c22036d3bd628da8ed` |
| `make-runtime` | `873ddcfa636b3ae9e285613a6fb65c643e21ac749e00197d582e0c820dd70149` |
| `request-runtime` | `471fd470efeae102140b96b4f97db857e0d6d79b0839afa10a1a00e911b33b5f` |

## Publication and heartbeat observation

The installer-time observation at 07:33–07:34 retained the old three-file publication kit and no helper. A later normal hub-sync published all four exact live files. Committed hub `HEAD` is `3497fb2f42e838ad740e187c58dab95ff21500bb`, commit time `2026-10-24 07:38:36 +0000`, subject `hub-sync main 2026-10-24T07:35:59Z`; its diff adds `verify_dependency_seed.py` and modifies the other three kit files.

At the final snapshot (`2026-10-24T07:39:43Z`), `hub-sync.heartbeat` and `hub-push.ok` both contained `2026-10-24T07:38:38Z` and were each about 65 seconds old. The hub worktree had unrelated normal-sync modifications in `hub/design/BOARD-HEADER.md`, `hub/inbox/app.md`, `hub/inbox/app2.md`, and `hub/status/runtime.md`; no worker write caused these.

The reviewed `hub-sync` source establishes the publication seam at lines 109–114: on main it executes `cp -p $ORCH/bin/* hub/kit/bin/` (then removes backup files), followed by normal hub commit/push handling. Therefore the helper's initial absence was not an allowlist omission; it was publication lag, now resolved. No hub-sync or hub-push command was executed by this review.

## Checks

- `bash -n` live `make-child-venv`: PASS.
- `bash -n` live `request-child-venv`: PASS.
- In-memory `compile()`/AST checks on live `bench_store.py`, `verify_dependency_seed.py`, maker `STORE_PY`, and maker `STORE_VERIFY_BODY`: PASS.
- `Store.ensure` signature includes `failure_name`; maker's `Store.ensure` call supplies `failure_name`; maker pins/loads the reviewed helper: PASS.
- Runtime worktree is clean at review base; no source or configuration files changed.
- No maker, requester, Store, imports, provisioning, network, package, or process probe was run.
