**REJECT — the frozen controller is not ready for a central capture grant.** Independent read-only gate completed after the creator's REPORT/DONE and the source-vector READY. No creator artifact, repository, dependency, shared cache, suite or grant was edited. Fixes belong to the creator; this report makes no capture authorization.

Exact reviewed SHA256 values, unchanged between initial and final review:

- `controller.py`: `9df40fc1950874199a037676703f02023bd0e1a681d2dc2a3a1c10094dda4b67`
- `render.mjs`: `8845a035415ddd14bbee65586956101cc011d80b4edac7fdb77f4f74860f447d`
- `COMMAND.txt`: `e0f6a2142328481734da2e4c9a36e5dd0158e78b868aed77f916fffe6041a739`
- `REPORT.md`: `1b80fcd1c8a5b74a9dcc81f24125c8a4bf01533ac517f24abdaff34ce9059290`

All four filenames above have the absolute prefix `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-main-cap-capture-controller-`.

Blocking findings:

1. **Preflight depends on a recycled creator worktree.** `controller.py:29,149,169` uses `/home/user/work/wt/vw-m3-main-cap-capture-controller` for original MAIN git reads. That directory is already absent after creator completion. Running the real preflight functions with only evidence/disk paths redirected to this reviewer's directory fails with git exit128 / `CalledProcessError` before graph/resource checks. The proposed central command therefore cannot run as frozen. Use an explicitly retained read-only repository/object store and still verify exact MAIN a411628f8fd6129f9c58c332019b56769d997384; do not weaken source comparison.
2. **Refused pre-existing staging data would be deleted.** `source_stage` refuses an existing `capture-stage` at lines253–255, but `main` unconditionally executes `shutil.rmtree(stage)` at lines434–437 in its finally block. A failed allocation/refusal does not establish ownership. The offline regression probe created only a tiny private sentinel, mocked grant/preflight/graph/process functions and mocked deletion, then ran the real refusal/finally path. It observed exactly one deletion request for the refused stage; the sentinel remained intact because deletion was mocked. Track successful allocation separately and clean only the directory allocated by this attempt, including partial staging failures. Add a refusal-preserves-existing-data calibration before re-freezing.
3. **The grant does not bind the reviewed script bytes.** `suite_line`/`central_grant` at lines323–338 and `render.mjs:40–43` check a command containing a mutable script path. Neither compares a manager-approved controller/render SHA256. A changed script at that path still satisfies the same grant contract. Add a small explicit manager-owned exact-hash check for both scripts before staging/execution; fresh hashes and a new independent verdict are required after fixes. No new authority protocol or evidence ledger is needed.

Separate resource/admission holds remain: the diagnostic preflight observed **12,625,637,376 free bytes**, below **13,021,077,036 required bytes** (10GiB reserve + 2,283,658,796 staging/headroom). It correctly returned STAGE_BLOCKED. The exact grant and capture-stage were absent. No 80–90MiB source extraction was attempted. No floor bypass, cleanup of others' data, grant creation or central request was performed.

What passed independently:

- Diagnostic preflight, with ONLY evidence/disk paths and the read-only git repository location redirected to this worker: original MAIN **2,414 files**, original Root/generator/components, **29-member lock-exact Composition6**, generated package bytes, immutable closure/image/seven expected output hashes. This diagnostic does not repair or approve the frozen script and does not execute the seven-output consumer replay.
- Physical SSR checkout **f8164bef73215272562c4d6974acadbd82c2898a**, **21,488 entries**, canonical graph SHA256 `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`; full graph and all six peer byte hashes identical before/after. React/DOM18.3.1, Remotion/bundler/renderer/media4.0.509, Node/browser hashes match. Polluted App/scene-host traversal is rejected by the inventory code. Their graphs were not used.
- Python Ruff and Node syntax checks; seven reserve/headroom/QUIET/absent-grant/no-allocation guard checks; independent pixel instrument synthetic self-calibration. Exact commands and results are in the sibling absolute `handoff-vw-m3-main-cap-controller-final-gate-commands.txt`; the executable offline probe is its sibling `commands.py`.

Code review confirms that the intended capture path requires raw-closure consumer replay and all seven byte-equal outputs before renderer invocation, original registered MAIN Root/TimelineComposition and aliases, private locked6, real private scope/cache parents with peer leaf links, exact actual metadata1920x1080/numeric30/duration120 before PNGs, and only frames90/105/119 without end-clamping. Source/fixture/full graph/six-peer postflight failures invalidate results. PNG metadata and original file hashes are retained. RGB inference uses actual frame90 RGB240 control and the source-defined #050814 background, reports RGBA separately, and never treats alpha255 as layer opacity. These are reviewed requirements in code, not completed capture evidence.

MAIN rawhold5/cap4 becomes projected/serializedhold4. The resulting source prediction is 1/0.5/1⁄30 at90/105/119, contrary to the suggested raw-clock1 at105. **0.5 is not an approved golden.** Agent/compiler owner must reconcile the decision using actual MAIN pixels; this review does not deviate from PLAN or choose semantics.

Consumer generation/replay, bundling/cache behavior in execution, actual metadata, PNG correctness/pixels and RGB inference remain **unverified**. No render, browser, listener, socket, network, install, service request, full/product suite or git mutation ran. Repository status and diff checks are clean. No parity, audio, App, Runtime admission or Gate6 claim.

Next step: creator fixes the three findings and freezes new scripts/commands; manager supplies reserve plus staging/bundle headroom; an independent gate checks the new exact hashes before any manager-only central grant. This review task is complete with REJECT, not blocked awaiting capture.
