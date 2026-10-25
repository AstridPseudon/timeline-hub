# D134 independent review

## Verdict: FAIL

The candidate is source-scoped to the two authorized test files and does not
weaken tests, but it does not preserve all required behavior predicates.

### D134-F1 — blocking: recipe persistence/history/restart coverage was removed

In the parent, `test_reference_is_authoritative_and_kernel_never_searches_echo`
submitted `change-echo` for each non-null `echo`, restarted, and then compiled
the reloaded bundle. The candidate removes that Runtime commit and restart. It
restarts only after the first `reference` commit, then changes `current` in
memory. This is explicitly acknowledged in the author's setup proof.

That proves the kernel ignores an in-memory echo while retaining the stable
word reference, but it does not prove that the real provider accepts and
persists the changed declaration, records history/revision state, or reloads it
after restart. The native family still has this path, but the recipe family is
the separate test-local registered-provider path and its original persistence
predicate must remain. Exact7 PASS therefore cannot close this loss.

### D134-F2 — blocking: mirror mutation references are stale after aliasing

Both new helpers do:

```python
mirror = next(... for clip in mirrors ...)
bundle["parent"]["config"]["clips"] = clips
return [primary[...], mirror[...]]
```

`mirror` is a dictionary from the old independent mirror list. Reassigning the
list does not retarget that dictionary. A mutation loop updates the active
`primary` and a detached object. The final bundle looks correct only because
`config.clips` now aliases the primary list; the detached mutation is discarded.

This is especially material in
`test_invalid_authored_reference_never_falls_back_to_valid_echo`: only the
`missing-clip` branch loops over both refs. The missing-word, wrong-pin,
malformed-id, duplicate-id, offset, and other branches mutate the first stale
reference only. No current aliased mirror plumbing is verified for those
inputs, and the helper does not prove conservation of every authored field,
word, anchor, or pin across both views.

### D134-F3 — major: broad aliasing changes all bundle consumers

`bundle(case)` now aliases `config.clips` for every test in both files, not just
the seven exact selectors. The author reports unrelated word cases were not
run. Consequently the claimed unchanged D14/D23/D133 and neighboring predicates
are unverified under the new fixture shape; the alias can hide a divergence that
the former independent mirror copies would expose.

### D134-F4 — major: live result is not against the required Runtime pin

The author records Runtime `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` from
`/home/user/work/runtime`. The requested immutable review Runtime is
`ab1e4f6141987706132916e2da16477f5a019464` at
`/home/user/work/wt/rt-pin-ab1e4f61`. The required pin is clean and was verified
read-only during this review. The reported 7/7 live result is therefore
unqualified for this review; source PASS and live qualification remain
distinct.

## Required follow-up

Restore the real recipe change-echo commit/restart, retarget mirror references
after alias assignment (or otherwise operate on the current captured list),
preserve every original assertion/input, and re-check affected unchanged cases.
Then run only the exact owned selectors with the required immutable Runtime pin.
