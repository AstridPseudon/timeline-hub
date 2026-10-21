# Canonical1140 command record

Worker: `vw-m3-canonical1140-sole-executor-1145`

Packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-canonical-stage-sort-packet-1140/packet`

Registered exactly:

```text
composition e2e-viewing-canonical1140-preflight-1145 bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-canonical-stage-sort-packet-1140/packet/run.sh --preflight
composition full-e2e-viewing-canonical1140-physical-1145 bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-canonical-stage-sort-packet-1140/packet/run.sh
```

Preflight request/result:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-canonical1140-sole-executor-1145 e2e-viewing-canonical1140-preflight-1145
ID vw-m3-canonical1140-sole-executor-1145-e2e-viewing-canonical1140-preflight-1145-1021114524-6250
PASS exit=0 48s
```

Physical request/result:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-canonical1140-sole-executor-1145 full-e2e-viewing-canonical1140-physical-1145
ID vw-m3-canonical1140-sole-executor-1145-full-e2e-viewing-canonical1140-physical-1145-1021114631-32323
FAIL exit=1 77s; packet-ready.mjs:19 before bodies
```

Five-case counts: discovered 5, executed 0, passed 0, failed 0, not executed
5. No frame/PCM/picture/half-gain result exists. No retry was submitted.
