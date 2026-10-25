# D108 canonical baseline custody repair (0820)

Status: **complete, source-only; independent narrow review pending**.
This repairs both publication findings in the retained 0813 FAIL_SECOND
review without changing source facts, current joins, or historical evidence.

The canonical full index is the original author evidence at SHA-256
`d6ed7dc547645742c405e9b9288e00617f33e5f8ee378233b46fc621affd226a`. It is published byte-for-byte as
`design/handoff-agt-D108-baseline-return-0803-upstream-index.tsv`, with a
second retained copy under this worker's evidence directory. The prior
publication and four predecessor MD/JSON preimages are preserved under
`workers/agt-F-D108-baseline-custody-sol-0820/evidence/preimages/`.

The 23 changed rows are exactly XML ordinals 12309–12331. Only their file,
line, and source-location method change. Every restored definition was
verified against the real upstream commit
`92443771676ef2bbb547d0a103d708fa8bec4c63`; the two source Git blobs are
`d7cf15fda7b490c5fa6bb569a427cc3faa00acc8` (`test_check_zero.py`) and
`3c94a63a458b92857f53a6c74a4aa9dfdfe01f18` (`test_rename.py`) under
`tools/astrid-rename/tests/`. Full before/after/source pairs are in
`workers/agt-F-D108-baseline-custody-sol-0820/evidence/source-pairs-23.json`.
All 12,517 indexed definition-line mappings were checked against the real
924 Git blobs in 762 source files. Both disputed source files compile in
memory; no product code is imported or executed.

The authentic XML remains SHA-256
`2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`:
12,517 testcases, 12,396 PASS / 91 FAIL / 14 ERROR / 16 SKIP, zero duplicate
raw IDs, and 566 subtests by suite-total delta, yielding root total 13,083.
The 9,268 current joins remain byte-identical at SHA-256
`0fbcdf46e9272a2a3bd1e3f275cfa09f2887e50bef848f41c68c2c71a8ef12c5`:
2,956 exact, 6,312 absent, zero ambiguous. The restored 23 rows affect no
exact current join. Historical 276 rows remain separate (75 exact: 66 FAIL /
9 PASS; 201 UNKNOWN); D63 order-181 references remain correct.

The non-F prep0756 and return0803 MD/JSON publications now reference the
actual canonical index and original summary bytes. The unchanged original
summary is SHA-256
`7af40efb74bc171142e5a89f7cc25b17c710001c7dba61bb8e04c971764dbfd7`.
Its zero ambiguous-source count is stale: canonical ordinals 9439 and 9440
explicitly retain both valid AST definition lines. Correct source accounting
is 12,515 exact bases, two ambiguous bases, zero unresolved. This ambiguity
is separate from the zero ambiguous current-selector joins. Original summary
bytes and F0756/0758review/0813review bytes remain unchanged.

Upstream remains **FAIL/exit 1**; full-run Runtime isolation remains
**UNCERTAIN**. D13 ENV and both D23 deferred identities remain explicit.
Current failure classification and current core-open count remain
**WITHHELD_UNTIL_D108_TERMINAL**. Production caller, guard, and authority
behavior are unchanged.

Validation command (stdlib CSV/XML/AST/JSON/hash and read-only Git only):

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D108-baseline-custody-sol-0820/evidence/validate-custody.py
```

Final readback counts, path/hash pairs, canonical byte equality, all 23 source
pairs, original-file preservation, in-memory compile, and whitespace checks
are recorded in
`workers/agt-F-D108-baseline-custody-sol-0820/evidence/final-validation.json`.
No pytest, collection, body, service, probe, browser, install, or full suite
was run. Next step: independent narrow custody review.
