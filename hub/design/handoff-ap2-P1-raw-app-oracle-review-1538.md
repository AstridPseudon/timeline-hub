# Handoff: P1 raw App oracle review 1538

**Review PASS for the scoped one-assertion correction; P1/H3 remains NO-GO.**

Author and review resolve to `6759fcacdb4f56f2ceed356d1a8f0232cffda55a`;
tree `9d2634630f59861cc4415fb522a1d74af0f5c261`; base
`6294895141ffe0e92a83c61ba0541249a41243eb`. Base-to-author is exactly one
insertion/one deletion in the P1 test, changing line 824 to whole-object
equality with captured `originalClip.app`. All other bytes/assertions and all
production code are unchanged.

Independent review confirms this is the correct oracle for a from-only trim:
the mounted UI split copies the authored clip object, and the Source In caller
emits only the timing `from: 0 -> 3` patch. No implicit clear or self-derived
expected value was introduced.

Checks passed: root/app/node TypeScript no-emit, targeted ESLint,
`git diff --check`, and Playwright list with exactly 2 tests. No live/full body
run was performed. The separate 1531 second-case no-POST failure remains open;
P1 cannot be accepted until the original current chain passes with no hidden
failure.
