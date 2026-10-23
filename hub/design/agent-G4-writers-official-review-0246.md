# G4 writers official-join review — FAIL

Reviewed candidate `135a1ab5a5d39dd796e5d7c6975b805e2e4ca147` against current parent `5243eca7354db667eaa33ac69c725ddb33147d15` and official parent `2410c3bbbb14f4ca2b177dc894f5eea0246826ee`, with PLAN §3 and `commit-v2.md` §§1–7.

The candidate fails source preservation: clean `git merge-tree` is `fbd602303047aa104dff1c8be6b90543a5ba8fea`, while the candidate differs from it by exactly six resurrected `live-scenes` files deleted by V4 commit `ef6455ebdff80d20a2d15f9cae9e5e58e393d5ca`. They must remain absent.

The candidate also fails actual wire independently. The first official-wire failure is the provider's valid native alias `occurrence:occurrence-1/text-binding:voiceover_script` (with the related collection alias) rejected by Runtime `timeline_commit_auth.site()` at its unsupported-alias fallback. Runtime schema/store already admit/project these refs; repair belongs in Runtime authenticated alias normalization, not Agent writer code. Author's exact result was 10 passed/11 failed; no fake transport was credited.

Targeted reviewer evidence: narration/element changed behavior and exact bad case **42 passed**; R1/P1/R3/V1/V4 pure Python lane **131 passed, 41 skipped**; actual original wire test file unchanged. Composition/capture host checks were attempted but remained unverified because the sandbox lacks provisioned Remotion peers/package. `git diff --check` passed. Client pin is exact official `21482a416d1f0f976ec563b9e1bf96a765f80e56`; known generated `merged` decoder bug remains unchanged. No tracked edits.
