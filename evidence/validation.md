# Validation record

## Independent checks performed

- Verified receiver, candidate, and receiving-worktree commit/tree IDs with
  Git; the receiving diff SHA-256 is
  `3ffa61f81dfdf088693fc728e824454321c82963b73b3abbe5b1066074919cda`.
- Verified the two changed paths only and all received/protected SHA-256
  values in `source-manifest.json`.
- Verified the immutable Runtime pin is clean at commit
  `ab1e4f6141987706132916e2da16477f5a019464`, tree
  `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- Compared Python ASTs without running pytest: 19/19 non-FPS validation
  functions and 7/7 prior D136 test functions are unchanged; three functions
  are additive.
- Parsed the private JUnit XML structurally without exporting payload or raw
  stack: exact nine case names, 9 tests, 9 errors, 0 failures, 0 passes, and
  0 skips. All nine error messages have the same first-seam text.
- Verified private XML, log, and run-metadata files are mode 0600 and recorded
  their hashes in `source-manifest.json`.

## Supplied checks reused

The receiving worker's exact focused evidence was reused: 57 passed, Ruff
PASS, mypy PASS, compile PASS, and `git diff --check` PASS. The completed
independent D136a source/security review 2119 and D100 security review 1803
were read and their explicit limits retained.

No pytest, full suite, browser, socket, collection, profile, benchmark,
acquisition, or rerun was performed by this reviewer. TSC/lint is not needed
for unchanged source in this read-only custody/result review.

## Actual run facts

The sole run started at `2026-10-25T21:38:05.288316673Z`, with
5,316,198,400 free bytes, ended with 5,309,915,136 free bytes, measured
35,996,764,405 ns, and exited 1. XML-reported time was 34.783 seconds.
There was no retry, adaptation, selector substitution, alternate Runtime,
fixture migration, or false-green conversion.
