# Validation

Task: `rt-F-tail-upstream-census-1844`.

## Method and source integrity

- `git merge-tree --trivial-merge BASE OURS THEIRS` was run against the four captured integration heads and named `origin/main` objects. The exact output SHA-256, byte count, base, parent, and tree identities are recorded in `census.json` and `source-manifest.json`.
- Fresh clone: not attempted. Exact read-only merge-tree facts succeeded locally; available disk was 4,777,416 KB, close to the 4 GB stop line.
- No fetch, checkout, merge, rebase, reset, ref movement, source-tree write, installer, build, ZIP, browser, render, wheel, or live-service command was run.
- JSON parse: PASS for `census.json`, `already-upstream.json`, and `source-manifest.json`.
- Census/map integrity: PASS; conflict counts are Runtime 10, Agent 40, App 16, Composition 0, with 66 unique conflict paths.
- Exact Git object/tree/parent checks: PASS for every live merge-base, live integration head, named upstream tip, and frozen candidate tip.
- D68 reviewed-wrapper SHA-256: PASS (`bae840fad6ea496457a3d6138609ce9d89b0b10825827c94f855257bce6c6779`).
- D68 builder SHA-256 reference: PASS (`f25dfab13bbfb090bf26cf97a85e59bdcc4be67365fcc32930b7846bbd41a65f6f`).
- D123 `b0ff` patch identity reference: PASS (`b0ff420595441fccb3d0a37b70715e5b2bff373cecd9d2e51c82be51cbe58f6b`).

## Patch-equivalence checks

`git cherry -v UPSTREAM OURS` / normalized patch-id comparison: PASS as a census. No `-` (already-upstream) matches were found. Non-merge local commits are listed as not already upstream; merge commits are listed separately as unclassified because `git cherry` does not assign them patch identities.

## `git diff --check`

Command form: `git -C REPO diff --check BASE SIDE`.

- Named upstream sides: PASS for Runtime, Agent, App, and Composition (exit 0, no output).
- Runtime captured integration side: FAIL, exit 2, 3 committed-tree `new blank line at EOF` findings (`runtime_protocol/timeline_commit_port.py`, `tests/schema_fixtures.py`, `tests/test_timeline_projection_occupancy.py`).
- Agent captured integration side: FAIL, exit 2, 162 committed-tree findings, led by `new blank line at EOF` in `.github/workflows/chat.yml`, `astrid/chat/THIRD_PARTY_LICENSES.txt`, and `astrid/chat/__init__.py`.
- App captured integration side: FAIL, exit 2, 56 committed-tree findings, led by `new blank line at EOF` in `playwright.auto-real-proxy.config.ts`, `scripts/testing/auto-real-proxy-main95.mjs`, and `scripts/testing/auto-real-proxy-main95.test.mjs`.
- Composition captured integration side: PASS, exit 0, no output.
- This worker worktree: PASS, `git diff --check` exit 0; it has no product changes.

The failed integration-side checks are committed-source whitespace findings from the captured trees, not edits made by this census. No cleanup was made because this task is read-only conflict preview and must preserve both sides.

## Evidence hashes

```text
2adbabd4a8e9f93dbc1d60b3c1489f611b527e402dc40629597d49f5502c0e16  census.json
3c03a417eb6d9a3a52c496b2d919348b0171aa34dfa0ac005f72d2805b312025  conflicts.md
3ec7a337b6f7e13db39b005a711e47272ba056b9a0021feca80cbbb84b7681c9  already-upstream.json
d4a449ebac4509e3d5cff094d6e69f3ccac7ab8b46ba6fcf3062a7ab2f09b535  source-manifest.json
```
