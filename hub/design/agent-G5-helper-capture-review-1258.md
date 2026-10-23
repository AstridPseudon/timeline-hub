# G5 helper-capture independent review — bounded PASS, whole G5 BLOCKED

Worker: `agt-G5-helper-capture-review-1258`  
Reviewed: `tl/agt-G5-helper-capture-1232` (`6bd5e1a89`) against `aa2fa8677`  
Disposition: bounded source-capture slice PASS; whole G5 remains DRAFT-only / P1 NO-GO. No product files were changed and no integration merge was performed.

## Source provenance decision

The direct opaque disjoint test is new in the blocked `1205` author commit, not an inherited acceptance:

- `aa2fa8677:tests/sdk/test_timeline_normal_publish.py` is an added file. Its `test_ordinary_disjoint_clips_merge_onto_peer_head` is exactly lines 167–180 and performs direct mutable `checkout.clip('p1').data['opaque']` and peer `p2` opaque edits.
- At `aa2fa8677^`, and at requested upstream refs `431681a6d3cfa0bba2c8c9baa03f152d33032df1`, `74f3f7edba35230d0a01824eae7b663143e6aa5b`, and `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`, `tests/sdk/test_timeline_normal_publish.py` does not exist.
- The actual pre-existing positive is `tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head`, present at all four refs above, with the operation-time `a.do("nudge", clip="a-rocket", seconds=0.5)` at lines 447–450 and the successful disjoint-head assertions at lines 457–462.

Therefore the new direct-opaque test must not be described as faithful preservation of the persistence behavior. C0 requires an unknown/direct free transform with no authoritative helper capture to remain conservative atomic (the commit contract, `commit-v2.md` lines 129–142, makes omitted-read `doc.patch` effective `atomic` and forbids invented empty reads). There is no evidence of a pre-existing free/direct-opaque disjoint promise.

The correct future test decision is to split the claims: preserve the actual pre-existing `Clip.nudge` disjoint positive (using a genuine helper capture), and retain a separate direct-opaque/unknown-free negative asserting atomic conflict and no write. Do not change the contract or waive reads merely to make the new, never-passing direct test green. This review made no test edit.

## Bounded implementation review

The one-helper slice is internally aligned with its stated boundary:

- `journal.begin_nudge` (`astrid/sdk/timeline/journal.py:113–150`) observes before mutation and records the whole original internal clip row as a finite JSON field, the actual FPS/theme input, and both occurrence start codecs. It refuses anchored, cut, structured, missing-source, invalid-argument, and non-unique cases rather than guessing.
- The existing `_journaled` wrapper (`astrid/sdk/timeline/store.py:166–197`) captures the original helper arguments before calling the original implementation, then emits the existing guarded `doc.patch` from the before/after closure. It does not replace the helper with a different semantic operation.
- `Checkout._save_locked` persists the capture in the existing save journal (`astrid/sdk/timeline/checkout.py:225–235`). The journal verifier (`journal.py:423–447`) checks sequence, predecessor hash, and each record hash before replay; self-rehashed command/read/after-digest forgeries are then rejected by replay comparison.
- `journal.helper_batch` (`journal.py:165–218`) selects only a matching authenticated base pair and authored before digest, replays the original helper against the authenticated base, compares the complete generated capture, and requires the replay authored digest to equal the complete candidate. It returns a bounded fields request only for one complete helper capture.
- `fetch_bundle` (`astrid/sdk/timeline/store.py:653–690`) scans all history pages for a unique revision/publication pair and then uses the publication-bound `open_bundle` read to restore the authenticated source closure. It refuses ambiguity, missing history, cursor loops, and unavailable hydration; it does not substitute a later head.
- Unknown, mixed, old snapshot-only, and multi-helper cases remain atomic: `helper_batch` returns `None` for a non-single complete chain, and `_commit_document` submits the ordinary conservative atomic request without caller-invented reads. No copied recorder authority, unverified-history trust, guard waiver, alternative executor, schema/generated/pin/contract change, or Runtime/auth change was found.

The production caller continues to preserve the v2 base pair, commands, label/source, steps, patch and ordinals, request/step reads, merge mode, idempotency/retry behavior, dry-run path, canonical receipt/history data, and existing narration/reset handling. The implementation is a bounded qualification, not a whole-G5 acceptance.

## Evidence run for this review

The designated worker `tmpdir` was a regular file, so the first attempted pytest setup could not create its basetemp and produced 13 setup errors; this was an environment failure, not a product result. The same permitted subset was then run once with a private `/tmp` basetemp:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_helper_capture.py -k 'not contiguous_helpers_keep_sequential_steps' --basetemp=/tmp/agt-G5-review-1258.ga00Lh/pytest-passing-subset
```

Result: **13 passed, 1 deselected in 76.98s**. The known sequential failure and the two retained original positives were not rerun in this review.

```sh
RUFF_CACHE_DIR=/tmp/agt-G5-review-1258.ga00Lh/ruff PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline
```

Result: **Ruff current=2149, baseline=2149; PASS**.

```sh
MYPY_CACHE_DIR=/tmp/agt-G5-review-1258.ga00Lh/mypy PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```

Result: **Mypy current=1912, baseline=1912; PASS**.

No full, browser, HTTP/socket, native, P1/P4, daemon, shared-install, or Git mutation run was performed.

## Remaining ownership and next bounded acceptance

1. **Sequential root binding — production/G3/provider boundary, Sol follow-up (`agt-G5-helper-sequential-cut-1258`).** The retained `test_contiguous_helpers_keep_sequential_steps` must pass with two operation-time captures, sequential step ordinals and per-step reads. The recorded failure is provider `root is outside the verified closure` / `provider alias is outside or ambiguous in its boundary`: the second emitter output names a locally compiled successor physical internal revision, and logical alias substitution was also rejected. Qualify the existing physical boundary binding and sequential input declarations through the existing G3/provider inputs. Do not guess a future pin, retarget an alias, waive a guard, or broaden Runtime auth without an explicit owner decision.

2. **Cut/anchored helper — same production owner/slice.** The pre-existing positive uses `a-rocket`, which is cut-linked and anchored (`tests/fixtures/timeline_editing/tiny_publishable.json` has `app.astrid.cut=c1` and `on="\"viral\""`). The current guard intentionally excludes it. Acceptance needs actual operation-time capture of the word/transcript resolution, cut/child timing, theme/FPS, occurrence, and retime inputs; authenticated full replay and final-candidate comparison; plus same-cut conflict/no-write, forged-call/hash-chain, mixed/uncaptured atomic, and exact-retry controls. Do not derive those reads from final bytes.

3. **Process fixture — test-only Luna owner (`agt-G5-process-fixture-port-1258`).** `tests/sdk/test_timeline_persistence.py:48–102` is still a fake head-file client with a stubbed `publish_authoring_candidate`, while the current `Checkout.publish` path needs the genuine authenticated client transport. Port only the fixture to the existing genuine Runtime service/client seam, preserving the child-process restart, original `a-rocket` nudge, peer `b-type` change, exact merged candidate assertions, and same-clip/no-write assertions. Do not fix production capture in this test-only split or copy a fake authority/current head over the historical base.

Until the actual pre-existing helper positive, sequential helper acceptance, cut-helper coverage, and genuine process fixture are green, G5 remains blocked and must not merge. 
