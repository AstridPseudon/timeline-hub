# Dead worker finalization needs lead tooling — 15:20 UTC
Session restart killed all four prior live workers (lead15:16 inbox confirms); stale running markers remain.
request-stop twice refused: unknown arg ap2-m2-<name>; STOP requests apparently dispatched as normal worker arguments. Safe token-only retry also refused. No .git mutations attempted.
Please repair/restart stop routing and finalize own orphans duplicate-native-capture, ordinary-native-parity-review, elements-serializer-source-review, parentmedia-source-review, preserving WIP.
Fresh resume workers build/recover existing source; useful new worker capacity maintained. This does not block the rest of M2.
Recommended: lead runs bin/stop-worker on these four outside sandbox, then confirm recorded branches; do not discard dirty WIP.
Not covered because: dispatcher rejects the prescribed management operation; manager cannot finalize Git state in read-only .git sandbox.
Rule that would let me decide next time: a functioning outside-sandbox orphan-finalization queue, or documented alternate request accepted by this dispatcher.
