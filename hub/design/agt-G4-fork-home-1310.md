## D30 Report — PASS (scoped G4)

Actual integrated source:

- SHA: `9b055a93ff15fce0a2e80f2647d47743b1fc4c33`
- Tree: `cba425b61958f380f25b7bdea83d23c92f627761`
- Runtime: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`

Results:

- Authoring/fork semantic subset: **33 passed, 1 duplicate deselected**
- Original authoring fork: **41 passed, 1 duplicate deselected**
- Native fork: **8 passed**, including 7 negatives
- Focused replay: **2 passed**
- Conformance: **79 passed, 1 integration deselected**
- Ruff, mypy, vendor lock, artifact manifest, and diff check: **PASS**
- Protected AST/byte hashes: **exact**
- Production caller confirmed: `publish_authoring_candidate → writer.commit_timeline`
- Post-fork reservation witness: accepted, with source/parent/internal closures preserved
- Lost custody: **none**
- Worktree remained clean; no source or merge changes made.

Durable XML and custody evidence: [qualification.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-fork-home-1310/evidence/qualification.txt)

The separately owned duplicate review (`23f`) remains unmerged; this is not a full G4 completion claim.