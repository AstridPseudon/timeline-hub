## P2 D141cc single custody review

- Verdict: `FAIL_CUSTODY`.
- Execution: `NOTRUN`; exactly one native `--submit` returned exit 1 before request/row/artifact creation.
- First native error: ordinary D66 agent source-selection mismatch from the manually typed SHA `...e89c2a6f92` versus accepted `...e89a2c6f92`.
- Additional custody delta: the receipt records all four integration checkout paths instead of the exact detached paths in dispatch recipe index 2; the worker log renders conflicting detached values.
- No actual request, registry row, artifact, service body, retry, second submit, or test verdict exists.
- Current four source pins/trees, builder hash/blob, Composition worktree, and product source remain unchanged. No product-registry inference or journey GO is made.
- First-tool trace coverage is not claimed; sampler lifecycle and raw log hashes are retained in `review.json` and `sampler-lifecycle.json`.

No product or test suite was run by this review.
