# Active future Agent-tip corrections

Scope: finite inventory of future F-final/ZIP-tail inputs that can still resolve Agent to the old `547e10456250c1b5bcf63b44a50c90ff0563ce1e`. Historical census/classification artifacts are listed only as provenance and must not be rewritten.

| Input | Stale assignment/failure mode | Minimal update owner | Required correction |
|---|---|---|---|
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build` (`BRANCH = "tl/integration"`; `build_repo()` resolves `tip` from that branch) | Implicitly consumes whichever local Agent `tl/integration` is mounted; the local Agent ref is stale `547e…` even though the actual hub home integration is `a30e…`. | D135 builder-guard owner (`rt-F-D135-builder-guard-1938`), then Runtime/Farm lead | Future caller must take Agent tip from the concrete D59 pinned-tuple input, verify object/tree identity and reject missing/malformed/mismatched input; no fallback to local `tl/integration`. |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/kits/area-agent/orch/bin/delivery-build` and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/kits/area-farm/orch/bin/delivery-build` (`BRANCH = "tl/integration"`) | Kit copies preserve the same implicit branch lookup. | D135 builder-guard owner / kit publisher | Bind the same explicit tuple field for all repos, with Agent override from D59; preserve defaults only when no pinned tuple is requested. |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/farm/INBOX.md:1643-1651` (18:42Z/18:54Z future ZIPtail request) | Future ZIPtail tuple names Agent `547e…` alongside Runtime `e319…`, App `d5a1…`, Composition `635f…`. | Farm lead with Runtime inbox owner | Replace only the future Agent tuple field with the actual received home object `a30e74e901a28b39c28facba3deb00d76f186e23` / tree `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`, or hold it pending the eventual D59 successor. |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/peer-farm-to-lead-20261025T1902-ZIP-dryrun-confirm.md:2-5` | Active Farm dispatch confirmation requests checkout of Agent `547e…`; it would reproduce the stale proofpin. | Farm lead | Do not dispatch from this four-tuple as written; update the Agent commit/tree from D59 home tuple or return exact missing normal-route input. |
| `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-pin-547e1045` / detached candidate `wt/agt-pin-547e1045` | Explicit old candidate branch/pin (`547e…`) is a historical D108 proofpin, not Agent-home integration. | Runtime/Agent lead; Farm lead for future pin creation | Preserve this pin as historical evidence. Do not retarget it. Create/use a new D59-bound pin only after the owner publishes the tuple. |

## Historical-only inputs not to rewrite

`design/farm-zip-dryrun-1905-*`, `design/rt-F-tail-upstream-census-1844-*`, `workers/rt-F-tail-Agent-A-1928`, `workers/rt-F-tail-Agent-B-1935`, and the older D108/D123 manifests cite `547e…` as captured proof scope. The completed farm dry-run already records the mismatch: home integration was `a30e…`, while detached pin was `547e…`. Those records are immutable historical evidence.

## Repository/script inventory result

No literal `547e10456250c1b5bcf63b44a50c90ff0563ce1e` assignment was found in the Agent, Runtime, App, or Composition product repositories. The risk is in the delivery script's implicit `tl/integration` lookup and in the active orchestration tuple above.

## Placeholder guard

The D59 final tuple remains pending. This note records the exact current home object received by the hub for source census only; it does not invent or authorize a production F-final/ZIP tuple. Main builder guard 1938 owns pinned-tuple input; this worker owns no builder code.
