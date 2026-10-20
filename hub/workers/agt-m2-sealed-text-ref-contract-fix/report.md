Implemented the minimal Agent-side regression and peer proposal.

- Added exact authored-key coverage for `occurrence:occurrence-1/text-binding:voiceover_script::`; authorship and expect claims remain preserved.
- Confirmed Agent schema `6ba…` accepts the key.
- Confirmed current Runtime integration rejects it, while frozen Runtime `a0dca169` accepts it—indicating a source/artifact mismatch in the failed qualification.
- Published proposal and peer request: [agent-sealed-text-ref-contract-fix.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-sealed-text-ref-contract-fix.md)

Tests:

```text
pytest ... tests/editing_conformance/test_recipe_text_binding_native.py
26 passed
git diff --check
passed
```

No Runtime/schema/product bytes were changed. Commit message and `DONE` marker were written.