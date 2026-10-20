# App root8130 current browser gate

## Result

Blocked: the required native lane qualified, but the separate fresh cold-open
lane's product assertion passed while its shared-cache postflight was invalidated
by an unrelated central full App run mutating the shared `.vite-temp` directory.
No App product or test files were changed. This report does not claim a later
source or d874's separate evidence, and it makes no M2 exit claim.

## Exact source tuple

| Source | Exact value |
| --- | --- |
| App | HEAD `3599fc49ad76dfdd7847ab4c813fc9317a0304eb`; tree `74130f681f6b0c87a7c61cb33d4ae6a092c03046` |
| Agent safety keeper | HEAD `8130a401bf44a518d5a40ae274d398b8c560be55`; tree `236c3e57e0265c52b81ba8085de3193026176bff`; keeper result `KEEP` |
| Runtime keeper/producer | HEAD `2c4ac180c2220bdad966bc01e95ad230e99ce26a`; tree `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Runtime/client | `workspace.v1` / `0.2.13` |
| Schema | `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4` |
| Runtime artifact | `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`; normal manifest count 75 |
| Component manifest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| App normal lock | `runtime.lock.json` SHA-256 `550de9dc3269380c79f44a6db4c87a5d5459058d550ae49e635a6dda809e76a2`; 13 files |
| Agent normal lock | `runtime.lock.json` SHA-256 `c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311`; 15 files |
| Public12 source | tracked public source SHA-256 `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`; `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` unset |
| Composition public12 | archive SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; 77 regular members; React/React DOM `18.3.1`; Remotion/media/layout-utils `4.0.509` |
| Browser | Chromium `141.0.7390.37`; SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95` |

The keeper report is [app-agent8130-safety-source-keeper.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-agent8130-safety-source-keeper.md).

## Compatibility decision

The Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` → `8130a401bf44a518d5a40ae274d398b8c560be55` delta changes 57 paths, concentrated in selected-parameter authority, command recording/validation, and rendering/source preparation. `git diff --name-only ... | rg -i 'track|label'` returned zero paths. Therefore regularlabel3 was not requested; the source analysis found no relevant track-set delta. Existing d874 evidence is not reused as evidence for this tuple.

## Central lanes

The strict runner used private module/cache overlays, exact 40-character SHA
preflight, normal 75-artifact/locks/source guards, public12 77-member and peer
checks, Chrome141, and short `TMPDIR=/tmp/tl13-root8130`. Runner hashes were:
`run-lane.sh` `ebb65e52bc0fb25aac9c5fdcd6719392a07c9892a930f9b3dcbf23dae38308a7`,
`run-selected.mjs` `bfa4d0c6d3009f66977eb6e09aa446575e53efb63e14e98e8d8878213c07b908`,
`prepare-overlay.py` `3e304cc8c5a24863dd7c08613a30f077915ee3c8aaa06d98694dad8c40043fe9`,
`audit.py` `4a81d012c5b2676c458d7e92241864e6fd7a2ef95ba2b41105490a99f1e2d259`,
and `public-source.py` `1452b2098b7360b85521fc38789ca30cf98416419231f2ea01ac442f3796ef7e`.

1. Initial native environment attempt, TestID
   `app-e2e-root8130-current013-74130f68-agent8130-runnereb-bundle-native3-1020151417-21429`:
   3/3 product tests passed, but postflight failed because shared
   `/home/user/work/app/node_modules/.vite-temp` mtime changed. Not counted.
2. Repaired native3, TestID
   `app-e2e-root8130-current013-74130f68-agent8130-runnerfix-native3-1020151812-166`:
   **PASS**, 3/3 in 3.0m:
   - M1 real lost durable ACK/dependent B/reopen/restart/retry/undo;
   - M2 real Gate 5 lost ACK/new gesture/restart/undo;
   - M1 real dependency conflict preserves B guards/pending identity.
   Hosted build, Chromium, source fingerprints, normal locks, 75 artifacts,
   public12 77 members/peers, and shared-cache guards passed.
3. Separate fresh cold-open1, TestID
   `app-e2e-root8130-current013-74130f68-agent8130-runnerfix-cold-open1-1020152146-19811`:
   product result **1/1 passed** — `track-label-command.spec.ts:525`, “M2
   cold-open ordinary Unicode track rename uses the initial head and guarded UI
   undo” — but postflight failed because the unrelated central full run changed
   the shared `.vite-temp` mtime. The source/public/75/77/peer guards passed;
   this lane is not a clean qualification result.

No full suite, install, TypeScript check, frame/audio PCM, or local browser/build
run was performed by this worker. The remaining limit is a fresh cold-open1
rerun after competing central jobs release the shared cache; no product failure
was observed.
