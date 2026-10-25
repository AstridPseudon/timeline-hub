## Report

- Verified exact reviewed blobs: Agent source `221e517...`, test `d85d96e...`; tuple locked to Agent `8aa672`, Runtime `0c62dfa6`, App `1e34f8`, Composition `635f4de0`.
- Central old-RED: `rt-R2-restore-candidate-main-0525-r2-restore-oldred-overlay-0525-1025053322-31475` — `1 failed, 3 passed, 1 error`. The reviewed regression failed as expected; unchanged word-binding control errored during setup.
- Central candidate run: `rt-R2-restore-candidate-main-0525-r2-restore-newgreen-preflightfix-0525-1025053518-30269` — `4 passed, 1 error`. Candidate regression and all three strict controls passed; the same unchanged word-binding setup error prevented full GREEN.
- Controls used the D73 launcher with parsed positive exit `17` and poison exit `1`; no local pytest/body execution.
- Initial zero-body harness/preflight failures were preserved and disclosed. The central suite registry was restored byte-identically (`sha256 4fbde9...`); Runtime worktree is clean.
- Evidence is under the worker evidence directory (~880 KB). Commit message written; `BLOCKED` marker created.

Blocked until the unchanged word-binding setup control is independently fixed or qualified; product remains unmerged.