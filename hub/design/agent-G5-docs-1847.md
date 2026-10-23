# Agent G5 documentation report

## Result

PASS for the requested documentation-only caller retirement. On source
`c59a751774cf74267daab779f6e3dc2604fc3993`, I changed only
`astrid/packs/rendering/docs/SKILL.md`, replacing the stale editing block with
the current `show` → direct `edit`/`apply` → `undo`/`redo` → detached `commit`
and `--help` flow.

The examples now match the checked-in parser and production callers:
`TimelineSession.move`/`trim`, `NativeSheet.apply`, guarded
`timeline.inverse`, and the detached-document `TimelineSession` commit
boundary. The text documents the exact base revision/publication pair,
commands, labels, per-step patch/read metadata, merge mode, declared reads,
idempotency key, dry-run behavior, API/project/timeline/source metadata,
optional rationale/group ID, complete canonical closure and receipt, recorder
bindings/dependencies/derived effects, history and per-step undo, plus
structured refused/invalid/conflict details and accepted/merged replies.

## Evidence

- Parser/help proof: [sourceparserproof.md](../workers/agt-G5-docs-1847/evidence/sourceparserproof.md)
- Body preservation: [bodypreservation.md](../workers/agt-G5-docs-1847/evidence/bodypreservation.md)
- SHA: [SHA.md](../workers/agt-G5-docs-1847/evidence/SHA.md)
- Credential scan: [credentialscan.md](../workers/agt-G5-docs-1847/evidence/credentialscan.md)

## Tests and checks

Passed:

- Offline `python3 -m astrid timelines --help` and `--help` for `edit`,
  `apply`, `undo`, `redo`, and `commit`, using the existing read-only Runtime
  source path in `PYTHONPATH`.
- `build_parser(None).parse_args(...)` for every documented CLI shape,
  including direct move/trim, sheet apply, receipt/step-map undo/redo,
  detached commit, `--dry-run`, and `--json`.
- Edited-section stale-route grep.
- `git diff --check`.
- Credential-pattern scan of the changed document.

The first help probe without the Runtime source path failed with the existing
environment error `ModuleNotFoundError: runtime_protocol`; the read-only path
rerun passed. No mutation, socket, network, or handler invocation was made.
No product test/full suite was run because this is documentation-only and the
brief explicitly says no new tests or scoped typecheck are needed.

## Scope/decisions

I edited only the named obsolete guidance block. No product code, tests, pins,
schemas, Runtime/App/Composition files, new docs, or process rules changed.
The P1 no-go/no-integration condition remains untouched. No destructive Git
operation or dependency installation was performed.

## Next step

Request the independent Luna narrow review of this documentation diff. The
orchestrator retains all integration and activation decisions.
