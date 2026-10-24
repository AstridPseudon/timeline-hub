# D40 installed original review

Overall: **FAIL for complete custody; PASS_WITH_EVIDENCE_CAVEAT for the original result.**

- Original body credit: **PASS, 1/1**, `1 passed in 3.32s`; original test unchanged with **3/3 assertions** and matching AST/source hashes.
- Current vs installed: candidate `2007cf7aaf` versus installed Agent `ba8f0bc…`; six relevant production modules are byte-equal, and production imports resolve from installed `site-packages`.
- Runtime custody: **PASS**. Runtime `f3208b…`, direct URLs, markers, five fixture hashes, non-symlinks, and `tests.__path__`-only fixture injection verified.
- Production caller: **PASS**. Installed `GenericPackHost.admit` → `invoke_capability` → subprocess worker path is the normal caller.
- Missing custody: the temporary `origin_observer` source/hash is not durable, so forwarding of args/results/exceptions and absence of observer mutation/bypass cannot be independently verified. `imported_from` was not directly captured; evidence reconstructs it from the retained fixture/source expression (`direct_stdout_observation: false`).
- The command used a temporary observer-only `PYTHONPATH`; no production module originated there. No editable install or metadata alias was found.
- Contract path was absent; reviewed `/tmp/.../scratchpad/orch/design/commit-v2.md` as instructed.

Evidence: [d40-installed-original-positive.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D40-integrated-installed-0520/evidence/d40-installed-original-positive.json>)  
SHA256: `77bddf5b34c107a53a518823e4faf42a6d373646636a1931596454d069af495f`

No tests or body reruns performed. Worktree unchanged. DONE marker and commit message were written.