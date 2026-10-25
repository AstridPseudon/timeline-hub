# D134 mirror7 final review

## Verdict: PASS (source-first gate)

The cumulative diff from `a30e74e901a28b39c28facba3deb00d76f186e23` to
`ff88764f0d3d3b3efcb03e8dec4feb735810be78` contains only the two authorized
test files.

The specific persistence concern is resolved in the final source. In
`test_word_binding_recipe.py::test_reference_is_authoritative_and_kernel_never_searches_echo`,
the test performs the first anchor submission, restarts before recapturing the
current bundle, performs the real `change-echo` submission for non-None echoes,
restarts again, and recaptures before the test-local echo perturbation. This
preserves the production Runtime commit/restart route present in the baseline;
the in-memory perturbation is an additional kernel-authority check, not a
replacement for that route. The test does not independently assert a history
row or the persisted declaration after recapture, so live validation would
still be the evidence for those runtime details.

Both helpers first compare parent and `parent.config` clip IDs and complete
clip dictionaries, then assign `config.clips` to the current captured
`parent.clips` list and reacquire both references. This removes the prior
recipe-wide aliasing and confines aliasing to the tests that deliberately
mutate mirrored clip applications. The mutations preserve the authored clip
dictionary, stable word IDs, anchors, opaque fields, and pinned source mapping;
the helper does not alter the source/pin capture. The invalid-reference cases
mutate the aliased reference consistently, including the missing-clip case.

Unchanged cases retain their original parent-clip, source-pin, no-write,
history, undo, restore, reload, and failure predicates. No production code,
runtime code, generated code, fixture source, skip/xfail, selector, or
assertion weakening was introduced.

No behavior selectors were run: the task explicitly requires the source-first
gate and forbids tests before the exact immutable Runtime prerequisite is used.
