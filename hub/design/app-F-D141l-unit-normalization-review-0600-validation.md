# D141l independent validation

Result: PASS. This was a data/provenance review and an isolated format control only.

## Exact validator control

Fixture ID: `d141l-unit-normalization-review-0600`.

Trusted manager root: `/tmp/d141l-unit-normalization-review-0600`.

Exact command:

```text
python3 -I /home/user/timeline-hub/hub/kit/bin/d141-validate-receipt.py /tmp/d141l-unit-normalization-review-0600/tests/d141l-unit-normalization-review-0600/recorded-measured-floor.json /tmp/d141l-unit-normalization-review-0600 d141l-unit-normalization-review-0600 app full /home/user/work/app 4de54db14bdc9ddc2ce2e5887258b03acbffd30d 84c3fb7f73f08c22220f8e808962fe3f24aaa0aa 'npm test -- --maxWorkers=3'
```

Observed stdout: `4793895424`.

Observed exit: `0`.

The validator was the existing installed file, SHA-256 `2987adbcd888400a41afbbd60e22ea2e4afe6c4580b084a4d63dcced6943a7f6`. The fixture root, receipt, and both witnesses were root-owned regular files with no symlink components. The fixture used the exact supported `timeline.d89d.measured-floor.v1` shape and the authentic App head/tree. No live service ID, `test-run`, test body, receipt attachment, kit edit, source/guard change, or new measurement was used.

## Production caller trace

The installed `/home/user/timeline-hub/hub/kit/bin/test-run` is unchanged (SHA-256 `f674569b4935ee03022fa209ec102f6323dce80be726f44b9698acbaf1300`). Its `app full` registration is `npm test -- --maxWorkers=3` (command SHA-256 `10ec988435479a2c3967d004429343b8bc5661b8b815d00ad30fbd455a2ca54b`). Before admission, the caller checks the heavy-suite scope, reads the actual worktree HEAD, computes the candidate tree, and invokes the validator with the receipt path, trusted manager root, job ID, repo, suite, worktree, HEAD, tree, and registered base command. The canonical inputs were accepted without changing source or guards.

## Data conservation

The exact bytes are `Avail\n5433016320\n` and `Avail\n4839120896\n`; their hashes are recorded in `source-manifest.json`. They are derived validator-input projections, explicitly not original stdout. The raw JSON admission and manager logs remain untouched. Arithmetic is `5433016320 - 4839120896 = 593895424`, yielding floor `4793895424`. `git diff --check` passes on the unchanged Composition worktree.

No tests/typecheck/lint were run because no code changed; those are not applicable to this review.
