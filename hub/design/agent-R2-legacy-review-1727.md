# R2 authenticated legacy restore review

## Verdict

**PASS** — d1d41c4056f509ce24af916ee20b7b683ac8f8f1 against exact base
63baa707b4bce52b36c06dc3345d2fd357b10f66 satisfies the requested
source-authenticated legacy inverse/restore validation. No blocking finding.

The task text's candidate hash has one trailing-character mismatch; the full
commit present in this worktree is the hash above.

## Scope and source-authentication review

The four-file delta is limited to:

- astrid/sdk/timeline/_commit_timing_validation.py (80 added lines);
- astrid/sdk/timeline/commit.py (6 changed lines);
- astrid/sdk/timeline/validation.py (10 changed lines);
- tests/editing_conformance/test_authenticated_legacy_restore.py (273 new lines).

The implementation is narrow and preserves the existing R1 private atomic
callbacks, map default handling, and history/source plumbing. The new
recognition in _restored_legacy_exemptions is restricted to parent-owned word
declarations. It requires:

1. an exact candidate parent clip equal to an authenticated source closure;
2. matching project/timeline scope;
3. an actual provider-executed timeline.inverse or timeline.restore write
   whose after value equals both the current candidate and source value;
4. no ordinary/authored write overlapping that clip in the same execution;
5. equal verified reference basis, including documents, placements, source
   shots, physical child inputs, parent configuration, and collection
   membership/order; and
6. the source declaration to be unresolved by the existing legacy resolver.

The production caller supplies only provider-loaded history boundaries and
guarded execution records. Inverse boundaries are obtained from
port.history_entry, _history, and _load; the latter checks project, timeline,
and revision identity. Restore loads the requested closure and checks its
exact parent content digest. A restore uses its verified closure as the
validation baseline. No request-supplied source image, operation-name
whitelist, or accepted-history blanket bypass is introduced. Parent-only
restoration does not authorize new child anchors, and no relational timing or
contract change is present.

The detached until_film_end adjustment is also scoped to the same exact
authenticated unresolved on restoration. It changes only the compiler view;
canonical declarations and aliases remain unchanged. The negative film-end
case refuses as required.

## Tests and checks

Focused real-provider/store command, with worker-owned TMPDIR and durable
evidence path:

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e ASTRID_AUTHENTIC_LEGACY_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz ASTRID_LEGACY_RESTORE_EVIDENCE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-legacy-review-1727/evidence/focused TMPDIR=/tmp/w-09d0a2f1c2 /home/user/work/venv-agent/bin/python -B -m pytest -q --tb=short -o addopts= -p no:cacheprovider -m integration --basetemp=/tmp/w-09d0a2f1c2/pytest-focused tests/editing_conformance/test_authenticated_legacy_restore.py

Result: 27 passed in 40.39s.

Neighbor command:

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-d9e2a71e TMPDIR=/tmp/w-09d0a2f1c2 /home/user/work/venv-agent/bin/python -B -m pytest -q --tb=short -o addopts= -p no:cacheprovider --basetemp=/tmp/w-09d0a2f1c2/pytest-neighbours tests/editing_conformance/test_commit_anchor_d12.py tests/editing_conformance/test_commit_legacy_text_reference.py tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_commit_v2_validation.py

Result: 80 passed in 3.26s.

The focused cases cover accepted inverse, selected-step inverse, whole
restore, preview no-write, merged disjoint parent movement, exact source
canonical equality, metadata/undo fields, new/modified/equal-authored writes,
forged source/publication/step, wrong digest, foreign source, ABA,
membership/order changes, changed/removed physical targets, owner successor,
document/source-context poisoning, absent writes, and changed film-end flags.
All refusal cases assert the store snapshot is unchanged.

Additional author-packet and local checks:

- exact base RED reproduction: 2 expected failures, both
  candidate.timing: legacy word anchor is missing;
- scoped mypy: Success: no issues found in 4 source files;
- mypy baseline: 1912/1912;
- scoped Ruff: All checks passed;
- Ruff baseline: 2149/2149;
- official Runtime 34eac004 vendor lock: PASS;
- artifact manifest: PASS;
- git diff --check: PASS.

The focused evidence captured the authentic archive SHA-256
2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3, Runtime
commit d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b, tree
9b07545cac9a8bbafb16246aaa6f72050ef7cffe, and source pair
a3e671256f1c42b8837d3e118c97b21b / txn-11c90075be6c4c8bb9e2627366f0fe4f
with digest
sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb.
Actual imported module origins and hashes were recorded before and after the
provider/store exercises. The candidate file hashes match the author packet.

## Limits and next step

No production repair, Runtime/schema change, Git write, integration-worktree
write, full suite, browser/socket suite, original FOUR, public redo, P1/P4,
native14, or prohibited historical body was run. The result is PASS for this
source-authenticated R2/V2 validation scope only. Next step is the
manager-controlled original FOUR on the qualified authentic carrier, followed
by normal integration review.
