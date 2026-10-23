# G5 sequential helper capture — independent bounded review

Review target: `34d00031f` (`tl/agt-G5-helper-sequential-cut-1258`) versus `6bd5e1a89`.
The prior author report was read from `scratchpad/orch/design/agent-G5-helper-sequential-cut-1258.md`.

## Verdict

**Bounded PASS. Whole G5 remains BLOCKED / P1 NO-GO.**

Within this diff, the literal cut-linked helper path has the required conservative
boundary and replay checks, and the passing authenticated controls remain intact.
The complete G5/P1 result is not green because two retained positive cases still
fail for the ownership issues identified by the author: moved-head sequential
rebinding in Agent core, and the anchored `"second"` fixture setup's missing exact
typed-word binding. Neither failure was converted to a refusal expectation or
weakened.

No new actual vulnerability was found. No product or test files were changed by
this review.

## Source review

- `begin_nudge` snapshots the pre-operation bundle and, for preceding helper
  calls, projects their commands through the existing `timeline.commands.execute`
  engine. It requires the projected authored digest to equal the actual operation
  boundary before capturing the next operation. It does not invent future revision
  IDs or use a second executor.
- For cut-linked or anchored nudges, `_retime_reads` captures operation-time
  inputs: parent config (including theme/FPS and cut notes), occurrence
  membership/order and placement timing, every consulted root's clip/track/registry
  membership and order, clip timing/type/track/asset/app fields, shot name/metadata,
  and deliberate picture flags. Whole `app` fields cover consulted VO word carriers
  and other cut-note intent. Reads are collected before mutation; they are not
  inferred from the resulting diff.
- `finish_nudge` retains the ordinary atomic path for placement-changing helpers
  and only records a helper when the authored candidate is a bounded, non-placement
  change.
- `helper_batch` authenticates the saved base pair, replays every saved and current
  helper call through `Checkout`/the existing helper path, compares each complete
  capture, and compares the final authored candidate digest. Direct/unknown,
  interleaved, mixed, and stale captures consequently retain the atomic/refusal
  policy.
- The journal is still hash-chain verified. A validly rehashed forged call is not
  trusted: replay and full-capture comparison reject it. Publication retry keeps
  the exact original request/reply pair and the original authenticated base pair.

## Reproduced blockers

1. `test_contiguous_helpers_keep_sequential_steps[True]` fails at publish with
   `root is outside the verified closure` after an intervening peer edit. The
   missing staged physical read/patch binding is Agent core rebase/materialization
   ownership, outside this journal-only review scope.
2. `test_cut_nudge_restart_merges_other_cut["second"]` fails during the setup
   commit with `candidate.timing: missing exact word binding for
   ('occ-film', 'film', 'inside').on`. This is the retained typed-word fixture
   setup issue, not evidence against the capture boundary.

The original process-persistence positive remains unverified as reported by the
author: its retained target still reaches a fake transport (`_remote` missing),
and belongs to the separate process-fixture port owner.

## Evidence

Passing bounded subset, using the requested Agent/runtime prefix and a fresh
pytest basetemp:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_helper_capture.py::test_contiguous_helpers_keep_sequential_steps[False] \
  tests/sdk/test_timeline_helper_capture.py::test_cut_nudge_restart_merges_other_cut[None] \
  tests/sdk/test_timeline_helper_capture.py::test_cut_nudge_restart_merges_other_cut[+1s] \
  tests/sdk/test_timeline_helper_capture.py::test_conflicts_and_uncaptured_edits_never_write \
  tests/sdk/test_timeline_helper_capture.py::test_cut_nudge_guarded_inputs_never_write \
  tests/sdk/test_timeline_helper_capture.py::test_journal_tamper_and_forged_capture_refuse \
  tests/sdk/test_timeline_helper_capture.py::test_helper_lost_ack_retries_exact_request \
  tests/sdk/test_timeline_helper_capture.py::test_original_publication_pair_is_required \
  --basetemp=<fresh-temp-dir>
```

Result: **19 passed in 149.29s**.

The two retained failures were independently reproduced with the same prefix:

```text
...pytest ...::test_contiguous_helpers_keep_sequential_steps[True] \
  ...pytest ...::test_cut_nudge_restart_merges_other_cut["second"]
```

Result: **2 failed in 13.08s**, with the exact errors above.

Static and integrity checks:

- `python -m ruff check --no-cache --output-format=json astrid/sdk/timeline/journal.py`:
  2 inherited `BLE001` findings at journal.py:340 and :430; no new scoped finding.
- `ruff check --no-cache tests/sdk/test_timeline_helper_capture.py`: pass.
- `scripts.reshape.compare_mypy_baseline`: **current=1912, baseline=1912**.
  The author's private raw current/base Mypy identity comparison was also reused:
  both had 1912 errors and zero added/removed identities.
- `scripts/vendor_lock.py check runtime.lock.json`: pass.
- `scripts/artifact_manifest.py --check`: pass.
- `git diff --check 6bd5e1a89..34d00031f`: pass.
  The author's unchanged normal Ruff evidence was reused: **2149/2149**.

No full/browser/HTTP/native suite was run, per the brief. No Git writes, branch
operations, shared dependency/cache mutations, daemon work, or integration merge
was performed.

## Next steps

Keep this slice unmerged until the Agent core owner qualifies staged physical
read/patch bindings across a moved head, the process-fixture owner connects the
original positive to the genuine Runtime fixture, and the source/word-binding
owner qualifies the anchored typed-word setup. Then rerun the retained positives
and the strict negative/retry controls on the integrated head.
