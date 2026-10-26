# Follow-up: custom Remotion elements that export

Source: chat-33 assessment (chat33-issues-assessment-20261026.md), traced against the shipped tuple.

## The gap
An element is already a Remotion component (for example am-discord's component.tsx). A user can make their own as a project pack, and it previews in the editor. But:
- the final render loads only installed packs (`load_default_registry`), so a project element fails on export;
- nothing warns before export (App exportGuard treats any non-draft ref as allowed);
- admission rejects copied built-ins (type-only theme-api imports are checked), and needs ASTRID_ELEMENT_BUILD_COMMAND plus a Node shim;
- `timelines update-element` refuses clips inside a shot.

## Plan
1. **Now (S):** an export blocker plus a `timelines check` finding for project-pack refs.
2. **S each:** exempt type-only imports at admission; a default build command with pinned Node.
3. **M:** a shot-aware update-element.
4. **L:** the render path loads admitted project packs (narrow element parity, pulled forward from extensibility Phase 3).

## Smooth zoom
The user wanted eased "very / next / day" zooms. Two routes:
- **(a) Custom element:** blocked until step 4 above lands.
- **(b) Built-in am-discord:** add optional per-step `ease`/`frames` and fractional zoom, reusing am-presenter's `pushedZoom`, plus `focus:{word}` (S–M). Existing clips keep snapping. It exports today because it's installed.

Owner decides.

## Fit with today's workflow (5 Haiku traces at the shipped SHAs, 26 Oct)
It finishes the existing project-pack loop (init → validate → admit → `update-element --revision --expected-head`); it is not a new workflow. There is no separate publish step: the confirmed new revision is the save.

**Required design rule:** at render, resolve each clip's pinned revision from its admitted snapshot, never by comparing it with the current catalog. Today managed_timeline.py:442-450 refuses any pin whose revision differs from the current registry descriptor ("stale pinned element revision"). That would break "old timelines keep their old version".

**Smallest render change:**
- Materialise the verified pinned snapshots into a pack-shaped staging directory, scoped by realm and project and keyed by pack/kind/id/revision.
- Pass it as `extra_pack_roots` (registry.py:244) to the validator and to run.py:584/628/757.
- Give the registry generator a root argument.
- Critical path: the global generator and the global render lock (remotion/lock.py:22).

**Placement:** a pack-aware place command that writes `elementRef` plus its pin. `--add-layer` builds only am-* built-ins. update-element and set-element should accept `occurrence:` targets. Authoring discovery (project_packs.py:755) should list shot clips too.

**Authoring:**
- The shared element contract becomes an allowed import, so copies don't paste it in.
- A default build command.
- Cross-machine export needs the snapshot_object upload; re-admit legacy admissions.

## Live playback (3 Haiku traces, verified by main at app abac6c809da2)
- **Local editor (Vite dev, no Runtime origin):** project elements play live and hot-reload (admitted-elements.ts:41 gate). A missing component renders blank (TimelineRenderer.tsx:375); it should show a message.
- **Hosted build (Dockerfile:28 sets VITE_RUNTIME_ORIGIN):** only elements compiled into the build play. A missing one shows element_source_missing (TimelineRenderer.tsx:1386).
- **Not a route:** embedded remotion_source / remotion_module clips are never executed (TimelineRenderer.tsx:1402). The authoring doc rejects that route; do not extend it.
- **Hosted playback, after export parity:** serve the build-once bundle by pin from the Runtime and load it isolated (separate origin or sandboxed frame).
- **Untraced:** how the render worker loads external/<pack>/<digest> componentPaths.
