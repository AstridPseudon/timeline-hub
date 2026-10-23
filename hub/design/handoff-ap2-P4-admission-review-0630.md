# P4 admission review: Runtime owner handoff

**Review PASS; current Runtime admission FAIL.** Independent inspection confirms the prior diagnosis on exact Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`: `runtime_protocol/store.py:6392` treats omitted occurrence `gain` as `None`, while the writer (`timeline_commit_store.py:1220`), row verifier (`:550`), service validator (`service.py:2697`) and admission sequence check (`store.py:6411`) use unit gain. The schema (`contract/schemas/shot-composition.json:200-211`) makes `gain` optional.

The retained realm `/tmp/pytest-of-root/pytest-7/test_http_ten_note_commit_per_0/realm` was inspected through Runtime's read-only snapshot path in normal and deep modes. Both report exactly two `composition_revision_occurrences / occurrence_field_mismatch / gain` errors (`expected=None`, `actual=1.0`); schema, SQLite, FK, relational, CAS and event-chain checks pass. No broad `RealmAdmissionError` cause is claimed.

Independent private-copy evidence preserves strict corruption detection: normalized omitted-gain baseline mismatches are `0`; changing one copied stored gain to `2.0` produces `1` normalized mismatch. The source correction must therefore normalize the optional field without accepting actual stored corruption. Do not add gain to the fixture, bypass admission, weaken restart, or rewrite the seed.

Seed provenance remains exact: Agent `ce4dc2b879a81688b10b870959837bb266ac3f39`, test blob `cdb186d001fe8bd7476c2a059ee65e9a312dbec5`, authentic 69-byte PNG, shared physical closure, and the complete v2/P4 assertions are unchanged. The original node still fails at seed restart, so ten-note behavior after restart is unverified.

Owner: **Runtime lane**. Next action: smallest Runtime correction plus strict regression, then rerun the original P4 node from the compatible checkout. No code changes were made by this review; no HTTP/socket/service/full/retry run was performed.
