# F/R1 preview oracle — independent review handoff

**PASS — bounded test-oracle qualification only.** Reviewed
`95709b37d5c16c92954b312b73177d555a850105` over provider source
`fad05679ae45ff4eb32190fdae40ae1cd1e56db6`. The only author delta is the
existing producer-insertion test (3 insertions/1 deletion); no reviewer edits
were made.

The expected records are recomputed through the existing `commands.execute`
caller with the authentic submitted request and evaluated head. The test still
uses exact complete-record equality, so the provider-derived physical
`commit.input` boundary at command ordinal 2 is required. Media selections and
custody/order, canonical document, refusal for missing media, preview-only
accept guard, and zero-accept state remain asserted. No provider rows are
copied and no metadata is dropped.

Evidence: exact original parameterized node **2 passed**; existing
normalization/golden and four media tamper guards **6 passed**; scoped test
mypy **success**; Ruff **2149/2149**; global mypy baseline **1912/1912** with
normal completion; vendor lock, artifact manifest, and diff checks passed.
`astrid`/`scripts/reshape` are unchanged from `fad05679` (`git diff --quiet`
exit 0), so the 1912 production-scope evidence is directly applicable.

This does not accept product ancestry, Runtime behavior, or the prior
provider review's other six nodes. No full/P1/P4 HTTP/native14/crash24/heavy/
browser/renderer duplicate was run.
