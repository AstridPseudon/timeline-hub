# AP2 M2 ordinary compiler-canary project-data native recipe

Date: 2026-10-20

## Verdict

**Native replacement is missing.** Do not activate the current generic native
session for the compiler-canary `project-data.write` positive. The current App
root still has the required legacy snapshot path for this standalone producer;
the producer must remain reachable until Agent and Runtime expose a paired
native operation.

This is an independent unsupported standalone patch, not evidence that a
mixed native batch may partially commit. If a future patch contains a
supported native member plus this unsupported member, reject the complete
batch before capture, owner resolution, preview, enqueue, or snapshot
fallback. The compiler canary's source/source-map operations must remain one
data batch; do not split them into per-key submissions.

## Source status and exact positive

Reviewed current roots:

- App: `05b6b488d1834650c459c5c565f2530d9bea20e9`
- Agent: `30fc8dd1` (`/home/user/work/agent`, `tl/integration`)
- Runtime: `a51af885ea631c695a857985239c7fe7bf2e871f`

App's `compiler-canary.ts:155-170` builds this ordinary positive source
operation (the value is the exact `JSON.stringify` form produced by the
canary):

```json
{
  "op": "project-data.write",
  "target": "com.example.compiler-canary",
  "payload": {
    "key": "__dsl__:dsl://com.example.compiler-canary/main.json",
    "value": "{\"version\":1,\"sourceUri\":\"dsl://com.example.compiler-canary/main.json\",\"clips\":[{\"id\":\"canary-clip-1\",\"track\":\"V1\",\"at\":0,\"duration\":1,\"clipType\":\"hold\",\"sourceLine\":3}]}",
    "mode": "replace"
  }
}
```

The canary assembles this with any source-map writes into one `dataPatch` at
`compiler-canary.ts:421-441`, then separately creates the generated-clip
proposal. A successful authored change is therefore: set exactly one
extension-owned project-data entry at the target/key, preserve other extension
entries and timeline state, and advance the authored revision once for the
data batch. This positive does not add or alter a clip.

## Exact rejection evidence

The private probe submitted the corresponding candidate command to current
Agent:

```json
{
  "schema_version": 1,
  "op": "project-data.write",
  "version": "1",
  "select": "parent",
  "args": {
    "key": "__dsl__:dsl://com.example.compiler-canary/main.json",
    "value": "{\"version\":1,\"sourceUri\":\"dsl://com.example.compiler-canary/main.json\",\"clips\":[{\"id\":\"canary-clip-1\",\"track\":\"V1\",\"at\":0,\"duration\":1,\"clipType\":\"hold\",\"sourceLine\":3}]}",
    "mode": "replace"
  }
}
```

Results with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent
/home/user/work/venv-app2-native/bin/python`:

- `validate_command`: `CommandError: unsupported operation
  'project-data.write'`, `kind=unsupported_operation`.
- `execute`: the same rejection; the input authoring bundle was unchanged.
- The current Agent operation registry (`astrid/sdk/timeline/commands.py:29-72`)
  has no project-data operation. Runtime's `contract/schemas/edit-command.json`
  has the same closed union and no `project-data.write` branch.

The probe also ran an existing native `clip.set` control with the same Agent
engine: its recorded hold write inverse-restored the original bundle,
redo restored the forward bundle, and `replay()` matched both bundle and
records. That proves the existing recording/inverse/replay machinery works;
it does not qualify project-data support.

## Why existing operations are insufficient

- `clip.set` and `clip.set-params` address authored clip fields, not an
  extension target/key namespace.
- `track.set`, `shot.set`, and `app`-carrying authored rows cannot express the
  canary's extension project-data entry without changing the wrong authored
  object and losing the current project-data limits/ownership semantics.
- `timeline.restore` is a whole-timeline restore operation, not a stable
  project-data write recipe; using it would bypass the required semantic
  target/key recording and guarded inverse behavior.
- App's current `useTimelineOps.ts:298-303` snapshot path remains the only
  valid route for this standalone operation. The held generic session path
  must not turn this valid positive into a refusal.

## Smallest Agent peer contract requested

Please add and pair one native operation for the `replace` form above, without
changing the Runtime endpoint or adding a second store. The command envelope
may follow Agent's chosen stable target encoding, but it must carry the exact
existing App semantics: extension target ID, non-empty project-data key,
finite JSON value, and `mode: "replace"` (defaulting only if that is already
the command convention).

The operation must:

1. Read and record the prior presence/value for the exact target/key, write the
   new value, and preserve every other extension entry and authored field.
2. Produce an authoritative recording for the target/key and value presence;
   `timeline.inverse` must restore an absent prior entry as absent, or restore
   the exact prior JSON value, with the normal guarded-intervening-write and
   A→B→A checks.
3. Replay deterministically against the recorded target/key and preserve
   opaque values. A batch of source plus source-map writes must execute
   atomically and in input order, with no partial supported-member submission.
4. Be registered in Agent and the byte-compatible Runtime command schema and
   provider registry. Runtime acceptance must use the existing `/v1` commit
   request and existing accepted-revision/idempotency behavior.

`merge` and `project-data.delete` are not required to close this one positive;
they should remain separate contract rows rather than being smuggled into a
replace-only implementation.

## Current App preservation boundary

Keep `compiler-canary.ts` unchanged. Keep the current legacy snapshot writer
reachable for an all-unsupported standalone `project-data.write` patch until
the paired Agent/Runtime operation is qualified. Once the new operation is
available, the App adapter should be a thin builder that captures the complete
source/source-map batch into one existing `commands[]` outbox intent and
returns the native local projection. Before then, no App-only mapper can
honestly claim native replacement.

## Evidence and limits

Passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/compiler-canary.test.ts \
  src/tools/video-editor/lib/timeline-patch.test.ts
=> 2 files, 360 tests passed
```

```text
Private Agent probe against /home/user/work/agent at 30fc8dd1
=> project-data.write validation/execution rejected atomically;
   existing clip.set control inverse/redo/replay all matched
```

No product source, shared worktree, dependency, schema, generated contract,
pin, new test, browser, localhost, socket, Runtime HTTP, or full suite was
run or changed. Runtime registry/schema evidence is source inspection only;
Runtime acceptance remains unverified until Agent supplies the paired
operation.
