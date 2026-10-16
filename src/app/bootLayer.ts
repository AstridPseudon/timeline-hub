/**
 * index.html's boot layer: the page paper and Astrid's running mink, shown before the bundle
 * runs. index.html owns its look and CSS timings; this lifts it once the page's first real
 * frame has committed.
 *
 * Ready means #root has content and nothing in it holds the boot (`data-boot-hold`, which the
 * video editor renders while its workspace answers), so the paper dissolves straight into the
 * editor's frame rather than into an empty sky. The lift starts on the next frame, with that
 * frame already painted under it.
 *
 * With a visible mink and a logo to land on (`data-boot-mink-target`), the mink turns and runs
 * home to the logo while the paper dissolves, then trades places with it on the same pixels.
 * Otherwise (no logo, a fast load the mink never appeared for, or reduced motion) it runs on
 * and fades as the paper dissolves. Only transform and opacity move, so the compositor carries
 * it all on a busy main thread.
 */

/** The run home: long enough to read as travel, short enough not to keep anyone waiting. */
const FLIGHT_MS = 560;
/** Across first, then up: it runs left and rises into the corner, easing into place. */
const FLIGHT_X_EASE = 'cubic-bezier(0.4, 0, 0.2, 1)';
const FLIGHT_Y_EASE = 'cubic-bezier(0.6, 0, 0.3, 1)';
/** The landing crossfade with the real logo (matches #boot.boot-landed in index.html). */
const LANDING_MS = 160;

export function releaseBootLayerWhenReady(root: HTMLElement): void {
  const boot = document.getElementById('boot');
  if (!boot) return;
  let lifted = false;
  const ready = () => root.childElementCount > 0 && root.querySelector('[data-boot-hold]') === null;
  const lift = () => {
    if (lifted) return;
    lifted = true;
    observer.disconnect();
    requestAnimationFrame(() => {
      const target = root.querySelector<HTMLElement>('[data-boot-mink-target]');
      if (target && minkIsShowing(boot) && !prefersReducedMotion()) flyMinkHome(boot, target);
      else fadeOut(boot);
    });
  };
  const observer = new MutationObserver(() => {
    if (ready()) lift();
  });
  observer.observe(root, { childList: true, subtree: true, attributes: true, attributeFilter: ['data-boot-hold'] });
  if (ready()) lift();
}

function minkIsShowing(boot: HTMLElement): boolean {
  const mink = boot.querySelector<HTMLElement>('.boot-mink');
  return Boolean(mink) && Number(getComputedStyle(mink!).opacity) > 0.05;
}

function prefersReducedMotion(): boolean {
  return typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function fadeOut(boot: HTMLElement): void {
  const paper = boot.querySelector<HTMLElement>('.boot-paper');
  if (!paper) {
    boot.remove();
    return;
  }
  // The mink's own transitions bubble here too; only the paper's end removes the layer.
  boot.addEventListener('transitionend', (event) => {
    if (event.target === paper) boot.remove();
  });
  boot.classList.add('boot-done');
  // Reduced motion turns the transitions off, so no transitionend arrives.
  if (getComputedStyle(paper).transitionDuration === '0s') boot.remove();
}

function flyMinkHome(boot: HTMLElement, target: HTMLElement): void {
  const mink = boot.querySelector<HTMLElement>('.boot-mink');
  const flightY = boot.querySelector<HTMLElement>('.boot-mink-flight-y');
  const flightX = boot.querySelector<HTMLElement>('.boot-mink-flight-x');
  if (!mink || !flightY || !flightX) {
    fadeOut(boot);
    return;
  }
  // FLIP: from the running frame to the logo's box, centred on it, the frame as wide as the logo.
  const from = flightX.getBoundingClientRect();
  const to = target.getBoundingClientRect();
  const dx = to.left + to.width / 2 - (from.left + from.width / 2);
  const dy = to.top + to.height / 2 - (from.top + from.height / 2);
  const scale = to.width / from.width;

  const land = () => {
    target.style.transition = `opacity ${LANDING_MS}ms ease-out`;
    target.style.opacity = '';
    mink.addEventListener('transitionend', (event) => {
      if (event.target !== mink || event.propertyName !== 'opacity') return;
      boot.remove();
      target.style.transition = '';
    });
    boot.classList.add('boot-landed');
  };

  // The real logo waits, hidden, for the mink to arrive on its pixels.
  target.style.opacity = '0';
  flightY.style.transition = `transform ${FLIGHT_MS}ms ${FLIGHT_Y_EASE}`;
  flightX.style.transition = `transform ${FLIGHT_MS}ms ${FLIGHT_X_EASE}`;
  flightX.addEventListener('transitionend', (event) => {
    if (event.target === flightX && event.propertyName === 'transform') land();
  });
  boot.classList.add('boot-flying');
  flightY.style.transform = `translateY(${dy}px)`;
  flightX.style.transform = `translateX(${dx}px) scale(${scale})`;
  // Already home (no distance to travel): no transition will run, so land now.
  if (Math.abs(dx) < 0.5 && Math.abs(dy) < 0.5 && Math.abs(scale - 1) < 0.01) land();
}
