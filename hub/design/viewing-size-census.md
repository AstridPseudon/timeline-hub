# Viewing actual-current source census

This is the manager-publication payload for the approved Viewing timeline-core
boundary. It corrects the prior partial refresh, which paired Composition
`4788…` with stale Agent `01ee…` and App `a12…` snapshots. It is a measured
source snapshot, not a final M4 freeze, foundation claim, owner claim, or hard
size gate.

## Census timestamp and exact source pins

The census was run on 2026-10-21 UTC after reading the Viewing manager status
and the home integration worktrees. Current source is the committed
`tl/integration` ref in each included home repository. The local integration
ref and its `hub/tl/integration` mirror matched for all three included repos at
measurement time.

| repository | Main baseline commit | Main tree | Main commit time | actual current ref | current tree | current commit time | head verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` | 2026-05-07T14:05:54+02:00 | `tl/integration` at `4788e107f183e0523a740b691a20eb8261d7183c` | `585e8c4784ee78ccbfbff4b6ce26f577b8eda05e` | 2026-10-21T01:06:58+00:00 | VERIFIED CURRENT: manager STATUS advertises `4788…`; local and hub refs match |
| Agent (Astrid/sdk) | `a411628f8fd6129f9c58c332019b56769d997384` | `e0ca791bb8adbf11e25e0e97843aaf246a04f965` | 2026-10-19T21:18:13+02:00 | `tl/integration` at `57d6635616f2982b814cfcc059b670ea1a7c9f2c` | `0174fd49bd175a726a44542d1d6e31bca13c0f02` | 2026-10-21T00:31:00+00:00 | VERIFIED CURRENT: advertised current snapshot and local/hub refs match |
| App (Reigh) | `580508eed1bf6ed95caaf476c9d69a4672472a2f` | `ab3a5e296b01cc5458c88049c9eb5be402a05ccf` | 2026-10-19T21:26:14+02:00 | `tl/integration` at `813a85106ecb4abbaf224081abe6c33b8dab0df7` | `2a19a78bb1bdfb3fd779f568a1b513b094318982` | 2026-10-21T01:01:05+00:00 | VERIFIED CURRENT: latest home parent advertised in peer evidence and local/hub refs match |

Runtime was checked at home integration `9d1c43c647301da48a6e86ad82e466b501bd2418`
(`50e74e3243c5da4cf77b6e6cc76605fae8aeb649`, 2026-10-20T22:50:56+00:00),
with matching local and hub refs, but remains outside the approved Viewing census
boundary and is not counted here.

No newer advertised head was missing from the home mirrors at measurement time.
The older external Gate-6/test tuples (`e7ef…` Composition, and older frozen
consumer inputs) are test inputs, not replacements for the actual current home
integration refs. No unmerged donor or worker ref receives census credit;
donors remain separate until merged into `tl/integration`.

Peer-head evidence read for this refresh:

- Viewing manager `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/STATUS.md`
  (2026-10-21 01:20 UTC) advertises Composition `4788…`.
- Agent current-head evidence is recorded in
  `design/runtime-gate7-current-integration-dryrun.md` and the central
  snapshot records Agent `57d…`.
- App current-parent evidence is recorded in
  `design/peer-app-to-app2-runtime-20261021T0104-parent-ready-nativeproof.md`
  and records App `813a…`.

## Exact canonical counts

Columns are files / bytes / physical lines / nonblank lines. Delta is current
minus the exact Main baseline. Physical lines count committed UTF-8 blob lines,
including blank and comment lines; nonblank lines count lines containing a
non-whitespace character.

| approved owned slice | Main baseline | actual current | delta |
| --- | ---: | ---: | ---: |
| Composition `typescript/src/**`, excluding generated registries/curves and timer declaration | 16 / 45,621 / 1,550 / 1,398 | 79 / 195,818 / 4,526 / 4,175 | +63 / +150,197 / +2,976 / +2,777 |
| Agent `timeline_visualize/**`, excluding schemas, stage/docs, fonts, inspector assets | 54 / 1,253,951 / 27,700 / 24,911 | 56 / 1,304,914 / 28,775 / 25,924 | +2 / +50,963 / +1,075 / +1,013 |
| Agent explicit render/evaluator adapters and `rendering/elements/**` text | 29 / 375,489 / 11,381 / 10,993 | 20 / 363,724 / 11,068 / 10,701 | −9 / −11,765 / −313 / −292 |
| Agent `onscreen.py`, `scene_answers.py` | 1 / 18,156 / 452 / 375 | 2 / 27,895 / 653 / 551 | +1 / +9,739 / +201 / +176 |
| Agent Remotion host, excluding adjacent paths and generated/declaration/test files | 11 / 24,264 / 631 / 573 | 10 / 28,084 / 690 / 630 | −1 / +3,820 / +59 / +57 |
| App non-test source in `PreviewPanel/**`, `compositions/**`, `render/**`, excluding fallback | 29 / 282,934 / 7,533 / 6,932 | 30 / 307,481 / 7,945 / 7,335 | +1 / +24,547 / +412 / +403 |
| **Viewing-owned canonical total** | **140 / 2,000,415 / 49,247 / 45,182** | **197 / 2,227,916 / 53,657 / 49,316** | **+57 / +227,501 / +4,410 / +4,134** |

Compared with the prior partial current snapshot (`53,305` physical /
`48,981` nonblank), the corrected current tuple is **+352 physical / +335
nonblank**, because Agent and App are now measured at the actual home
integration heads rather than `01ee…` and `a12…`. Composition remains the
same `4788…` source in both snapshots.

## Boundary and exclusion notes

- The existing census manifest and read-only Git-blob mechanism were reused
  unchanged; only the three current ref substitutions were refreshed.
- Counts include committed source only. Tests, fixtures, generated registries
  and declarations, vendor copies, archives, stale `dist`, fallback paths, and
  untouched infrastructure remain excluded as already approved.
- The Composition `4788…` merge is included because it is the actual current
  home integration head. Its unmerged package/archive or donor material is not
  counted.
- The Agent `57d…` and App `813a…` heads are current integration snapshots;
  separate unmerged donors are not silently substituted or credited.
- This document makes no deletion-completion, foundation-complete, final ZIP,
  or owner-film assertion. The canonical design census remains unchanged until
  the manager accepts this complete-current proof.

## Reproduction

See the accompanying `COMMAND` for the exact read-only command. It substitutes
the three current commits into
`handoff-vw-m4-size-census-gate-review-script.mjs` and adds only the existing
physical-line field used by the prior census reports; it does not check out,
install, build, or write into any repository.
