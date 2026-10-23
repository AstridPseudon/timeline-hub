Corrected only `docs/runtime-portability-testing.md:112–115`. Read PLAN and independent review 2344 first. No decisions changed or blockers.

The wording now matches `.github/workflows/ci.yml`’s Ubuntu/macOS portability matrix and README’s Windows policy. Windows native validation remains explicitly outstanding.

Complete diff, including exact old/new statement:

```diff
diff --git a/docs/runtime-portability-testing.md b/docs/runtime-portability-testing.md
index 57289e7cc..31188e3f8 100644
--- a/docs/runtime-portability-testing.md
+++ b/docs/runtime-portability-testing.md
@@ -109,8 +109,10 @@ qualification belong to the subsequent installer and agent workstreams.
 Port-binding and process-signaling integration tests are written and collected
 but require an unrestricted runner. Exploratory server tests were rejected by
 the sandbox before binding; the full macOS suite could not be completed here.
-Windows-native APIs cannot be executed on this host. The three-host CI job is
-the remaining native validation gate, not a claim that it has already passed.
+Windows-native APIs cannot be executed on this host. The portability CI job on
+Ubuntu and macOS is the remaining native validation gate for those hosts, not
+a claim that it has already passed. Windows is not supported yet and has no CI
+job; Windows-native validation remains outstanding.
 The safe test selection and final result are recorded below.
 
 Final safe selection: **453 passed, 13 skipped, 9 deselected** on macOS.
```

Checks—all exited 0:

- `git diff --check`
- `git diff --name-only fe4e7c38f8072181a7c9a67bb7766816087a8a25` — only the allowed Markdown.
- `git diff --no-ext-diff --exit-code fe4e7c38f8072181a7c9a67bb7766816087a8a25 -- . ':(exclude)docs/runtime-portability-testing.md'` — empty; all other tracked files unchanged.
- `git merge-base --is-ancestor aa6c5b0cb1b05e47fc3bb597f63565f1aa8f7a70 HEAD`
- `rg -n 'Windows|three.host|CI|native' docs/runtime-portability-testing.md .github/workflows/ci.yml docs/visual-seam-policy.md README.md` — inspected; corrected gate wording is coherent.

No tests, lint, type checks, or generators rerun. Reused independent2344 evidence: 208 behavior tests, 88 contract/client/artifact tests, generator/artifact checks, Ruff and compile passed; Pyright had 28 baseline diagnostics and zero new. Production caller verification at `store.py:2023`, `service.py:1889`, and conftest→lanes remains prior evidence. Contract §§1–7 and all product behavior are unchanged. No Windows validation is claimed.

Wrote the U1c commit message and created `DONE`. Next: independent focused re-review; hold integration until freeze.