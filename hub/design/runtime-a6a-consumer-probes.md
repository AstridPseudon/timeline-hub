# Runtime a6a consumer-probe evidence

Date: 2026-10-20 UTC

Candidate tree: `a6a11a806a51262192447fdeccc726b01ffd78fb`.

Frozen Agent source: commit `357230816c86da65d5f8cc92b10a3a90d29874e0`, schema SHA-256 `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`.

The schema has 55 `$defs`, 29 operation clauses, and 12 v2-capable operations: `track.set`, `shot.set`, `clip.set-params`, `clip.set-element`, `clip.move`, `occurrence.add-media`, `occurrence.swap-media`, `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`, and `clip.set`.

Generated candidate digests:

- `packages/python/astrid_runtime_client/__init__.py`: `5e0b9adee1649d89d5447b5affb888b680943e992be6ef639cbf794acc68195d`
- `packages/python/astrid_runtime_client/timeline_commit_types.py`: `ad8deaf65feafb88158d2747d1df2751cde3a0f06d5f122e0d2827c91a846e9c`
- `packages/typescript/src/index.ts`: `2d23f8ee1cb38e6b1d3366663887b88a4981ec298d8c8d5a758a62a7ad8cc0e4`
- `packages/typescript/src/timeline-commit-types.ts`: `970d306de53e35bb7cd8c599f84f1f5ae62ad23a425987c48048f962afe78828`

Prepared probe results are in the worker report. No Runtime files were edited. The candidate is blocked on generated output issues; no generated artifact was hand-edited.
