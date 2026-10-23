# Handoff: P3 15659 retained trace-custody review

## Verdict

**INSUFFICIENTEVIDENCE.** The new retained packet is custody-identifiable but
causally incomplete. It preserves only the original Gate5 failure at
`openCommandTimeline`: `ready: false` after the 90-second fresh-owner wait,
224 s total, before the first gesture. It does not prove which readiness stage
failed.

Packet SHA-256:
`8bd6a34f23bdd6a26862790419b9b77f6e02600f1b2963b2b962c1dbc95c3c98`.

`trace.zip`, `error-context.md`, and the snapshot directory are LOST. Mounted
identity, basis GET, authenticated identity/scope, owner ID/settled record,
runtime connection state, and predicate diagnostics are absent. Preflight
`17114` GREEN/97 s is distinct setup/native-seed evidence and does not supply
those missing facts.

## Source result

App `tl/integration` is verified at commit
`2107e1870e51c650d59315f4cc1ab6af338f198c`, tree
`a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`. The P3 source guard is exact HEAD
or an exact full-parent-list snapshot match plus that tree; it is not generic
ancestry. The logged `43b71a9e` App object is unavailable locally, so its
historical `%P`/`%T` cannot be proven and it must remain unresolved.

The packet's Agent `787...` `ext` value is cache-key/integration metadata.
P3's actual pinned Agent is `079580ca...`; without direct module-origin
projection, neither value may be relabeled as the runtime import source.
Runtime pin `2a9e347f...` remains unchanged.

Original Gate5 body remains exact: blob
`37caf28577d42fbe98afd2320dffa3c72e6e74b1`, SHA-256
`0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`.

## Finite safe request to Farm/App

Return only the following projections if still available: exact `ext` lines
and hash; exact `snap` tree/key/worktree lines and hash; exact P3 row hash/bytes;
historical snapshot `%H/%P/%T` or explicit unavailable; one actual-run source
tuple plus resolved module origins/source commits; and pre-gesture basis
status/head pair, identity presence/scope, owner create/settled/pending/intents
state, and error code/class. Do not send whole logs/traces or credentials.

If these projections cannot identify the basis, authenticated-identity, or
owner-settlement stage, retain this verdict. No product causal fix is justified
without the actual cause.

## Preserved obligations

The original Gate5 body and full v2 request/reply contract remain required;
there is no P3 credit for full v2, gestures, undo, or zero-old-route traffic.
No browser/HTTP/socket/body/service/graph/install/provision/retry/full run or
permission workaround was performed. The existing Farm graph denial and STOP
request remain STOPPED.

