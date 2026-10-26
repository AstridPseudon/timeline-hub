# D141 cut tuple: upstream tips frozen at 2026-10-25T23:42:41Z (lead fetch; equal to ls-remote)
- agent upstream main = 8b6ed2116fd1803d24b2be5bc08bd9490407fe4a
- app upstream main = 7ca61bb3280beca21d98a854af266a382f7ce5df
- runtime upstream main = fa9cd5464a8b37b02f971de375e56be846cd69e2
- composition upstream main = 67b8aa3d0d6831d3e3504a340ff583c3da253707

Each lane: ONE final merge-forward of integration to its tip above, through the normal reviewed route; then integration is FROZEN for the cut. Record the resulting integration heads below as they land.

## Integration heads after the final merge-forward
- agent: 28e56cacb42d3da85b02e5b3543895b44f3d0f70 (tree 2ebe2ddf5a61; final merge-forward to upstream 8b6ed211 plus Runtime 6a011 provenance; bounded review 0015 PASS; FROZEN 00:27Z 26 Oct)
- app: 5fe3e4debec5fb030f772ca41f16c86cc80e6150 (tree af51793b7cc9; REG#1 fix D141e merged on 867cb273 after independent review 0203 PASS; supersedes 867cb273 at 02:13Z 26 Oct)
- composition: 635f4de06fda (upstream 67b8aa3d IS an ancestor, verified by main 2026-10-26T00:41:17Z; no merge needed)
- runtime: 6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d (frozen; upstream fa9cd5464a8b; independent rt-U1-D141-final-review-2350 PASS; author119 PASS)
