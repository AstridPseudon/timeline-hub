# R2 original `[True]` evidence review

## Verdict

**FAIL_EVIDENCE.** Evidence custody and source integrity pass; the exact lower
redo-birth result does not pass. The owner is **UNKNOWN**. The smallest proved
seam is the Agent inverse/recording/materialization to Runtime authenticated
inverse-boundary alias-validation boundary. `EXACTMISSING` is explicit in
`review.json`; no source fix or ownership claim is made.

## Independent receipt checks

- Agent `d4ba991638f7d94e6b9f91f5a463cd3587af00eb`, tree
  `6abf383217363d08fe0cf00558b010f5a9dd506f`; Runtime
  `ab1e4f6141987706132916e2da16477f5a019464`, tree
  `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- Manifest, admission, source-map and result JSON parsed successfully.
- `original.xml` parsed successfully: one testcase, one failure, zero errors,
  zero skips. SHA-256 is
  `9464f762b8606e04a3680a42791f038c142ce1ab02e271ec78b93c8183f3bdfb`; size
  16,823 bytes.
- Exact selector inventory is unchanged and selects `grouped=True` from the
  two-case parametrization. Test source SHA-256 is
  `f1d86c7a95140a3f69a60e3ac348511eedf2eca52d75da135eb04450f9935ca1`.
- The XML records raw exit 1, 1 failed, and 8.188 seconds. The first unmet
  operation is `inverse(undone, 'redo-birth')`; the outer assertion is the
  unchanged subprocess return-code assertion at test line 70.
- The traceback's actual stage is Runtime `validate_step` line 426,
  `native_site` line 218, then `site` line 156, which rejects
  `provider occurrence alias is outside its boundary`.

## Whole-path conclusion

The genuine caller reaches the registered Agent provider through
`RuntimeService.commit_timeline`. Agent loads authenticated undo history and
boundaries, runs `apply_inverse`, and records inverse-stage ranges. The
`CommitPatch` layer then projects stage-local effects and materialization
successor/edge bindings. Runtime validates the prepared record against the
source/base closures, sequential command inputs, authenticated continuations
and history before publication.

The failure is specifically during a recorded native read lookup. Runtime's
`site()` requires exactly one occurrence row in the command boundary before it
can resolve the occurrence's shot/internal source. This proves the refusal
seam, not the owner. Static source also shows the narrow inverse-absence
exception and the later effect/materialization checks, but the public receipt
does not expose which recorded read, boundary image, stage range, physical
root, owner edge, or continuation was supplied at redo.

Therefore it is not safe to say whether the Agent emitted an invalid read or
stage boundary, or Runtime applied the wrong boundary/projection. Final effect
and closure conservation are unverified because validation stops before those
facts can be compared.

## Comparators and limits

The earlier original10 evidence reviewed at 1357/1405 has the same safe
occurrence-alias error class, but its first unmet operation was grouped
`undo-birth`; this exact lower result reaches `redo-birth`. The separate
`genuine3` and `native2` PASS controls retained by the 1550/1537 release
receipts are not original `[True]` closure credit. No original closure is
claimed.

Admission in the producing receipt was 5,130,645,504 bytes free before the
single body and 5,108,240,384 after, with no concurrent heavy body. This review
did not rerun the body, native smoke, old controls, full/family/P4/browser
paths, or any D130 held WAL/SWAP qualification/store-recovery work.

## Checks run

Read-only checks performed:

```text
Python JSON parse/hash of manifest, admission, source-map, result: PASS
Python ElementTree parse/hash and per-case inventory of original.xml: PASS
Python AST parse and selector inventory for the retained test and reviewed source: PASS
git diff --check (review worktree, Agent pin, Runtime pin): PASS
Relevant Agent d4ba -> released a0d839 source comparison: identical
Relevant Runtime ab1e -> released a5fc auth/store source comparison: identical
```

No product tests, typecheck, lint, build, package, collector, reconstruction,
or source edits were performed. No product security PASS is added.
