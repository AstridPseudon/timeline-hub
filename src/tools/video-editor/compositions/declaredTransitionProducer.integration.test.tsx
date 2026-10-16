// @vitest-environment jsdom
import {webcrypto} from 'node:crypto';
import {act, renderHook, waitFor} from '@testing-library/react';
import {afterEach, beforeEach, describe, expect, it, vi} from 'vitest';
import {querySceneFrame} from '@banodoco/timeline-composition/evaluation';
import {defineExtension} from '@/sdk/index';
import {flagshipLocalExtension} from '@/tools/video-editor/examples/extensions/flagship-local';
import {createExtensionContext} from '@/tools/video-editor/runtime/extensionContextFactory';
import {normalizeExtensionRuntime} from '@/tools/video-editor/runtime/extensionSurface';
import {createTransitionRegistrationService} from '@/tools/video-editor/runtime/transitionRegistrationService';
import {createTransitionRegistry} from '@/tools/video-editor/transitions/registry/TransitionRegistry';
import type {ExtensionDiagnosticsService} from '@/sdk/index';
import type {ResolvedTimelineClip, TrackDefinition} from '../types/index.ts';
import {usePlayerTrackEvaluation} from './usePlayerTrackEvaluation';

const routeHost = vi.hoisted(() => ({
  worker: false,
  browser: false,
  delay: vi.fn(() => 42),
  resume: vi.fn(),
  cancel: vi.fn(),
}));

vi.mock('remotion', () => ({
  useRemotionEnvironment: () => ({
    isRendering: routeHost.worker,
    isClientSideRendering: routeHost.browser,
  }),
  delayRender: routeHost.delay,
  continueRender: routeHost.resume,
  cancelRender: routeHost.cancel,
}));

const OWNER = 'com.reigh.examples.flagship-local';
const CONTRIBUTION_ID = 'flagship-transition-cross-fade';
const TRANSITION_ID = 'com.reigh.flagship.transition.cross-fade';
const REVISION = 'sha256:1048af49b051ab1a1505b7d85707c4dc96aa2225a7bf38ff8f11b64077e7f1e7';
const track: TrackDefinition = {id: 'V1', kind: 'visual', label: 'Picture'};

async function activateFlagshipAgainstRegistry() {
  const registry = createTransitionRegistry();
  const diagnosticsService = {report: vi.fn()} as unknown as ExtensionDiagnosticsService;
  const transitionService = createTransitionRegistrationService({
    extension: flagshipLocalExtension,
    transitionRegistry: registry,
    diagnosticsService,
  });
  const context = createExtensionContext(
    flagshipLocalExtension,
    undefined,
    undefined,
    undefined,
    transitionService,
  );
  const dispose = await flagshipLocalExtension.activate!(context);
  return {registry, dispose};
}

function declaredClips(revision = REVISION): ResolvedTimelineClip[] {
  return [
    {id: 'out', track: 'V1', at: 0, hold: 2, clipType: 'media'},
    {
      id: 'in',
      track: 'V1',
      at: 2,
      hold: 2,
      clipType: 'media',
      transition: {type: TRANSITION_ID, revision, duration: 1},
      elementRef: {kind: 'transition', id: TRANSITION_ID, packId: OWNER, revision},
    },
  ];
}

beforeEach(() => {
  routeHost.worker = false;
  routeHost.browser = false;
  vi.clearAllMocks();
  vi.stubGlobal('crypto', webcrypto);
});

afterEach(() => vi.unstubAllGlobals());

