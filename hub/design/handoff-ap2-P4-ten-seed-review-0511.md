# Handoff: AP2 P4 ten-note seed review

**Result: PASS.** Reviewed candidate commit
`0afe4e082fd01fc7ffbff469b842538dc21fa50b`, tree
`41b002d59bcbcca0840a774b2bb8b7620e4c92f4`; staged base is reviewed `9b658b28c3a7bc3ebda3ad5a7b5b417d78553720`, tree
`84bd8ef3429c06ced18c0639388be8b2c8ecd030`.

The candidate changes only `_seed_original` (plus its import/docstring) and
`report.md`; `cases.json` and the original ten-note body/assertions are
unchanged. The seed uses the complete original `document_fixture(shared=True)`,
adds the empty `p4_note` parent namespace in both mirrors, converts through
`bundle_from_document`, compiles with `compile_authoring_candidate`, preserves
the compiler's complete parent/shot/internal closure, and ensures the normal
Runtime `registry` envelope.

Offline review confirms the authored-vs-derived boundary: authored parent
fields, timing, opaque values, null/absence state, list order, placement fields,
and internal payloads are preserved. Compiler-owned occurrences, child revision
IDs, shot-item IDs, internal links, digests, pins, and dependency manifest come
from actual compilation and the seeded closure reopens successfully. No
fixture substitutions or expected-pin assertions were introduced.

Evidence:

- exact selector collection: PASS, 1 test collected;
- scoped Ruff: PASS;
- private mypy scope: PASS, no issues in 4 files;
- `git diff --check 9b658b28c..HEAD`: PASS;
- minimal offline compiler/closure witness: PASS.

The HTTP/body test, sockets, browser, build, full suite, and service execution
were intentionally excluded. Manager next step: run the exact one-test selector
against the existing `p4-v2-http-nodes` service.
