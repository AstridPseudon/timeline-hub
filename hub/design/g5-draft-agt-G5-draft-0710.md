# G5 draft handoff — Agent

- Base/source: `4edc4b321cae5cfc58252d7ed89e3f0408238646`, branch `tl/agt-G5-draft-0710`.
- Diff: 8 files; 15 insertions, 866 deletions.
- Production carrier proof: active connected sheet path remains `cli._cmd_apply` → `cli_native.commit_edit` → `NativeSheet.load(...).apply` → `TimelineSession.commit_many`; Python free edits remain `timeline.open()` → emitter → `Timeline.commit`; ordinary literal move/trim remains session-backed. Parser smoke rejects commands-file, apply --native, CLI publication undo, and publish.
- Deleted/retired: native edit subparser registry, commands-file parser/batch branch, apply `--native` registration, CLI undo/redo `--publication`, `document_diff.py`, `store.three_way`, `store.publish_bundle`, detached concurrent three-way save call.
- Targeted evidence: emitter + authoring diff `46 passed`; full requested targeted selection on runtime-enabled PYTHONPATH `57 passed, 3 errors, 1 failed`, all failures from the retained `publish_bundle` monkeypatch seam; exact requested command first failed collection because `runtime_protocol` is not on its default PYTHONPATH.
- Quality: scoped Ruff on edited core retirement modules passed; vendor lock/artifact checks and diff check passed; `make ruff` reports baseline gate `current=2148 baseline=2149` (no baseline write); mypy baseline comparison produced no result within 60 seconds and is unverified; compileall passed.
- Merge gate: do not merge until P1 GO is present on the orchestrator header.
- Remainder: `publish.py` remains for Checkout document/read helpers with `publish()` fail-fast; duplicate/restructure and dead `_cmd_publish` still reference the retired method and need an explicit later migration/classification. Old tests/imports remain untouched.
