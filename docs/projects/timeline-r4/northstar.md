# North Star: "One timeline, many hands"

Latest Release-3 scope: [restored extension kinds](amendments/r4-release3-extension-kinds-restored.md). Current cards/DAG/routes/estimates govern over legacy row labels: EXT-ONE, EXT-VIEW, EXT-COMPONENT, EXT-CHECK-GEN and EXT-CURVES deliver all five kinds plus declared curves/transitions/music/macros. Advisory presence stays excluded.

**The desired end state:** a film is the same object, with the same history, whoever touches it and however. That covers the Astrid CLI, the sheet, Python and scripts, extensions, agents, and the App's web editor at astrid.haus. Every edit is validated, undoable, journaled, attributable, checked and guarded by the head check. The App's preview and Astrid's render agree because one evaluator draws both. This spans every repo: Astrid, the Runtime, the App (reigh-app → astrid-app), and the shared packages (timeline-schema, timeline-composition, timeline-ops).

## Enduring properties

> **The architecture that realizes this North Star** (15 Oct): [architecture.md](architecture.md): one document, one change path (commands + rebase), one timing compiler, one shared evaluation grown from the renderer's own plan; show/visualize/check/edit as faces of one revision; extensions proven one at a time.
- **Time belongs to anchors.** A timeline is relations over anchors (spoken words, lines, beats, cuts, other clips, the film's ends) with ONE resolver. Stored seconds are a cache the resolver recomputes.
- **One change path:** every edit, from any surface, becomes OpCalls run by one runner. Ordinary App gestures emit explicit commands. `reconcile(before, after)` is the bounded compatibility path for document-level saves (the sheet and out-of-band saves), with the absorption rule; it never invents gesture intent. One journal, one undo step per transaction.
- **One evaluated scene** (what's on screen at t) feeds render, preview, views, checks and queries. No hand-kept mirrors across repos.
- **One small vocabulary:**
  - **nouns:** Reference · Property · OpCall · Plan · View · Check;
  - **verbs:** set · add · remove · place · move;
  - **the loop:** find → show → edit (prints its Plan) → see → publish.
- **Extensible in five slots, one per loop step:** operation · view · component · check · generator. Every contribution inherits validation, journaling, undo and a free conformance harness.
- **Storage stays the Runtime's:** Astrid's meaning is namespaced under `app.astrid` and compiled to the shared composition. Changes are additive; nothing breaks the live App. Shared contracts are JSON Schema first, with generated TS and Python types.
- **Intuitive is proven, not asserted:** by live practice (fresh agents, skill only), measured.

## Anti-patterns
- One concept implemented in two or three repos (hand-kept mirrors, pattern 2).
- Success-shaped failure (pattern 1).
- Raw seconds where an anchor exists.
- A write path that skips the runner.
- Building around Astrid instead of fixing it (the HARD RULE).
- Building on a branch that's about to be superseded.
- Process for its own sake.
- Writing into Codex's receiving trees.
- Publishing to main, or to an upstream, without authority.
