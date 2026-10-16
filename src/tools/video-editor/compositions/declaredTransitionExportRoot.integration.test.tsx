// @vitest-environment jsdom
import {webcrypto} from 'node:crypto';
import {useContext, type PropsWithChildren} from 'react';
import {act, cleanup, render, renderHook, screen, waitFor} from '@testing-library/react';
import {afterEach, beforeEach, describe, expect, it, vi} from 'vitest';
import {flagshipLocalExtension} from '../examples/extensions/flagship-local';
import {createExtensionContext} from '../runtime/extensionContextFactory';
import {createTransitionRegistrationService} from '../runtime/transitionRegistrationService';
import {createTransitionRegistry} from '../transitions/registry/TransitionRegistry';
import {TransitionRegistryProvider, useTransitionRegistryContext} from '../transitions/registry/TransitionRegistryContext';
import type {TransitionRegistry} from '../transitions/registry/types';
import {VideoEditorRuntimeContext, type VideoEditorRuntimeContextValue} from '../contexts/VideoEditorRuntimeContext';
import type {AstridElementHost} from '../runtime/astrid-element-host';
import type {ExtensionDiagnosticsService} from '@/sdk/index';
import type {ResolvedTimelineConfig} from '../types';
import {useClientRender} from '../hooks/useClientRender';
import {TimelineRenderer, type TimelineRendererProps} from './TimelineRenderer';
import {PlayerClipEvaluationContext} from './PlayerClipSequence';

const host = vi.hoisted(() => ({
  worker: false, browser: true, cancel: vi.fn(), delay: vi.fn(() => 42), resume: vi.fn(),
  render: vi.fn(),
}));
vi.mock('remotion', () => ({
  AbsoluteFill: ({children, style}: PropsWithChildren<{style?: object}>) => <div style={style}>{children}</div>,
  Sequence: ({children}: PropsWithChildren) => <>{children}</>,
  Freeze: ({children}: PropsWithChildren) => <>{children}</>,
  useCurrentFrame: () => 45,
  useVideoConfig: () => ({fps: 30, width: 1280, height: 720, durationInFrames: 120}),
  useRemotionEnvironment: () => ({isRendering: host.worker, isClientSideRendering: host.browser}),
  delayRender: host.delay, continueRender: host.resume, cancelRender: host.cancel,
}));
vi.mock('@remotion/web-renderer', () => ({
  canRenderMediaOnWeb: async () => ({canRender: true, resolvedVideoCodec: 'h264'}),
  renderMediaOnWeb: host.render,
}));
vi.mock('@/shared/components/ui/toast.tsx', () => ({toast: {error: vi.fn(), success: vi.fn()}}));
vi.mock('./AudioAnalysisProvider.tsx', () => ({AudioAnalysisProvider: ({children}: PropsWithChildren) => <>{children}</>}));
vi.mock('./VisualClip.tsx', () => {
  const Probe = ({clip}: {clip: {id: string}}) => {
    const evaluation = useContext(PlayerClipEvaluationContext);
    return <div data-testid={`draw-${clip.id}`} data-opacity={evaluation?.layer?.transitionOpacity}
      data-frame={evaluation?.layer?.ownFrame} />;
  };
  return {VisualClip: Probe, VisualClipSequence: Probe};
});

const ID = 'com.reigh.flagship.transition.cross-fade';
const REVISION = 'sha256:1048af49b051ab1a1505b7d85707c4dc96aa2225a7bf38ff8f11b64077e7f1e7';
const elementHost: AstridElementHost = {
  descriptors: [], sequenceRegistry: {}, resolveComponent: () => undefined,
  resolveSequenceClipEntry: () => undefined, describeClipCapability: () => undefined,
};
const config = (): ResolvedTimelineConfig => ({
  output: {resolution: '1280x720', fps: 30, file: 'export.mp4'}, registry: {},
  tracks: [{id: 'V1', kind: 'visual', label: 'Picture'}],
  clips: [{id: 'out', track: 'V1', at: 0, hold: 2, clipType: 'media'},
    {id: 'in', track: 'V1', at: 2, hold: 2, clipType: 'media', transition: {type: ID, revision: REVISION, duration: 1},
      elementRef: {kind: 'transition', id: ID, packId: 'com.reigh.examples.flagship-local', revision: REVISION}}],
});
const disposals: Array<() => void> = [];
async function activate(registry: TransitionRegistry) {
  const transitions = createTransitionRegistrationService({extension: flagshipLocalExtension,
    transitionRegistry: registry, diagnosticsService: {report: vi.fn()} as unknown as ExtensionDiagnosticsService});
  const handle = await flagshipLocalExtension.activate!(createExtensionContext(
    flagshipLocalExtension, undefined, undefined, undefined, transitions));
  if (handle && typeof handle === 'object') disposals.push(() => handle.dispose());
}
async function standaloneSnapshot() {
  const registry = createTransitionRegistry();
  disposals.push(() => registry.dispose());
  await activate(registry);
  return registry;
}

