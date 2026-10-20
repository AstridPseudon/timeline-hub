# Independent review: legacy selected PARAM positive

## Verdict

**APPROVE_BOUNDED_TEST_FIX.** Candidate `tl/agt-m2-authority-legacy-alias-positive`
(`6868e16a590af64fc764159489b8e4ed22f526d0`) restores the original positive with
an authentic pre-enforcement acceptance fixture and preserves the original
inverse, alias, opaque-data, and exact selected-object assertions. It makes no
product, provider, public S2, generated-client, Runtime artifact, or lockfile
change.

This is not compatible-integration approval. The independent authority review's
F1 same-batch inverse gap remains inherited from base, and Runtime port ACK plus
App authenticated/browser gates remain separate qualifications. They are not
introduced or repaired by this test-only change.

## What was verified

- The original `test_inverse_of_older_param_record_uses_only_selected_identity`
  passed from an immutable candidate archive: **1 passed in 1.06s**.
- The selected-schema neighbor pair, including the native companion,
  passed: **59 passed in 53.94s** using the frozen real Runtime archive.
- The native companion passed independently: **1 passed in 1.76s**. It restores
  an authenticated backup, checks exact persisted history, retries the original
  ledger request, refuses `seed=16` against retained max-10 authority despite
  the ignored max-20 alias, performs inverse/redo, and accepts a new `seed=9`
  after restart. Its object-read observer saw only the selected revision's
  object. The monkeypatch is observation-only; it does not authorize acceptance.
- The implementing worker's final lanes were also inspected: parameter/history
  lane **447 passed**, native Runtime lane **27 passed**, and the original
  positive passed with `--runxfail` before its marker was removed.
- Ruff passed on all changed Python files (`All checks passed!`), and
  `git diff --check 654da693..6868e16a` passed.

## Fixture and boundary review

The fixture records immutable source identities in its README and generator:

- Agent old provider: `ce363f6d6d60e504dbd4d79803c2d6299f648ade`, tree
  `78af007de1d7c5a59f86fffacd9823de355cd260`.
- Runtime: `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`, tree
  `1711b198be7f693f11ee4640eb0922ec0d0da952`.

The generator uses private `git archive` exports and the normal old provider,
Runtime admission, commit, and backup APIs. It does not check out a moving
worktree or guess at `HEAD`. Independent regeneration from those archives
exited 0 and produced the same seven-member, 801,680-byte fixture shape.

The ZIP contains only `accepted.json`, the fixture operator key, the authenticated
Runtime backup, its manifest, and two CAS JSON objects. No source/build tree,
SQL write, Prepared provider, validator replacement, schema override, or
authority-accept monkeypatch is present. The backup is restored and HMAC-checked
by the native companion.

The detached test reads the genuine accepted facts and changes only its in-memory
record dependency/binding projection to the old inverse-compatibility shape.
It does not claim that the untouched native accepted record lacks
`params.snapshot`; the native record retains that field. No explicit
`set-element` is used, so the legacy `element_ref` alias is not erased by
current cleanup semantics. The alias and canonical `elementRef` point to
distinct genuine admitted revisions, and opaque `params` values remain present.

The source diff from `654da693` contains only the two tests, one JSON reader,
the fixture, its README, and its generator. Product tree, `runtime.lock.json`,
and generated-client paths are unchanged. No full or `full*` suite was run or
requested.

## Required follow-up boundaries

Keep F1's concrete same-batch inverse reproduction and the Runtime ACK/App
gates in their own reviews. Do not attribute them to this fixture or use this
bounded approval as release/integration approval.
