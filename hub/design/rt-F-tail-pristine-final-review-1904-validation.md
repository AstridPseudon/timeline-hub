# Independent first-return review

Verdict: **FAIL**. Four of the five 1851 findings are corrected and one remains
blocking: the Composition frozen-R4 ref mapping is still incorrect/omitted.

This was an evidence-only review. No install, build, clone, ZIP, core,
preflight, provider, Store, registry, network, or Git mutation was performed.
Lint/type checks are N/A.

## Exact validation commands and results

- `python3 -m json.tool "$E/inputs.json" >/dev/null` — exit 0.
- `python3 -m json.tool "$E/selector-map.json" >/dev/null` — exit 0.
- `python3 -m json.tool "$E/source-manifest.json" >/dev/null` — exit 0.
- `awk '/^~~~sh/{f=1;next}/^~~~/{if(f){print;f=0};next}f' "$E/commands.md" | bash -n` — exit 0; normal and preflight blocks parse.
- Independent selector assertion over `design/agent-core-full-command.md` and 1857 `selector-map.json` — PASS; 22 roots, exact order, no extra root; five missing roots and the D73 launcher are all `UNKNOWN_MISSING_UPSTREAM_SELECTOR`; five D54a nodeids are retained exactly.
- Independent C0 source/header assertion — PASS; 1857 uses `steps[].reads`, contains no `optionalreads`, puts `Idempotency-Key` in HTTP metadata outside the JSON body, and current Runtime integration contract objects contain `reads` plus the required header wording.
- Read-only named-object/ref/tree assertion — PASS for named commit/tree/parent/origin objects and Agent/Runtime/App frozen refs; FAIL for Composition mapping: actual frozen candidate ref is `c82eb7c459d0a41263954bf007071a6a0e8e0a6a` / tree `49975e7a54fd594e1b7fc807681fe28611d57864e`, while 1857 records origin/main `67b8aa3d0d6831d3e3504a340ff583c3da253707` / tree `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` as frozen resolution.
- Read-only exact source checks against named Agent commit — PASS; all five missing route roots and `tools/p4-d73-pinned-launch.sh` are absent, so none is PASS/zero.
- Runtime 7070 source assertion — PASS; immutable commit `7070f1378d1917fcce69857ebd33cd2b3015568b`, 100/100 Python SHA-256 matches, 100/100 Python AST parses, TypeScript identity exactly `packages/typescript: npm test`.
- Independent matrix enumeration and hash assertion — PASS as reconciled source-only evidence; actual 41 files = 34 manifest-listed entries + 1 manifest self-file + 7 generated caches; 33 stable source-only files; one listed cache hash mismatch is disclosed/unqualified and six caches are unlisted/unqualified.
- `git diff --check` — exit 0.
- `git status --short --branch` — clean review worktree (`tl/rt-F-tail-pristine-final-review-1904`).

## Boundary

The final D59 tuple remains `pending`; no current final tuple was cut. Because
the five roots and launcher are absent from the named Agent object, the
upstream route is not executable and no zero/PASS/preexisting inference is
allowed. The private 100-Python/TypeScript identity remains qualification
evidence only, not pristine-upstream gate credit. D130 is excluded.

## Durable evidence hashes

- `review.json`: `2e5696dfba8685e6deb6168c7f32c3c866271cc85f52df8a76d4b29419d8c2e3`
- `source-manifest.json`: `708482845bf408625aad75ac10e21262d08454db39497004c2ade413ce91cb6f`
- `validation.md`: content file; no self-referential hash recorded.
