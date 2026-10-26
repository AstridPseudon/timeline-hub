# D141 cut tuple: upstream tips frozen at 2026-10-25T23:42:41Z (lead fetch; equal to ls-remote)
- agent upstream main = 8b6ed2116fd1803d24b2be5bc08bd9490407fe4a
- app upstream main = 7ca61bb3280beca21d98a854af266a382f7ce5df
- runtime upstream main = fa9cd5464a8b37b02f971de375e56be846cd69e2
- composition upstream main = 67b8aa3d0d6831d3e3504a340ff583c3da253707

Each lane: ONE final merge-forward of integration to its tip above, through the normal reviewed route; then integration is FROZEN for the cut. Record the resulting integration heads below as they land.

## Integration heads after the final merge-forward
- agent: 28e56cacb42d3da85b02e5b3543895b44f3d0f70 (tree 2ebe2ddf5a61; final merge-forward to upstream 8b6ed211 plus Runtime 6a011 provenance; bounded review 0015 PASS; FROZEN 00:27Z 26 Oct)
- app: 520d7e4fc12a03392afaed3f486aba34a2b5c319 (tree 70ad390c56b0; = 5fe3e4de + D141d placement expectation, review 0243 PASS; FROZEN 02:53Z 26 Oct; supersedes 867cb273/5fe3e4de)
- composition: 635f4de06fda (upstream 67b8aa3d IS an ancestor, verified by main 2026-10-26T00:41:17Z; no merge needed)
- runtime: 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d (frozen; upstream fa9cd5464a8b; independent rt-U1-D141-final-review-2350 PASS; author119 PASS)

## Freeze 2 tuple (D141l, recorded 2026-10-26T05:00Z by main)
| Repo | Upstream base (freeze 2) | Integration head | Tree | Receipt |
|---|---|---|---|---|
| agent | 64197afa297f | 8585ed9c0404d0187b2ce70242d25114a32747c2 | 92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c | Sol 0408 merge, independent review 0432 PASS_SOURCE, merges.log 04:41:28Z |
| app | d822d2f5d2bd | 5344c53e3063001bb3255bd0c9cd32cc5e77967f | dd989783046aeff652486a1ba39db42aea86e201 | merge 8f278b91 plus manifest pin to Agent 8585ed9c, review 0454 PASS zero findings, design/app-D141p-freeze2-source-home-0459.json |
| runtime | fa9cd5464a8b (unchanged) | 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d | ac5b8627 | freeze 1 |
| composition | 67b8aa3d (unchanged) | 635f4de06fda | 5ab5191a2969 | freeze 1 |

These are source qualifications only: no GO, REG0, build or ZIP claim. Still owed on freeze 2:
- Agent: the full rerun pair (merged head and pristine 64197afa) plus P4.
- App: P1, P2-six and P3, plus the popup ADD (D141j); unit suites on the new head and pristine d822 with real Node coverage.
- Runtime: the targeted-15 and P5 receipts.

App upstream had moved on to fc24f849 at 04:39Z. It gets one catch-up merge just before F-final (D141l item 5).

**Update 05:39Z:** the Runtime integration head moved to 95d98f0383 after two REG fixes (857e4c3b, 95d98f03). App and Agent re-pin to it through their normal receiving rows.

**Update 05:48Z:** App integration head = 4de54db14bdc9ddc2ce2e5887258b03acbffd30d (tree 84c3fb7f73f08c22220f8e808962fe3f24aaa0aa). It supersedes 5344c53e and is pinned to Runtime 95d98f03 (tree 78df31d6) and Agent 8585ed9c (tree 92a3ffdb). Review 0540 PASS; receipt design/app-D141s-postREG-source-home-0545.json. Current freeze-2 tuple: **App 4de54db1 / Agent 8585ed9c / Runtime 95d98f03 / Composition 635f4de0.** Agent still has to adopt Runtime 95d98f03 (U4a post-REG row, queued behind the REG author on the disk-held box).
