## Result

The actual `test_contiguous_helpers_keep_sequential_steps[True]` failure is **not losslessly retained**.

Surviving evidence is limited to the test traceback:

- Runtime refusal: `sequential replay binding is duplicated or omitted from the authenticated map`
- Location: `timeline_commit_auth.py:2196`
- No accepted write.

Missing for the actual failure:

- original and landing execution envelopes;
- exact request and provider context;
- prepared digest;
- complete replay bindings;
- authenticated history/intervening records;
- structured Runtime trace comparing submitted versus expected maps.

The numeric archive is unrelated and must not be used:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-helper-digest-sol-0048/numeric-capture.json.gz`

- Size: 39,080 bytes
- SHA-256: `8d16c9e4b70203fe329654c54bd50c34772c9f61981a6a87e1eb2848e781e854`
- Valid finite JSON; credential scan: 0 matches
- Contains accepted/merged numeric-normalization captures, not the target sequential failure.

Its command record is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-helper-digest-sol-0048/commands.txt`

- Size: 3,101 bytes
- SHA-256: `c7622d0b61272c23935c80c256bef7077f0956675e0821f652fa9fc9f6887653`

The G5 boundary captures are also excluded as historical lookalikes: they use Agent `34d00031f` / Runtime `3b926efa` and record `root is outside the verified closure` or missing word binding, not the current Agent `3b0dc9e80` / Runtime `8ea0766f` replay-map refusal.

## Source comparison

Relevant Agent production files are byte-identical between current HEAD `521c8880` and failing candidate `3b0dc9e80`; only the fixture wrapper differs (`pop(..., None)`).

Runtime relevant files are also byte-identical between current `/home/user/work/runtime` and failing pin `/home/user/work/wt/rt-pin-8ea0766f`:

- `timeline_commit_auth.py`: `ecc0149e...`
- `timeline_commit_port.py`: `0d44b5a...`
- `timeline_commit_store.py`: `b1cfdcee...`

No behavioral cause is claimed.

## Verification

- Tests rerun: none, as instructed.
- JSON finite checks and credential scans: passed, zero credential matches.
- `git diff --check`: passed.
- Worktree: clean.
- No product, test, schema, client, pin, or source files changed.

## Next bounded diagnostic

Use the existing public `tl.commit` path and the exact named test on the current Agent/Runtime tuple. At the existing private `capture_sequential_execution` → Runtime preview/validation seam, retain one complete finite JSON envelope containing the request, context, original/landing executions, prepared digest, replay bindings, authenticated history, and structured refusal trace. Compare the submitted map against Runtime’s computed expected map; do not add wire fields, waive guards, or infer attribution from numeric or historical captures.