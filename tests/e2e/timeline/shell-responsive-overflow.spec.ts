import { expect, test, type Page } from "@playwright/test";
import { browserEvidencePath, openEditor, resetFakeRuntimeBaseline } from "./support";

/**
 * `markerLayerCapacity` is the host's layers-per-page budget: 6 from 640 px up, 3 below it
 * (`markerLayerCapacity` in TimelineExtensionOverlayHost.tsx). The fixture catalog contributes more
 * overlay layers than either budget, so every viewport has a second page to walk.
 */
const VIEWPORTS = [
  {
    name: "desktop",
    width: 1600,
    height: 1000,
    touch: false,
    markerLayerCapacity: 6,
    screenshot: "25-shell-desktop-node20.png",
  },
  {
    name: "tablet-portrait",
    width: 834,
    height: 1194,
    touch: true,
    markerLayerCapacity: 6,
    screenshot: "26-shell-tablet-portrait-node20.png",
  },
  {
    name: "phone",
    width: 420,
    height: 820,
    touch: true,
    markerLayerCapacity: 3,
    screenshot: "27-shell-phone-node20.png",
  },
] as const;

async function auditMarkerLayerPages(
  page: Page,
  capacity: number,
): Promise<{ total: number; keys: string[] }> {
  const legend = page.getByTestId("timeline-marker-layer-legend");
  await expect(legend).toBeVisible();
  // On touch the pager is one corner button that steps to the next page and wraps
  // ("Marker layers 1–3 of 11: show the next layers"); at a desk it has Next/Previous.
  const compact = await legend.evaluate((element) => element.tagName === "BUTTON");
  if (!compact) {
    // The first page shows exactly one budget of layers.
    await expect(legend).toContainText(new RegExp(`Layers 1[–-]${capacity}/`));
  }
  const next = legend.getByRole("button", { name: "Next marker layers" });
  const previous = legend.getByRole("button", {
    name: "Previous marker layers",
  });
  const keys = new Set<string>();
  let total = 0;

  for (let pageIndex = 0; pageIndex < 12; pageIndex += 1) {
    const label = compact
      ? (await legend.getAttribute("aria-label")) ?? ""
      : (await legend.textContent()) ?? "";
    const match = compact
      ? /Marker layers \d+[–-]\d+ of (\d+)/.exec(label)
      : /Layers \d+[–-]\d+\/(\d+)/.exec(label);
    expect(match, `unexpected marker pager label: ${label}`).not.toBeNull();
    total = Number(match![1]);

    const composition = await page.evaluate(() => {
      const layers = Array.from(
        document.querySelectorAll('[data-testid="timeline-marker-layer"]'),
      );
      const markers = Array.from(
        document.querySelectorAll("[data-marker-anchor-x]"),
      );
      const groups = new Map<
        string,
        Array<{ lane: string | null; offset: string | null }>
      >();
      for (const marker of markers) {
        const anchor = marker.getAttribute("data-marker-anchor-x") ?? "";
        const group = groups.get(anchor) ?? [];
        group.push({
          lane: marker.getAttribute("data-marker-layer-lane"),
          offset: marker.getAttribute("data-marker-visual-offset-x"),
        });
        groups.set(anchor, group);
      }
      return {
        keys: layers.map((layer) =>
          layer.getAttribute("data-marker-layer-key"),
        ),
        indexes: layers.map((layer) =>
          layer.getAttribute("data-marker-layer-index"),
        ),
        coincident: [...groups.values()]
          .filter((group) => group.length > 1)
          .map((group) => ({
            count: group.length,
            positions: new Set(
              group.map((entry) => `${entry.lane}:${entry.offset}`),
            ).size,
          })),
      };
    });

    expect(composition.keys.length).toBeGreaterThan(0);
    expect(new Set(composition.indexes).size).toBe(composition.indexes.length);
    for (const key of composition.keys) {
      expect(key).not.toBeNull();
      keys.add(key!);
    }
    for (const group of composition.coincident) {
      expect(group.positions, JSON.stringify(composition)).toBe(group.count);
    }

    if (compact) {
      const pageNumber = Number(await legend.getAttribute("data-marker-layer-page"));
      const pageCount = Number(await legend.getAttribute("data-marker-layer-page-count"));
      if (pageNumber + 1 >= pageCount) break;
      await legend.click();
      await expect(legend).toHaveAttribute("data-marker-layer-page", String(pageNumber + 1));
      continue;
    }
    if (await next.isDisabled()) break;
    const oldLabel = label;
    await next.click();
    await expect(legend).not.toHaveText(oldLabel);
  }

  expect(keys.size).toBe(total);
  if (compact) {
    // The last page's step wraps back to the first.
    await legend.click();
    await expect(legend).toHaveAttribute("data-marker-layer-page", "0");
  } else {
    while (!(await previous.isDisabled())) {
      await previous.click();
    }
  }
  return { total, keys: [...keys] };
}

