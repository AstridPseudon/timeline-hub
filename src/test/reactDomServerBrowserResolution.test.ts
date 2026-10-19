// @vitest-environment node
import { mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { build, type Plugin } from 'vite';
import { describe, expect, it } from 'vitest';
import { createReactDomAliases } from '../../config/vite/reactDomAliases';

const normalizedId = (id: string): string => path.resolve(id.replace(/^\0+/, '').split('?')[0]).replaceAll('\\', '/');

function collectOutputItems(output: unknown): Array<{ type?: string; modules?: Record<string, unknown>; code?: string }> {
  if (Array.isArray(output)) return output.flatMap(collectOutputItems);
  if (!output || typeof output !== 'object') return [];
  if ('type' in output) return [output as { type?: string; modules?: Record<string, unknown>; code?: string }];
  return Object.values(output).flatMap(collectOutputItems);
}

describe('React DOM browser server resolution', () => {
  it('bundles the browser server without Node streams and keeps React entries on the locked install', async () => {
    const nodeModulesRoot = await realpath(path.resolve(process.cwd(), 'node_modules'));
    const reactRoot = path.join(nodeModulesRoot, 'react');
    const reactDomRoot = path.join(nodeModulesRoot, 'react-dom');
    const reactPackage = JSON.parse(await readFile(path.join(reactRoot, 'package.json'), 'utf8')) as {
      version: string;
    };
    const reactDomPackage = JSON.parse(await readFile(path.join(reactDomRoot, 'package.json'), 'utf8')) as {
      version: string;
    };
    expect(reactPackage.version).toBe('18.3.1');
    expect(reactDomPackage.version).toBe('18.3.1');

    const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'react-dom-browser-resolution-'));
    try {
      const entryPath = path.join(tempRoot, 'entry.js');
      await writeFile(entryPath, [
        'import * as React from "react";',
        'import * as ReactDOM from "react-dom";',
        'import * as ReactDOMClient from "react-dom/client";',
        'import * as ReactDOMServer from "react-dom/server";',
        'import * as ReactDOMServerBrowser from "react-dom/server.browser";',
        'globalThis.__reactDomResolution = {React, ReactDOM, ReactDOMClient, ReactDOMServer, ReactDOMServerBrowser};',
      ].join('\n'));

      const aliases = [
        ...Object.entries(createReactDomAliases(nodeModulesRoot)).map(([find, replacement]) => ({ find, replacement })),
        { find: 'react', replacement: reactRoot },
      ];
      const resolved: Record<string, string | undefined> = {};
      const captureResolutions: Plugin = {
        name: 'capture-react-dom-browser-resolutions',
        async buildStart() {
          for (const source of [
            'react',
            'react-dom',
            'react-dom/client',
            'react-dom/server',
            'react-dom/server.browser',
          ]) {
            resolved[source] = (await this.resolve(source, entryPath, { skipSelf: true }))?.id;
          }
        },
      };

      const output = await build({
        configFile: false,
        root: tempRoot,
        cacheDir: path.join(tempRoot, 'vite-cache'),
        logLevel: 'silent',
        plugins: [captureResolutions],
        resolve: { alias: aliases, dedupe: ['react', 'react-dom'] },
        build: {
          write: false,
          emptyOutDir: false,
          minify: false,
          rollupOptions: { input: entryPath, treeshake: false },
        },
      });

      expect(normalizedId(resolved.react ?? '')).toBe(normalizedId(path.join(reactRoot, 'index.js')));
      expect(normalizedId(resolved['react-dom'] ?? '')).toBe(normalizedId(path.join(reactDomRoot, 'index.js')));
      expect(normalizedId(resolved['react-dom/client'] ?? '')).toBe(normalizedId(path.join(reactDomRoot, 'client.js')));
      const browserServerEntry = normalizedId(path.join(reactDomRoot, 'server.browser.js'));
      expect(normalizedId(resolved['react-dom/server'] ?? '')).toBe(browserServerEntry);
      expect(normalizedId(resolved['react-dom/server.browser'] ?? '')).toBe(browserServerEntry);

      const chunks = collectOutputItems(output).filter((item) => item.type === 'chunk');
      const moduleIds = chunks.flatMap((chunk) => Object.keys(chunk.modules ?? {}));
      const normalizedModules = moduleIds.map(normalizedId);
      const bundleCode = chunks.map((chunk) => chunk.code ?? '').join('\n');

      expect(normalizedModules).toContain(browserServerEntry);
      expect(normalizedModules).toContain(normalizedId(path.join(reactDomRoot, 'client.js')));
      expect(normalizedModules).toContain(normalizedId(path.join(reactDomRoot, 'index.js')));
      expect(normalizedModules.some((id) => id.includes('/react-dom/') && id.includes('.node.'))).toBe(false);
      expect(normalizedModules.some((id) => id === 'stream' || id.endsWith('/stream'))).toBe(false);
      expect(bundleCode).not.toMatch(/(?:from\s*|require\s*\()\s*["']stream["']/);
      const reactModules = normalizedModules.filter((id) => id.includes('/node_modules/react/'));
      expect(reactModules.length).toBeGreaterThan(0);
      expect(reactModules.every((id) => id.startsWith(normalizedId(reactRoot) + '/'))).toBe(true);
    } finally {
      await rm(tempRoot, { recursive: true, force: true });
    }
  });
});
