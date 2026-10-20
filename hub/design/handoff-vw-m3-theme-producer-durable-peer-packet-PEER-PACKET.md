# D08 peer packet: normal render explicit-theme carrier

Decision: blocked at the App/Runtime producer boundary; no App patch is
published.

## Exact current chain

| Stage | Existing source-backed behavior | Gap |
| --- | --- | --- |
| App preview | `useVideoEditorPreviewComposition.ts:53-84` and `useRenderState.ts:582-599` select the paired config/fact used for preview. | No retained resolved Theme artifact is produced. |
| App normal producer | `renderRouter.ts:852-883` emits `theme_id` and media IDs; `:940-977` admits `timeline_ref` with `input_object_ids: []`. | Slug metadata is not a theme document or object identity. |
| Runtime admission | `store.py:1709-1773,1935-1955,2003-2065,2103-2140` freezes canonical config/registry/media and authority. | No immutable `theme.json` is retained or bound to the task. |
| Agent consumer | `task_adapter.py:215-247,332-366` accepts only admitted `materialized_objects["theme"]` named `theme.json`; `root_preparation.py:167-177` supplies it to `merged_props["theme"]`. | Consumer is ready; upstream named input is empty. |

## Minimal peer request

The normal App/Runtime render producer must bind the resolved Theme from the
same selected config/fact/profile/revision as preview to the existing named
Runtime-managed object carrier. The host must then materialize that immutable
document as `materialized_objects["theme"]` with filename `theme.json`.

Preserve the current `timeline_ref`, canonical authority, revision pairing, and
existing Agent admission/path guards. Do not add a slug resolver, mutable
latest lookup, caller path authority, copied default theme, new DTO, endpoint,
store, or second resolver. `theme_id` alone is insufficient.

## Source identities

- App: `a12b19be56816112da9b16cd8db4c48f9c5c399b`
- Agent: `384918908aa8c75229c2b6ccdd8fda03b7ce24a1`
- Runtime: `e8a24e301c2d5fed7ac5a9d10c7ec226e11199d8`

## Non-claims

This packet does not claim normal explicit-theme parity, a retained theme
object, end-to-end render success, or any Runtime/Agent implementation. It is
the D08 integration blocker handoff only. The exact source trace and prior
targeted test result are preserved in `REPORT.md`.
