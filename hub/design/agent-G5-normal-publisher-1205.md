# G5 ordinary publisher — bounded draft, BLOCKED

Worker: `agt-G5-normal-publisher-1205`. Base: `ee7f0b809266690f5c46d6824af1e6ee82f03714`.
Worktree: `/home/user/work/wt/agt-G5-normal-publisher-1205`.

**Do not merge. The promised disjoint-clip success still fails. No independent restructure approval is claimed; review1203 remains separate. Integration requires P1 GO.**

## Change

Ordinary `_PublishMixin.publish` now calls the existing G3 `emit_document_commands` and durable `TimelineSession.submit`/`flush`, rather than `store.publish_bundle`. The facade retains its receipt, narration/transcript follow-up and checkout reset behavior. No executor, three-way replacement, journal, authority substitute, prepared acceptance, managed-edge patch or private-cache injection was introduced. The existing Runtime history and outbox supply acceptance/retry facts. Outbox evaluation metadata contains only a local candidate retry fingerprint; it does not authorize acceptance.

The adapter recovers the unique historical publication paired with a detached checkout revision, fetches that exact authenticated closure, verifies provenance, and emits guarded payload edits. It uses the same conservative closure-read policy as normal `Timeline.commit` for arbitrary free edits. It retains the original request/key after an unknown outcome and recovers acknowledged cuts whose narration ingestion failed before a narration flight existed. Changed-key payload and force controls preserve the film/history. Validation runs on a copy so it cannot silently create an absent empty `slots` field in the authored candidate.

The complete Runtime-backed positive compares the whole raw parent payload, shot revisions, internal revisions and media/dependency manifest with the compiler's expected publication. It covers unchanged IDs/order/media, explicit null/false/zero, unknown payload fields, absence, narration/transcript follow-up, file reload/reset and an empty local journal, under a renderer/process fence. Additional cases cover exact cut/narration lost-ACK replay, one history entry per actual commit, narration ingestion recovery, before/base/media/stale no-write controls and read-only preview `would_status` with dependencies.

Existing reset/history/transcript tests moved their mock boundary from the retired store publisher to the facade's commit adapter, preserving their original assertions. The two old renderer-fence compiler units still execute the real compiler; the new real-provider positive supplies the actual commit-path renderer fence with Runtime-authenticated media. No passing behavior expectation was changed to refusal, skipped, deleted or marked xfail.

## Blocking evidence and decisions

`tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head` (line 447) promises that an ordinary edit to one clip merges while another clip changes at the head. The new real Runtime test `test_ordinary_disjoint_clips_merge_onto_peer_head` preserves exactly that successful property: local clip `p1`, concurrent clip `p2`, both in the same internal timeline. Runtime instead raises `CommitConflict: intervening publication changed a guarded address`.

C0 §1 explicitly forbids inventing `reads: []` after diffing bytes; normal `Timeline.commit` conservatively guards arbitrary free transformations. The detached Checkout has final bytes and draft snapshots, without authoritative semantic/read capture. Therefore the task's full preservation requirement and the existing conservative free-transform policy cannot both be met by this bounded diff-only adapter. This is evidence of an unresolved requirement/ownership gap, not permission to relax C0 or convert the promised success into a refusal test. The success assertion remains failing in this draft. Coordinated helper/read capture is needed outside the allowed publisher-only scope.

A second unqualified limitation: legacy Checkout records its revision/digest without its original publication ID. If Runtime history contains the same revision at multiple publications (for example restore), this adapter refuses to guess a base pair. Persisting that pair at checkout time belongs to the excluded checkout/store owner. This case was identified from source, not experimentally qualified here. General managed membership/placement/media-binding edits also still need their existing semantic command rather than generic patch substitution; full migration of those detached workflows is not claimed.

## Exact evidence

