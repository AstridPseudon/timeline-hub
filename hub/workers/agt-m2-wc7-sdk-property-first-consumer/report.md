Implemented WC7 SDK consumer slice on base `0b2f662e`.

- Parent `Checkout.attach(...).clip(...).set(hold=...)` now captures via existing `clip.set` and `TimelineSession` outbox.
- Added lost-ACK/restart/exact-retry/reload/guarded-undo proof.
- Added mixed SET/PARAM atomic-refusal proof.
- Unsupported occurrence, narration, draft, and other property shapes remain held.
- No wire/client API, Node save path, or private014 dependency added.

Tests:

- 148 passed: native Checkout, native sync, scalar conformance.
- 22 passed: native Checkout rerun.
- Ruff and `git diff --check` passed.
- No full suite requested.

Remaining old writer: detached `_PublishMixin.publish` → `store.publish_bundle` at `astrid/sdk/timeline/publish.py:44`; narration’s secondary call remains at line 119.

Commit message written and `DONE` marker created.