# ORCHREPORT — vw-m3-resolved-theme-common-source

**Design task complete; implementation/qualification held at the missing source-result read.** No tracked product/test/fixture/pin/core/provider/Runtime file changed. No commits/merges/checkouts/pushes. FINAL06:07 policy followed; rejected public-default/core and literal-copy adapters remain unapplied.

## Delivered

Source-backed contract and diagram: [DESIGN](handoff-vw-m3-resolved-theme-common-source-DESIGN.md). Actual existing common authority is Agent `_resolved_theme_for_render`; final export already sends its whole output as Root props.theme. The private props JSON is deleted after each render, source/capture returns no theme, and the reviewed inactive scene transport only consumes supplied themes/returns frame rows. Ordinary App config/load/store/preview has no resolved-theme result or artifact descriptor. Optional local prop alone cannot close that gap.

Proposed minimal local seam is `theme: Theme` alongside the same exact source-prepared config (or existing `props.theme` if the Agent source owner returns complete props), passed as `resolvedTheme?: Theme` through App's existing config/revision/generation delivery. Exact source/candidate pairing, theme-only generation, metadata guards and materialization lifetime are specified. This is a local result proposal, not a new getter, Runtime method, provider, wire DTO or endpoint. Source/materialization owner must supply an authorized delivery connection; none is claimed to exist.

For the implicit-default-only scope, the existing `@astrid` build-source read can carry generated full resolver JSON, pinned by existing Agent vendor commit/tree/file hashes and a native regeneration check. The prototype demonstrates generation and stale-output refusal. Design states exact missing build invocation/manifest inclusion and native-host deployment pairing; none is implemented. It does not qualify runtime-pinned themes, installed-slug equivalence or partial nested merges. No frozen 0.0.8/9/10/11 artifact is changed. No copied policy literals or fixture override.

Coordinated with `vw-m3-app-delivered-theme-seam` through flat `...-to-app.md` and read its `...-COORDINATION.md`. Supplied actual Agent-resolved values for implicit/default/authored color/complete visual cases. Its consumer prototype/tests are independent evidence and are not claimed as run here. App main remains b8064ecf1; current inactive public10 candidate is not represented as installed preview.

## Exact commands and results

Run from `/home/user/work/wt/vw-m3-resolved-theme-common-source` unless a script has an absolute path below. Definitions used only for readability; these expand to the exact paths executed:

```sh
THEME_DESIGN=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design
THEME_WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-resolved-theme-common-source
THEME_TREE=/home/user/work/wt/vw-m3-resolved-theme-common-source

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$THEME_TREE" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= --basetemp="$THEME_WORKER/pytest-tmp" "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-test_resolved_preview_theme.py" tests/packs/rendering/test_remotion_backend.py::test_hype_merged_render_props_match_golden tests/packs/rendering/test_remotion_backend.py::test_explicit_missing_theme_path_does_not_fall_back_to_workspace_theme tests/core/rendering/test_profile.py
# exit 0: 17 passed in 3.14s. 5 UNAPPLIED tests executed externally + 12 existing main-suite tests.
# targeted.log. No skip/xfail/it.fails or behavior rewrite added.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$THEME_TREE" /home/user/work/venv-agent/bin/python "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-prototype.py" --output "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-values.json"
# exit 0. Whole values from actual Agent resolver, Agent commit and source file hashes recorded.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$THEME_TREE" /home/user/work/venv-agent/bin/python "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-prototype.py" --default-only --output "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-generated-default.json"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$THEME_TREE" /home/user/work/venv-agent/bin/python "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-prototype.py" --default-only --check --output "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-generated-default.json"
# both exit 0; check says matches actual selected Agent resolver.
# Same check against $THEME_WORKER/stale-default-probe.json (one deliberately changed background):
# expected exit 1, 'Stale generated theme: regenerate from the selected Agent source'.
# Probe removed. Exact two check argv/results in generation-check.log.

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-prototype.py" "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-test_resolved_preview_theme.py"
# exit 0: All checks passed; lint.log.

git apply --check "$THEME_DESIGN/handoff-vw-m3-resolved-theme-common-source-UNAPPLIED-tests.patch"
git diff --check
git status --short
# each exit 0; final status empty. Check only, nothing applied.
```

No browser, render/capture, sockets, install, network, full suite or central test request run. No new custom runtime pin / nested App merge / historical-source delivery positive, so all remain unqualified. No film data inspected or rewritten. Proposed tests are destined for Agent main's existing `tests/packs/rendering` lane; not registered there yet. Temporary pytest data was removed; no product build output remains.

## Decisions / blockers / next action

- Reused actual final resolver; did not invent new authority or copy the navy style. This is the smallest source that already knows runtime materialization + authored override semantics.
- Kept source certification and saving separate. Agent provider/capture/Runtime DTOs stay read only. Theme shape is not source authority.
- Complete per-source delivery is blocked by a missing producer/result/read seam, not just a missing Player prop. Design work is complete; this is the next implementation prerequisite, not a claim of full parity.
- Default generated artifact is explicitly narrower and cannot detect a separately upgraded native host by itself. Require source-release pairing before treating it as product evidence. Custom pins/nested merges remain unqualified until positive tests exercise actual delivery.
- Recommended next: Agent source owner and App owner review the contract together with App's flat consumer prototype. Approve either the bounded implicit-only generated resource through the existing source build, or complete the source-result connection within existing authorized reads before wiring whole resolved themes. No broad browser run until source delivery is owner-reviewed. Add approved App implicit full-style change to owner-film-differences.md; export unchanged. Do not apply either earlier rejected proposal.

## Flat artifact list (absolute directory)

All files are under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/`:

- `handoff-vw-m3-resolved-theme-common-source-DESIGN.md`
- `handoff-vw-m3-resolved-theme-common-source-ORCHREPORT.md` (this report)
- `handoff-vw-m3-resolved-theme-common-source-to-app.md`
- `handoff-vw-m3-resolved-theme-common-source-prototype.py` (UNAPPLIED/offline)
- `handoff-vw-m3-resolved-theme-common-source-values.json` (actual outputs + source binding)
- `handoff-vw-m3-resolved-theme-common-source-generated-default.json` (generated demonstration, not product authority)
- `handoff-vw-m3-resolved-theme-common-source-test_resolved_preview_theme.py`
- `handoff-vw-m3-resolved-theme-common-source-UNAPPLIED-tests.patch`
- `handoff-vw-m3-resolved-theme-common-source-targeted.log`
- `handoff-vw-m3-resolved-theme-common-source-generation-check.log`
- `handoff-vw-m3-resolved-theme-common-source-lint.log`

## Final coordination acknowledgement

App's flat COORDINATION note confirms it consumed this handoff's actual `cases.implicit.theme` and `full_visual_override.theme` in mounted whole-theme assertions using the real public ThemeProvider/useTheme. It reports 117 passing tests in its own five-file lane and still explicitly holds the absent producer/read seam. This is peer-reported evidence only, not a command run by this worker; see its separate final ORCHREPORT for exact commands. No dependency on applying either earlier rejected proposal.
