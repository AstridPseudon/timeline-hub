# Handoff: ap2-P1 isolated Python environment

App base was `18354adfa3e8f12b24816a159f28a9a6cbb9a3f6` (tree `90e739bca902ed0c5ed5a4641e9fdb925aae2b1e`).

The only product-source change is in `tests/e2e/local/support/astrid.ts`: `AstridCli.env()` now sets `PYTHONPATH` to Astrid first and the exact existing `RUNTIME_CHECKOUT` second. `spawnGroup` still receives this environment with `exactEnv: true`, so isolation, credential-file use, redaction, and source guards remain in force.

The existing `ap2-P1-chain-h6` row in `scratchpad/orch/tests/suites.conf` was adjusted only from a `HEAD^` equality guard to `git merge-base 8770aa1625198826778828173ef6e2c55a3c07f3 HEAD`, preserving the reviewed product/spec/resolver/artifact hashes. Modified row hash: `7b41bddf895dc8eda8cc0c040a07d11d6e7b482a941b41b1482f0adf5ee1f97d`.

Offline proof used Agent `f894c3c9dda25ab03527eeb7f52da5da31d627c1` and Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`; the child imported Astrid from `/home/user/work/wt/agt-pin-f894c3c9/astrid/__init__.py` and Runtime protocol from `/home/user/work/wt/rt-pin-34eac004/runtime_protocol/__init__.py`. The constructed child path was exactly `/home/user/work/wt/agt-pin-f894c3c9:/home/user/work/wt/rt-pin-34eac004`.

Validation passed: TypeScript no-emit, ESLint on `astrid.ts`, exact P1 list (`2 tests in 1 file`), offline child import, and `git diff --check`. P1 spec SHA-256 remains `dfcdee357a822bb8516fdcadae88a074a78c7bdaca3d053991d28721ebfae7d2`; durable `819acf` graph and 6144 heap checks remain unchanged. The live original two-case run is intentionally left to independent review and the central test service.
