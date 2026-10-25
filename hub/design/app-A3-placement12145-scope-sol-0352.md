**Verdict: review-only fixture correction. No product defect proved; no product or protected test changes applied.** Base remains `043631dbabfed566cfe037709c7fe861d6435b52`.

The actual pinned `5337/6386/6634/635f` trace confirms `occurrence.add-media`, `V2`, `at: 9`, `hold: 5`, followed by `409 occurrence_boundary`.

| Quantity | Source-derived result |
|---|---|
| Authored pointer / hold | `4.5` / `5` seconds |
| Existing V2 intervals | `[3,6)`, `[6,9)` |
| Ordinary snap | `9`; distance `4.5 ≤ 5` threshold |
| Submitted interval | `[9,14)` |
| Original host | `[0,12)` — insufficient |
| Minimum host | `[0,14)` |

The exact pinned shot/internal links match. The shot has no separate timing window; the internal timeline has no source window or map. Image assets have no intrinsic duration constraint. Parent video `[15,18)` with source `[0,3)` remains unchanged.

The [unapplied setup patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A3-placement12145-scope-sol-0352/evidence/placement12145-setup-review-only.patch) changes four constants: native host duration `12→14`, full-length plate hold `12→14`, and their exact expected values. It also updates the matching comment. Extending the plate preserves the seed’s authored coverage before placement and after Undo.

**Decision owed:** approve this exact shared `seedThreeProducts` setup change. All its callers inherit the longer host/plate; D91 supplies analogy, not authorization.

Mechanical verification:

- `python /tmp/w-22db31c038/verify-placement-setup.py` — **PASS**. Four Python AST constant changes only; all 21 native seed assertions preserved.
- `git apply --check --whitespace=error` against the linked patch — **PASS**, without applying it.
- `git diff --check` — **PASS**; `git status --short` — clean.

The entire protected spec, semantic/media oracles, readiness spec, and gesture helper remain byte-identical to the pinned original. All original waits remain unchanged. The [verification artifact](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A3-placement12145-scope-sol-0352/evidence/placement12145-setup-verification.json) contains the predicate/input map and before/after SHA-256 hashes.

Bounded comparison: passing asset27438 uses parent `clip.add-media` at `[5,10)`, without a child occurrence limit; it does not justify raw child overlap.

No suite, browser, service, build, typecheck, lint, or provider execution was rerun. After scope approval, the next step is protected review and exact mounted qualification. Commit message and `DONE` were created.