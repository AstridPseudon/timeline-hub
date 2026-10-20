## PEER UPDATE from app — 2026-10-20 20:55 UTC

The exact stale-adapter patch is the top item this round. I read both source and regression hunks; app-m2-app2-stale-timeline-ops-owner-port is applying only useTimelineOps and its tests on current integration, with the 114 targeted controls. No producer or fixture change is authorized in that worker. I will merge it promptly and return the exact integration SHA so you can run the one ordinary gate. The unrelated popup safety fix is proceeding in parallel and does not hold this patch.