describe('declared transition producer-to-Player/export path', () => {
  it('discovers and registers the real declaration, then uses the same admitted plan in preview and both export routes', async () => {
    const {registry, dispose} = await activateFlagshipAgainstRegistry();
    try {
      const record = registry.getSnapshot().get(TRANSITION_ID);
      expect(record).toMatchObject({
        transitionId: TRANSITION_ID,
        contributionId: CONTRIBUTION_ID,
        ownerExtensionId: OWNER,
        implementationResource: {
          owner: OWNER,
          id: CONTRIBUTION_ID,
          kind: 'transition',
          transitionId: TRANSITION_ID,
          implementation: {host: 'timeline-composition', id: 'cross-fade'},
          supportedParams: [],
          defaults: {},
        },
        implementationRevision: REVISION,
        status: 'active',
        renderability: {
          determinism: 'deterministic',
          capabilities: expect.arrayContaining([
            {route: 'preview', status: 'supported', determinism: 'deterministic'},
            {route: 'browser-export', status: 'supported', determinism: 'deterministic'},
            {route: 'worker-export', status: 'supported', determinism: 'deterministic'},
          ]),
        },
      });
      expect(Object.isFrozen(record!.implementationResource)).toBe(true);

      const discovered = normalizeExtensionRuntime([flagshipLocalExtension]).transitions
        .find((descriptor) => descriptor.transitionId === TRANSITION_ID);
      expect(discovered).toMatchObject({
        id: CONTRIBUTION_ID,
        extensionId: OWNER,
        implementationResource: record!.implementationResource,
        implementationRevision: REVISION,
      });

      const parity: Array<{plans: unknown; layers: unknown}> = [];
      for (const route of ['preview', 'browser-export', 'worker-export'] as const) {
        routeHost.browser = route === 'browser-export';
        routeHost.worker = route === 'worker-export';
        const clips = declaredClips();
        const {result, unmount} = renderHook(() =>
          usePlayerTrackEvaluation(track, clips, 30, 1280, 720, registry.getSnapshot()),
        );
        await waitFor(() => expect(result.current.status).toBe('ready'));
        if (result.current.status === 'ready') {
          const evaluation = result.current.evaluation;
          expect(evaluation.declarations[0]).toMatchObject({
            implementation: {host: 'timeline-composition', id: 'cross-fade'},
            contribution: {revision: REVISION, resource: record!.implementationResource},
            spec: {T: 30, kind: 'dissolve', align: 'end'},
          });
          expect(evaluation.legacyTiming.size).toBe(0);
          const layers = querySceneFrame(evaluation.scene, 45).layers
            .map((layer) => ({clipId: layer.clipId, ownFrame: layer.ownFrame, transitionOpacity: layer.transitionOpacity}));
          expect(layers).toEqual([
            {clipId: 'out', ownFrame: 45, transitionOpacity: 1},
            {clipId: 'in', ownFrame: 0, transitionOpacity: 0.5},
          ]);
          parity.push({plans: evaluation.scene.tracks[0].prepared.plans, layers});
        }
        unmount();
      }
      expect(parity).toHaveLength(3);
      expect(parity[1]).toEqual(parity[0]);
      expect(parity[2]).toEqual(parity[0]);
      expect(routeHost.delay).toHaveBeenCalledTimes(2);
      expect(routeHost.resume).toHaveBeenCalledTimes(2);
      expect(routeHost.cancel).not.toHaveBeenCalled();
    } finally {
      if (dispose && typeof dispose === 'object') act(() => dispose.dispose());
      registry.dispose();
    }
  });

  it('refuses a digest mismatch on the real export admission path and cancels the frame', async () => {
    const {registry, dispose} = await activateFlagshipAgainstRegistry();
    try {
      routeHost.browser = true;
      const wrongRevision = 'sha256:' + '0'.repeat(64);
      registry.updateRecord(TRANSITION_ID, (current) => ({
        ...current,
        implementationRevision: wrongRevision,
      }));
      const snapshot = registry.getSnapshot();
      const clips = declaredClips(wrongRevision);
      const {result} = renderHook(() => usePlayerTrackEvaluation(
        track,
        clips,
        30,
        1280,
        720,
        snapshot,
      ));
      await waitFor(() => expect(result.current.status).toBe('refused'));
      if (result.current.status === 'refused') {
        expect(result.current.error).toMatchObject({code: 'transition/revision-mismatch'});
      }
      expect(result.current).not.toHaveProperty('evaluation');
      expect(routeHost.cancel).toHaveBeenCalledWith(expect.objectContaining({code: 'transition/revision-mismatch'}));
    } finally {
      if (dispose && typeof dispose === 'object') act(() => dispose.dispose());
      registry.dispose();
    }
  });

  it.each([
    ['missing revision', {implementation: {host: 'timeline-composition', id: 'cross-fade'}, supportedParams: [], defaults: {}}],
    ['unsupported implementation', {implementation: {host: 'timeline-composition', id: 'zoom'}, supportedParams: [], defaults: {}, resourceRevision: REVISION}],
    ['unsupported parameters', {implementation: {host: 'timeline-composition', id: 'cross-fade'}, supportedParams: ['strength'], defaults: {strength: 0}, resourceRevision: REVISION}],
  ] as const)('refuses a malformed declared producer binding: %s', (_case, binding) => {
    const transitionId = `com.reigh.examples.invalid.${_case.replace(/ /g, '-')}`;
    const contribution = {
      id: 'invalid-transition',
      kind: 'transition',
      transitionId,
      label: 'Invalid Transition',
      ...binding,
    };
    const extension = defineExtension({manifest: {
      id: 'com.reigh.examples.invalid' as never,
      version: '1.0.0',
      label: 'Invalid Transition Fixture',
      contributions: [contribution as never],
    }});
    const registry = createTransitionRegistry();
    const diagnosticsService = {report: vi.fn()} as unknown as ExtensionDiagnosticsService;
    const service = createTransitionRegistrationService({
      extension,
      transitionRegistry: registry,
      diagnosticsService,
    });

    service.registerRenderer(transitionId, () => ({}));
    const registered = registry.getSnapshot().get(transitionId);
    expect(registered?.status).toBe('error');
    expect(registered).not.toHaveProperty('implementationResource');
    expect(registered).not.toHaveProperty('implementationRevision');
    expect(registered?.diagnostics?.some((diagnostic) => diagnostic.severity === 'error')).toBe(true);
    registry.dispose();
  });
});
