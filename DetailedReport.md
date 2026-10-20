# M4 delivery post-refresh check

## Result

The single central named run completed with exit 1. Agent, Runtime, and Composition passed the
reviewed delivery proof. App failed before producing its patch, so this is not a complete
four-repository delivery proof and does not claim the M4 delivery gate or any other gate.

## Exact run

Submitted once:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime delivery-current-integration
```

Result ID waited to completion:

```text
runtime-delivery-current-integration-1020110552-4257
```

The central command was:

```text
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/delivery-build --dry-run --repos "agent runtime app composition"
```

The final wait summary was `fail exit=1 in 144s`. No full suite, browser, localhost, install,
shared-cache write, publish, ZIP, or final-delivery build was run.

## Captured source tuple

The service-owned staging README records these exact heads, `origin/main` refs, and trees:

| Repo | `tl/integration` head / tree | `origin/main` ref / tree | Result |
|---|---|---|---|
| Agent | `5430a9719542880ddf295ae0acd181270aac42ac` / `0be9a236663de18b7614a91c324a75759b105645` | `96b283d5d6fd8031538f881e486bb2ebf45dce75` / `1e31c58ff3aa35229ba07a8f6bb9c04dc31dd795` | PASS |
| Runtime | `8609333456b9537339ee1a5dfc7ffd9609242de8` / `2ae8508a1d3dac62e99c27056585eedc62bf5ff6` | `29d0954b6d78a7d7937d81bc36567b6dee7ca976` / `eb06dfd08e6d489204f03d65e55951bcf521b326` | PASS |
| App | `7bb885b638838588a0dff81b64b7c34960ac07f3` / `065b46ac13026d3e3a1d760b44bab1ab8e1e930e` | `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa` / `85ab85d225f106990cb04b0a22e4eaff1d0c8035` | FAIL |
| Composition | `e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab` / `23a994070b8e25aba18703af1c6a0c840df1ab62` | `67b8aa3d0d6831d3e3504a340ff583c3da253707` / `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` | PASS |

The service snapshot itself records Runtime tree `2ae8508a1d3dac62e99c27056585eedc62bf5ff6`.
The external cache tuple changed while the request was queued; the final build README is the
authoritative captured tuple above. The older Agent cache-key entries (`6a595224...`) were not
used as the reported final head.

## Per-repository proof

- Agent: one patch; fresh-clone patch tree, bundle tree, and integration tree all
  `0be9a236663d` (full values above). Bundle verification/fetch passed.
- Runtime: one patch; fresh-clone patch tree, bundle tree, and integration tree all
  `2ae8508a1d3d`. Bundle verification/fetch passed.
- Composition: one patch; fresh-clone patch tree, bundle tree, and integration tree all
  `23a994070b8e`. Bundle verification/fetch passed. The approved history join remains visible:
  `e80c46b` has second parent `67b8aa3` and message `join history to upstream main 67b8aa3
  (tree unchanged)`. This proof was not hidden or replaced after the App failure.
- App: zero patches. The squash step reported `git log --first-parent ... main..refs/delivery/tip`
  with both refs unavailable in the fresh build repository. The dependent checks then reported
  no `main` checkout, disconnected bundle prerequisites, no bundle tip, and no applied patch.
  The partial App bundle was not accepted as sane.

## Follow-up recommendation

Do not add a product feature or claim a gate. Before another delivery attempt, the Runtime
manager should reproduce only the App source-fetch setup in a private throwaway clone and assert
that the exact two refspecs used by `delivery-build` create `main` and `refs/delivery/tip`.
App is the only source worktree currently shallow (`true`; Agent, Runtime, and Composition are
`false`), despite its local `origin/main` and `tl/integration` refs being present and ancestrally
related. If confirmed, use a complete/non-shallow App source mirror or resolve the two captured
object IDs from a complete source before rerunning the named delivery check. No script change was
made because the exact failure mechanism still needs that isolated confirmation.

## Artifacts and limitations

The central service preserved partial staging at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/build-20261020T110716Z
```

It contains passing Agent/Runtime/Composition patch and bundle artifacts and a failed App bundle,
but no ZIP was written. This report covers patch/bundle application proof only; it says nothing
about client/server compatibility, rendered output, all gates green, owner-film review, macOS, or
the final handoff.
