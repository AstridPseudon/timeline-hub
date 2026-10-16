import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { releaseBootLayerWhenReady } from '@/app/bootLayer.ts';

const BOOT = '<div class="boot-paper"></div><div class="boot-mink"><span class="boot-mink-flight-y"><span class="boot-mink-flight-x"><span class="boot-mink-window"><span class="boot-mink-strip"></span></span></span></span><span class="boot-mink-ground"><span></span></span></div>';

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

  it('runs the showing mink home onto the logo, which waits hidden for it', async () => {
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
    expect(boot.querySelector<HTMLElement>('.boot-mink-flight-x')!.style.transform).toBe('translateX(-606px) scale(0.3333333333333333)');
    expect(boot.querySelector<HTMLElement>('.boot-mink-flight-y')!.style.transform).toBe('translateY(-292.5px)');
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
