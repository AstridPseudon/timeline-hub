# Agent box: /home/user/work/wt clean-checkout inventory (READ-ONLY; nothing deleted, 13:30Z)

Method: per worktree, du -sb size; git status --porcelain empty = clean; 'on hub/upstream ref' = HEAD is contained by at least one remote-tracking ref (git branch -r --contains HEAD) in that worktree's repo; KEEP = workers/<name>/KEEP marker (reason first 90 chars); running = running marker without ended; leased = named in managers/*/notes lease/ACTIVE files.

Total: 63 worktrees, 4653 MB.

| status | reachable | KEEP | running | count | MB |
|---|---|---|---|---:|---:|
| CLEAN | on-ref | KEEP | idle | 52 | 4308 |
| CLEAN | on-ref | KEEP | RUNNING | 1 | 179 |
| DIRTY | on-ref | no-KEEP | idle | 1 | 109 |
| CLEAN | on-ref | no-KEEP | idle | 8 | 57 |
| DIRTY | on-ref | KEEP | idle | 1 | 0 |

## A. CLEAN, HEAD on a hub/upstream ref, KEEP-marked, idle (52 / 4308 MB): recreatable from git, but KEEP-protected so recycle refuses them

| worktree | MB | HEAD | kind | KEEP reason |
|---|---:|---|---|---|
| agt-U2-D141ee-writers15-decision-next-review | 180 | c61c56d2f2 | worker | D141ii protected writer15 migration source and raw22case evidence; retain through integrat |
| agt-U2-D141ii-writers15-return-1319 | 179 | 3638da7233 | worker | Open D141ii writer return and protected review; retain source and raw proof.  |
| app-pin-867cb273 | 150 | 867cb2737a | pin |  |
| app-pin-96d4754b | 150 | 96d4754b4e | pin |  |
| app-pin-d8a1cd40 | 150 | d8a1cd40b8 | pin |  |
| app-pin-7ca61bb3 | 142 | 7ca61bb328 | pin |  |
| agt-U2-D141ee-inverse38-decision-next-review | 129 | 2ffdfdb7d7 | worker | D141ii protected exact source and targeted raw evidence; retain through final integrated p |
| agt-pin-070dfc5e | 118 | 070dfc5ef4 | pin |  |
| agt-pin-28e56cac | 118 | 28e56cacb4 | pin |  |
| agt-F-D141b-pristine-controller-0035 | 117 | 28e56cacb4 | worker |  |
| agt-F-D141ee-installer2-scope-1134 | 117 | 445b9c1a7f | worker |  |
| agt-F-D141ee-installer2-scope-review-1137 | 117 | 445b9c1a7f | worker |  |
| agt-F-D141ee-inverse38-scope-1134 | 117 | 445b9c1a7f | worker |  |
| agt-F-D141ee-inverse38-scope-review-1137 | 117 | 445b9c1a7f | worker |  |
| agt-F-D141ee-writers15-return-review-1148 | 117 | 445b9c1a7f | worker |  |
| agt-F-D141ee-writers15-scope-1134 | 117 | 445b9c1a7f | worker |  |
| agt-F-D141ee-writers15-scope-return-1143 | 117 | 445b9c1a7f | worker |  |
| agt-F-D141ee-writers15-scope-review-1137 | 117 | 445b9c1a7f | worker |  |
| agt-P4-D141-body-continuation-0105 | 117 | 271095edf0 | worker |  |
| agt-P4-D141-bound-proof-controller-0128 | 117 | 271095edf0 | worker |  |
| agt-U2-D141ee-installer2-decision-next-review | 117 | e8d1598458 | worker | D141ii protected retirement source and exact owner quote; raw targeted XML and trace neede |
| agt-U2-D141ee-installer2-decision-next | 117 | e8d1598458 | worker | D141ii protected exact source and targeted raw evidence; retain through final integrated p |
| agt-U2-D141ee-inverse38-decision-next | 117 | 2ffdfdb7d7 | worker | D141ii active exact approved author and protected review; retain raw targeted XML and curr |
| agt-U2-D141ee-writers15-decision-next | 117 | c61c56d2f2 | worker | D141ii active exact approved author and protected review; retain raw targeted XML and curr |
| agt-pin-21c6f514 | 117 | 21c6f51458 | pin |  |
| agt-pin-3b2db4bd | 117 | 3b2db4bdf9 | pin |  |
| agt-pin-4c4ee35d | 117 | 4c4ee35d56 | pin |  |
| agt-pin-a4e016b6 | 117 | a4e016b6a9 | pin |  |
| agt-pin-bae5ab76 | 117 | bae5ab76f0 | pin |  |
| agt-pin-c2a63bbe | 117 | c2a63bbee9 | pin |  |
| agt-F-final-source-join-0816 | 116 | 0c2c28da4f | worker | Keep exact 0c2c qualified service execution target through the single planned ABA original |
| agt-pin-64197afa | 107 | 64197afa29 | pin |  |
| agt-pin-8b6ed211 | 107 | 8b6ed2116f | pin |  |
| rt-pin-1daca2a3 | 23 | 1daca2a33f | pin |  |
| rt-pin-369ffa7c | 20 | 369ffa7c00 | pin |  |
| rt-pin-5e9ad1c6 | 20 | 5e9ad1c6f7 | pin |  |
| rt-pin-6a011d58 | 20 | 6a011d58e6 | pin |  |
| rt-pin-ab1e4f61 | 20 | ab1e4f6141 | pin |  |
| rt-pin-68935201 | 19 | 689352013e | pin |  |
| rt-pin-732c48c6 | 19 | 732c48c6f5 | pin |  |
| rt-pin-bc04caa2 | 19 | bc04caa23f | pin |  |
| rt-pin-d23a8e0d | 19 | d23a8e0d24 | pin |  |
| rt-pin-dc55b8bc | 19 | dc55b8bc6e | pin |  |
| rt-pin-fa9cd546 | 6 | fa9cd5464a | pin |  |
| agt-F-D141l-fullpair-controller-next | 1 | a5f1c40b47 | worker | KEEP |
| agt-F-D141i-corrected-controller-0321 | 0 | 635f4de06f | worker | KEEP  |
| agt-F-D141i-terminal-final-review-0318 | 0 | 635f4de06f | worker |  |
| agt-F-D141l-binding-return-0735 | 0 | 6a2d1c22ec | worker | Open D141l binding return0735 source/control evidence; /tmp/claude-0/-home-user-repo/7dc61 |
| agt-F-D141l-command-sol-0638 | 0 | 635f4de06f | worker |  |
| agt-F-D141l-sol-review-0707 | 0 | 635f4de06f | worker |  |
| vw-pin-635f4de0 | 0 | 635f4de06f | pin |  |
| vw-pin-67b8aa3d | 0 | 67b8aa3d0d | pin |  |

