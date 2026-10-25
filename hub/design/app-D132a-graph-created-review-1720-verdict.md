# D132a protected source verdict

Source review: PASS.

The cumulative tree is exactly `160c675a2` / `b809955f`. Against `20177e6656`, only the two authorized test files differ: six graph request-metadata lines, the approved setup migrations `gain: null -> 1` and `payload.metadata: null -> {}`, and `create_command(roots)` declaring the ordered refs already consumed by the registered handler. The fixture remains 22 test bodies/90 assertions/6 parametrizations and the graph consumer remains 11/33/7; test-body, assertion, and parametrization ASTs are unchanged. Semantic-reservation and created-root-stage-redo consumers are byte-exact. No consumer graph predicate claims absence of the created declaration.

The created refs are exactly `['shot:new-shot', 'occurrence:new-occ']` for the default roots and are derived from the same caller `roots` sequence passed to `ctx.create_entity` in handler order, including custom-root callers. The genuine route remains `RuntimeService.commit_timeline` with registered provider `astrid`.

The prior complete schema census and chronology remain qualified and unchanged: the approved metadata migration removed the sole `PreparedCommit` object-slot error; no product, Runtime, schema, guard, generated, pin, or authored-root change was made. Runtime custody is clean `5e9ad1c6` / `de2954a`; all recorded guard/schema hashes match.

The author’s earlier 47-control and 8/9 body result is retained only as unqualified evidence and receives no review or behavior credit.

The one admitted graph9 launch produced 8 passes and 1 fail in 8.15s. The sole failure is the later authenticated Runtime closure boundary, not the created-claim seam: `invalid_records`, `provider occurrence alias is outside its boundary`, at `runtime_protocol/timeline_commit_auth.py:156`, in the child-stage inverse/redo node. A finite source-only comparison with the genuine passing root-only caller found identical created refs and root writes; only the child-stage path adds the created-occurrence aliases `occurrence:new-occ/collection:clip` and `occurrence:new-occ/clip:title` plus its reads, binding, and child writes. This is an exact Runtime authenticated-boundary seam. No second body, retry, alternate route, speculative edit, or test-only correction was applied.
