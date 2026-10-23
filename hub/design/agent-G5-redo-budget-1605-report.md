# G5 observer budget diagnostic — agt-G5-redo-budget-sol-1605

**Capture PASS; public redo FAIL (HTTP 409 inverse_conflict).** One authorized invocation, exit 1, complete final packet after 19.629248s. No timeout, rerun, product change, inverse change, or body/assertion change. Live work stopped at this failure.

## Observed result and owner

Genesis, forward restructure and whole undo completed. Public redo `inverse-redo` entered the Agent provider and threw at `_recording.py:286`, called by `inverse.py:640` (`apply_inverse`), through `commands.py:250` and `commit.py:1072`. Agent translated the actual CommandError at `commit.py:1204` to CommitRejected; Runtime surfaced HTTP 409 `conflict` / `inverse_conflict`, and Agent `sync.py:558` raised CommitConflict. The chained provider traceback and actual guard locals are retained, together with Runtime failure frames and full original error envelope.

The rejected address is `ref="parent"`, `path=["config"]`. Expected/base contains `registry: {}`; observed actual/theirs omits `registry`. All other keys/values at that address compare equal. The guard's six locals (`actual`, `expected`, `kind`, `path`, `ref`, `state`) are captured using the lossless codec; arbitrary state object internals remain explicit type metadata. Precise observed owner: **Agent provider inverse/guard boundary**, not a Runtime SQL failure. This identifies the throw and mismatch, not the code that originally removed/introduced the registry field. No source correction or common-cause attribution to a29df is justified here.

Before/after redo document, head, history and all 266 SQL dump lines compare exactly equal. No redo preview or accept port call occurred. Later overlap assertions remain unreached; their original expectations and c271 body remain untouched.

## Offline audit and budget decision

The immutable 6bb399e… packet verifies 105/105 canonical content hashes and contiguous sequences. Resolving duplicate references yields 12 genesis and 93 forward observations (the old manifest's 28 phase=None records were unresolved duplicates). No serializer exception or redo result is present. Exit 124 at the explicit 30s boundary is the sole observed 1602 termination mechanism. The 1456 record's separate preflight24.16s + body11.56s measurements total35.72s and show that 30s was not a defensible diagnostic budget; they are not a measured setup cost for this exact observer. This new run completed below30s, so it cannot establish why historical execution was slower or prove budget was the only latent fault. It does show the corrected observer reaches the real redo boundary without another harness failure.

D21's single allowed diagnostic used an external finite180s limit covering imports, fixture setup, capture/fsync, scenario and cleanup. Existing product/test timeouts were unchanged. The new observer records durable import/fixture/scenario progress, phase SQL/head/origins and state snapshots, preserving all observed JSON and authorization/admission facts. It delegates the unchanged 1534 scenario and all provider/guard calls; no trace hooks or alternate executor/history implementation are installed.

## Sources, commands and evidence

- Agent `91ac58a9fc6f1f752be16c0e4b8a1bf17095acee`; Runtime `9ce4242bc01f100bab9efc51032a73985cefb2b2`.
- Original body6798bytes SHA-256 `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`.
- Original1534 source SHA-256 `153be3ff0db9e473bde9289e9964ea7900e8666713073677a8d4251c42c91740`; original1552 SHA-256 `2188e04aeafd32e088f59438bac8efd56ff4a7cd67d80c8b8635a6c7010fb3d3`. Both unchanged.
- [New observer](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-redo-budget-1605-observer.py), SHA-256 `6f8b44eac8d94d78be1939b14c5d8b2190a9e4e9d597bd222e37ab78c2f2d9a7`.
- [Immutable complete flat packet](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/evidence/agent-G5-redo-budget-1605-7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15.packet.jsonl), SHA-256 `7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15`;320events /24,089,759bytes. Kept outside design because design forbids multi-MB artifacts. Every event hash and dedup reference verified; final aggregate is event320.
- [Manifest](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-redo-budget-1605-7ab92b619cbe6466b782852afd63c46309722d6d65d88f8fbb8c1e93111a6c15.manifest.json), including source/phase/throw details and85 same-process final module origins. All Agent/Runtime origins resolve to their exact pinned worktrees.
- [Offline audit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/offline-audit.json), [preflight](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/preflight.json), [analysis](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/analysis.json), [invocation rationale](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/invocation.md).

Exact offline preflight command (PASS:10 checks + inherited5-check smoke):

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9ce4242b PYTHONPATH=/home/user/work/wt/agt-G5-redo-budget-sol-1605:/home/user/work/wt/rt-pin-9ce4242b:/home/user/work/wt/rt-pin-9ce4242b/packages/python TMPDIR=/tmp/w-027387f013 /home/user/work/venv-agent/bin/python /tmp/w-027387f013/preflight.py
```

This compiled the new source; verified original hashes/body/pins/clean trees; imported exact origins; exercised callable and cycle encoding, critical JSON/auth roundtrip, fsync/readback, and wrapper return/exception identity/order using a synthetic provider only. It did not instantiate the real fixture or run the body.

Exact live command (executed once; exit1; full final diagnostic retained):

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9ce4242b PYTHONPATH=/home/user/work/wt/agt-G5-redo-budget-sol-1605:/home/user/work/wt/rt-pin-9ce4242b:/home/user/work/wt/rt-pin-9ce4242b/packages/python TMPDIR=/tmp/w-027387f013 timeout 180s /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-G5-redo-budget-1605-observer.py --agent-root /home/user/work/wt/agt-G5-redo-budget-sol-1605 --runtime-root /home/user/work/wt/rt-pin-9ce4242b --net --tmpdir /tmp/w-027387f013 --out /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-redo-budget-sol-1605/evidence
```

Read-only completed-packet verification command (PASS,320 hash/sequence checks):

```sh
python3 /tmp/w-027387f013/analyze.py
```

The old1602 worktree/temp path no longer existed. The assigned Agent worktree already carried91ac, and `/tmp/w-027387f013` was its existing actual temporary directory. Runtime used existing `/home/user/work/wt/rt-pin-9ce4242b`; the moving integration home was not used. No Git writes or hand provisioning occurred. Final `git status --short` and `git -C /home/user/work/wt/rt-pin-9ce4242b status --short` were empty.

## Limits and next step

The full requests, transport idempotency keys, structured failures, canonical replies, records/bindings/effects/dependencies/history/undo data actually observed are retained verbatim. The actual redo request uses api_version1 and omits reads/rationale/group_id and step reads; the observer neither drops present fields nor fabricates absent fields. No redo preview exists because the guard refused first. The capture codec tags arbitrary objects rather than serializing hidden object attributes. No contract qualification, full suite, pytest lane, P1–P4, native14, browser, or duplicate original-body run was performed.

No environment blocker remains. The next action belongs to the orchestrator: assign an Agent inverse investigation using packet events266(request),313(guard throw),314(provider rejection),315(transport failure),320(complete aggregate). Determine where the config registry expectation diverges before authorizing a source fix. Do not infer its creator from this report. Reports and observer live exclusively under ORCH; product worktree remains unchanged. Conventional harness task commit message supplied separately.
