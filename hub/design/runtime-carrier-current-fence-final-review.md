# Runtime carrier current-fence final review

Decision: **APPROVE — private carrier only**.

Exact reviewed source:

- Runtime commit: `7b8d6d9afe963e2b7a6c6b32fd4e3797451090da`
- Runtime tree: `d20b745c26a33c2ea4e20863f846335c8cf33e1e`
- Current Runtime source image: `81f8c7e0b22c34804015c054762af3d737e4698a`
- Private carrier basis: `83fe4a1cc8e79ba6db2f06271097a96ff2e7c59a`, tree `2d9d740ef22eea3b9ec4899bb8e400251bd6d444`
- Frozen Agent counterpart: `3730d0bd51686a1692450359482205df64dcc839`, tree `3892a10bcffa9bf520b4c79591637cf3259d6724`
- Matched Agent command schema: SHA-256 `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f` (48 definitions, 22 operation clauses, 13 source-bound v2 operations including `track.create`; not ordinary 55/29).

Review findings:

- The current 81f composition changes exactly the documented 16-path allowlist; all 415 tracked paths outside it match 81f. The private fence adds the intended current-film, inverse-source, and accepted-historical-slot checks: each requires the project-scoped `shot_revision_heads.revision_id` to equal the authenticated accepted image revision.
- The existing provenance/owner/item checks, `_same_materialization_slot` join, global raw-item reservation, canonical `item_id` over opaque `id`, accepted-ledger-first retry, and C4 exact historical reuse behavior remain in place. No broad ancestry/read exemption or blanket historical-reuse ban was added.
- The public floor remains strict: `tests/fixtures/published-command-schemas/agent-26ef2bbb.json` is unchanged at SHA-256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`. No new xfail, skip, weakened expectation, DTO, endpoint, activation, or public pin was added.
- The old-RED/current-GREEN distinction is valid. The archived pre-fence probe replaces only `_check_shot_destinations` with the 83fe implementation; its reported discriminating run fails at the current-slot overwrite. The decisive current-GREEN native-provider case passed:

  `PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-carrier-catalog-fence-compose/agent-source PYTHONPATH=$PWD:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-carrier-catalog-fence-compose/agent-source /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-carrier-current-fence-review -m integration tests/test_timeline_projection_ownership.py::test_source_bound_owned_slot_cannot_overwrite_newer_catalog_head`

  Result: `1 passed in 2.14s`.

This approval is private-source review only. It does not approve public pinning, release, activation, merge, or native-comprehensive qualification. Any future Runtime CAS/text fixes or composition must retain this exact catalog-head fence and the matched Agent 3730/f802 source pair. No full 195/209 suite, public adoption, or comprehensive native lifecycle run was performed here.
