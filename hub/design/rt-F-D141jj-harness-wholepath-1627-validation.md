# F D141jj validation

Read-only/static checks performed:

- Read `PLAN.md`, the controlling publication, the exact failed log, the
  original `check_jj.py`, and the candidate caller/D68/lifecycle/checker
  sources.
- `git show ce9e0532...:evidence/tmp/check_jj-positive.log` — exact failed
  sequence confirmed.
- `sha256sum` on the original checker, caller, lifecycle, D68 wrapper, SAME33
  script, and controlling publication — recorded in `source-manifest.json`.
- Static line/AST inspection only; no checker, staging, builder, installer,
  service, browser, socket, full suite, or qualification command was run.

Result: source identity is preserved in the supplied evidence. The complete
checker result remains invalid for qualification because the stale-upstream
negative was intercepted by the shared trace fixture and the checker also
does not observe nonzero caller returns as refusal exceptions.

