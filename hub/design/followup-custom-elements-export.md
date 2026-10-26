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
