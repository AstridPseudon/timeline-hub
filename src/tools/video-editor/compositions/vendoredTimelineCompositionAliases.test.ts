import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const WORKSPACE_ROOT = process.cwd();
const PACKAGE_ROOT = 'vendor/timeline-composition';
const THEME_API_PATH = 'vendor/timeline-composition/typescript/src/theme-api.ts';
const RUNTIME_ALIAS_CONFIGS = [
  'config/vite/vite.config.ts',
  'config/testing/vitest.config.ts',
  'config/testing/vitest.boundary.config.ts',
] as const;
const REGISTRY_FAMILIES = [
  {
    family: 'effects',
    generated: 'vendor/timeline-composition/typescript/src/effects.generated.ts',
    vendorRoot: 'vendor/banodoco-effects',
  },
  {
    family: 'animations',
    generated: 'vendor/timeline-composition/typescript/src/animations.generated.ts',
    vendorRoot: 'vendor/banodoco-animations',
  },
  {
    family: 'transitions',
    generated: 'vendor/timeline-composition/typescript/src/transitions.generated.ts',
    vendorRoot: 'vendor/banodoco-transitions',
  },
] as const;

function workspaceSource(relativePath: string): string {
  return readFileSync(path.join(WORKSPACE_ROOT, relativePath), 'utf8');
}

describe('vendored timeline-composition workspace aliases', () => {
  it('maps public type and runtime subpaths to the stable package surfaces', () => {
    const { exports } = JSON.parse(workspaceSource(`${PACKAGE_ROOT}/package.json`));
    for (const subpath of ['theme-api', 'evaluation', 'registry.generated']) {
      const target = `./typescript/src/${subpath}.ts`;
      for (const condition of ['types', 'remotion', 'import', 'require', 'default']) {
        expect(exports[`./${subpath}`][condition]).toBe(target);
      }
      expect(existsSync(path.join(WORKSPACE_ROOT, PACKAGE_ROOT, target))).toBe(true);
    }
    // Generated workspace imports are resolved by the host's runtime aliases;
    // the package does not promise a workspace-aliases declaration sidecar.
    const themeApi = workspaceSource(THEME_API_PATH);
    expect(themeApi).toContain("export {interpolateKeyframeInterval} from './lib/keyframe-easing'");
    expect(themeApi).toContain("export {motionCurveName, motionCurveProgress, motionCurveInverse} from './lib/motion-curves.generated'");
  });

  it.each(REGISTRY_FAMILIES)(
    'keeps generated $family exports and imports aligned with runtime aliases and vendored modules',
    ({ family, generated, vendorRoot }) => {
      const { exports } = JSON.parse(workspaceSource(`${PACKAGE_ROOT}/package.json`));
      expect(exports[`./typescript/src/${family}.generated`]).toBe(
        `./typescript/src/${family}.generated.ts`,
      );

      for (const configPath of RUNTIME_ALIAS_CONFIGS) {
        const alias = workspaceSource(configPath).match(new RegExp(
          `["']@workspace-${family}["']\\s*:\\s*path\\.resolve\\(\\s*(projectRoot|__dirname),\\s*["']([^"']+)["']`,
        ));
        expect(alias, `missing runtime alias in ${configPath}`).not.toBeNull();
        const configRoot = alias![1] === 'projectRoot'
          ? WORKSPACE_ROOT
          : path.dirname(path.join(WORKSPACE_ROOT, configPath));
        expect(path.resolve(configRoot, alias![2])).toBe(
          path.join(WORKSPACE_ROOT, vendorRoot),
        );
      }

      const generatedSource = workspaceSource(generated);
      const importPattern = new RegExp(
        `from ["']@workspace-${family}/([^"']+)["']`,
        'g',
      );
      const moduleSpecifiers = [...generatedSource.matchAll(importPattern)]
        .map((match) => match[1])
        .filter((specifier): specifier is string => specifier !== undefined);

      expect(moduleSpecifiers.length).toBeGreaterThan(0);
      for (const moduleSpecifier of moduleSpecifiers) {
        expect(
          existsSync(path.join(WORKSPACE_ROOT, vendorRoot, `${moduleSpecifier}.tsx`)),
          `missing vendored source for @workspace-${family}/${moduleSpecifier}`,
        ).toBe(true);
      }
    },
  );
});
