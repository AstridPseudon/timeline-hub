import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { once } from 'node:events';
import { readFile } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import http from 'node:http';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import {
  AUDIO_REACTIVE_FIXTURE_TIMELINE_ID,
  AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID,
  AUDIO_REACTIVE_OFFSET_START_FRAME,
  createAudioReactiveColourFixtures,
  createOffsetAudioReactiveColourFixtures,
  createTimelineFixtures,
} from '../../../src/test/bridgeFixtures.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const STUB = resolve(HERE, 'astrid-bridge-stub.mjs');

async function freePort() {
  const server = http.createServer();
  await new Promise((resolvePromise) => server.listen(0, '127.0.0.1', resolvePromise));
  const address = server.address();
  assert.ok(address && typeof address !== 'string');
  const port = address.port;
  await new Promise((resolvePromise, reject) => server.close((error) => error ? reject(error) : resolvePromise()));
  return port;
}

async function waitForHealth(origin) {
  for (let attempt = 0; attempt < 50; attempt += 1) {
    try {
      const response = await fetch(`${origin}/health`);
      if (response.ok) return;
    } catch {
      // The child may still be binding its listener.
    }
    await new Promise((resolvePromise) => setTimeout(resolvePromise, 20));
  }
  throw new Error(`stub did not become healthy at ${origin}`);
}

