# P5 D141 immutable Agent-tree correction handoff

Completed the requested finite metadata correction.

- Original immutable source remains at
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/rt-F-D141-postREG-custody-review-0513-p5-applicability.json`.
- Original SHA-256: `a46bcb2d7e566b01c54da297968a2236eb81d6598f5ac85bf18c55e70d096389`.
- Corrected derivative: `p5-applicability-corrected.json`.
- Derivative SHA-256: `688d08bc899c3c1583fb2010d0f8ff2251e2c593b24d62d2a703856d90a26ce6`.
- The sole correction is `/actual_integrated_heads/agent/tree`, from
  `92a3ffdb5a8bf476f10bfa1bbda3e2856fb9938c` to
  `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`.
- Git proof: Agent head `8585ed9c0404d0187b2ce70242d25114a32747c2` resolves to
  tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`.
- The 0513 handoff agrees with Git. The separately named 0513 source manifest
  still contains stale copied tree text `92a3ffdb5a8bf476f10bfa1bbda3e2856fb9938c`;
  this finite unrelated metadata discrepancy was reported and not modified.
- The original 6934 38/38 PASS at Runtime 6a / Agent 28 remains untouched and
  is not retargeted. Source-independent 0513 applicability PASS remains
  controlling for final Runtime 95d / Agent 8585 changed-path applicability.
- No tests were run, as explicitly excluded; this work is read-only evidence
  correction and structural/hash/Git validation only.

The correction receipt is `correction.json`. The production caller remains on
the original P5 path; the derivative is separately named for human/control use.
