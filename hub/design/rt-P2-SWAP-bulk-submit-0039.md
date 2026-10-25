## Report

- Copied committed plans/profile lineage into worker evidence, preserving hashes.
- Verified fixed tuple and clean detached checkouts.
- Ran central service serially:
  - SWAP preflight: pass, ID `...1025004133-9183`
  - SWAP original: fail, ID `...1025004250-11089`; unexpected `created` field.
  - Bulk preflight: pass, ID `...1025004623-19129`
  - Bulk original: fail, ID `...1025004656-21061`; commit POST response timed out after 90s.
- No product or test files changed; worktree remains clean.
- Recorded profile-hash inconsistency: lineage claims `7c1663…/1c2ac0…`, actual committed files are `e082c9…/fe3aac…`.
- Wrote commit message and created `DONE`.

Recommended next steps: investigate the SWAP `created` field mismatch and bulk commit-response timeout using the durable service logs/traces.