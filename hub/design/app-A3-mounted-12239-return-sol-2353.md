**actual12239: intended mutation POST ABSENT.** Read-only attribution completed; no source or protected-test changes.

The retained browser trace contains 273 network records:

| Transport | Count | Result |
|---|---:|---|
| POST `/projects/:project/timelines/:timeline/commits` | **0** | Absent |
| POST `/projects/:project/media-imports` | 1 | 201; 160.103 ms |
| GET `/projects/:project/media-selection` | 1 | 200; 10.622 ms |
| GET `/projects/:project/timelines/:timeline/commits` | 1 | 200, before gesture |

Import began 106.240 ms after drop dispatch; selection began 266.749 ms afterward. The drop-to-timeout interval was 89,724.712 ms. Both unfinished network entries were GETs. The retained phase file has 108 records and two terminal `http_response` summaries; these do not establish a browser mutation.

**Mounted finding:** the helper computes the pointer at the intended **5 s** start, but production `computeDropPosition` subtracts half the default **5 s** preview duration. The resulting start is **2.5 s**, overlapping the existing parent clip at 0–3 s. The planner then chooses another compatible track.

The same-event DOM snapshot confirms an uploading skeleton on the **occurrence lane**, and the terminal snapshot confirms a materialized local clip there, followed by the conflict dialog and unconfirmed-save banner. Import asset/object/generation/variant relationships match exactly.

Source proof:

- `support/app.ts:320`: pointer calculated directly from intended start.
- `drop-position.ts:129–131`: half-duration offset subtracted.
- `clip-drag-planner.ts:505–519`: overlap redirects to a free track.
- `timelineLocalSaveHandoff.ts:422–424`: parent prepared-media capture refuses an occurrence-owned lane before enqueueing.

The exact **first thrown capture guard remains unverified**: this trace retains no capture-rejection diagnostic. The ownership guard necessarily rejects that lane if reached; I do not claim its rejection code was observed.

Captured production sourcemap contents equal own source, actual `def3fb17ae`, and currentnormal `364f124b5c`:

| Source | Git blob |
|---|---|
| `useAssetManagement.ts` | `d6307d310fce33bb0907e65eca6792eb9f28ddeb` |
| `external-drop-utils.ts` | `1c4c84b2534e10e51325bee79faf3e192461f6b0` |
| `useExternalDrop.ts` | `b80a1151fc4dc27496e08e8c1019f5ab11863721` |
| `drop-position.ts` | `b781573f00c61269f8b1b2237bbb7bed5b81d35a` |
| `clip-drag-planner.ts` | `fd0b657e5b89915976f9b1a919db5791ea892cb3` |

The helper also matches actual/currentnormal/own source.

Verification commands, all exit 0:

```bash
python /tmp/w-c08f6c2aa4/attribute_actual12239.py
python /tmp/w-c08f6c2aa4/verify_protected.py
git diff --check
git status --short
```

Protected files: **6/6 unchanged against own HEAD**. Worktree clean. No tests/typechecks rerun under the read-only instruction; no browser, service, build, endpoint, or install action performed. No new oldRED/newGREEN or acceptance claim.

**Next step:** separately scope `tests/e2e/local/support/app.ts::dropFileOnTimeline` for a strict pointer-centre geometry correction, preserving the intended 5 s parent-lane placement and every original assertion. Add faithful real-coordinator regression evidence and obtain independent protected review before another body. That helper is outside this worker’s edit allowance; weakening the production ownership guard is unjustified.

`commit-msg` and `DONE` created.