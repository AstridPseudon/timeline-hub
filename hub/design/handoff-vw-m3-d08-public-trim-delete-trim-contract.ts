import { computeMediaTrim } from '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/@banodoco/timeline-composition/dist/evaluation.js';
import type { TimelineClip } from '/home/user/work/wt/vw-m3-d08-public-trim-delete/src/tools/video-editor/types/index.ts';
type ExistingTrimSignature = (
  clip: Pick<TimelineClip, 'from' | 'to'>,
  fps: number,
) => { trimBefore: number; trimAfter?: number };
const existing: ExistingTrimSignature = computeMediaTrim;
const replacement: typeof computeMediaTrim = existing;
void replacement;
