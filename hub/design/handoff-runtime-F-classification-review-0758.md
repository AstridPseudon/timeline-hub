Classification: **PASS** (complete classification); authorized full suite: **FAIL**.

- Integration: `a5d4258312c979024865ee704da2d632ca5b2730`, tree `f74b016ea837f8148db4a602c972073a226ed177`
- Runtime upstream: `4563bb5ff06171b3290fc5e2300e08d7fa125b01`, tree `8ba929e0cfdd03f189f20566294fbae4bc82f195`
- Full service `runtime-full-1023074118-30869`: `5 failed, 5956 passed, 26 skipped, 15 xfailed, 245 errors`

All 250 non-passing nodes are accounted exactly once:

- 1 R0 public-export regression: missing `DocPatchArgs`; owner R0/generated clients. Genuine public namespace gap, still P1/frozen34e gated.
- 4 R2r regressions: HTTP 422 `provider label differs from the request`; owner R2r store/prepared fixture.
- 245 environment errors: `34 + 7 + 59 + 145`, all missing `ASTRID_CHECKOUT`; not product failures.

The exact upstream lacks the new union/history/store/port/template files, so no false upstream-baseline or deferred classification applies.

Targeted service result on the existing row: `37 passed, 245 errors`; author’s targeted HTTP artifact independently reproduced all four 422 failures. No full rerun was requested. The env-qualified targeted row does not exist; I did not add one or add speculative Agent `PYTHONPATH`. Normal34e Agent lock bytes and Runtime-origin bytes were verified.

No product, test, harness, pin, or integration edits. `git diff --check` passes; worktree clean. Evidence: [evidence.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-classification-review-0753/evidence.md). `DONE` and commit message were written.