# Parent trim boundary parity — Agent escalation

Verdict: the boundary defect is shared native domain behavior. Stop App product edits. Agent owns the correction; App must follow its approved semantics.

App source: `349cf9c77a04f4f4f887ef4b8f539782e1ca1609` (this worker's unchanged HEAD). Native source: fixed Agent integration SHA `76737ca2f9c86a075e7e03dfc8990e3090acc234`, executed from a private `git archive`, not a moving checkout. The original App golden is byte-preserved and JSON-equal to that SHA's native golden. Native `_trim_commands.py`, `_common.py`, and the fixture have no diff against previously qualified native SHA `c456b3281497653cecf44f61acd6fa30565d83c8`.

The executable counterexample uses the existing `recipe_m2_clip_trim.json` raw document, changes only `parent_revision.payload.registry.assets.picture.duration` to `9.9999999`, recomputes that payload's required digest with native `_digest`, and requests `{in_s: 0, out_s: 9.99999989}`. It does not round the input, change source units, remove opaque fields, or fabricate capture claims.

Native results:

- `capture_clip_trim` succeeds; re-executing its complete captured command with `execute` succeeds.
- Authored clip: `{from: 0.0, to: 10.0, hold: 10.0, speed: 2}`. The raw requested endpoint is below registry duration, but authored `to` exceeds it.
- Closed EditCommand JSON schema validation succeeds; exact recorded replay, inverse and redo all succeed; the input remains unchanged.
- `document_from_bundle(plan.bundle)` succeeds through the actual `compile_authoring_candidate` publication path. Both parent payload `clips` and `config.clips` retain `to=10.0`, with registry duration still `9.9999999`. Rational fps, sibling immutable shot/internal images, placements and opaque clip fields survive.
- The existing `Clip.trim` model produces the same row when only `_source_duration` is supplied as `9.9999999` (no media IO). Asking native capture for raw `out_s=10` is correctly refused: the defect is introduced by rounding after the guard.
- The original unmodified golden command records and compiled output match exactly before the boundary variant is exercised.

These are successful native domain execution and compilation observations. No Runtime request, persisted Runtime acceptance, browser preview, evaluator or rendering result is claimed. Preview availability is not used as acceptance evidence.

Exact source at the pinned Agent SHA:

| Path | Relevant lines / behavior |
| --- | --- |
| `astrid/sdk/timeline/_common.py` | 93–94: `_r(value) = round(float(value), 6)`; existing authored precision is six decimal places. |
| `astrid/sdk/timeline/_trim_commands.py` | 63–73 read/guard the unrounded authoritative duration and endpoints; 75–81 round hold/endpoints and record writes without another duration guard; 93–99 capture by actual execute. |
| `astrid/sdk/timeline/model.py` | 432–450: existing `Clip.trim` also guards before `_r`, matching the command recipe. |
| `astrid/sdk/timeline/commands.py` | 144–211: execute runs the registered operation, checks claims and compiles mirrors. |
| `astrid/sdk/timeline/_recording.py` | 193–218: compile inputs/mirrors retain dependencies and mirror authored clips; they do not clamp the rounded endpoint. |
| `astrid/sdk/timeline/commit.py` | 218–225: document materialization invokes `compile_authoring_candidate(bundle).publication`. |
| `astrid/core/timeline/authoring_bundle.py` | 778 onward: current publication compiler accepts this candidate, demonstrated by both compiled clip arrays. |

Smallest proposed Agent-owned domain fix (proposal only): retain the raw-range guard and the existing six-decimal authored precision, then check the rounded endpoint against the same **unrounded** registry duration before recording writes. In the native trim recipe, an additional `_r(source_out) > limit` refusal prevents this counterexample without global precision changes, duration rounding, an epsilon, clamping, a duration alias, or a new command format. Keep source-time hold and speed behavior unchanged. Agent must decide and coordinate consistency with `Clip.trim`, which has the same defect; then App can mirror the approved narrow guard. Add new boundary coverage for this input, exact file-end contact, and preserved source units, keeping all original positive tests/goldens and capture/undo guards intact. This proposal changes currently accepted boundary behavior and therefore needs Agent/orchestrator ownership; no App-only policy was implemented.

Reproduce (the script and output remain in this worker's shared directory; the disposable source archive is cleaned after testing):

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER="$ORCH/workers/app-m2-trim-native-boundary-parity"
APP=/home/user/work/wt/app-m2-trim-native-boundary-parity
SOURCE_SHA=76737ca2f9c86a075e7e03dfc8990e3090acc234
mkdir -p "$WORKER/agent-source"
git -C /home/user/work/agent archive "$SOURCE_SHA" | tar -x -C "$WORKER/agent-source"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WORKER/agent-source" /home/user/work/venv-agent/bin/python "$WORKER/native-counterexample.py" "$WORKER/agent-source" "$APP/src/tools/video-editor/commands/fixtures/recipe_m2_clip_trim.json"
cd "$WORKER/agent-source"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WORKER/agent-source" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_trim.py
```

Counterexample exits **0**, printing `native_domain_accepts_out_of_range_authored_endpoint: true`. Native existing targeted conformance: **79 passed in 3.63s**, exit 0; this includes the original 78 plus one newer native ripple/group regression. No native test expectation was changed.

Artifact paths: `$WORKER/native-counterexample.py`, `$WORKER/native-counterexample.log`, `$WORKER/report.md`, and `$WORKER/app-targeted.log`. The worker report records the App targeted result and exact runner command. No App product/test/protocol/pin, original claim document, root adoption or ingress edit was made. No full suite, build, browser, live socket, TypeScript compiler, install, shared dependency or shared cache write was performed.

App verification completed: **14 files / 621 passed**, exit 0, 42.94s, using the private Composition 0.0.12 alias config, runner loader, no cache and one worker. Exact command and full file list are in the worker report. App tracked tree remains clean.
