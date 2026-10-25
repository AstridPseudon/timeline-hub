## Result: PASS

The claimed contract necessity is confirmed. No product or test files changed.

Runtime’s native `parent/collection:asset` read is normalized to `{"kind":"scope","ref":"parent","path":[]}` by `native_site()` and `validate_step()`; `covers()` cannot accept narrower field/collection entries for this capture.

A union of existing field entries could preserve raw/config mirror absence/null/dict states, and existing collection entries cover members/order where applicable. However:

- Field/collection entries cannot cover Runtime’s required parent-root scope.
- Adding `scope,parent,[]` makes Agent `rebase_patch()` guard every parent write.
- The same dependency is consumed by inverse selection and `_dependency_overlap()`, so guarded undo also becomes overbroad.
- Asset registries are object maps, not C0 identity arrays; collection encoding cannot represent their complete value state.

This is a normative C0 contradiction: one dependency array must simultaneously be Runtime’s complete authenticated capture union and Agent’s narrow merge/undo guard index. The exact unresolved contract question is whether C0 should authorize a separate authenticated multi-location logical-shape representation/channel, or explicitly permit distinct Runtime authentication and Agent rebase/undo representations.

The six failed prepared arrays remain UNKNOWN. Existing passing comparators—explicit raw/config asset field reads and ordinary doc.patch field/collection reads—do not exercise the native asset-collection alias.

Checks:

- In-memory compile/AST checks for Runtime and Agent sources: PASS.
- `git diff --check`: PASS.
- Worktree: clean.
- No pytest, fixtures, services, browsers, or full suites run.

Next step: resolve the single C0 question, then perform the protected six-case proof with the original assertions intact.