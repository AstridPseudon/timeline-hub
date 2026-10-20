Implemented the reason-preserving AG01 cut.

- Confirmed legacy `Checkout.publish()` → Runtime whole-document publication carries no reason/rationale field.
- Restored the existing local publish note and original `reason`/revision `evidence` assertions, documenting the WC7 dependency.
- Kept Runtime-authenticated sheet history migration and local draft recovery intact.
- No DTO/API or shared dependency changes.

Tests:

- Targeted journal tests: **3 passed**
- Central `native-script-current-integration --files "tests/sdk/test_timeline_checkout_history_runtime.py"`: **2 passed**
- `git diff --check`: passed

Report and commit message written; `DONE` created.