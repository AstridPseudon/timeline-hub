# F-agent full classification review

## Verdict

**FAIL for PASS classification.** The supplied terminal inventory is mechanically
complete, but the exported classification report needs correction before it can
be treated as an approved PASS/FAIL report. This review is read-only: no product,
test, generated, dependency, pin, runner, process, or Git state was changed.

Reviewed base: Agent `d46210398` (`fcc33e0eb964dd48d422673e8f692f195c88748c`
in the sole full-run snapshot). Evidence was limited to the exported design,
the exact service `summary`, `log.txt`, `snap`, `ext`, and static source/schema
inspection.

## Inventory and totals

The exact log contains:

- 240 `FAILED tests/...` node lines, all unique;
- 140 `ERROR tests/...` node lines, all unique;
- eight `ERROR root:journey.py:1281 Journey failed before teardown` captured
  records, excluded from the pytest-node count;
- no overlap between failed and error node sets.

The exported report lists the same 380 node identities exactly once: 140
collection/setup errors, 176 child-environment/external-resource failures, 40
source-backed current failures, and 24 unconfirmed failures. The service totals
also match exactly: 16,388 passed, 40 skipped, 5 xfailed, 565 subtests passed,
85 warnings, exit 1.

The 316 environment/resource/collection total is therefore arithmetically
verified as `140 + 176`. The log supports that disposition for the listed groups
with missing `runtime_protocol` in isolated children, missing Composition or
Remotion resources, and runtime/child transport setup failures. The 24
unconfirmed nodes remain unconfirmed; no automatic H9 deferral is justified.

## Required corrections

1. The 40-node bucket must not be called **confirmed integration regression**.
   Current source-backed failure evidence establishes that those assertions fail
   on `d462`, and it identifies useful owners, but it does not establish that
   integration introduced them. No exact targeted 431 baseline was run or
   supplied, so the report must call these **current source-backed failures,
   integration causality unproven**. Likewise, “confirmed upstream-431
   preexisting: 0” should be written as **0 proven preexisting; baseline not
   established**, not as a causal conclusion.

   The report should also distinguish stale expected/canonical inventory from
   behavior defects. Static log evidence identifies canonical-inventory or
   fixture/projection mismatches among the 40, including the checked-in
   TypeScript projection, S2’s expected-55-versus-current-58 definition count,
   the `occurrence.fork` operation/schema inventory, the missing `meta` fixture
   coverage, the exact public-surface golden, and the structure-baseline golden.
   Those must not be presented as proven runtime behavior regressions. The
   remaining source-backed nodes may be actionable current defects, but their
   integration introduction is still unproven.

2. Correct the D14 footer. The authoritative Viewing delivery paragraph says
   the exact two deferred positives are the parameterizations of:

   ```text
   tests/editing_conformance/test_native_word_anchor.py::test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-False]
   tests/editing_conformance/test_native_word_anchor.py::test_undo_recovers_before_binding_even_when_text_writes_are_equal[True-True]
   ```

   The exported report incorrectly names
   `test_equal_text_restore_recovers_the_selected_publications_binding` as the
   second D14 node. The current source confirms the first test is parameterized
   by `retained=True` and `same_text in {False, True}`; the restore test is a
   separate non-parameterized test and is not one of the authoritative D14
   positives. Both D14 nodes remain unchanged, unskipped, visibly failing where
   applicable, and receive no PASS credit.

3. Keep the required production/C0 contract wording intact. Static inspection
   finds the request fields in Agent
   `astrid/sdk/timeline/_commit_patch.py:218-228` and the Runtime contract/schema
   preserves `api_version`, scope, exact base pair, commands, label, steps,
   merge, reads, idempotency key, dry-run, source, rationale and group. The
   reply contract still carries `{data, receipt}`, `accepted`/`merged` plus
   historical `rebased`, head/document/records, dependencies/effects/steps,
   history and `undo_steps`; preview retains `would_status`; conflict retains
   reason and head; invalid retains code, path, hint and suggested command.
   This is static contract evidence only, not a live acceptance claim.

   The current source still has separate actionable caller-boundary findings:
   the production-caller scan identifies the concrete Remotion-lock import at
   `astrid/core/rendering/_effect_registry.py:655`, and the platform-boundary
   assertion identifies `os.getuid` at
   `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:48`.
   Repair those through their owning source seams and rerun the exact nodes; do
   not change the C0 contract or weaken the assertions.

## Evidence limits and next steps

No full, targeted behavior, socket, browser, P1/P4 HTTP/native, crash, or known
anchor-body rerun was performed. No upstream-431 preexisting claim is made.
After the classification wording and D14 identities are corrected, farm owners
should provision the missing environment and rerun the exact 316 environment
nodes; source owners should repair and rerun their exact current-source groups;
the 24 unconfirmed nodes need bounded diagnostics only after provisioning.

Evidence files:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-F-full-classify-0815.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-full-1023072419-4249/summary`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-full-1023072419-4249/log.txt`
