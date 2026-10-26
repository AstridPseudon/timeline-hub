# D141l handoff

Completed the existing `app-pin-d822d2f5-full-1026063854-17524` receipt
attachment only. The request remains `queued` with its existing `KEEP` marker;
no fresh request, body, result, or admission claim exists.

- Source: `/home/user/work/wt/app-pin-d822d2f5`, clean HEAD
  `d822d2f5d2bd05187b4ff5b6071c3e13945d4747`, tree
  `2af40a015057779ceb4e4b37cad62e1469aa7e36`.
- Request SHA-256:
  `26f6a8d0dfded2d7c96eba9cf2577862da0a841c91e84a26debe7a933a304321`.
- Receipt: `tests/app-pin-d822d2f5-full-1026063854-17524/recorded-measured-floor.json`;
  SHA-256 `4c01fb145865378a8405f8cdca5e263c9a9a44eac30046113b780e274aa52fbc`.
- Validator exit `0`; exact floor `4793895424` bytes.
- Current actual free space: `4699176960` bytes at
  `2026-10-26T06:53:53.474Z`; service must independently meet the floor before
  this same ID can leave the queue.

Next step: the normal dispatcher/test-run path may continue this same queued ID
when its unchanged service guard admits it. Do not create a duplicate ID or edit
the queue state.
