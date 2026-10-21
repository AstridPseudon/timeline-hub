# Selected seed publication refusal 13522

## Result

No repository or shared edit was made. The existing refusal is correctly caused by
fixture phase, not by Agent/Runtime authority:

1. `DirectHarness.start()` creates the private realm at
   `tests/e2e/local/support/harness.ts:461-479`, starts Runtime without the
   authoring profile, provisions the product credential, and calls
   `seedRuntime()`.
2. The normal seed producer creates the project and accepts its ordinary
   `compositionPublication(...)` at `harness.ts:790-797`; the returned
   `data.new_head` becomes `seed.headRevisionId` at `harness.ts:807-812`.
3. `enableTimelineAuthoring()` stops and restarts Runtime at `harness.ts:498-505`.
   `startRuntime()` then adds `--authoring-profile astrid` at `harness.ts:516-520`.
4. The selected seed currently does that restart first at `harness.ts:642-644`,
   then sends the raw `composition-revisions` publication at `harness.ts:693-698`
   with `expected_head = this.seed.headRevisionId`. That is tracked timeline
   publication after authoring has been enabled, so the observed 409
   `timeline_commit_required` is the expected refusal before P1/P2.

This preserves the settled decision that public Agent/Runtime tracked timeline
publication is command-only. No grant, guard, source pin, or Runtime context
should change.

## Existing supported carrier

Use the existing normal `DirectHarness` fixture producer and its existing private
realm, not a new writer or a synthetic history operation:

- `compositionPublication()` is the existing normal payload builder at
  `harness.ts:277-294`.
- `seedRuntime()` already proves the accepted pre-authoring phase at
  `harness.ts:790-813`: project creation, raw publication, and `new_head`
  capture happen while `timelineAuthoring` is false.
- The selected method can use the same existing route and builder for its
  selected payload before the existing authoring restart. The private realm is
  already created by this harness for this test worker; no cross-test or shared
  state is involved.

The existing private native genesis helper was also checked:
`tests/e2e/timeline/viewing-parity/native-fixture-helper.py:139-181` prepares a
hard-coded frame-parity document through Runtime internals before daemon startup,
then `fixture.ts:156-175` adopts it with `timeline.restore`. It is not a carrier
for this seed: its parent/shot/internal closure, media set, occurrence, and
payload are different, and changing it to accept the selected payload would be a
new generic writer/recipe. It must not be guessed, reused by substitution, or
used to drop selected fields.

## Exact smallest patch proposal (not applied)

HOME owns `harness.ts`; this is a proposal only. In
`tests/e2e/local/support/harness.ts:642-701`:

```diff
   async seedSelectedParamDev(): Promise<SelectedParamDevSeed> {
     if (this.selectedParamDevSeed) return this.selectedParamDevSeed;
-    await this.enableTimelineAuthoring(this.agentPython());
     const python = this.agentPython();
     const sourceRoot = path.join(this.tmp, 'selected-project-packs');
     const artifactRoot = path.join(this.tmp, 'selected-element-artifacts');
     const credentialFile = path.join(this.tmp, 'selected-agent-credential.json');
     const verifier = path.join(this.tmp, 'selected-element-build-verifier.py');
     mkdirSync(sourceRoot, { recursive: true, mode: 0o700 });
     mkdirSync(artifactRoot, { recursive: true, mode: 0o700 });
-    await this.provisionCredential('astrid-selected-param', path.basename(credentialFile));
-    const discovery = this.discovery();
     writeFileSync(verifier, "import hashlib,json,sys\\nfrom pathlib import Path\\np=Path(sys.argv[1])\\nselection=json.loads(p.read_text())\\nprint(json.dumps({'schema':'astrid.element-build/v1','selectionDigest':'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest(),'elements':[{'projectId':e['projectId'],**{k:e['descriptor'][k] for k in ('packId','id','kind','revision')}} for e in selection['elements']]}))\\n");
     this.selectedParamPython = python;
     this.selectedParamVerifier = verifier;
     const { projectId, timelineId, image } = this.seed;
+    const elementId = 'selected_param_fixture';
+    const clipId = 'selected-param-clip';
+    const clips = [
+      { id: 'selected-base-clip', at: 0, track: 'V1', clipType: 'media', asset: 'selected-image', from: 0, to: 3, speed: 1 },
+      { id: clipId, at: 0, track: 'FX', clipType: elementId, hold: 3,
+        elementRef: { id: elementId, kind: 'effect', revision: 'draft-1' }, params: { amount: 4 } },
+    ];
+    const publication = compositionPublication({ projectId, timelineId }, this.seed.headRevisionId, 'Selected PARAM', 30);
+    publication.parent_composition.config = { ...publication.parent_composition.config, clips,
+      tracks: [{ id: 'V1', kind: 'visual', label: 'V1' }, { id: 'FX', kind: 'visual', label: 'FX' }] } as typeof publication.parent_composition.config;
+    publication.parent_composition.clips = clips as unknown as typeof publication.parent_composition.clips;
+    publication.parent_composition.registry = { assets: { 'selected-image': {
+      file: 'selected-image.png', type: 'image/png', media_id: image.objectId, content_sha256: image.digest,
+    } } } as unknown as typeof publication.parent_composition.registry;
+    const published = await this.runtimeJson('POST', `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, publication);
+    if (published.status !== 200) throw new Error(`selected PARAM timeline: ${published.status} ${JSON.stringify(published.body)}`);
+    await this.enableTimelineAuthoring(python);
+    await this.provisionCredential('astrid-selected-param', path.basename(credentialFile));
+    const discovery = this.discovery();
     this.selectedParamEnv = {
       ...selectedParamEvalEnv(process.env, credentialFile, {
         endpoint: discovery.endpoint,
         realmId: this.realmId,
         actorId: 'astrid-selected-param',
       }),
       ...this.runtimeEnv(),
       ASTRID_RUNTIME_ENDPOINT: this.runtimeUrl,
       ASTRID_PROJECT_PACKS_ROOT: sourceRoot,
       ASTRID_ELEMENT_ARTIFACT_ROOT: artifactRoot,
       ASTRID_ELEMENT_BUILD_COMMAND: JSON.stringify([python, verifier]),
     };
     const initialized = this.projectPackCommand(['init', ...]);
     ...existing pack/P1 setup...
