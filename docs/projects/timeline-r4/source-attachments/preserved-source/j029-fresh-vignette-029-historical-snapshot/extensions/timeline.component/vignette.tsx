import * as React from 'react';
import { useId } from 'react';

type Rect = { x: number; y: number; width: number; height: number };
type ModifierContext = {
  bounds: { status: string; rect?: Rect };
};
type ModifierProps = {
  instanceId: string;
  params: unknown;
  context: ModifierContext;
  children: React.ReactNode;
};
type ComponentDescriptor = {
  point: string;
  id: string;
  kind: string;
  hosts: string[];
  bounds?: string;
  alpha?: string;
  support?: string;
};
type ModifierRegistration = {
  kind: 'modifier';
  element: string;
  hosts: string[];
  bounds: 'preserve' | 'unknown';
  alpha: 'preserve';
  support: 'preserve';
  Component: React.ComponentType<ModifierProps>;
  resolveParams: (params: unknown, context: ModifierContext) => { strength: number };
};
type ThemeApiHost = {
  declareModifier(registration: ModifierRegistration): unknown;
};

function resolveParams(params: unknown, _context: ModifierContext): { strength: number } {
  if (params === null || typeof params !== 'object' || Array.isArray(params)) {
    throw new TypeError('vignette params must be an object');
  }
  const values = params as Record<string, unknown>;
  if (Object.keys(values).some((key) => key !== 'strength') || !Object.hasOwn(values, 'strength')) {
    throw new TypeError('vignette accepts exactly one required parameter: strength');
  }
  const strength = values.strength;
  if (typeof strength !== 'number' || !Number.isFinite(strength) || strength < 0 || strength > 1) {
    throw new TypeError('vignette strength must be a finite number from 0 through 1');
  }
  return { strength };
}

function Vignette({ params, context, children }: ModifierProps): React.ReactNode {
  const rawId = useId();
  const filterId = `fresh-vignette-${rawId.replace(/[^a-zA-Z0-9_-]/g, '')}`;
  const { strength } = resolveParams(params, context);
  if (strength === 0) return children;

  const rect = context.bounds.status === 'known' ? context.bounds.rect : undefined;
  if (
    !rect ||
    ![rect.x, rect.y, rect.width, rect.height].every(Number.isFinite) ||
    rect.width <= 0 ||
    rect.height <= 0
  ) {
    throw new Error('vignette requires known, finite, positive target bounds');
  }

  const edgePercent = (1 - strength) * 100;
  const imageSvg =
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">` +
    `<defs><radialGradient id="falloff" cx="50%" cy="50%" r="50%">` +
    `<stop offset="50%" stop-color="rgb(100% 100% 100%)"/>` +
    `<stop offset="100%" stop-color="rgb(${edgePercent}% ${edgePercent}% ${edgePercent}%)"/>` +
    `</radialGradient></defs><rect width="100" height="100" fill="url(#falloff)"/></svg>`;
  const imageHref = `data:image/svg+xml,${encodeURIComponent(imageSvg)}`;

  return (
    <div style={{ position: 'absolute', inset: 0, filter: `url(#${filterId})` }}>
      <svg aria-hidden="true" focusable="false" width="0" height="0">
        <defs>
          <filter
            id={filterId}
            x={rect.x}
            y={rect.y}
            width={rect.width}
            height={rect.height}
            filterUnits="userSpaceOnUse"
            primitiveUnits="userSpaceOnUse"
            colorInterpolationFilters="sRGB"
          >
            <feImage
              href={imageHref}
              x={rect.x}
              y={rect.y}
              width={rect.width}
              height={rect.height}
              preserveAspectRatio="none"
              result="attenuation"
            />
            <feComposite
              in="SourceGraphic"
              in2="attenuation"
              operator="arithmetic"
              k1={1}
              k2={0}
              k3={0}
              k4={0}
            />
          </filter>
        </defs>
      </svg>
      {children}
    </div>
  );
}

export function bindVignette(host: ThemeApiHost, declaration: ComponentDescriptor): unknown {
  if (declaration.point !== 'timeline.component' || declaration.id !== 'fresh_vignette_029.vignette') {
    throw new TypeError('unexpected vignette component identity');
  }
  if (declaration.kind !== 'modifier') throw new TypeError('vignette must be a modifier');
  if (
    declaration.hosts.length !== 2 ||
    !declaration.hosts.includes('composition') ||
    !declaration.hosts.includes('app')
  ) {
    throw new TypeError('vignette hosts must be composition and app');
  }
  if (declaration.bounds !== undefined && declaration.bounds !== 'preserve') {
    throw new TypeError('vignette only supports preserved output bounds');
  }
  if (declaration.alpha !== 'preserve' || declaration.support !== 'preserve') {
    throw new TypeError('vignette must preserve alpha and support');
  }

  return host.declareModifier({
    kind: 'modifier',
    element: `${declaration.point}/${declaration.id}`,
    hosts: declaration.hosts,
    bounds: declaration.bounds === undefined ? 'unknown' : 'preserve',
    alpha: 'preserve',
    support: 'preserve',
    Component: Vignette,
    resolveParams,
  });
}