for (const viewport of VIEWPORTS) {
  test.describe(viewport.name, () => {
    test.use({
      viewport: { width: viewport.width, height: viewport.height },
      ...(viewport.touch
        ? { hasTouch: true, isMobile: true, deviceScaleFactor: 2 }
        : {}),
    });

    test(`keeps composed editor shell inside the ${viewport.name} viewport`, async ({
      page,
    }, testInfo) => {
      test.setTimeout(120_000);
      await resetFakeRuntimeBaseline();
      await openEditor(page);

      const geometry = await page.evaluate(() => {
        const rect = (selector: string) => {
          const element = document.querySelector(selector);
          if (!element) return null;
          const box = element.getBoundingClientRect();
          return {
            x: Math.round(box.x),
            y: Math.round(box.y),
            width: Math.round(box.width),
            height: Math.round(box.height),
            right: Math.round(box.right),
            bottom: Math.round(box.bottom),
          };
        };
        return {
          viewport: { width: window.innerWidth, height: window.innerHeight },
          page: {
            bodyWidth: document.body.scrollWidth,
            documentWidth: document.documentElement.scrollWidth,
          },
          main: rect("main.grid"),
          toolbarNavigation: rect(
            '[data-testid="toolbar-navigation-controls"]',
          ),
          phoneTopRow: rect('[data-toolbar-layout="touch"]'),
          phonePlaybackRow: rect('[data-testid="touch-playback-row"]'),
          touchAgentBar: rect('[data-testid="touch-agent-bar"]'),
          removedModeUi: document.querySelectorAll(
            '[data-timeline-mode-switcher], [aria-label="Phone timeline mode bar"], [aria-label="Timeline mode switcher"]',
          ).length,
          markerPager: rect('[data-testid="timeline-marker-layer-legend"]'),
          sceneMarkersPanel: rect('[data-testid="scene-markers-panel"]'),
          editArea: rect(".timeline-canvas-edit-area"),
          preview: rect('[data-testid="video-editor-preview-surface"]'),
          selectors: Array.from(
            document.querySelectorAll(
              '[data-testid="editor-project-timeline-selectors"] [role="combobox"]',
            ),
          ).map((element) => {
            const box = element.getBoundingClientRect();
            return { left: Math.round(box.left), right: Math.round(box.right) };
          }),
          // The scene-markers extension panel's own controls (the panel itself is measured above).
          sceneMarkerControls: Array.from(
            document.querySelectorAll(
              'button[data-testid^="scene-markers-"], select[data-testid^="scene-markers-"], input[data-testid^="scene-markers-"]',
            ),
          ).map((element) => {
            const box = element.getBoundingClientRect();
            return {
              label:
                element.getAttribute("data-testid") ??
                element.getAttribute("aria-label") ??
                element.textContent?.trim() ??
                element.tagName,
              left: Math.round(box.left),
              top: Math.round(box.top),
              right: Math.round(box.right),
              bottom: Math.round(box.bottom),
            };
          }),
        };
      });

      expect(
        geometry.page.bodyWidth,
        JSON.stringify(geometry),
      ).toBeLessThanOrEqual(viewport.width);
      expect(
        geometry.page.documentWidth,
        JSON.stringify(geometry),
      ).toBeLessThanOrEqual(viewport.width);
      for (const region of [
        geometry.main,
        geometry.editArea,
        geometry.preview,
        geometry.markerPager,
      ]) {
        expect(region, JSON.stringify(geometry)).not.toBeNull();
        expect(region!.x, JSON.stringify(geometry)).toBeGreaterThanOrEqual(0);
        expect(region!.right, JSON.stringify(geometry)).toBeLessThanOrEqual(
          viewport.width,
        );
      }
      // The scene-markers panel is a desk surface: its box lies inside the viewport width.
      if (!viewport.touch) {
        const panel = geometry.sceneMarkersPanel;
        expect(panel, JSON.stringify(geometry)).not.toBeNull();
        expect(panel!.x, JSON.stringify(geometry)).toBeGreaterThanOrEqual(0);
        expect(panel!.right, JSON.stringify(geometry)).toBeLessThanOrEqual(
          viewport.width,
        );
      }
      // Extension panels are a desk surface: the touch editor (phone and tablet) leaves that
      // work to the agent and draws no extension footer.
      if (viewport.touch) {
        expect(geometry.sceneMarkerControls, JSON.stringify(geometry)).toHaveLength(0);
      }
      for (const selector of geometry.selectors) {
        expect(selector.left, JSON.stringify(geometry)).toBeGreaterThanOrEqual(
          0,
        );
        expect(selector.right, JSON.stringify(geometry)).toBeLessThanOrEqual(
          viewport.width,
        );
      }

      // The touch editor's thumb bar (gallery, Text, Ask Astrid…) must fit the viewport width: a button
      // pushed off the right edge is a button nobody can tap.
      if (viewport.touch) {
        expect(geometry.touchAgentBar, JSON.stringify(geometry)).not.toBeNull();
        expect(geometry.touchAgentBar!.x, JSON.stringify(geometry)).toBeGreaterThanOrEqual(0);
        expect(geometry.touchAgentBar!.right, JSON.stringify(geometry)).toBeLessThanOrEqual(
          viewport.width,
        );
      }

      // The touch mode switcher is gone on every device.
      expect(geometry.removedModeUi, JSON.stringify(geometry)).toBe(0);
      if (viewport.name === "phone") {
        for (const row of [geometry.phoneTopRow, geometry.phonePlaybackRow]) {
          expect(row, JSON.stringify(geometry)).not.toBeNull();
          expect(row!.x, JSON.stringify(geometry)).toBeGreaterThanOrEqual(0);
          expect(row!.right, JSON.stringify(geometry)).toBeLessThanOrEqual(
            viewport.width,
          );
        }
      }

      // The status-bar chrome scrolls sideways inside its own box; whatever it holds stays
      // reachable inside the viewport once scrolled into view (the page-width checks above prove it
      // never widens the page).
      // Desk sizes only: the touch editor draws no extension footer (asserted above).
      if (!viewport.touch) {
        const panelControls = page.locator(
          '[data-testid="scene-markers-panel"] button, [data-testid="scene-markers-panel"] select, [data-testid="scene-markers-panel"] input',
        );
        expect(await panelControls.count()).toBeGreaterThan(0);
        for (const control of await panelControls.all()) {
          await control.scrollIntoViewIfNeeded();
          const box = await control.boundingBox();
          expect(box, "status-bar control has a box").not.toBeNull();
          expect(box!.x, JSON.stringify(box)).toBeGreaterThanOrEqual(0);
          // One CSS pixel of slack: a control scrolled flush to the box edge lands on a fractional px.
          expect(box!.x + box!.width, JSON.stringify(box)).toBeLessThanOrEqual(
            viewport.width + 1,
          );
          expect(box!.y, JSON.stringify(box)).toBeGreaterThanOrEqual(0);
          expect(box!.y + box!.height, JSON.stringify(box)).toBeLessThanOrEqual(
            viewport.height + 1,
          );
        }
      }

      const layerComposition = await auditMarkerLayerPages(
        page,
        viewport.markerLayerCapacity,
      );
      expect(layerComposition.total).toBeGreaterThan(
        viewport.markerLayerCapacity,
      );

      await page.screenshot({
        path: browserEvidencePath(testInfo, `chrome-acceptance/${viewport.screenshot}`),
        fullPage: true,
        animations: "disabled",
      });
    });
  });
}
