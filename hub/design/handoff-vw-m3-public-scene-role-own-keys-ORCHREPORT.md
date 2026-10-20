# ORCHREPORT — public scene role own-key correction

**Disposition: owner-ready tiny unapplied fix; product worktree clean.**

Base: Composition `ff0536bb5` in `/home/user/work/wt/vw-m3-public-scene-role-own-keys`.

## Actual finding

The public evaluator reads `scene.roles[clip.id]` directly. An ordinary empty role map therefore returns inherited `Object.prototype` members for valid IDs `__proto__`, `constructor`, and `toString`, instead of the existing visual-track `content` fallback. The red direct public-source repro observed object/function values. This is source behavior, not a compiler/provider/certification claim.

## Proposed source/test delta

- Patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-public-scene-role-own-keys-proposal.patch`
- Repro: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-public-scene-role-own-keys-repro.mjs`
- Detailed report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-public-scene-role-own-keys-REPORT.md`

The source change uses `hasOwnProperty.call` plus the existing nullish track fallback. The direct scene test proves an own JSON-parsed `__proto__` value remains an exact override and absent reserved IDs fall back to `content`.

## Evidence

ORCH-only offline copy, read-only existing Composition dependencies:

- Red-before: `npm run build:test` passed; direct `scene-evaluation` test was **5 passed / 1 failed**, failing on inherited `__proto__` (`actual [Object: null prototype] {}`).
- Green-after: `npm run build:test` passed; direct `scene-evaluation` test was **6 passed / 0 failed**.
- Adjacent scene diagnostics: **15 passed / 0 failed**.
- Green repro: `__proto__`, `constructor`, and `toString` each report string role `content`; own JSON-parsed `__proto__` reports `background`.
- `git apply --check --whitespace=error-all` against the clean product worktree passed.

No product files changed. No artifact/package/version/theme/params/API/dependency changes; no host workaround or new ID restriction/refusal; no browser/render/socket/full suite/install/network; no production pack/rebuild/publish/merge. `build:test` only emitted the temporary ORCH offline test copy. Sealed 0.0.8/0.0.9/0.0.10/0.0.11 state remains untouched. This proposal awaits the next authorized coordinated Composition release.
