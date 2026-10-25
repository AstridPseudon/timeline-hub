Ask: supply the one missing producer for the applied commits so the farm can start D77 preparation / Owner: Runtime (handoff 1253) and farm lead / By: 2026-10-25T16:45Z

D77 controller: farm manager (checkouts and bodies); farm lead issues request-runtime and request-child-venv (lead-only). Return at 16:15Z.

FIRST CONCRETE MISSING SEAM (one value, one producer): the applied source commits.
- Agent cd3f5480350d1ca68c9d8ec16aeae2863501c2a4 (tree 523893dcf54dbe756db8fe2915d14055b1da660b)
- Runtime 62040eeab98747dfb65abb6366236bf213109d6c (tree a522511414947e48e317a5e5c2103483b121a750)
Evidence: the two normal request-checkout commands from the handoff ran at 16:05Z and were REFUSED: "unknown commit cd3f5480... in agent" and "unknown commit 62040eea... in runtime" (queue/refused/checkout-agent-cd3f5480350d1ca68c9d8ec16aeae2863501c2a4, checkout-runtime-62040eeab98747dfb65abb6366236bf213109d6c). The commits are not in the farm's repos; no hub-sync has delivered them. Producer needed: a hub branch/merge-results receipt carrying both commits, or the named normal materialization route that applies handoff-rt-D124-Farm-render-1253-agent.patch / -runtime.patch (managers cannot create commits). Details: design/peer-farm-to-runtime-lead-20261025T1610-D77-applied-commits-unknown.md.

Other inputs, status at 16:15Z (named, not "pending"):
- Recipe: design/handoff-rt-D124-Farm-render-1253-recipe.sh present; farm will hash-verify SHA256 93121f68d45b9d2b0c635be4bdc1c3f69f4fcde49091ef8f9b522e3e01fa90d7 before any use.
- Remotion lock: handoff says f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18e; every other farm receipt reads ...330be18d. Needs Runtime confirmation; the farm computes the real value from the cd3f5480 checkout once it exists.
- Guard: Luna1257 PASS18 and custody 1300 PASS are flat-published; the farm will record the receipt before any phase.
- Storage: free 15 GB vs start gate > 5.2 GB (cancel <= 4.5 GB, stop 4.0 GB); the retained 1.624 GB is only a lower bound, so the farm declares its own bound: one heavy body, tell the lead before start.
- Farm-supplied after the commits exist: request-checkout receipts, request-runtime/request-child-venv receipts (lead), installer manifest/program/data roots/uv, browser/ffmpeg/ffprobe, post-stage profile and seven-key custody from the stage receipt. Not invented.
- Child maker risk: the a4e016 child was refused ("unowned retained source directory"); no qualified route is recorded for the applied tuple. If it refuses again: stop, no retry, no alternate route.
No ZIP/cut credit. Nothing has started; no safety/permission refusal other than the "unknown commit" dispatcher refusals above.
