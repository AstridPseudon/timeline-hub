# Handoff: app-F-exports-independent-review-1104

Independent review of `tl/app-F-exports-public-graph-1054` (`b0bdd9a0`):

- **Alias scope PASS:** exactly two testing-config files and eight added lines;
  the three `@workspace-*` aliases normalize to the same production Vite paths
  and point at all 1 effects, 6 animations, and 2 transitions generated
  imports. Original alias test: **4/4 PASS**.
- **Renderer scope FAIL, precisely 3 original failures:** exact private
  Composition archive `0.0.14`, 73,451 bytes/80 members,
  SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`;
  focused run **16 PASS / 3 FAIL**.
  - Two installed-host undefined component observations are the existing
    source-less Astrid public catalog / Composition bridge seam (`rendering:text-card`
    and the first loop entry `rendering:animation:fade`). Existing author-1101
    bridge candidate `305b40ac0` is the likely owner; no duplicate product fix.
  - The third is exact package provenance: archive registry emits
    `bundled:2rp@0.1.0`, while the unchanged test expects `timeline-theme-2rp`.
    Smallest no-weakening follow-on is a line-level exact bundled provenance
    assertion (or exported version/source pair), retaining all registry and
    fallback assertions.
- Serialized App typecheck (heap 4096), scoped ESLint, and target diff check:
  **PASS**. Worktree clean; no v2 request/reply/history/reads caller changes,
  source/test/generated/pin/operational writes, or commits.

Full evidence: `workers/app-F-exports-independent-review-1104/report.md`.