beforeEach(() => {
  host.worker = false; host.browser = true; vi.clearAllMocks();
  vi.stubGlobal('crypto', webcrypto);
  vi.stubGlobal('VideoEncoder', class {});
  vi.stubGlobal('URL', {createObjectURL: vi.fn(() => 'blob:export')});
});
afterEach(() => {
  cleanup();
  for (const dispose of disposals.splice(0).reverse()) dispose();
  vi.unstubAllGlobals();
});

// The Web Renderer creates a separate root: deliberately render outside the editor wrapper.
async function renderDetached({composition, inputProps}: {
  composition: {component: typeof TimelineRenderer}; inputProps: TimelineRendererProps;
}) {
  const Component = composition.component;
  const view = render(<Component {...inputProps} />);
  await waitFor(() => {
    if (host.cancel.mock.calls.length) throw host.cancel.mock.calls[0][0];
    expect(screen.getByTestId('draw-in')).toHaveAttribute('data-opacity', '0.5');
  });
  expect(screen.getByTestId('draw-out')).toHaveAttribute('data-frame', '45');
  view.unmount();
  return new Blob(['export'], {type: 'video/mp4'});
}

async function clientExport(timeline = config(), binding: 'runtime' | 'provider' = 'runtime') {
  let registry!: TransitionRegistry;
  function CaptureRegistry() { registry = useTransitionRegistryContext().registry; return null; }
  const state = {setRenderStatus: vi.fn(), setRenderProgress: vi.fn(), setRenderLog: vi.fn(),
    setRenderDirty: vi.fn(), setRenderResult: vi.fn()};
  const runtime = {astridElementHost: elementHost,
    ...(binding === 'runtime' ? {getTransitionRegistrySnapshot: () => registry?.getSnapshot()} : {}),
  } as VideoEditorRuntimeContextValue;
  const wrapper = ({children}: PropsWithChildren) => <VideoEditorRuntimeContext.Provider value={runtime}>
    <TransitionRegistryProvider><CaptureRegistry />{binding === 'provider' ? children : null}</TransitionRegistryProvider>
    {binding === 'runtime' ? children : null}
  </VideoEditorRuntimeContext.Provider>;
  const hook = renderHook(() => useClientRender({resolvedConfig: timeline,
    metadata: {fps: 30, durationInFrames: 120, compositionWidth: 1280, compositionHeight: 720}, ...state}), {wrapper});
  await act(async () => activate(registry));
  return {registry, hook, state};
}

