# OPS Runtime request custody 1351 — independent PASS and conditional install

Independent review PASS and conditional install completed at `2026-10-23T13:54:14Z`.

- Live `$ORCH/bin/make-runtime`: `9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09`
- Exact predecessor backup: `$ORCH/bin/make-runtime.20261023T135414Z.bak`
- Backup SHA-256: `5245f264336d65c4a5847d9e4f05734e77d25ede0dd35d64008e5a4c45aac0e6`
- Live file: root-owned regular `0755`, hash verified after atomic `.new` then `mv` replacement.
- Candidate source: `$ORCH/workers/rt-OPS-runtime-request-custody-1343/evidence/make-runtime.candidate`

The independent private smoke used the unchanged request writer and exact dispatcher RUNTIME branch with `env -i`, a throwaway name, private roots, and no injected `RUNTIME_*` identity variables. Explicit `remotion-env-nodes` (the only approved remote template) carried Agent `f6116e1b658514021cbbf08d5a6f16a240523f1a`, Runtime `8592822fd11275540f596562f43c715676f2bc0f`, and lock `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d` into the emitted env and suite guard. No real provisioning, download, package installation, host script, sync, or Git mutation was performed.

Supported command:

```text
$ORCH/bin/request-runtime agent-remotion-ap2-p1-f611-1351 f6116e1b658514021cbbf08d5a6f16a240523f1a f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d /home/user/work/wt/agt-pin-f6116e1b /home/user/work/wt/rt-pin-8592822f 8592822fd11275540f596562f43c715676f2bc0f remotion-env-nodes
```

The fresh idle proof found no normal non-hidden pending records at install time; the dispatcher heartbeat was current. The worker namespace process view is retained without host-wide claims. The normal hub kit/HEAD publication path was absent from this namespace during a bounded 50-second read-only observation; no direct publication action was taken.

Manager board line:

`KIT CHANGE: make-runtime 9fc7f72a7d03fcb4618310ad57f5c9cf111b78a59b2c02caa702073d0951fd09 — exact Agent/Runtime positional custody carrier; predecessor 5245f264 backed up at 20261023T135414Z.`

Full report: worker `ORCHworkerreport.md`. Evidence and exact custody logs: `$ORCH/workers/rt-OPS-runtime-custody-review-install-1351/evidence/`.

This is an OPS D21 kit change only. Proof remains owner of the fresh remote immutable bench; this does not claim production readiness or P1/P3 credit.