All pytest commands ran from the assigned worktree with this prefix:

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=.:/tmp/w-a822a5b7b6/runtime-3b926ef \
ASTRID_RUNTIME_CHECKOUT=/tmp/w-a822a5b7b6/runtime-3b926ef \
PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest
```

Runtime source was archived with `git -C /home/user/work/runtime archive 3b926efab2eed122d374540baee297d4cdcec62a | tar -x -C /tmp/w-a822a5b7b6/runtime-3b926ef`. The worker's `tmpdir` file points to `/tmp/w-a822a5b7b6`; it is not itself a directory. No shared install was modified.

Bounded ordinary + narration/reset/history + unchanged restructure selection:

```sh
-q --tb=short -o addopts= -p no:cacheprovider \
--basetemp=/tmp/w-a822a5b7b6/bounded-final \
tests/sdk/test_timeline_normal_publish.py \
tests/sdk/test_timeline_narration_commit.py \
tests/sdk/test_timeline_transaction.py \
tests/sdk/test_timeline_checkout_history_boundaries.py \
tests/sdk/test_timeline_journal.py \
tests/sdk/test_media_transcript.py \
tests/sdk/test_timeline_publish_connection.py \
tests/sdk/test_scene_save_core.py \
tests/sdk/test_timeline_restructure.py -k 'not duplicate'
```

**133 passed, 1 failed, 6 duplicate cases deselected in 173.98s.** The only failure is the retained disjoint success. This run preceded the last additional provenance check and preview case. The restructure/narration/reset helper bodies were compared against HEAD by AST source segment and are byte-for-byte unchanged.

The next ordinary-only command used the same pytest flags, `--basetemp=/tmp/w-a822a5b7b6/normal-final tests/sdk/test_timeline_normal_publish.py`: **10 passed, 1 failed in 72.91s** (same disjoint failure), including the new preview control. It preceded the final additional shot-provenance check.

After the final product change, the same flags with `--basetemp=/tmp/w-a822a5b7b6/last-guard tests/sdk/test_timeline_normal_publish.py::test_ordinary_publish_preserves_complete_closure_and_followups` gave **1 passed in 9.06s**.

A final targeted replay on the final source tree is running with the same flags, `--basetemp=/tmp/w-a822a5b7b6/source-final`, the eight ordinary/narration/history/transcript/connection/renderer-fence files above (omitting restructure), and `-k 'not duplicate'`. Its result will be recorded before exit.

Quality commands, with no repository baseline changes:

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-a822a5b7b6/ruff make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-a822a5b7b6/mypy make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

**Ruff 2149/2149 PASS; private mypy 1912/1912 PASS; vendor/artifact/diff PASS.** Scoped Ruff compared before/after through `ruff check --no-cache --stdin-filename astrid/sdk/timeline/publish.py --output-format json -`: the same two existing findings, zero added `(code,message)` identities. Scoped mypy used `mypy astrid/sdk/timeline/publish.py --hide-error-context --no-pretty`, first with `--shadow-file astrid/sdk/timeline/publish.py /tmp/w-a822a5b7b6/publish-before.py`, then without: **19 -> 19**, zero added `(message,code)` identities. All caches were private.

Actual module origins were printed before and after. `publish`, `emitter`, `sync`, `commit` resolve to this worktree. Runtime resolves to `/tmp/w-a822a5b7b6/runtime-3b926ef/runtime_protocol/service.py`. The reused fixture independently checks its Runtime module origin. Durable JSON and logs are in the worker's `logs/` directory.

## Scope and next steps

Only `astrid/sdk/timeline/publish.py` and narrowly related SDK publisher/history/narration/reset tests changed. CLI, checkout, `_doc_patch`, store/facade, sync/commit_session, native restructure/order carrier, D17, generated/schema/pins/contracts/dependencies remain unchanged. Existing store functions remain for other callers. Full v2 transport request/reply handling remains in the unmodified session/provider, including structured failure and preview forms; broad v2/HTTP/undo qualification is not claimed by this task.

No Git mutation, merge, push, daemon, network/browser/full suite, dependency install/shared cache write, safety denial or approval claim occurred. No P1/P2/P3/P4 HTTP/native14/58/D17 suite was run. Initial probes exposed stale mock seams, one mistaken fixture clip name and one incorrectly constructed test transport exception; these were corrected without changing promised properties. An initial mypy +5 was resolved by reusing the existing base/changes access once; final count and scoped identities match the original.

Commit message and `BLOCKED` are written; **no DONE marker**. Recommended next step: coordinate authoritative read/semantic capture and durable checkout base-pair ownership, then finish this draft, run this same bounded acceptance, and obtain independent review. Do not merge until those gaps are resolved and P1 is GO.