test('deterministic Astrid stub serves the typed Runaway contract', async () => {
  const port = await freePort();
  const origin = `http://127.0.0.1:${port}`;
  const child = spawn(process.execPath, [STUB], {
    env: { ...process.env, ASTRID_BRIDGE_PORT: String(port), BASE_URL: origin },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  try {
    await waitForHealth(origin);

    const workspaceConfigResponse = await fetch(`${origin}/runtime-config/v1/workspace.json`);
    assert.equal(workspaceConfigResponse.status, 200);
    assert.deepEqual(await workspaceConfigResponse.json(), {
      schemaVersion: 1,
      endpoint: origin,
      actorId: 'reigh-product-connector',
      realmId: 'realm-reigh-editor-e2e',
      runtimeInstanceId: 'runtime-instance-reigh-editor-e2e',
    });
    const healthResponse = await fetch(`${origin}/v1/health`);
    assert.equal(healthResponse.status, 200);
    const health = await healthResponse.json();
    const runtimeClient = await readFile(resolve(HERE, '../../../src/integrations/runtime/client.ts'), 'utf8');
    const generatedMetadata = await readFile(resolve(HERE, '../../../src/integrations/runtime/generated-contract-metadata.ts'), 'utf8');
    const contractMetadata = await readFile(resolve(HERE, '../../../src/integrations/runtime/contract-metadata.ts'), 'utf8');
    const expectedScopes = /export const RUNTIME_CLIENT_SCOPES = \[([\s\S]*?)\];/
      .exec(runtimeClient)?.[1].match(/'([^']+)'/g)?.map((scope) => scope.slice(1, -1));
    const expectedDigest = /SCHEMA_DIGEST = "(sha256:[0-9a-f]+)"/.exec(generatedMetadata)?.[1];
    const expectedCapability = /RUNTIME_TARGETED_EXECUTION_CAPABILITY = '([^']+)'/.exec(contractMetadata)?.[1];
    assert.ok(expectedScopes?.length);
    assert.ok(expectedDigest);
    assert.ok(expectedCapability);
    assert.equal(health.schema_digest, expectedDigest);
    assert.equal(health.runtime_instance_id, 'runtime-instance-reigh-editor-e2e');
    assert.equal(health.runtime_session_id, 'session-reigh-editor-e2e');

    const handshakeResponse = await fetch(`${origin}/v1/handshake`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ protocol: 'workspace.v1', client_name: 'contract-test', client_version: '1', requested_scopes: expectedScopes }),
    });
    assert.equal(handshakeResponse.status, 200);
    const handshake = await handshakeResponse.json();
    assert.equal(handshake.protocol, 'workspace.v1');
    assert.equal(handshake.schema_digest, expectedDigest);
    assert.equal(handshake.actor_id, 'reigh-product-connector');
    assert.equal(handshake.realm_id, 'realm-reigh-editor-e2e');
    assert.deepEqual(handshake.scopes, expectedScopes);
    assert.deepEqual(handshake.capabilities, [expectedCapability]);

    const realmResponse = await fetch(`${origin}/v1/realm`);
    assert.equal(realmResponse.status, 200);
    assert.equal((await realmResponse.json()).realm_id, handshake.realm_id);
    const projectsResponse = await fetch(`${origin}/v1/projects?limit=200`);
    assert.equal(projectsResponse.status, 200);
    assert.deepEqual(await projectsResponse.json(), { items: [], next_cursor: null });

    const response = await fetch(`${origin}/v1/projects/cross-browser-release-gate/runaway-transitions?limit=1000`);
    assert.equal(response.status, 200);
    assert.equal(response.headers.get('X-Astrid-Bridge-Version'), 'v1');
    const body = await response.json();
    assert.equal(body.api_version, 'v1');
    assert.equal(body.project, 'cross-browser-release-gate');
    assert.equal(body.count, 566);
    assert.equal(body.total_count, 566);
    assert.equal(body.page.limit, 1000);
    assert.equal(body.page.next_cursor, null);
    assert.equal(body.transitions.length, 566);
    assert.equal(body.timing_summary.data.frame_count, 8085);
    assert.equal(body.timing_summary.data.transition_count, 566);
    assert.equal(body.timing_summary.data.fps, 48);
    assert.equal(body.transitions[0].metadata.manifest_id, 'T0001');
    assert.equal(body.transitions.at(-1).metadata.manifest_id, 'T0566');

    const frames = body.transitions.map((transition) => transition.metadata.frame);
    const durations = body.transitions.map((transition) => transition.duration_ms);
    assert.equal(frames[0], 0);
    assert.equal(frames.at(-1), 8084);
    assert.ok(frames.every((frame, index) => index === 0 || frame > frames[index - 1]));
    assert.ok(durations.every((duration) => duration > 0));
    for (const [index, transition] of body.transitions.entries()) {
      const frame = frames[index];
      const nextFrame = index + 1 < frames.length ? frames[index + 1] : 8085;
      const expectedStartMs = Math.round((frame * 1000) / 48);
      const expectedDurationMs = Math.max(1, Math.round((nextFrame * 1000) / 48) - expectedStartMs);
      assert.equal(transition.start_ms, expectedStartMs);
      assert.equal(transition.duration_ms, expectedDurationMs);
    }
    const totalEnvelopeMs = Math.round((8085 * 1000) / 48);
    assert.equal(
      body.transitions.reduce((total, transition) => total + transition.duration_ms, 0),
      totalEnvelopeMs,
    );
    assert.equal(
      body.transitions.at(-1).start_ms + body.transitions.at(-1).duration_ms,
      totalEnvelopeMs,
    );

    const firstPage = await fetch(`${origin}/v1/projects/cross-browser-release-gate/runaway-transitions?limit=3`);
    assert.equal(firstPage.status, 200);
    const firstPageBody = await firstPage.json();
    assert.equal(firstPageBody.count, 3);
    assert.equal(firstPageBody.total_count, 566);
    assert.equal(firstPageBody.page.limit, 1000);
    assert.equal(firstPageBody.page.next_cursor, '3');
    assert.deepEqual(firstPageBody.transitions.map((transition) => transition.ordinal), [0, 1, 2]);

    const secondPage = await fetch(`${origin}/v1/projects/cross-browser-release-gate/runaway-transitions?limit=3&cursor=3`);
    assert.equal(secondPage.status, 200);
    const secondPageBody = await secondPage.json();
    assert.equal(secondPageBody.count, 3);
    assert.equal(secondPageBody.page.next_cursor, '6');
    assert.deepEqual(secondPageBody.transitions.map((transition) => transition.ordinal), [3, 4, 5]);

    const tasks = await fetch(`${origin}/projects/demo-project/tasks?limit=1`);
    assert.equal(tasks.status, 200);
    assert.deepEqual(await tasks.json(), { tasks: [], next_offset: null });
    const generations = await fetch(`${origin}/projects/demo-project/generations?limit=1`);
    assert.equal(generations.status, 200);
    assert.deepEqual(await generations.json(), { generations: [], next_cursor: null });

    // Browser workspace.v1 discovery is proxied through these versioned
    // aliases after Vite strips /api/astrid. Keep them distinct from the
    // legacy unversioned bridge endpoints above so a contract regression
    // cannot pass by silently falling through to an empty legacy response.
    const versionedTasks = await fetch(`${origin}/v1/projects/demo-project/tasks?limit=1`);
    assert.equal(versionedTasks.status, 200);
    assert.equal(versionedTasks.headers.get('X-Astrid-Bridge-Version'), 'v1');
    assert.deepEqual(await versionedTasks.json(), { items: [], next_cursor: null });
    const versionedGenerations = await fetch(`${origin}/v1/projects/demo-project/generations?limit=1`);
    assert.equal(versionedGenerations.status, 200);
    assert.equal(versionedGenerations.headers.get('X-Astrid-Bridge-Version'), 'v1');
    assert.deepEqual(await versionedGenerations.json(), { items: [], next_cursor: null });

    // The runtime can probe the same managed object with GET and HEAD. Verify
    // both methods receive a real, deterministic image response; HEAD must
    // preserve the GET representation headers without sending the body.
    const objectUrl = `${origin}/v1/objects/deterministic-contract-fixture`;
    const objectGet = await fetch(objectUrl);
    assert.equal(objectGet.status, 200);
    assert.equal(objectGet.headers.get('content-type'), 'image/jpeg');
    const objectBytes = Buffer.from(await objectGet.arrayBuffer());
    assert.ok(objectBytes.length > 0);
    assert.equal(Number(objectGet.headers.get('content-length')), objectBytes.length);
    const objectHead = await fetch(objectUrl, { method: 'HEAD' });
    assert.equal(objectHead.status, 200);
    assert.equal(objectHead.headers.get('content-type'), 'image/jpeg');
    assert.equal(objectHead.headers.get('content-length'), String(objectBytes.length));
    assert.equal((await objectHead.arrayBuffer()).byteLength, 0);

    const projectChat = await fetch(`${origin}/projects/demo-project/chat`);
    assert.equal(projectChat.status, 200);
    assert.deepEqual(await projectChat.json(), {
      project_id: 'demo-project',
      scope_key: 'project:demo-project',
      revision: 0,
      selected_session_id: null,
      sessions: [],
      draft: { text: '', revision: 0, queued_messages: [] },
    });
    const savedProjectDraft = await fetch(`${origin}/projects/demo-project/chat/draft`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expected_revision: 0, text: '', queued_messages: [] }),
    });
    assert.equal(savedProjectDraft.status, 200);
    assert.equal((await savedProjectDraft.json()).draft.revision, 1);
    const staleProjectDraft = await fetch(`${origin}/projects/demo-project/chat/draft`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expected_revision: 0, text: 'stale', queued_messages: [] }),
    });
    assert.equal(staleProjectDraft.status, 409);
    const otherProjectChat = await fetch(`${origin}/projects/other-project/chat`);
    assert.equal(otherProjectChat.status, 404);
    const acpConnect = await fetch(`${origin}/connect`, { method: 'POST', body: '{}' });
    assert.equal(acpConnect.status, 200);
    assert.deepEqual(await acpConnect.json(), { connection_id: 'local-test-connection', initialize: {} });
    const acpSessionList = await fetch(`${origin}/local-test-connection/rpc`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ method: 'session/list', params: {} }),
    });
    assert.equal(acpSessionList.status, 200);
    assert.deepEqual(await acpSessionList.json(), { result: { sessions: [] } });
    const acpPrompt = await fetch(`${origin}/local-test-connection/rpc`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ method: 'session/prompt', params: {} }),
    });
    assert.equal(acpPrompt.status, 404);

    const timelineUrl = `${origin}/projects/demo-project/timelines/demo-timeline`;
    const pristine = createTimelineFixtures({ assetSrcBaseUrl: origin });
    const initialTimeline = await (await fetch(timelineUrl)).json();
    const mutatedConfig = {
      ...initialTimeline.config,
      app: { leaked_from_previous_test: true },
      output: { ...initialTimeline.config.output, fps: 12 },
      clips: [{ id: 'mutated-only', track: 'V1', at: 99, clipType: 'text', hold: 1 }],
    };
    const mutatedRegistry = {
      assets: {
        ...initialTimeline.registry.assets,
        'mutated-only': { file: 'mutated.bin', type: 'application/octet-stream' },
      },
    };
    const mutation = await fetch(`${timelineUrl}/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        config: mutatedConfig,
        registry: mutatedRegistry,
        expected_version: initialTimeline.config_version,
      }),
    });
    assert.equal(mutation.status, 200);
    const mutated = await mutation.json();
    assert.deepEqual(mutated.config, mutatedConfig);
    assert.ok(mutated.registry.assets['mutated-only']);

    const firstResetResponse = await fetch(`${origin}/__test/reset`, { method: 'POST' });
    assert.equal(firstResetResponse.status, 200);
    assert.equal(firstResetResponse.headers.get('X-Astrid-Bridge-Version'), 'v1');
    const firstReset = await firstResetResponse.json();
    assert.equal(firstReset.reset, true);
    assert.ok(firstReset.config_version > mutated.config_version);
    assert.deepEqual(firstReset.config, pristine.config);
    assert.deepEqual(firstReset.registry, pristine.registry);
    assert.equal(firstReset.config.app, undefined);
    assert.equal(firstReset.registry.assets['mutated-only'], undefined);

    const publicAfterReset = await (await fetch(timelineUrl)).json();
    assert.equal(publicAfterReset.config_version, firstReset.config_version);
    assert.deepEqual(publicAfterReset.config, pristine.config);
    assert.deepEqual(publicAfterReset.registry, pristine.registry);

    const secondResetResponse = await fetch(`${origin}/__test/reset`, { method: 'POST' });
    assert.equal(secondResetResponse.status, 200);
    const secondReset = await secondResetResponse.json();
    assert.equal(secondReset.config_version, firstReset.config_version + 1);
    assert.deepEqual(secondReset.config, pristine.config);
    assert.deepEqual(secondReset.registry, pristine.registry);

    // The audio-reactive proof is a separate timeline state. Mutating it must
    // not leak into the ordinary demo timeline, and the same hard reset must
    // restore both states atomically.
    const audioTimelineUrl = `${origin}/projects/demo-project/timelines/${AUDIO_REACTIVE_FIXTURE_TIMELINE_ID}`;
    const audioPristine = createAudioReactiveColourFixtures({ assetSrcBaseUrl: origin });
    const audioInitial = await (await fetch(audioTimelineUrl)).json();
    assert.deepEqual(audioInitial.config, audioPristine.config);
    assert.deepEqual(audioInitial.registry, audioPristine.registry);
    assert.equal(audioInitial.config.output.fps, 30);
    assert.deepEqual(audioInitial.shot_composition, audioPristine.shotComposition);
    assert.equal(audioInitial.shot_composition.occurrences[0].at_ms, 0);
    assert.equal(audioInitial.shot_composition.shot_revisions[0].internal_timeline_revision.timeline.clips[0].params.initialColor, '#000000');
    const audioBytes = await readFile(new URL('../../../public/audio-reactive-colour-tone.wav', import.meta.url));
    const audioDigest = `sha256:${createHash('sha256').update(audioBytes).digest('hex')}`;
    assert.equal(audioInitial.shot_composition.shot_revisions[0].assets[0].digest, audioDigest);
    assert.equal(audioInitial.shot_composition.shot_revisions[0].audio.digest, audioDigest);
    assert.deepEqual(
      audioInitial.config.clips[0].params.events.map((event) => event.frame),
      [2, 4],
    );
    const audioMutation = await fetch(`${audioTimelineUrl}/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        config: { ...audioInitial.config, clips: [] },
        expected_version: audioInitial.config_version,
      }),
    });
    assert.equal(audioMutation.status, 200);
    const defaultAfterAudioMutation = await (await fetch(timelineUrl)).json();
    assert.deepEqual(defaultAfterAudioMutation.config, pristine.config);

    const audioResetResponse = await fetch(`${origin}/__test/reset`, { method: 'POST' });
    assert.equal(audioResetResponse.status, 200);
    const audioAfterReset = await (await fetch(audioTimelineUrl)).json();
    assert.deepEqual(audioAfterReset.config, audioPristine.config);
    assert.deepEqual(audioAfterReset.registry, audioPristine.registry);
    assert.deepEqual(audioAfterReset.shot_composition, audioPristine.shotComposition);

    const offsetTimelineUrl = `${origin}/projects/demo-project/timelines/${AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID}`;
    const offsetPristine = createOffsetAudioReactiveColourFixtures({ assetSrcBaseUrl: origin });
    const offsetInitial = await (await fetch(offsetTimelineUrl)).json();
    assert.deepEqual(offsetInitial.config, offsetPristine.config);
    assert.deepEqual(offsetInitial.registry, offsetPristine.registry);
    assert.deepEqual(offsetInitial.shot_composition, offsetPristine.shotComposition);
    assert.notEqual(offsetInitial.shot_composition.project.document_id, audioInitial.shot_composition.project.document_id);
    assert.notEqual(offsetInitial.shot_composition.primary_timeline.head.revision_id, audioInitial.shot_composition.primary_timeline.head.revision_id);
    assert.equal(offsetInitial.shot_composition.occurrences[0].at_ms, AUDIO_REACTIVE_OFFSET_START_FRAME * (1000 / 30));
    assert.equal(offsetInitial.shot_composition.shot_revisions[0].internal_timeline_revision.timeline.clips[0].params.initialColor, '#102030');
    assert.equal(offsetInitial.config.clips[0].at, AUDIO_REACTIVE_OFFSET_START_FRAME / 30);
    assert.equal(offsetInitial.config.clips[0].hold, 0.6);
    assert.equal(offsetInitial.config.clips[0].params.initialColor, '#102030');
    assert.deepEqual(
      offsetInitial.config.clips[0].params.events.map((event) => event.frame),
      [2, 4],
    );
  } finally {
    child.kill('SIGTERM');
    await once(child, 'exit');
  }
});
