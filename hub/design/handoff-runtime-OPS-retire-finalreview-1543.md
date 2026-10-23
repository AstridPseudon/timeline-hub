# Independent OPS-retire-venv final review — rt-OPS-retire-finalreview-1543

## Verdict

**PASS — the corrected three-file fixture packet is independently qualified for a separate host-only installation review.** This is report-only / NEVERMERGE product work. No live kit installation, production dispatcher execution, daemon launch, venv build/removal, host script launch, network, Git mutation, or product/test/source edit was performed.

Reviewed packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-return-1539/evidence/kit/`

Durable independent source reused with only its `KIT` fixture path substituted:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-review-resume-1534/independent-review.sh`

## Independent matrix

- Original packet rerun: **33 pass / 3 fail**, exit 1. The three failures are exactly the prior refusal gaps: dangling pending entry, non-regular pending entry, and dangling running-worker `env`.
- Corrected packet rerun: **36 pass / 0 fail**, exit 0. All 33 original positive/guard cases remain passing; the three formerly failing cases now refuse with rc=2. No old pass label is missing from the corrected run.
- Corrected output contains no `Broken pipe` diagnostics from the handler's ancestor scan.
- Coverage includes eligible aged read-only removal, strict names/containment, young and exact-one-hour targets, target/nested symlinks, partial and active builders, valid/missing/malformed markers, suite/env references, pending dangling/non-regular entries, running-worker metadata and dangling env, unreadable suite input, live process argv/exe/cwd/fd use, outside sentinel preservation, dispatcher call shape, malformed requests, and request payload.

## Dispatcher and scope evidence

- `bash -n` on exactly `request-retire-venv`, `dispatcher-daemon`, and `retire-child-venv`: exit 0.
- Private fixture request → exact dispatcher branch → actual handler: **3/3**, exit 0.
  - aged target: removed and written to `queue/done/`;
  - young target: preserved and written to `queue/refused/`;
  - FIFO: older `venv-agent-child-aa` refuses while the newer dependent `venv-agent-child-aa-b` succeeds, proving oldest-first handling.
- Dispatcher diff against authoritative ORCH: expected diff exit 1, exactly one non-header added line (`RETIREVENV` branch), zero non-header removed lines.
- `request-retire-venv` is byte-identical to the previous packet.
- `sha256sum -c evidence/hashmanifest.txt`: exit 0. Corrected packet hashes:

```text
f18bc20b23010dc47a6891d4ef7a357da5991a620b83b5cdc67e0c8741892c15  dispatcher-daemon
4713b456ae4b0dcabdbc64ddf41aff731ac10fe4d11695d315e6743b864aef10  request-retire-venv
48cac6c70578b9435a259da7cb9adbd07bf045a3346d77235a401ca848e02ed5  retire-child-venv
```

- The manifest also verifies unchanged authoritative `request-child-venv` and `make-child-venv` hashes. ShellCheck is unavailable (`command -v shellcheck` exit 1); no ShellCheck result is claimed.

## Safety inspection and limits

The final handler performs the two shell `check_all` passes and fingerprint comparison, then repeats canonical/type/fingerprint validation in Python immediately before bounded removal. The target replacement race was inspected in source and exercised through the existing final-fingerprint checks, but no adversarial swap was injected in the small final `stat`→`rmtree` interval; no stronger race-proof claim is made.

The private fixture overrides `RETIRE_VENV_ORCH_ROOT` and `RETIRE_VENV_WORK_ROOT` only for temporary roots. The handler's production default remains `/home/user/work`; the dispatcher packet retains its fixed production ORCH path. No fixture path was allowed to authorize deletion outside its target. The independent live-process case proves ancestor/process-use refusal, and source inspection confirms failed process argv/exe/cwd/fd reads refuse unless the process has disappeared. A controlled unreadable `/proc` entry was not manufactured in this sandbox, so that specific kernel-state branch remains source-inspected rather than independently fault-injected.

## Host-only next step (not executed here)

The host lead owns installation under the existing HEADER 13:39 process; no new permission gate is added. Before any install, record a timestamped receipt proving:

1. dispatcher idle, no executing request, no active child-venv builder, and no concurrent retirement;
2. current destination hashes and timestamped predecessor backups (`*.bak.<UTC timestamp>`);
3. each packet file copied to its destination `.new`, mode/hash checked, then atomically installed with `mv` (dispatcher last);
4. post-`mv` exact hashes, `bash -n`, and the same one-line dispatcher diff;
5. normal host coordination and rollback names in the receipt.

The host lead must perform this outside the sandbox and must **never launch the host installation script from the sandbox**.

## Durable evidence

Evidence and logs are under:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-retire-finalreview-1543/evidence/`

Key files: `old-packet-independent-review.log`, `independent-review.log`, `dispatcher-boundary-v3.log`, `bash-n-exact3.log`, `hashmanifest-check.log`, `dispatcher.diff`, `scope-status.txt`, and `matrix-retention-status.txt`.
