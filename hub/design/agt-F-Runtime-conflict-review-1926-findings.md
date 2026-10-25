# Findings

Verdict: **FAIL**, limited to evidence corrections. No product or Runtime source was changed.

## F1 — recorded merge-tree SHA is incorrect

The classification records `2d341b37bafebc1feb09d4e69971bcde5ed12b729dcdc6e1c041838e714254e0`.
Re-running the exact read-only command against Runtime's objects produces
`2d341b37bafebc1feb09d4e69971bcde5ed12b729dcdc6e1c041838e7142540e` for the
same 71,105 bytes. The 1844 census has the recomputed value; the 1902
classification JSON and validation text carry the transposed final two hex
characters. This is an evidence-integrity defect, not a changed source tuple.

## F2 — three semantic-question anchors are not exact hunk identities

The 17 semantic questions are present, but these three question anchors do not
match the corresponding exact merge-tree headers or the source-side hunk
headers:

| Path | Question anchor | Exact merge-tree header | Relevant source-side header |
|---|---|---|---|
| `runtime_protocol/door.py` | `@@ -199,0 +200,8 @@` | `@@ -199,6 +200,8 @@` | upstream `@@ -195,0 +197,2 @@` |
| `runtime_protocol/door.py` | `@@ -236,0 +239,7 @@` | `@@ -236,6 +239,13 @@` | upstream `@@ -232,0 +236,7 @@` |
| `tests/test_door_routes.py` | `@@ -110,0 +111,2 @@` | `@@ -110,6 +111,8 @@` | upstream `@@ -111,0 +113,2 @@` |

The remaining 14 question anchors match exact merge-tree headers, and the
classification crosswalk itself matches the 1844 census for all 22 hunks.

## Scope note — routine approved merge choices

The two `tests/lanes.py` marker additions are test-selection metadata. With
the existing lane registry and declared-skip behavior retained, they are
routine approved upstream merge choices, not new product/C0 decisions. The
other 15 semantic entries remain genuine owner review items because they
affect startup ordering, route/auth behavior, process custody, redaction,
managed-output identity, fixture isolation, or route assertions.

## Patch/C0 result

The exported patch has exactly the two intended CI/documentation paths. A
read-only `git apply --check` against exact upstream blobs passes, including a
separate `--whitespace=error` check. It cannot alter `commitTimeline`, the
registered provider, request/reply fields, auth predicates, or C0's accepted,
merged, conflict, invalid, and preview forms. No actual merge, ZIP, or service
dry-run was attempted.
