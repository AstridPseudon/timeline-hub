# V3 packaging automatic safety refusal — STOPPED

Owner: orchestrator/lead. Worker vw-V3-pack-once (Composition635f4de06) log records an automatic command rejection at23:46:36Z: `rm -f style commands are not permitted. Use a safer approach`. The rejected composite command combined npm pack, archive rename and private cache cleanup. This is a classifier/safety refusal, not an ordinary localhost/git sandbox limitation.

Manager discovered it during completion/progress audit23:48Z, immediately queued bin/request-stop vw-V3-pack-once with the refusal reason. V3 packaging/smoke/adoption is HELD. Do not retry the rejected cleanup, use another deletion implementation, repack, continue consumer adoption or infer a usable artifact. The worker log appears to show subsequent packaging/smoke attempts before manager intervention; their outputs are explicitly unqualified, no adoption/merge request authorized. Preserve evidence, no cleanup of this worker tree/archive/cache.

Need orchestrator resolution of the refusal and worker stop receipt. Existing app-pin cleanup denial remains separately parked; no retry there. Unrelated V1 repairs and V4 workers may continue within their original scope but must stop/report any own safety/permission denial. No alternate package or install route is requested here.
