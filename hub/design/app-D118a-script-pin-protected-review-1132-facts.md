# D118a protected review facts

- Verdict: **PASS**.
- Candidate `706e835598f9b00d9b27bf02a5539be57de6025b` vs base `36e44e1c0ed9b454faaf973715a2be7119552d0a` changes only `tests/sdk/test_timeline_script.py`, exactly 12 insertions and 0 deletions.
- Candidate source SHA-256: `72163d079c23ab7f67a2498cc6894de161556afc60969e7ca46a617d16168193`. Parent/original source SHA-256: `c2cabefe8a55cd2d98aeb22ab2d37095bd7139cba9af516d26797c0e0c8c2fc5`.
- Exact retained node passed independently: `1 passed in 2.41s` using `/home/user/work/wt/rt-pin-42aad0e9`, Runtime `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, and the normal checkout receipt `queue/done/checkout-runtime-42aad0e92f6da8ea83dd0a382a87e3acd12651b0`.
- The immutable Runtime checkout was clean. XML/log are in `evidence/node.xml` and `evidence/node.log`.
- Ruff, mypy with `--follow-imports=skip`, `py_compile`, and `git diff --check` passed.
- AST conservation: all 7 original assertions remain as an exact multiset subset; all 49 original call nodes remain as an exact multiset subset. The authored media inputs and old-script text/head/revision/full-config assertions remain unchanged.
- The test body predates D60 (`0d5d16af6f83d595144d21ea1cef2b5a468b9836`); the 12-line `pin-script-descriptor` patch is absent from the D60/upstream refs. This review treats the patch as local setup, not upstream behavior.
- Purpose finding: the added `doc.patch` uses the row returned by Runtime’s public `list_project_shot_text_bindings` and sends it via the registered current v2 commit provider. It does not fabricate `binding_id`, `head`, history, or media.
- Unapplied live product seam: `astrid/sdk/timeline/native_text_binding.py` strips Runtime-derived `binding_id` and `head`, while `astrid/sdk/timeline_script.py` correctly rejects incomplete descriptors. This remains a separate Agent owner/input; the setup workaround does not claim it fixed.
