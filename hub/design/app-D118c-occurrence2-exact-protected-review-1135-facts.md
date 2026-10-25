# D118c occurrence2 exact protected review facts

Verdict: PASS_SOURCE. The exact candidate edb6b9d839ea2f5e6c4184a5624802cfb57e622d changes only tests/editing_conformance/test_commit_runtime_occurrence_create.py from base 36e44e1c0ed9b454faaf973715a2be7119552d0a. The frozen candidate SDK branch does not contain this file.

The source delta is exact: old SHA-256 26ecb3e8da202dc9a1113f942cf9c1a7384600d8662cb9c1e8d983caf17afe6f, new SHA-256 f1d86c7a95140a3f69a60e3ac348511eedf2eca52d75da135eb04450f9935ca1; 29 assertions become 31. The only delta is replacing error.value.status == 409 with == 422 and adding details.status == 'invalid' plus details.code == 'unsupported_timing'. All other assertion source segments are byte-exact. The authored invalid_birth['args']['on'] = 1e308, exact unsupported_timing reason, no-write/history checks, and inverse/redo/retry purposes remain.

C0 contract/commit-v2.md:1299-1315 states that a request invalid at its claimed base, including final-validation timing failure, is HTTP 422 with details.status: "invalid", and explicitly distinguishes later-head guard failures. Current Agent _commit_errors.py:65-71,90-110 classifies unchanged-base unsupported_* as invalid, emits 422, and sets details.code to the reason. Approved D16 is cited only for the retained caller/dependency scope (app-P1-D16-caller-sol-2325.md:1-14,33).

The qualified Runtime is the receipt-backed immutable /home/user/work/wt/rt-pin-42aad0e9, HEAD 42aad0e92f6da8ea83dd0a382a87e3acd12651b0, tree 085a5be70b56353deb41ae7d743336a4ccb7f29c, clean. Fresh raw hashes are in facts.json; the private generated fixture roots used git archive HEAD from this pin, had no .git, matched key source hashes, and passed the established generator plus manifest commands.

The two exact nodes were run once with -m integration against that pin. Both reached the new invalid-timing assertions and the unchanged-base no-write/history assertions, then failed at retained lower Runtime seams: [False] at timeline_commit_auth.py:1645 during media_undo (inverse stage materialization differs from its recorded source image); [True] at timeline_commit_auth.py:2267 during grouped birth (provider intermediate image lacks an authenticated physical promotion). These are preserved genuine outcomes, not classified as product defects here; the owner boundary is authenticated Runtime producer/source comparison and guard remediation. No full/broad suite was run and whole-case green is not claimed.

Static checks: Ruff, mypy --follow-imports=skip, PYTHONPYCACHEPREFIX=... python -m py_compile, git diff --check, and the exact AST/delta conservation check all passed.

