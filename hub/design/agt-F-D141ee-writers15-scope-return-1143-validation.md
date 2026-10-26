# U2 G4 G5 F D141ee writers15 source-scope return validation

Result: `SOURCE_SCOPE_CORRECTED_REG_PENDING`.

- Exact scope: `per-id.json` contains exactly 15 unique IDs, n=4–18, with no omission or duplicate.
- Review findings: all seven finite findings F1–F7 from review 1137 are addressed once in `report.md` and `handoff.md`; F1 is handled by this worker's continuous sampler, F2 by not restoring or rerunning tests, and F3–F7 by the per-ID classifications and source maps.
- Git: Agent HEAD `445b9c1a7f8d0e7e3405ad01f4475b9af02acfaf`, tree `6806fec5657f26097d0d0f3da29082907e6faadd`, pristine `64197afa297f86f1e738238d5e80aff6d33e303a`; Runtime integration `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`.
- Source only: inspected Git/line-numbered source and the named immutable evidence. No pytest, collection, typecheck, lint, vitest, browser, request, CAS, service, generated-client, dependency, body, profile, or child execution was performed.
- AST source validation passed for Agent `_PublishMixin.publish`, `_commit_restructure`, `_publish_narration`, `_cmd_restructure`, `WorkspaceClient` publish/commit methods, `RemoteTimelines` create/replace methods, and Runtime `_timeline_commit`, `_require_timeline_command`, `commit_timeline`, and `publish_parent_composition` definitions.
- Tests were already restored in `445b9c1`, merged by HOME `14ccf296f376`, and their targeted result is retained as failure evidence. This worker does not recommend restoring or running them again unchanged.
- No original protected purpose is credited as PASS. No retirement is approved. All 15 remain REG-pending; rows 8, 12, and 13 additionally require exact MAIN/Agent owner decisions.
- Source route result: `_cmd_restructure` calls `_PublishMixin.publish`, but `_commit_restructure`, `_commit_document`, and `_publish_narration` submit through `TimelineSession` to `commitTimeline`; no second writer body is proven. `WorkspaceClient.publish_parent_composition` and RemoteTimelines' dispatch surface reach Runtime's `_require_timeline_command` refusal, not a writer.
- Disk sampler: `disk-trace.txt` is this worker's fresh available-byte sampler, sampled every five seconds and kept alive through worker exit; it stops only at `availableBYTES <= 4000000000`.

Validation commands:

```text
python3 -m json.tool evidence/per-id.json
python3 -m json.tool evidence/source-manifest.json
python3 - <<'PY' ... exact 15/unique and all F1-F7 checks ... PY
```

The JSON tools passed. The semantic check was performed after writing the packet and passed; no product test suite was run.
