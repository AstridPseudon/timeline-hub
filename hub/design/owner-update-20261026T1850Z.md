# Timeline: owner update, H93 (18:50 UTC, 26 Oct)

## The headline
- **The ZIP is built.** All four repos pass: each squashed patch applies cleanly to its upstream base and reproduces our final version exactly.
- File: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/delivery/timeline-delivery-20261026T183845Z.zip` (15.3 MiB)
- sha256: `5bf110face517d044e7d94f7476936af5eb99e76b3d33aebae0f4cea06406d9a` (sidecar `.sha256` next to it)
- **One independent review is running** (Runtime): it re-applies each patch on a fresh repo at the exact base, checks the bundles and the README. ETA about 20 min.

## What's in it
| Repo | Upstream base | Our final version | Tree |
|---|---|---|---|
| Agent | 64197afa (= upstream main now) | ec0a9f5b | 83b84c79 |
| Runtime | fa9cd546 (= upstream main now) | 95d98f03 | 78df31d6 |
| App | fc24f849 (your option B; upstream main is now 4e667aa5) | abac6c80 | e2632a4f |
| Composition | 67b8aa3d (= upstream main now) | 635f4de0 | 5ab5191a |

Plus one bundle per repo, the README, SHA256SUMS and the two owner-film extras. Known gaps, documented in the README: SWAP, Element, popup ADD.

Note: the README's proof sections refer to App 82e9e13d. The shipped App abac6c80 is 82e9e13d plus the final pin and metadata pass (only the manifest's Agent SHA and provenance changed; tested in D141v).

## Numbers
| | H90 (15:40) | **H93 (18:50)** |
|---|---|---|
| Done | ~95% | **~99%** (ZIP built; review pending) |
| Regressions vs plain upstream | 0 in all four | 0 in all four |

## Blockers hit since 15:40, and the deeper fix
| Blocker | Handling | Deeper fix |
|---|---|---|
| Disk short on main (twice) | You approved removing 3 pins, then old build temp and 2 idle venvs | The real peak was measured at ~1.8 GB for the App check, not the 1.3 GB estimated. Floors will be set from measured peaks |
| Test scripts reused fixed output paths | Repaired | Every check run gets its own fresh folder (lesson #109) |
| Repairs fixed one error per round | Whole-check repair brief | Repairers rerun the whole check and list every failure (#110) |
| The launcher failed at start, and the checks missed it | Fixed and reviewed | Checks must run the exact real command (#111) |
| Our own safety check refused the shared /tmp | One private-temp re-run (you approved) | Private temp folder becomes the default for all tests (#112) |
| The build wrapper dropped an argument and hid its own error | Main found it and ran the build tool directly | The wrapper is removed from the delivery path |

## Opus second opinion (headline)
"delivery-build's PASS shows the patches round-trip against each repo's base. Before handing it over, check it the way a recipient would." Acted on: I confirmed all four bases exist in live upstream history (fetched 18:48Z), and the independent review re-applies each patch on fresh repos. Its other points are next, below.

## Next (after the review)
1. One kit-hardening round, no new features: private temp by default; checks run the real command; per-run folders; an asserted base in the tuple; temp cleanup that survives a kill; floors from measured peaks.
2. App catch-up onto the latest upstream (eac97ea5), then the shot-layering release, then minimal extensibility (~3 weeks).
3. Your rule that deletions need your approval is back in force from now on. Your "just do it" covered today's ZIP push only.

## Your to-dos
None for the ZIP. When the review passes I'll send the final confirmation.