-    const clipId = 'selected-param-clip';
-    const clips = [the exact existing two clip objects];
-    const publication = compositionPublication(...the exact existing call...);
-    ...the exact existing config/clips/registry assignments...;
-    const published = await this.runtimeJson('POST', ...);
-    if (published.status !== 200) ...;
     const applied = this.agentCommand([... '--expected-head', published.body.data.new_head, ...]);
```

The remaining `...` markers stand only for unchanged pack/P1 and command context
outside the moved hunk; they are not proposed helpers or new behavior. Apply the
current `harness.ts:685-698` block verbatim at the marked pre-restart location,
hoist `elementId`/`clipId`, and remove the later duplicate block. The existing
`draft-1` carrier remains. In particular, do not use the admitted P1 revision in
the initial payload, do not add `pack_id`, and do not alter the selected spec.

Raw initial P1 equality is therefore structural and field-for-field: the same
`project_id`, `timeline_id`, `expected_head`, generated `parent_revision_id`,
`slug`, `name`, output `{resolution: '1280x720', fps: 30, file: 'out.mp4'}`,
the same V1/FX tracks, the same two clips, the same `selected-image` media
registry entry, empty occurrences, empty shot revisions, and empty internal
timeline revisions. The selected element ref remains the original unowned
`{id: 'selected_param_fixture', kind: 'effect', revision: 'draft-1'}` and the
original params remain `{amount: 4}`. Only the phase moves earlier.

Expected accepted history after the proposal is applied:

- the existing seed head remains the parent of the selected raw publication;
- the selected raw publication is accepted before the authoring restart as the
  normal `parent_composition.publish` entry, with its exact payload read back;
- the restart changes Runtime profile only and does not rewrite accepted history;
- the existing Agent `update-element` call then accepts P1 from the selected
  head and its current assertion at `harness.ts:702-707` proves the next entry's
  operations are exactly `clip.set-element`, `clip.set-params`;
- P2 and later behavior are not claimed here.

This matches the existing Main bootstrap history precedent in
`tests/e2e/local/main95-native-bootstrap.integration.spec.ts:139-187` and
`tests/e2e/local/three-products.spec.ts:1722-1764`: accepted history is
baseline `parent_composition.publish` followed by a native `timeline.commit`,
with no accepted-history rewrite.

## Verification and limits

Passed, offline and targeted:

- `node --import tsx --test tests/e2e/local/support/selected-param-credential.test.ts`
  — 1 test file passed, 1 test passed.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/three-products.selected-param-dev.spec.ts`
  — passed.
- `git diff --check` — passed (no repository diff).

Not run by instruction: the selected seed, Runtime, daemon, browser, localhost,
live socket, build, install, central service, full suite, or any P1/P2 behavior
journey. The current source still contains the refusal order because HOME owns
the file and this worker was explicitly forbidden to edit it. Therefore the
proposal is not actual qualification and does not claim that P1/P2 accepts.

After HOME applies the proposal, the focused fixture-only check should be the
existing offline command above plus a readback assertion in the HOME-owned
selected fixture that the pre-restart publication returns 200, its returned
`new_head` is the Agent command's `expected-head`, and history contains the
publication before the `clip.set-element`/`clip.set-params` entry. Do not use a
browser or full suite for this fixture check; the real selected journey remains
central-service work.

## Blocker / owner dependency

No supported existing carrier other than the pre-authoring
`compositionPublication` seam fits every original selected field. The private
native genesis helper does not fit the payload. HOME must apply the order-only
fixture patch and provide the requested exact pre-restart readback; no Runtime,
Agent, grant, guard, DTO, schema, pin, or source change is warranted.
