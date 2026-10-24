# F-authoring-ABA report

Verdict: the valid same-alias condition is authored by the Agent fixture/test; the `invalid_records: sequential source binding is ambiguous` failure is caused by Agent’s capture producer. Runtime owns the guard, but no Runtime defect is evidenced.

Evidence:

- The test adds `clip-1b` with the same `asset: "picture-1"` as `clip-1` in [`test_authoring_media.py:764-778`](/home/user/work/wt/vw-F-authoring-ABA-cause-0101/tests/timeline/test_authoring_media.py:764).
- The authenticated physical binding is the internal closure `film-internal-1`, owned by `occurrence:occurrence-1/shot`, with ref `occurrence:occurrence-1/track:picture` and path `["tracks", "id:picture"]`.
- Production caller chain: `timeline_document.py` → `emit_document_publish_commands` → `native_occurrence_media_commands._swap` → `_clip` → `ctx.bind` → Agent sequential capture → Runtime `validate_sequential_capture`.
- `_swap` processes both same-alias clips, but `_clip` records the same `media.track` binding twice. Agent preserves both duplicate identities in the private capture.
- Runtime rejects duplicate normalized identities at `timeline_commit_auth.py:2063-2119`, specifically the `key not in originals` guard. This guard is byte-identical to frozen Runtime `8ea0766f5`; current Runtime HEAD is `458595850c354f4403dabc58a72b98bebbc2c3a3`.
- The frozen Agent test used archived `a0dca` for source data and Runtime `8ea` for execution. Current integration pins `a0dca` for execution too; I did not relabel those provenance facts.

The fixture is therefore a valid multi-consumer trigger, not malformed ownership. The minimal owned next action is Agent-side capture normalization/identity correction for repeated same-physical-track bindings, while preserving both consumer effects and all canonical assertions. No product change was made.

Checks:

- `git diff --exit-code` — passed.
- `git diff --check` — passed.
- AST parse with `/home/user/work/venv-agent/bin/python` and `PYTHONDONTWRITEBYTECODE=1` — passed.
- Original live test, full suites, browser/HTTP runs, and dependency changes — intentionally not run.
- Offline Agent-shaped reproducer confirmed duplicate `media.track` identities on both source and landing capture paths. Exact live serialized private capture bytes remain unverified.

No tracked files changed. Commit message and `DONE` marker were written to the assigned harness paths.