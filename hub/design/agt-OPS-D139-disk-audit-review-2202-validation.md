# D139 independent review validation

Verdict: **FAIL**, narrowly. The author's finite no-eligible-normal-cleanup conclusion is supported, but its proposed normal retirement route and future age eligibility for the two bench-store entries are not supported by the authoritative scripts.

Source identity:

- Composition review worktree `tl/agt-OPS-D139-disk-audit-review-2202`: HEAD `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`, clean.
- Author capture: `2026-10-25T21:56:57Z`. Review capture: `2026-10-25T22:01:15Z`.
- Every author-listed witness hash matched current bytes: `recycle`, `request-retire-venv`, `bench_store.py`, `tests/suites.conf`, and `bench-store/index.json`.
- The author did not hash the executed guard `bin/retire-child-venv`; current SHA-256 is `954d5d87fe2e6fcf42b34953ec0edc519a2eb97ade8f66f0f2f96f523516b791`.

Current finite accounting:

- `df -B1 /home/user/work`: `/dev/vda`, available `5,172,244,480` bytes.
- Child admission reserve in `bench_store.py`: `5,905,580,032` bytes; deficit is `733,335,552` bytes. Applying the author's explicitly unverified `200,000,000`-byte source estimate still leaves `533,335,552` bytes short.
- Current free space is `172,244,480` bytes above the 5 GB source floor and `1,172,244,480` bytes above the 4 GB stop line.
- Bounded `du -sx -B1` reproduced the author's named top-directory sizes exactly, including bench-store `1,620,480,000`, runtimes `1,971,752,960`, d22 `517,910,528`, f1012 `1,054,433,280`, and both child entries (`848,089,088` and `772,354,048`).

Eligibility and exclusions:

- `agt-G2-open-commit` is dirty (`M astrid/sdk/timeline/sync.py`), although its head `a086cc6db7928dc4a3516d304dd9a472b050f1cf` is an ancestor of Agent `tl/integration`; `bin/recycle` therefore refuses it.
- `agt-F-final-source-join-0816` has the worker `KEEP` marker and remains protected source evidence.
- d40 is an active bench-store entry and is referenced by `tests/suites.conf:173`; its process cwd/fd scan is clear, but that does not override the suite reference.
- d137 is an active bench-store entry at `/home/user/work/bench-store/entries/child-3e163...`, with retained owner/source/provision metadata. Its registration receipt is `2026-10-25T21:24:50Z`; age at review is 2,185 seconds, before the 3,600-second guard boundary of `2026-10-25T22:24:50Z`.
- There is no `/home/user/work/venv-agent-child-d137-a4e016` or `/home/user/work/venv-agent-child-d40-ba8f-f320` root directory. `request-retire-venv` only enqueues a name; the dispatcher invokes `retire-child-venv`, which resolves `/home/user/work/NAME` and would refuse these names as nonexistent.
- `make-child-venv` states that legacy benches have no store deletion authority. `bench_store.py`'s guarded `Store.ensure` invokes `_evict`, holds entry leases, updates registrations/suite projections, and removes old store entries as part of normal admission. No standalone bench-entry retirement command was found.
- d22 and f1012 remain absolute protected paths regardless of process-clear status. No process cwd/fd matched either protected path or any reviewed candidate.
- Prior refusal records for `agent-remotion-main95bd`, `agent-remotion-published14-091aa23e`, `agent-remotion-0013`, and `venv-agent-child-f1012-installed` still say `target is referenced`; none was retried or rerouted.
- Manager lease search found no exact references to the reviewed worktrees or bench names. The queue had zero real pending request files and zero running entries at review; twelve hidden `.why` notes existed, but none contained the reviewed candidate names.

Exact normal routes:

1. A clean, non-KEEP finished worktree may be offered to the manager's `bin/recycle WORKER` route. G2 is not eligible because it is dirty.
2. A genuine work-root legacy child directory uses `bin/request-retire-venv NAME`; the dispatcher consumes `RETIREVENV NAME` and runs `bin/retire-child-venv NAME`. This route is not a route for `bench-store/entries/child-*`.
3. Bench-store lifecycle is owned by `bench_store.py` during ordinary `Store.ensure` child admission. The reserve remains `5,905,580,032` bytes; no guard was lowered and no admission was attempted.

No cleanup, recycle, retirement, queue, process, lease, KEEP, bench, source, or repository mutation was performed. No tests/build/venv/provider/Store/body execution was performed, per the brief.

Commands and results:

- `sed`/`jq` read of author `report.md`, `evidence/audit.json`, `evidence/candidates.json`, and `evidence/validation.md`: parsed successfully; author result and nine exclusions recovered.
- `sha256sum` on the author-listed controls and current `retire-child-venv`: author-listed hashes matched; omitted guard hash recorded above.
- `df -B1 /home/user/work`: PASS for finite disk witness.
- bounded `du -sx -B1` over named top directories and reviewed candidates: PASS; values reproduced.
- `git worktree list --porcelain`, `git status --short`, and `git merge-base --is-ancestor`: PASS for dirty G2 and merged ancestry facts.
- `python` JSON/index parsing of `bench-store/index.json`: PASS; exactly two active child entries, d40 seq 3 and d137 seq 4.
- exact `/proc/*/cwd` and `/proc/*/fd` checks for reviewed paths: CLEAR for all reviewed paths.
- finite queue/refusal/lease/KEEP marker reads: PASS for the stated exclusions; no refusal was retried.
- source reads of `recycle`, `request-retire-venv`, `retire-child-venv`, `dispatcher-daemon`, `make-child-venv`, and `bench_store.py`: PASS for the route finding above.
