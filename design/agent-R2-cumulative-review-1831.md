# Agent R2 cumulative independent review — FAIL

Candidate reviewed: `0b735c13710d74600cc51bf55e4963b54163087e` (`tl/agt-R2-native-partition-sol-1818`). The cumulative five-path diff from `22f1cb169` is 549 insertions and 4 deletions across the retained registry baseline, imported `8875589f6` mirror partition, `fb97d24bf` stage-order repair, and this native-aggregate partition. No source or test files were edited by this review.

## Verdict

**FAIL.** A normal provider-produced repeated-value history is accepted once, but its inverse cannot itself be undone:

1. Start from the real `DetachedRealm` document and land the normal split.
2. In one publication, run two native `clip.move` commands for `clip-right`: first to `2.25`, then back to its original `2.2355666666666667` value. The second command was captured from the first command's resulting bundle, so both authored guards are valid.
3. Undo that publication through the normal provider. The provider accepts it and records a nested inverse with stage `b` at `native_write_range=[0,9]`, `effect_range=[0,0]`, and stage `a` at `native_write_range=[9,19]`, `effect_range=[0,2]`.
4. Undo the accepted inverse publication through the normal provider. It refuses with `nested inverse ranges differ from accepted history`.

This is a real accepted-history/provider-path refusal, not an offline mutation of an accepted entry and not a public forged request. It violates the required legal repeated-value undo/redo chain. The current implementation's `inverse_stages()` requires every nested effect range to be nonempty (`_step_undo.py:280-299`), while the provider can emit a valid native stage whose canonical effect contribution is empty. The first inverse execution does not run that validation against its newly emitted nested record; the next inverse does, exposing the inconsistency. Repair must make the recorder, stage validator, and executor agree on legal zero-effect stages without reintroducing first-equal-byte endpoint selection.

## Authority and trust-boundary findings

- Runtime/provider history is authoritative for public inverse execution: `commit.py:999-1045` loads target entries and exact revision boundaries from `port.history_entry`, builds `AcceptedRecords`, and strips `steps` before native ABI execution. Caller-supplied inverse writes do not enter the engine.
- Nested source authentication is performed by `_commit_patch.py:954-965` and `_step_undo.py:311-345`: source publication/intent, step partition, expected stage identity, command ordinals, and native write lengths are checked against loaded history. The native partition at `_step_undo.py:131-195` follows accepted native write order and exact derived compiler observations, not an arbitrary first equal byte.
- The unique stage boundary authority is the accepted `inverse.stage` binding's contiguous native/effect ranges plus the validated source publication, step, command ordinals, native writes, derived writes, and effect slice. The defect above is that this authority is internally inconsistent for a provider-emitted empty effect slice.
- Independent offline negatives for derived cause/site/previous value, native site/order, source publication, step identity, and range type all refused with `history_unavailable`.
- Public request probes through the provider refused caller-supplied `writes`, an unknown publication, and an unknown step, leaving head/history unchanged. These use the test `DetachedRealm`; they are not evidence about a corrupted offline entry being accepted by a production Runtime store. No Runtime HTTP claim is made.

## Evidence and commands

Permanent evidence is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-cumulative-review-1831/evidence`, with pre-validation diffs/hashes, command logs, the repeated-value reproduction, public-request probes, offline guard negatives, `SHA256SUMS`, and credential scan.

- Focused four-path lane: **110 passed**.
- Exact five split selection: first invocation could not import author plugin `capture1750` (no test body ran); rerun with the author evidence plugin on `PYTHONPATH`: **5 passed, 30 deselected**.
- Exact original-14 selection: **14 passed, 71 deselected**.
- Scoped Ruff over 2 changed source files + 3 new tests: **passed**.
- Scoped mypy over the same 5 files: **no issues**.
- Ruff ratchet: **2149 current / 2149 baseline**.
- Mypy ratchet: **1912 current / 1912 baseline**.
- Vendor lock: **ok**. Artifact manifest: **current**. `git diff --check`: **passed**.
- Credential scan over touched source/tests: **no credential-pattern matches**.

Commands used (with the pinned Runtime checkout `/home/user/work/wt/rt-pin-2a9e347f`, existing `venv-agent`, and private temporary directory) are recorded verbatim in the evidence directory. No full suite, browser/socket suite, excluded old lanes, or Runtime HTTP suite was run, per the brief. The separately assigned transient-root baseline failure remains unqualified and was not swept under this result.

## Recommended next step

Keep this candidate unmerged. Add a narrow regression for the provider-produced two-native-command repeated-value chain, then repair the stage/effect recording and validation contract so a genuine zero-effect native stage remains identifiable and reversible. Re-run the mandated 110/five/original-14 lanes and a fresh independent cumulative review. Preserve all source/identity/cause/site/order/previous-value/physical-binding guards and do not replace them with byte-equality endpoint selection.
