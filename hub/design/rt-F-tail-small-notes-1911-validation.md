# F final tiny evidence split and delivery-note installation

## A — pristine evidence correction

The five 1857 artifacts were copied byte-for-byte into `evidence/pristine/`.
Only the Composition frozen-reference crosswalk in `inputs.json` and
`source-manifest.json` was corrected. The named upstream remains
`origin/main` at `67b8aa3d0d6831d3e3504a340ff583c3da253707`, tree
`62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`, parent
`bd1011bce5fb4f172269911555568d18e6b22f3c`. The separate frozen candidate
ref is `origin/codex/handover-timeline-r4-20261019-candidate-composition` at
`c82eb7c459d0a41263954bf007071a6a0e8e0a6a`, tree
`49975e7a54fd594e1b7fc807681fe28611d57864`, parent
`5947abc0f5d6c0f5ca20bb478521e010e76be039`.

The 1904 review JSON spells the candidate tree with an extra trailing `e`
(`49975e7a54fd594e1b7fc807681fe28611d57864e`), which is not a valid 40-hex
Git object ID. Local Git verification is authoritative; the corrected
artifacts use the valid 40-hex object above. This is recorded in
`composition-correction.json`.

Exact correction patch: `evidence/composition-correction.json`.

## B — approved paragraph installation

The exact one-line source paragraph from
`design/app-D133-Gate3-deferred-ZIP-note-1853-zip-note.md` was inserted once
into each existing delivery input, after the existing D87 paragraph and
before the existing fake-runtime line. No other bytes changed. Gate3 remains
a visible deferred failure; the three other transcript-bound word cases stay
separate. No gate, cut, ZIP, or kit status was moved.

The installed builder was idle. Both targets were regular mode-0644 files;
predecessor hashes matched the captured evidence before the same-directory
temporary candidates were atomically renamed into place. UTC backups are
recorded in `receipt.json` and remain alongside the delivery inputs.

## Exact checks and results

- `python3` JSON parse of `inputs.json`, `selector-map.json`,
  `source-manifest.json`, and `composition-correction.json` — PASS.
- Copied `commands.md`, `selector-map.json`, and original `validation.md`
  against 1857 with `cmp` — PASS; their bytes are unchanged.
- `awk '/^~~~sh/{f=1;next}/^~~~/{if(f){print;f=0};next}f' commands.md | bash -n` — PASS.
- Composition ref/object/tree/parent checks with local `git show-ref` and
  `git rev-parse` — PASS; both frozen candidate and named `origin/main` are
  distinct and unchanged.
- Matrix reconciliation assertions — PASS: historical 41, manifest 34,
  stable source-only 33, generated caches 7; missing five route roots and
  D73 launcher remain `UNKNOWN_MISSING_UPSTREAM_SELECTOR`.
- Candidate/installed paragraph and outside-byte assertions — PASS for both
  files; exact source paragraph count is 1 in each.
- `bin/delivery-build.render_readme` with a controlled four-repository stub —
  PASS; both paragraphs rendered exactly and unresolved placeholder count is
  zero. This did not run the builder, build a ZIP, or write a kit.
- `git diff --no-index --check` on each predecessor/candidate pair — PASS
  with no whitespace diagnostics (expected comparison exit 1 because the
  files differ by the approved insertion only).
- Worktree `git diff --check` — PASS; no Composition product files changed.

No lint, type, product, core, E2E, provider, clone, install, network, wheel,
ZIP, or full suite was run; those are N/A for this prose/evidence-only task.
