## D91 report

- Used exact reviewed candidate `12c4efdd…` / tree `7a37b062…` with Runtime `6634a17f…`, App `24865fa…`, Composition `635f4de…`.
- No product, test, source, schema, pin, or generated files changed. Worktree remains clean.
- Controls:
  - `bash -n`: pass
  - Positive control: exit 17, 4 body bytes
  - Poison control: exit 1, 0 body bytes
- Central request: `rt-D91-final-ten-proof-0427-d91-final-ten-proof-0427-1025042938-2966`
- Exact command: `pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45`
- Result: **5 failed, 5 errors in 6.99s**. Original-third cases hit Runtime interval rejection; authored-first cases hit `missing or ambiguous identity 'repeated-third'`.
- No rerun or retarget occurred.

Evidence: [terminal summary](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D91-final-ten-proof-0427/evidence/terminal-summary.md>), [XML](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D91-final-ten-proof-0427/evidence/output/d91-final-ten-proof-0427.xml>), [first exceptions](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D91-final-ten-proof-0427/evidence/first-exceptions.tsv>).

Commit message supplied and `DONE` created. Next step is Runtime/fixture investigation; this terminal proof is NO-GO.