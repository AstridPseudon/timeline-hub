import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { releaseBootLayerWhenReady } from '@/app/bootLayer.ts';

const BOOT = '<div class="boot-paper"></div><div class="boot-mink"><span class="boot-mink-flight-y"><span class="boot-mink-flight-x"><span class="boot-mink-wipe"><span class="boot-mink-unwipe"><span class="boot-mink-window"><span class="boot-mink-strip"></span></span></span></span></span></span><span class="boot-mink-ground"><span></span></span></div>';

function mountBoot(minkOpacity: string) {
  const boot = document.createElement('div');
  boot.id = 'boot';
  boot.innerHTML = BOOT;
  boot.querySelector<HTMLElement>('.boot-mink')!.style.opacity = minkOpacity;
  const root = document.createElement('div');
  root.id = 'root';
  document.body.append(boot, root);
  return { boot, root };
}

const settle = () => new Promise((resolve) => setTimeout(resolve, 0));

describe('releaseBootLayerWhenReady', () => {
  beforeEach(() => {
    vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => {
      callback(0);
      return 0;
    });
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    document.body.replaceChildren();
  });

  it('waits for the first real frame and any hold, then fades out where no logo waits', async () => {
    const { boot, root } = mountBoot('1');
    releaseBootLayerWhenReady(root);
    const page = document.createElement('main');
    const hold = document.createElement('span');
    hold.setAttribute('data-boot-hold', '');
    page.append(hold);
    root.append(page);
    await settle();
    expect(boot.className).toBe('');

    hold.remove();
    await settle();
    expect(boot.classList.contains('boot-done')).toBe(true);
  });

  it('runs the showing mink home, its head landing on the logo, which waits hidden for it', async () => {
    const { boot, root } = mountBoot('1');
    const logo = document.createElement('img');
    logo.setAttribute('data-boot-mink-target', '');
    logo.getBoundingClientRect = () => DOMRect.fromRect({ x: 24, y: 17, width: 30, height: 30 });
    boot.querySelector<HTMLElement>('.boot-mink-flight-x')!.getBoundingClientRect = () => DOMRect.fromRect({ x: 600, y: 300, width: 90, height: 49 });
    root.append(logo);
    releaseBootLayerWhenReady(root);
    await settle();

    expect(boot.classList.contains('boot-flying')).toBe(true);
    expect(logo.style.opacity).toBe('0');
    // No WAAPI here, so the run holds frame 0: its eye (70, 14.5 sprite px) lands on the logo's
    // eye (10, 5 of 16), the head drawn at 1.45 sprite px per logo px.
    const px = 90 / 81;
    const logoPx = 30 / 16;
    const scale = logoPx / (1.45 * px);
    const [, dx, s] = /translateX\((-?[\d.]+)px\) scale\(([\d.]+)\)/.exec(boot.querySelector<HTMLElement>('.boot-mink-flight-x')!.style.transform)!;
    const [, dy] = /translateY\((-?[\d.]+)px\)/.exec(boot.querySelector<HTMLElement>('.boot-mink-flight-y')!.style.transform)!;
    expect(Number(s)).toBeCloseTo(scale, 4);
    expect(600 + 45 + Number(dx) + scale * (70 * px - 45)).toBeCloseTo(24 + 10 * logoPx, 3);
    expect(300 + 24.5 + Number(dy) + scale * (14.5 * px - 24.5)).toBeCloseTo(17 + 5 * logoPx, 3);
    // The body wipe: the masked layer travels up the 30deg gradient, its content back down.
    const wipe = boot.querySelector<HTMLElement>('.boot-mink-wipe')!.style.transform;
    const unwipe = boot.querySelector<HTMLElement>('.boot-mink-unwipe')!.style.transform;
    const [, wx, wy] = /translate\((-?[\d.]+)px, (-?[\d.]+)px\)/.exec(wipe)!;
    const [, ux, uy] = /translate\((-?[\d.]+)px, (-?[\d.]+)px\)/.exec(unwipe)!;
    expect(Number(wx)).toBeGreaterThan(0);
    expect(Number(wy)).toBeLessThan(0);
    expect(Number(ux)).toBeCloseTo(-Number(wx), 3);
    expect(Number(uy)).toBeCloseTo(-Number(wy), 3);
  });

  it('skips the flight when the mink never appeared (a fast load)', async () => {
    const { boot, root } = mountBoot('0');
    const logo = document.createElement('img');
    logo.setAttribute('data-boot-mink-target', '');
    root.append(logo);
    releaseBootLayerWhenReady(root);
    await settle();

    expect(boot.classList.contains('boot-done')).toBe(true);
    expect(boot.classList.contains('boot-flying')).toBe(false);
    expect(logo.style.opacity).toBe('');
  });
});
