# Legacy transition None remains silently ineffective; native replacement is staged

Problem: while implementing approved06:12 transition payload preservation, actual mounted single/bulk None callbacks correctly remove the own transition field, but rowsToConfig/RuntimeDataProvider legacy partial-coverage publication restores the old raw transition. This is a pre-existing legacy writer defect, not a new M1 regression. No native SET activation or guard relaxation has occurred.

Executable evidence: exact original raw inputs, mounted actions, positive expected-removal body and red outcomes (bulk=false/true) are retained in design/handoff-app-transition-none-repro.md. Both parent_composition.config.clips and parent_composition.clips still contain the old transition. Callback-only None tests and all other preservation cases pass. The two NEW unmerged it.fails declarations were rejected/removed; exact three original drag exceptions remain the ONLY allowed markers. No original test/input was removed or weakened.

Recommendation/action: keep D01-app-transition-none-serialization OPEN and finish native single+atomic-bulk transition clear in the existing durable session on the ONE current paired release, retaining all positive removal assertions; then actual reload/undo/retry/0legacy. app-m2-transition-none-native-stage-r1 is doing that source staging now. No snapshot-writer patch/second serializer authority and no M1 reopening proposed. The bounded metadata/unknown-payload preservation safety unit can land separately without claiming None publication is fixed.

Meanwhile: continue qualified dead-code deletion, internal assetDrop-boundary safety, canvas ground, and current-release preparation. All remaining legacy publishers are still D01 OPEN.
