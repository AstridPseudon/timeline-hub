# App2 element capture native parity review

## Verdict: REQUEST CHANGES

The 397-line App-only diff is not acceptable as current-Agent-native parity. The focused Vitest tests are internally consistent, but a native `310e5484` probe rejects the produced `clip.set-element` capture record, and the selected project-pack path does not perform the Agent's authoritative schema/snapshot capture or validation.

Reviewed App diff: `55e7e217..HEAD`, exactly:

- `src/tools/video-editor/commands/elementCapture.ts` (289 added lines)
- `src/tools/video-editor/commands/elementCapture.test.ts` (108 added lines)

Agent source: private `agent-ordinary` prepared from `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`.

## Findings

### 1. Required: `clip.set-element` records non-native reads and is refused by Agent

`elementCapture.ts:131-135` reads `clipType`, `hold`, `asset`, `file`, `src`, `source`, `from`, and `to` before reading `elementRef`/`element_ref`. Current Agent `clip_set_element` calls `_target` and then reads only `elementRef` and `element_ref` (`_clip_scalar_commands.py:111-127`).

The external draft-revision probe used the same ordinary clip shape and the same command arguments. The TS command had those eight additional reads. Submitting that exact TS command to native `validate_command` + `execute` produced:

```text
element CommandError submitted reads does not match authoritative capture
```

The native capture produced only `id`, `elementRef`, and `element_ref` reads. This is not merely a more conservative local guard: the Agent checks submitted capture fields exactly and refuses the command.

Minimal fix: make the element recorder use the existing `_target`-equivalent context plus the two element-reference reads only. Remove the copied scalar/clip-field read loop; do not add a new selection or authority abstraction.

### 2. Required: selected project-pack capture bypasses Agent authority and has the wrong record shape

The selected branch (`elementCapture.ts:200-212`, `261-272`) treats a locally retained `schema_source` as sufficient. `schemaSource` (`:79-91`) checks only that the pin appears in authored `dependency_manifest.documents` and `pinned_documents`. It does not prove the current Agent inputs.

Agent `_selected_schema` (`_scalar_commands.py:98-128`) requires all of the following:

- scoped `realm_id`;
- exactly one verified `schema_inputs` entry for the exact pin;
- an admission matching selected `id`, `kind`, and `revision`;
- the immutable admitted snapshot object and descriptor validation;
- `params.schema` and `params.snapshot` dependencies, with `params.element` bound to both.

The App selected implementation records only `params.schema` and binds `params.element` to `params.schema` (`elementCapture.ts:237-238`). Selected element revision capture uses different local names (`element.schema` / `element.target`, `:142-145`) and also omits the native snapshot dependency/binding. It also does not run the admitted descriptor's parameter-schema validation for changed known parameters.

The selected probe used a structurally valid native pin (`sha256:` plus 64 hex digits). Native `validate_command` accepted the command shape, but both native `execute` and `capture_clip_set_params` refused the hand-captured command without the authoritative realm/schema inputs:

```text
validate_command: accepted
execute CommandError selected pack capture requires the scoped realm identity
capture_clip_set_params CommandError selected pack capture requires the scoped realm identity
```

The App tests use `sha256:pack`, which is not a native `DocumentPin` digest (`edit-command.schema.json` requires `^sha256:[0-9a-f]{64}$`), so those tests cannot establish native acceptance.

Minimal fix: do not claim or locally synthesize selected-pack capture from retained authored JSON. Route selected element/PARAM capture through the existing Agent/provider capture seam with its authenticated `realm_id` and `schema_inputs`, and retain the returned authoritative command/record. If that seam is not available to this App producer, fail closed for selected-pack capture and leave it out of this bounded producer; do not add a caller-side schema/admission cache.

### 3. Not confirmed: `element.targets` is not a current Agent requirement in the named source

The review searched the `310e5484` timeline implementation and tests for `element.targets`; no such field or selection is present in the named `clip_set_element` path. The comment at `elementCapture.ts:131-133` therefore does not establish a missing native requirement. The actual native mismatch is the extra reads in the following loop, and the selected-pack record/authority mismatch above. No panel behavior was inferred from this source-only finding.

## What is in and out of scope

The bounded source is intended only for existing-clip element revision and literal PARAM commands. The existing panel operations for overlay creation/removal, transitions, and full-panel apply are not represented by these helpers and remain unqualified, as required by the handoff. No browser, panel, authenticated App session, outbox, Runtime-door, or zero-legacy-traffic claim is made here.

## Evidence

Focused App tests passed:

```sh
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/clipParamsCapture.test.ts
```

Result: **2 files, 135 tests passed**.

External parity probes were run from temporary files under `/tmp`, using `/home/user/work/venv-app2-native` read-only and the private Agent source. The ordinary draft-revision probe compared exact command/record fields and submitted the TS-produced command to native `validate_command`/`execute`; native PARAM capture matched and accepted the equivalent command, while element capture failed on the extra reads as above. The selected-pack probe submitted the TS-shaped command to native validation, execution, and capture; results are recorded above. Temporary probe files were removed after review.

No full, browser, socket, Runtime, or Agent full suite was run. The extracted Agent source does not contain the selected-schema pytest path from the archived reports, so no misleading Agent test result is claimed.

