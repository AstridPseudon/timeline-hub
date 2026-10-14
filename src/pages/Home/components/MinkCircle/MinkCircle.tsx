import loopUrl from './astrid-minks-loop.webp';
import stillUrl from './astrid-minks-still.png';

/** The original transparent circle loop, sized for the home loading mark. */
export function MinkCircle({ reducedMotion }: { reducedMotion: boolean }) {
  return <img
    data-astrid-mink-circle
    src={reducedMotion ? stillUrl : loopUrl}
    width={96}
    height={96}
    alt=""
    aria-hidden="true"
    decoding="async"
    style={{ imageRendering: 'pixelated' }}
  />;
}
