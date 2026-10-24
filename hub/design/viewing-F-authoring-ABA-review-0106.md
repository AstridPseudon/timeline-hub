# PASS — source/authority verdict

The author’s causal ownership is source-backed: Agent creates duplicate normalized `media.track` bindings; Runtime correctly refuses them. This is not product or behavioral approval.

- Current Agent: `b61cebe8e0d6…`.
- Current Runtime: `458595850c354f4403dabc58a72b98bebbc2c3a3`.
- Runtime guard blob at current HEAD and frozen `8ea0766f5e9fb23cea26c7398770a8aaac06b258` is identical: `6d97c6d6…`.

Evidence:

- The test mutates `film-internal-1`, adding `clip-1b`; both `clip-1` and `clip-1b` use alias `picture-1` and track `picture` ([test_authoring_media.py:764](/home/user/work/wt/vw-F-authoring-ABA-review-0106/tests/timeline/test_authoring_media.py:764)).
- The exact requested base is revision `wc6-baseline` plus the dynamically generated `baseline_publication` receipt ID ([test_authoring_media.py:929](/home/user/work/wt/vw-F-authoring-ABA-review-0106/tests/timeline/test_authoring_media.py:929)).
- The source closure maps `occurrence-1 → film-shot-revision-1 → film-internal-1`; the binding is logically `occurrence:occurrence-1/track:picture`, physically `internal-revision:film-internal-1`, path `["tracks", "id:picture"]`, owned by `occurrence:occurrence-1/shot`.
- Production caller chain is real: `publish` → `emit_document_publish_commands` → `capture_occurrence_swap_media` → `_swap` → `_clip` → `ctx.bind("media.track", ...)` ([timeline_document.py:281](/home/user/work/wt/vw-F-authoring-ABA-review-0106/astrid/packs/rendering/docs/scripts/timeline_document.py:281), [native_occurrence_media_commands.py:241](/home/user/work/wt/vw-F-authoring-ABA-review-0106/astrid/sdk/timeline/native_occurrence_media_commands.py:241)).
- `_clip` emits the same physical binding once per same-alias consumer ([native_occurrence_media_commands.py:188](/home/user/work/wt/vw-F-authoring-ABA-review-0106/astrid/sdk/timeline/native_occurrence_media_commands.py:188)).
- Runtime normalizes those bindings without `ref`/physical identity, so the second original binding hits `key not in originals` and raises `sequential source binding is ambiguous`; the landing side has the equivalent guard ([timeline_commit_auth.py:1800](/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:1800), [timeline_commit_auth.py:2066](/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py:2066)).

Offline reproducer passed and produced two identical `media.track` identities on both simulated original and landing captures. This is synthetic Agent execution evidence, not an observed live private packet.

Missing evidence: exact live serialized `capture["original"]`/`capture["landing"]` bytes were not observed. The current test source still runs Runtime `a0dca…` for execution; I did not relabel it as `8ea`.

Smallest next action: Agent-owned capture normalization/identity repair so repeated consumers share one authenticated physical binding while retaining consumer/target evidence. Do not weaken or waive Runtime’s guard.

Checks:

- `git diff --exit-code` — passed.
- `git diff --check` — passed.
- AST parse with `/home/user/work/venv-agent/bin/python` — passed.
- Offline probe under `$TMPDIR` — passed.
- No tracked files changed; no type/lint scope.
- No live/original test, full suite, browser, HTTP, SDK4, c271, install, or benchmark run.