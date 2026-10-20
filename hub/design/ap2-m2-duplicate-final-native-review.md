# ap2-m2 duplicate final native review

## Decision

**APPROVE source.** The repaired five-file App delta matches Agent `68a51203310eb7c1bad343e50a42cf75c46c5321` on the requested native duplicate behavior. The actual App gesture/session/editor/outbox gate remains **HOLD** and was not qualified by this review.

## Reviewed scope

- App HEAD: `f34054c624f78c4f2f3b73551733f9151fc1b930`
- Base: `05b6b488d1834650c459c5c565f2530d9bea20e9`
- Delta: exactly five added files under `src/tools/video-editor/commands/` (capture helper, gesture adapter, two tests, and the recipe fixture).
- Agent comparison source: `68a51203310eb7c1bad343e50a42cf75c46c5321`, via the read-only private extracted environment.

The source derives the destination shot revision identity and destination occurrence root identities before recording the occurrence create. It conditionally rewrites only root fields that exist on the source row; all other row/shot/internal values remain copied. No second wire contract, pin/cohort, stored field, or legacy writer was added in this delta.

## Evidence

Focused App tests, with shared Vite cache disabled and one worker:

```text
NODE_OPTIONS='--import=data:text/javascript,globalThis.__dirname%3D"/home/user/work/wt/ap2-m2-duplicate-final-native-review/config/testing"' ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --configLoader=runner --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts
```

Result: **2 files passed, 41 tests passed**.

Agent targeted recipe, using only the private read-only source extraction and private venv:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-duplicate /home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-duplicate/tests/editing_conformance/test_recipe_occurrence_duplicate.py
```

Result: **63 passed in 3.79s**.

Targeted lint:

```text
./node_modules/.bin/eslint src/tools/video-editor/commands/occurrenceDuplicateCapture.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts --ext ts,tsx --max-warnings 0
```

Result: **passed**.

Fresh native parity probe: the payload was generated in this current worktree by importing the current fixture and calling `captureOccurrenceDuplicate` then `finishOccurrenceDuplicate`; no prior payload JSON was reused. It was piped directly to the private read-only Agent source using `/home/user/work/venv-app2-native/bin/python`. The exact current-TS producer command was:

```text
PYTHONDONTWRITEBYTECODE=1 node --import tsx/esm --input-type=module <<'JS' | PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-duplicate /home/user/work/venv-app2-native/bin/python -c 'import copy,hashlib,json,sys; from astrid.core.timeline.authoring_bundle import compile_authoring_candidate; from astrid.sdk.timeline._collections import AcceptedRecords; from astrid.sdk.timeline.commands import execute,validate_command; from astrid.sdk.timeline.commit import bundle_from_document,document_from_bundle; from astrid.sdk.timeline.rebase import replay; from tests.editing_conformance.test_recipe_m1_commands import inverse; p=json.load(sys.stdin); b=p["basis"]["bundle"]; c=p["basis"]["command"]; ts=p["result"]; before=copy.deepcopy(b); validate_command(c); plan=execute(b,[c]); replayed=replay(plan,b); compiled=document_from_bundle(plan.bundle); raw=compile_authoring_candidate(plan.bundle).publication; reloaded=bundle_from_document(compiled); accepted=AcceptedRecords([{ "records": {"commands":plan.records}}],plan.records,lambda _: (copy.deepcopy(before),copy.deepcopy(reloaded))); undone=inverse(reloaded,accepted); ts_occ=next(w for w in ts["record"]["writes"] if w["ref"]=="occurrence:occ-copy" and not w["path"]); ag_occ=next(w for w in plan.records[0]["writes"] if w["ref"]=="occurrence:occ-copy" and not w["path"]); print("Agent validate/execute: PASS"); print("full record exact:",ts["record"]==plan.records[0]); print("full occurrence write exact:",ts_occ==ag_occ); print("raw occurrence roots:",json.dumps({k:ts_occ["after"]["value"].get(k) for k in ("stable_deep_link","output_identity")},sort_keys=True)); print("Agent occurrence roots:",json.dumps({k:ag_occ["after"]["value"].get(k) for k in ("stable_deep_link","output_identity")},sort_keys=True)); print("raw bundle exact:",ts["bundle"]==plan.bundle); print("compiled projection exact:",raw["parent_composition"]["occurrences"][-1]==compiled["parent_revision"]["payload"]["occurrences"][-1]); print("reload exact:",bundle_from_document(compiled)==reloaded); print("guarded inverse exact:",document_from_bundle(undone.bundle,source_bundles=(before,reloaded))==document_from_bundle(before)); print("replay record/bundle exact:",replayed.records[0]==plan.records[0] and replayed.bundle==plan.bundle); print("created IDs stable:",ts["record"]["created"]==plan.records[0]["created"]==replayed.records[0]["created"]); print("command sha256:",hashlib.sha256(json.dumps(c,sort_keys=True,separators=(",",":")).encode()).hexdigest())'
import fixture from './src/tools/video-editor/commands/fixtures/recipe_m2_app_occurrence_duplicate.json' with { type: 'json' };
import { captureOccurrenceDuplicate, finishOccurrenceDuplicate } from './src/tools/video-editor/commands/occurrenceDuplicateCapture.ts';
const basis = captureOccurrenceDuplicate(fixture.bundle, 'occurrence:occ-0', { occurrence_id: 'occ-copy', shot_id: 'shot-copy' });
const result = finishOccurrenceDuplicate(basis);
process.stdout.write(JSON.stringify({ basis, result }));
JS
```

Probe result: full record exact `True` (including all write values); full occurrence write exact `True`; raw and Agent destination roots identical; raw bundle exact `True`; compiled projection exact `True`; reload exact `True`; guarded inverse exact `True`; replay record/bundle exact `True`; created IDs stable `True`. Command SHA-256: `fb341fc784eb919796e5d65b6f2e8331239b3e8d77e6d61884c3ae5a4db91abb`.

An additional fresh in-memory current-TS case deleted both root fields and added nested `task`, `history`, `output`, and `unknown` values before capture. Direct Agent comparison reported: `absent-roots-with-nested-opaque record: True bundle: True opaque: True absent: True`.

The checked-in fixture’s direct assertions compare the whole occurrence outside identity roots, and explicitly compare `output_records` and `metadata`; the focused suite retains the absent-root case and serialized retry/ID guards. The fixture has no standalone `history` key, so the extra in-memory case covers that exact shape.

## Review limits

- No full suite, browser, localhost, socket, Runtime, or actual App gesture/session/editor/outbox run was performed, per brief.
- No source, dependency, shared node_modules, pin, generated artifact, or test mutation was made.
- `git diff --check 05b6b488d..HEAD` reports only a trailing blank line at fixture EOF; no whitespace error in executable source. This is non-blocking for the source decision.

