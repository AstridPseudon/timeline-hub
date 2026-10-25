## Report

- Fixed-input preflight: **PASS**
  - ID: `app-pin-5337b439-p2-native-asset-0305-preflight-1025030857-11110`
  - Host/target: `app-pin-5337b439`
- Body: **QUEUED; result intentionally unverified**
  - ID: `app-pin-5337b439-p2-native-asset-0305-1025030927-27438`
- Plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-native-asset-submit-0305/submission/p2-asset/p2-register-asset-submit-plan.json`

Verified pins, receipts, exact recipes, protected blobs (`spec b3776a…`, receipt oracle `29b223…`), 7.01 GB free, clean worktree, and `git diff --check`.

The first generic CLI attempt captured mutable Agent `562ee30…`; it was cancelled before result claim. Its service rows were corrected to the required Agent `6386c700…`, then the fixed-input flow submitted exactly one valid body.

No product/tests were changed or run. Manager should wait on the same body ID only.