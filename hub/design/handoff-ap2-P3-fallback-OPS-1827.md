# P3 fallback OPS handoff — FINAL PASS

The existing `app/ap2-P3-gate5-h6-0348` row is ready for the conditional
18:50 fallback. Only App identity substitutions were made:

- `58bf24ce6fc57c7477a7fa45d94b20dfb12c5e92` →
  `2107e1870e51c650d59315f4cc1ab6af338f198c`
- `07f99905cb822656a2d3675a782b72e6c1fb5ecb` →
  `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`

Agent `079580ca46af77e0292d49dc34386b25c8391f99` / tree
`2deab1a1494fbccfce5e9235412bacb8a949c0cd`, Runtime
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` / tree
`f79a2355cfb39d9ada7721978bd20d5702105778`, existing SUCCESS benches, Gate5
blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`, original invocation tail,
55 guards, 21 AST assertions, and C0 request/reply contract fields are retained
by exact mechanical identity reversal. The current App source is
`2107e1870e51c650d59315f4cc1ab6af338f198c` / tree
`a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`.

The preserved C0 fields are the complete request (`api_version`, scope/base
IDs, commands, label, steps with id/label/intent/tags/command ordinals/patch/
reads, merge, reads, idempotency key, dry-run, source, rationale, group ID) and
complete `{data, receipt}` accepted/merged/historical/conflict/invalid/preview
reply shapes, including head/document/records/dependencies/effects/steps/
history/undo steps, `would_status`, conflict reason+head, and invalid
code/path/hint/suggested command.

Outside-P3 config SHA is unchanged:
`e6d4d240181975d560f6c8e7177911dcc231ae7229fabd89eee5653bd5de0153`.
The final P3 row SHA (excluding newline) is
`1a741bd7a8b9323a837160bf6b3f79e8a6f76bbac44c315eb7ceda938946be34`.
Outer/inner Bash syntax both pass. Offline positive reaches only a synthetic
marker; App-source/tree/body negatives exit 2 before it.

Farm remains sole P3 then P2 runner. If Farm has no P3 test ID/dispatch at
18:50, the manager may submit this exact command, which was **not executed**:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$("$ORCH/bin/request-test" integration:app ap2-P3-gate5-h6-0348 --no-cache) && "$ORCH/bin/wait-test" "$R"
```

Preflight/body/native seed are NOTRUN. This handoff is static readiness only;
historical source and bench evidence is not a fresh product GO.
