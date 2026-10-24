## Report

- Ran list-only selectors: all three selected exactly 1 original test.
- Exact tuple verified in every manifest; pinned App venue: `app-pin-bceb0350`.
- Preflights passed; all originals failed:

  - Popup ADD — body `...1024222729-5083`; digest mismatch at line 452.
  - registerAsset — body `...1024223207-1155`; 90s commit-response timeout at lines 149/497.
  - Automatic placement — body `...1024223714-8259`; 90s commit-response timeout at lines 149/565.

- Readiness passed for all three. JUnit and manifests retained in central result directories; test hashes were unchanged before/after. Runtime: Node 20.19.4, schema digest `sha256:867f3553…`.
- No product/test files changed; worktree is clean.
- Decision: preserved the required pins using the prior exact submit packet because mutable Agent home had advanced beyond the pinned Agent SHA.
- Full tour not run because isolated cases did not all pass.
- Wrote P2 commit message and created `DONE`.