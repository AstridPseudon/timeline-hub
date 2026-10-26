# D141 P2 independent review

Verdict: PASS.

- The five publication originals match the author’s committed Composition
  evidence byte-for-byte and match the manager publication receipt hashes.
- The retained 3118 assertion attachment has two actual-only
  `commands[*].bindings[*]` objects, 22 safe structural key paths, and no
  expected-side structural additions. The published path sequence matches the
  retained diff twice; no unknown paths were introduced.
- The current and prior App source commits resolve the same recorded spec blob
  and source SHA. The recorded assertion anchor at source line 757 is the
  strict `expect` location inside the history helper; it is not a raw diff
  excerpt.
- The retained prior run has eight cases and counts 2 PASS, 2 FAIL, 1 ERROR,
  3 NOTRUN. Its exact automatic-placement case is PASS (88.78 seconds) even
  though the overall run is FAIL with exit 1. The current/prior App, Agent,
  Runtime, and Composition commit/tree tuple was independently resolved.
- Current manifest/XML/log/diff hashes and prior archive/XML/manifest/request/
  source-plan hashes all match their recorded receipts. Raw artifacts remain
  in place and were not modified.

No history-field values, dynamic identifiers from the diff, credentials,
request payloads, images, or raw test-diff text are included here. No semantic
classification or intended-history interpretation is made; Runtime0140 owns
that decision.
