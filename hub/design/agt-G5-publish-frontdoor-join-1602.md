# G5 normal CLI publisher frontdoor join

Worker agt-G5-publish-frontdoor-join-1602 imported the two requested test
blobs from tl/agt-G5-publish-ports-return-1548 onto 23cac8b72 and made only
the required-key correction in parser-only parity vectors. Final provenance
and exact commands/results are in:

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-publish-frontdoor-join-1602/report.md

Joined result: 74 passed, 2 failed. Adjacent frontdoor tests: 6 passed.
The two failures are independently diagnosed normal-frontdoor wrapper
boundaries (raw empty parent.config.app mismatch causes a clean write; human
output uses generic envelope formatting). No product files were changed.
