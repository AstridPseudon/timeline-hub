## Report

Diagnosed the remaining rendering support startup timeout. No product/test changes made.

Findings:

- Compared the identical trivial support request under:
  - installed child `c886d448…`
  - qualified source profile (`agent c3231fe…`, Runtime `8ea0766f…`)
- Both returned `supported: true` with empty stdout/stderr.
- Parent timings:
  - installed: `8.285s`
  - source: `7.349s`
- Import timing was only ~0.30s cumulative.
- cProfile identified the dominant cost as strict registry admission:
  - `_transition_ids()` → `load_default_registry()`
  - 56 pack manifests scanned and canonically validated
  - ~12.37s under profiling
- No Node, npx, Remotion, network, file-lock, or child `communicate` activity caused the startup delay.

Evidence retained in `/tmp/w-dc08723871/`:
`startup-comparison.json`, `source-cprofile.prof`, and the exact request/timeline inputs.

Checks:

- `/home/user/work/venv-agent/bin/python /tmp/w-dc08723871/compare-startup.py` — passed.
- Source cProfile trivial support boot — passed.
- `git diff --check` — passed.
- `bash -n tools/run-render-cohort-0013.sh` — passed.
- Original timed test body was not rerun.

Decision/blocker: no implementation. The smallest safe fix belongs in the validator/registry path (`validators/timeline.py`), outside the permitted rendering/CommandTransport or case-owned harness scope and overlapping its owner. Recommended fix: defer transition-catalog loading until a clip actually contains a transition, preserving all existing validation/refusal behavior; obtain separate focused review before running the original timeout once.