describe('declared transition binding across detached export roots', () => {
  it.each(['runtime', 'provider'] as const)('carries the public producer registration and exact %s host through useClientRender to a fresh browser render root', async binding => {
    host.render.mockImplementation(renderDetached);
    const {registry, hook, state} = await clientExport(config(), binding);
    const result = await hook.result.current();
    expect(result).toMatchObject({status: 'done'});
    const props = host.render.mock.calls[0][0].inputProps;
    expect(props.astridElementHost).toBe(elementHost);
    expect(props.transitionRegistrySnapshot).toBe(registry.getSnapshot());
    expect(props.transitionRegistrySnapshot.get(ID)).toMatchObject({
      provenance: 'bundled-extension', ownerExtensionId: 'com.reigh.examples.flagship-local',
      contributionId: 'flagship-transition-cross-fade', implementationRevision: REVISION,
      implementationResource: {implementation: {host: 'timeline-composition', id: 'cross-fade'}},
    });
    expect(host.cancel).not.toHaveBeenCalled();
    expect(host.delay).toHaveBeenCalled();
    expect(host.resume).toHaveBeenCalledWith(42);
    expect(state.setRenderStatus).toHaveBeenLastCalledWith('done');
  });

  it.each(['absent', 'stale'] as const)('refuses %s current producer registration through useClientRender', async problem => {
    host.render.mockImplementation(renderDetached);
    const {registry, hook, state} = await clientExport();
    act(() => {
      if (problem === 'absent') registry.unregister(ID);
      else registry.updateRecord(ID, rec => ({...rec,
        implementationResource: {...rec.implementationResource!, implementation: {host: 'timeline-composition', id: 'fade'}}}));
    });
    expect(await hook.result.current()).toMatchObject({status: 'error'});
    expect(host.cancel).toHaveBeenCalledWith(expect.objectContaining({code:
      problem === 'absent' ? 'transition/unknown-contribution' : 'transition/revision-mismatch'}));
    expect(state.setRenderDirty).not.toHaveBeenCalled();
    expect(state.setRenderStatus).toHaveBeenLastCalledWith('error');
  });

  it.each(['browser', 'native-worker'] as const)('binds the same exact snapshot into the standalone %s consumer', async route => {
    host.worker = route === 'native-worker'; host.browser = !host.worker;
    const registry = await standaloneSnapshot();
    await renderDetached({composition: {component: TimelineRenderer}, inputProps: {
      config: config(), astridElementHost: elementHost, transitionRegistrySnapshot: registry.getSnapshot()}});
    expect(host.cancel).not.toHaveBeenCalled();
    expect(host.resume).toHaveBeenCalledWith(42);
  });

  it.each(['absent', 'invalid', 'unsupported-host', 'blocked-route', 'stale-source', 'stale-pin', 'unknown-bounds'] as const)(
    'retains %s refusal at the native-worker root', async problem => {
      host.worker = true; host.browser = false;
      const registry = await standaloneSnapshot();
      const timeline = config();
      if (problem === 'absent') registry.unregister(ID);
      if (problem === 'invalid') registry.updateRecord(ID, rec => ({...rec, status: 'error', implementationResource: undefined}));
      if (problem === 'unsupported-host') vi.stubGlobal('crypto', {});
      if (problem === 'blocked-route') registry.updateRecord(ID, rec => ({...rec, renderability: {
        determinism: 'deterministic', capabilities: [{route: 'preview', status: 'supported', determinism: 'deterministic'}]}}));
      if (problem === 'stale-source') registry.updateRecord(ID, rec => ({...rec,
        implementationResource: {...rec.implementationResource!, implementation: {host: 'timeline-composition', id: 'fade'}}}));
      if (problem === 'stale-pin') timeline.clips[1].transition!.revision = 'sha256:' + '0'.repeat(64);
      if (problem === 'unknown-bounds') { delete timeline.clips[0].hold; timeline.clips[0].to = Infinity; }
      const codes = {'absent': 'transition/unknown-contribution', 'invalid': 'transition/inactive-contribution',
        'unsupported-host': 'transition/unsupported-host', 'blocked-route': 'transition/unsupported-route',
        'stale-source': 'transition/revision-mismatch', 'stale-pin': 'transition/reference-mismatch',
        'unknown-bounds': 'transition/invalid-span'};
      render(<TimelineRenderer config={timeline} astridElementHost={elementHost} transitionRegistrySnapshot={registry.getSnapshot()} />);
      await waitFor(() => expect(host.cancel).toHaveBeenCalledWith(expect.objectContaining({code: codes[problem]})));
      expect(screen.queryByTestId('draw-in')).not.toBeInTheDocument();
    });

  it('retains built-in precedence at a detached export root', async () => {
    const registry = await standaloneSnapshot();
    const timeline = config();
    timeline.clips[1].transition = {type: 'crossfade', duration: 1};
    delete timeline.clips[1].elementRef;
    const record = registry.getSnapshot().get(ID)!;
    registry.register({...record, transitionId: 'crossfade', status: 'error'});
    await renderDetached({composition: {component: TimelineRenderer}, inputProps: {
      config: timeline, astridElementHost: elementHost, transitionRegistrySnapshot: registry.getSnapshot()}});
    expect(host.cancel).not.toHaveBeenCalled();
  });
});