## B. CLEAN, on ref, NO KEEP marker (8 / 57 MB): not eligible only if live/leased

| worktree | MB | HEAD | kind | KEEP reason |
|---|---:|---|---|---|
| rt-pin-20207411 | 8 | 2020741107 | pin | - |
| rt-pin-7d1cfa6b | 8 | 7d1cfa6b1d | pin | - |
| rt-pin-a6a11a80 | 8 | a6a11a806a | pin | - |
| rt-pin-2c4ac180 | 7 | 2c4ac180c2 | pin | - |
| rt-pin-94114269 | 7 | 94114269d1 | pin | - |
| rt-pin-a0dca169 | 7 | a0dca16975 | pin | - |
| rt-m2-null-speed-clean-candidate | 6 | 4c145dc621 | worker | - |
| rt-m2-track-public-export | 6 | 6be970633c | worker | - |

## C. Everything else (dirty, not on a ref, or running): NOT proposed (3 / 288 MB)

| worktree | MB | HEAD | kind | KEEP reason |
|---|---:|---|---|---|
| agt-U2-D141ii-writers15-return-review-next | 179 | 3638da7233 | worker | Open D141ii writers protected return review; retain source and raw.  |
| agt-G2-open-commit | 109 | a086cc6db7 | worker | - |
| agt-F-D141l-controller-binding-prep-0718 | 0 | 6a2d1c22ec | worker |  |

Caveats: (1) 'on ref' means reachable from a remote-tracking ref in the checkout's own repo; it does not verify the hub copy is current. (2) The pins (agt-pin-28e56cac, 8585, 432f, ecdc, 64197 pristine, etc.) that still serve a pending proof or are cited by a receipt stay protected until the owner or MAIN says otherwise. (3) Nothing here was changed; a recycle would be bin/recycle per worktree after KEEP removal, which is the owner's call.
