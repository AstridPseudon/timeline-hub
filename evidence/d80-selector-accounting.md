# D80 selector accounting

Verdict: **PASS** for the bounded selector-set accounting requested by R2r/P2. This is an accounting proof, not a new semantic-security review. No test body, test collection, product source, generated file, pin, or route was changed.

## Source and evidence identities

- Integrated Runtime head: `87bc7f74e09330885cfaff551ca629f51beea7b6`.
- D80 carrier source: `52b0e38c5be26703bdb68dbf22d07e8041135983`.
- D80 base/original source: `a4d4b5a24964ec5b2a7752a6aeb1b2ef861a3669`.
- Runtime pre-D80 carrier base: `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f`.
- Final owner-projection test blob is byte-identical to the `52b` blob (`e0e008ef...`); the authority test file is byte-identical between `a4d4` and the final head (`16dc1297...`).
- The relevant Runtime auth ASTs (`_fork_owner_before`, `_project_created_child`, `command_output`, and `validate`) are byte/AST-equivalent between `52b` and the final head. The only final-head source delta from `52b` is the separately preserved empty-range comparator change from `1bae`.

Full SHA-256 values are in `evidence/d80-selector-source-hashes.txt`.

## Selector-set map

The original `a4d4` owner-projection file has six test functions and eight collected cases. Every original function remains at the same path and maps as follows:

| Original selector family | Cases | Final mapping | Preservation |
|---|---:|---|---|
| `test_fork_owner_uses_authenticated_agent_projection` | 1 | same selector | AST-identical, assertion preserved |
| `test_fork_owner_projection_rejects_tampering` | 3: `source`, `projection`, `missing` | same three parameters | AST-identical, parameters preserved |
| `test_fork_owner_projection_rejects_absent_identity_scope` | 1 | same selector | AST-identical |
| `test_fork_owner_projection_rejects_forged_identity_scope` | 1 | same selector | AST-identical |
| `test_fork_owner_projection_rejects_forged_local_identity` | 1 | same selector | AST-identical |
| `test_actual_agent_fork_add_media_reaches_owner_projection` | 1 | same selector | Original assertions preserved; final adds the exact four-call assertion, so this case is stronger |

Original owner-projection subtotal: **8 unique Runtime cases**.

The four original authority selectors are not renamed or dropped. They remain in the separate, unchanged `tests/test_timeline_popup_fork_authority.py`; the authentic author `focused12.xml` records those four plus the eight owner cases as 12 passes. They are therefore not part of the final owner-projection file's 23-case count.

D80's additive definition cohort is exactly 15 unique cases:

| New selector family | Cases | Evidence XML |
|---|---:|---|
| `test_fork_owner_definition_requires_exact_source_image` | 4: `shot-pin`, `revision-pin`, `physical-owner`, `physical-digest` | `definition11.xml` |
| `test_shared_owner_definition_matches_agent` | 4: `None`, `scope`, `sibling`, `owner` | `shared-definition4.xml` |
| `test_shared_source_fork_add_media_and_history_use_same_owner` | 2: `False`, `True` | `definition11.xml` |
| `test_production_fork_add_owner_tampering_never_writes` | 5: `owner-before`, `owner-after`, `source`, `alias`, `allocation` | `definition11.xml` |

New subtotal: **15 unique Runtime cases**. There is no overlap between the eight original owner cases and these 15 additions. Thus the final Runtime file is exactly **8 + 15 = 23** unique cases.

The earlier description “focused12 + definition15 = 27” counts the 12-case focused cohort (8 owner cases + 4 separate authority cases) and the 15 additive definitions. It is not a claim that one final Runtime file should collect 27 cases. The historical `focused-first.xml` (SHA-256 recorded below) is an intermediate author state and is not used to inflate or reduce the final count.

The final Agent home XML contains exactly four parameter cases for `test_public_helper_element_only_keeps_literal_params_and_exact_inverse`: `None-None`, `None-existing1`, `params1-None`, and `params1-existing1`.

## XML results and timing

- Authentic author `focused12.xml`: 12 passed, 4.856 s, timestamp `2026-10-24T18:51:51.916647+00:00`.
- Authentic author `definition11.xml`: 11 passed, 41.468 s, timestamp `2026-10-24T18:52:02.999979+00:00`.
- Authentic author `shared-definition4.xml`: 4 passed, 0.342 s, timestamp `2026-10-24T18:53:27.129892+00:00`.
- Current home Runtime `home-runtime.xml`: 23 passed, 42.555 s, timestamp `2026-10-24T19:09:01.790872+00:00`.
- Current home Agent `home-agent.xml`: 4 passed, 10.759 s, timestamp `2026-10-24T19:09:49.615374+00:00`.

The combined `home.xml` was overwritten by the isolated Runtime retry and is not evidence of a combined 31-case run. The initial combined attempt had a pytest `ImportPathMismatchError` before test bodies; the two isolated XML lanes above are the authoritative results. No full, browser, HTTP, or fresh security run was needed or performed for this bounded proof.

