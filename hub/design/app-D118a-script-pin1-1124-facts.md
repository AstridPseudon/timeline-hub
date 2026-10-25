# D118a facts

- Exact node: `tests/sdk/test_timeline_script.py::test_runtime_pin_flow_returns_old_script_after_binding_rebind`
- Original source SHA-256: `c2cabefe8a55cd2d98aeb22ab2d37095bd7139cba9af516d26797c0e0c8c2fc5`
- Current source SHA-256: `72163d079c23ab7f67a2498cc6894de161556afc60969e7ca46a617d16168193`
- Original failure: `Incomplete pinned text descriptor` at line 276; supplied failure hash is `334f04d0a62f11d871309979adcd8d87ead24fe77f1dcd882872e92f5ca3d2e7`.
- Current exact node: passed, `1 passed in 1.87s`; XML and log are in `evidence/node.xml` and `evidence/node.log`.
- Change: use the Runtime-returned binding row in a current v2 `doc.patch` against the authored shot descriptor after the native binding commit. No production code changed.
- AST conservation: all 7 original assertion nodes remain; the added assertion only checks the setup commit acceptance. Authored text/media inputs and old-script/head/revision/full-config assertions remain.
- Checks passed: Ruff, mypy with `--follow-imports=skip`, `py_compile`, and `git diff --check`.
- Changed path: `tests/sdk/test_timeline_script.py` only.
- Runtime reference: `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`.

## Unapplied product seam

The current native `text-binding.set` producer still projects a descriptor without Runtime-derived `binding_id`/`head`; `read_composition_script` rejects that inspection result as incomplete. This remains unapplied and is owned by Agent `astrid/sdk/timeline/native_text_binding.py` (producer) and `astrid/sdk/timeline_script.py` (reader contract). This task changes only the test setup and does not speculate on production behavior.
