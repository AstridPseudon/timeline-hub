/** Host-admitted facts, never authored registry fields. No renderer in frame queries. */
import type {TimelineClip, AssetRegistryEntry} from './types';
import type {ModifierBounds} from './modifier-types';

export const VIDEO_INTERPRETATION = 'remotion-media/html-video/first-video/h264-yuv-v1' as const;
export const IMAGE_INTERPRETATION = 'remotion-image/jpeg-v1' as const;
export type MediaSceneEvidence = {
  version: 1; objectId: string; contentSha256: string; file: string;
  interpretation: typeof VIDEO_INTERPRETATION | typeof IMAGE_INTERPRETATION;
  stream: {index: number; codec: 'h264' | 'mjpeg'; pixelFormat: string; profile: string | null; level: string | null; sampleAspectRatio: '1:1'; width: number; height: number};
};
/** Component-owned facts at the supplied content clock. Omitted means unknown.
 * Regions use canvas coordinates; intrinsic motion is not final geometry or visibility. */
export type ComponentDiagnostics = {
  /** Intrinsic scalar names/units belong to the component, before outer geometry. */
  motion?: Readonly<Record<string, number>>;
  face?: ModifierBounds;
  mouth?: ModifierBounds;
  /** Declared text layout and minimum drawn font size in canvas pixels, not glyph alpha. */
  text?: {bounds: ModifierBounds; minPx?: number};
};
export type ComponentFrameSupport = {
  presence: 'present' | 'absent' | 'unknown'; bounds: ModifierBounds;
  /** Rectangular support filled by the intrinsic source, before layer opacity.
   * Text/glyph layout rectangles must use 'none'. */
  opaqueSupport: 'rect' | 'none' | 'unknown';
  diagnostics?: ComponentDiagnostics;
};
export type PreparedComponentCapability = {
  identity: string;
  /** Content clock after the component's speed remap. */
  frame: (contentFrame: number) => ComponentFrameSupport;
};
export type ComponentCapabilityContext = {
  clip: TimelineClip; fps: number; width: number; height: number;
  /** Renderer-selected entry. An own property with undefined means no entry resolved. */
  assetEntry?: Readonly<AssetRegistryEntry>;
  /** Current authenticated renderer closure, including actual fonts/materials. */
  rendererIdentity: string;
  fontDigests: Readonly<Record<string, string>>;
};
export type SceneCapableComponent = {
  prepareSceneCapability?: (context: ComponentCapabilityContext) => PreparedComponentCapability;
};
export type SceneCapabilities = {
  media?: Readonly<Record<string, MediaSceneEvidence>>;
  components?: Readonly<Record<string, PreparedComponentCapability>>;
};
const digest = (value: unknown): string | null => typeof value === 'string'
  && /^(?:sha256:)?[a-f0-9]{64}$/.test(value) ? value.replace(/^sha256:/, '') : null;
export const provenOpaqueMedia = (asset: AssetRegistryEntry | undefined, proof: MediaSceneEvidence | undefined): boolean => {
  if (!asset || !proof || proof.version !== 1 || ![VIDEO_INTERPRETATION, IMAGE_INTERPRETATION].includes(proof.interpretation)) return false;
  const content = digest(asset.content_sha256);
  const s = proof.stream;
  return content !== null && proof.objectId === 'sha256:' + content
    && proof.contentSha256 === content && proof.file === asset.file
    && ((proof.interpretation === VIDEO_INTERPRETATION && s?.codec === 'h264' && !asset.type?.startsWith('image')
      && ['Constrained Baseline', 'Baseline', 'Main', 'High'].includes(s.profile ?? '')
      && /^\d+$/.test(s.level ?? '') && Number(s.level) >= 10 && Number(s.level) <= 52
      && ['yuv420p', 'yuvj420p'].includes(s.pixelFormat))
      || (proof.interpretation === IMAGE_INTERPRETATION && s?.codec === 'mjpeg' && asset.type?.startsWith('image') === true))
    && ['yuv420p', 'yuvj420p', 'yuv422p', 'yuvj422p', 'yuv444p', 'yuvj444p'].includes(s.pixelFormat)
    && s.sampleAspectRatio === '1:1'
    && Number.isSafeInteger(s.index) && s.index >= 0
    && Number.isSafeInteger(s.width) && s.width > 0 && Number.isSafeInteger(s.height) && s.height > 0
    && asset.resolution === s.width + 'x' + s.height;
};
