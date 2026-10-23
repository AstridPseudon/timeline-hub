## Report

- Fixed only the P1 row in [suites.conf](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf:242): `actual-request;; fi;; esac` → `actual-request; fi;; esac`.
- Real outer capture saved the exact `bash -c` `$2`; outer and inner `bash -n` both pass. Pre-fix captured inner fails with syntax error.
- Qualification passed: path positives/negatives, symlink guard, fail-fast exit 17, export/eval roundtrip, stage exit 7 with durable log and no body execution.
- No browser, backend, HTTP, global setup, seed, body, or full suite run. Existing service 4526 was not resubmitted.

Hashes: row `9935ad4f…997939`, captured inner `777511a9…f4e2d`, P1 body/source unchanged, Gate 5 and Composition archive unchanged. Worktree clean.

A concurrent update added two P3 continuation rows during qualification; they were preserved untouched. Commit message and `DONE` marker created.