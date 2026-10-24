## Report — finite gap

Current HEAD: `bb50a43c915ec00c05c5ee34569a040bab8e817c`  
Tree: `045dd0b01a1bddc6e3c7b822894151a116eacf1b`

The two test names and AST predicates are unchanged from qualified `ca93`:

- `test_timeline_composed_schema.py` blob: `23837a...`
- `test_timeline_current_union_schema.py` blob: `61254b...`

However, commit `544d589ca6` added a real registered operation:

- `commands.py:75-115`: 34 operations, including `media.admit`
- `native_media_admission.py`: closed `PARAMETERS`
- `authoring_commit.py:175-181`: production request emits `media.admit`
- `authoring_bundle.py:1855-1864`: production caller submits the request with an idempotency key and accepts `accepted|merged`, preserving receipt data

The retained census still expects 30 wire operations plus only five provider-only operations. `media.admit` is the sixth provider-only operation, so:

- composed census has no `PROVIDER_ONLY_ARGS` mapping and reaches `conditions['media.admit']`;
- union census fails its exact provider-only set equality;
- frozen schema remains unchanged: 30 branches, digest `de301d...`.

Therefore current qualification is not valid; this is a finite census-membership gap. The prior `ca93` six-plus-three evidence remains historical and must not receive aggregate current credit.

Contract mapping checked in `contract/commit-v2.md`: exact base pair, commands/label/steps/reads/merge/dry-run/source/idempotency; accepted/merged canonical result plus receipt; conflict/invalid structured details; preview with `would_status` and null receipt; authoritative records, dependencies, bindings/effects, undo/history/actor.

Tests were not run, per task restrictions. No product, schema, client, pin, or test files changed. Worktree remained clean. Commit message and `DONE` marker were written.

Next step: manager independent review of the `media.admit` source delta, then decide whether to extend the retained provider-only census mapping.