# F/D141i final command validation

Commands and results:

```text
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-command-return-0238/evidence/measurement-command.sh
=> PASS
bash -n /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh
=> PASS
```

A read-only standard-library validator checked JSON/hash/shlex data, exact poison one-field delta, all four source tuple commit/tree/origin/clean receipts, live physical hashes, exact 22-root selector membership and order, exact pytest settings, JUnit path joins, distinct input/output roots, one service row/body invocation, thresholds, and durable custody fields.

```text
/home/user/work/venv-agent/bin/python -P <read-only final wrapper/manifest/source validator>
=> PASS
```

The validator recorded:

- wrapper SHA: `87384df6e825af2e211b67135ec944aa51f855251e195bb955a8832c92ab0381`
- positive manifest SHA: `94d8d5813c7f96259547bc273cad388d6fefe60126c33fc5faa68385c56f8707`
- poison manifest SHA: `c1e9ae00cc7c4b94262b9277f3079e1234524d90610cbe807945961d5379fb4c`
- service-row SHA: `e29834abb52af15074269c6b7f00d5549943a966c79a74150a696ad09038a844`
- protected launcher SHA: `9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd`

The helper-only harness was built from the wrapper's authored function definitions through `finish()` and did not enter the wrapper main/body:

```text
<helper harness>
=> default=78 explicit=83 read=97 write=98
```

The genuine production launcher was run in `dry` mode only, with the retained stub:

```text
env P4_D73_EVIDENCE=<fresh-temp>/positive P4_D73_REQUEST_ID=agent-core-full-positive-final P4_STUB_COUNT=<fresh-temp>/positive/count /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh <final-positive.manifest> dry -- <retained-stub>
=> exit 17; preflight exit 0; one stub call

env P4_D73_EVIDENCE=<fresh-temp>/poison P4_D73_REQUEST_ID=agent-core-full-poison-final P4_STUB_COUNT=<fresh-temp>/poison/count /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh <final-poison.manifest> dry -- <retained-stub>
=> exit 1; D73 launcher: agent SHA mismatch; zero stub calls
```

Fresh control root: `/tmp/w-9605066ade/d141i-final-controls.6fUdp9`. The positive materialized manifest SHA equals the serialized positive SHA. The poison manifest was not materialized because the launcher refused at the agent-SHA guard. Stub SHA is `38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0`.

Not run: measurement body, pytest, collection, provider/product execution, request-test, full/targeted suite, install/acquisition, queue/admission operation, or any source/product/pin/launcher/kit change.

A further read-only environment-receipt check passed for the normal manifest maker, pinned launcher, profile archive, profile registry, installed Composition package, and Agent runtime lock. The mandated launcher dry preflight performed only its own built-in import guard; no standalone provider/product import or execution was run.
