import { useEffect, useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { Input } from '@/shared/components/ui/input.tsx';
import { Textarea } from '@/shared/components/ui/textarea.tsx';
import { getRegisteredClipTypeDescriptor, getSequenceDescriptorParams } from '@/tools/video-editor/clip-types/runtime.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from '@/tools/video-editor/commands/clipParamsGesture.ts';
import type { ClipParamsCapturePort } from '@/tools/video-editor/commands/clipParamsGesture.ts';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import type { AvailableSequenceMetadata } from '@/tools/video-editor/sequences/registry.ts';
import type { ResolvedTimelineConfig } from '@/tools/video-editor/types/index.ts';
import { getAssetDisplayReference } from '@/tools/video-editor/lib/asset-registry.ts';

type SequenceParamEditorProps = {
  clipType?: string;
  metadata?: AvailableSequenceMetadata;
  params: Record<string, unknown> | undefined;
  registry: ResolvedTimelineConfig['registry'];
  hideEmptyState?: boolean;
  onChange: (params: Record<string, unknown>) => void;
  /** Native discrete params ingress. Omit for detached presentation-only stories. */
  clipParamsPort?: ClipParamsCapturePort;
  current?: TimelineData;
  clipId?: string;
};

const PARAMS_WITH_TEXTAREA = new Set(['subtitle', 'caption', 'detail', 'action', 'note']);

const asAssetKeys = (value: unknown): string[] => {
  if (!Array.isArray(value)) return [];
  return value.filter((item): item is string => typeof item === 'string');
};

type AssetKeyCount = {
  key: string;
  count: number;
};

const countAssetKeys = (keys: readonly string[]): AssetKeyCount[] => {
  const counts = new Map<string, number>();
  const orderedKeys: string[] = [];
  for (const key of keys) {
    if (!counts.has(key)) {
      orderedKeys.push(key);
      counts.set(key, 0);
    }
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return orderedKeys.map((key) => ({ key, count: counts.get(key) ?? 0 }));
};

const setParam = (
  current: Record<string, unknown> | undefined,
  key: string,
  value: unknown,
): Record<string, unknown> => ({
  ...(current ?? {}),
  [key]: value,
});

const removeParam = (current: Record<string, unknown> | undefined, key: string) => {
  const next = { ...(current ?? {}) };
  delete next[key];
  return next;
};

const validateSchemaValue = (value: unknown, schemaValue: unknown, path: string): string | null => {
  if (!schemaValue || typeof schemaValue !== 'object' || Array.isArray(schemaValue)) return null;
  const schema = schemaValue as Record<string, unknown>;
  const type = schema.type;
  if (type === 'array') {
    if (!Array.isArray(value)) return `${path} must be an array.`;
    if (typeof schema.minItems === 'number' && value.length < schema.minItems) return `${path} needs at least ${schema.minItems} item(s).`;
    if (schema.items) {
      for (let index = 0; index < value.length; index++) {
        const error = validateSchemaValue(value[index], schema.items, `${path}[${index}]`);
        if (error) return error;
      }
    }
  } else if (type === 'object') {
    if (!value || typeof value !== 'object' || Array.isArray(value)) return `${path} must be an object.`;
    const object = value as Record<string, unknown>;
    const required = Array.isArray(schema.required) ? schema.required : [];
    for (const key of required) if (typeof key === 'string' && !(key in object)) return `${path}.${key} is required.`;
    const properties = schema.properties && typeof schema.properties === 'object'
      ? schema.properties as Record<string, unknown>
      : {};
    if (schema.additionalProperties === false) {
      const extra = Object.keys(object).find((key) => !(key in properties));
      if (extra) return `${path}.${extra} is not allowed.`;
    }
    for (const [key, child] of Object.entries(object)) {
      if (properties[key]) {
        const error = validateSchemaValue(child, properties[key], `${path}.${key}`);
        if (error) return error;
      }
    }
  } else {
    if (type === 'number' && (typeof value !== 'number' || !Number.isFinite(value))) return `${path} must be a finite number.`;
    if (type === 'string' && typeof value !== 'string') return `${path} must be a string.`;
    if (Array.isArray(schema.enum) && !schema.enum.includes(value)) return `${path} must be one of the listed values.`;
    if (typeof value === 'number') {
      if (typeof schema.minimum === 'number' && value < schema.minimum) return `${path} is below the allowed minimum.`;
      if (typeof schema.maximum === 'number' && value > schema.maximum) return `${path} is above the allowed maximum.`;
      if (typeof schema.exclusiveMinimum === 'number' && value <= schema.exclusiveMinimum) return `${path} must be greater than ${schema.exclusiveMinimum}.`;
    }
  }
  return null;
};

function JsonParamField({
  param,
  value,
  onCommit,
  onClear,
  clearDisabled = false,
}: {
  param: NonNullable<ReturnType<typeof getSequenceDescriptorParams>[number]>;
  value: unknown;
  onCommit: (value: unknown) => void;
  onClear: () => void;
  clearDisabled?: boolean;
}) {
  const serialized = value === undefined ? '' : JSON.stringify(value, null, 2);
  const [draft, setDraft] = useState(serialized);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { setDraft(serialized); setError(null); }, [serialized]);

  return (
    <div className="space-y-2 rounded-lg border border-border/70 bg-background/60 p-3">
      <div>
        <div className="text-sm font-medium text-foreground">{param.label}{param.required ? ' *' : ''}</div>
        <div className="text-xs text-muted-foreground">{param.description}</div>
      </div>
      <Textarea
        aria-label={param.label}
        aria-invalid={Boolean(error)}
        value={draft}
        rows={Math.min(12, Math.max(4, draft.split('\n').length))}
        placeholder={param.key === 'sourceSegments'
          ? '[{"at":0,"sourceStart":0,"speed":1}]'
          : '[{"at":0,"x":0,"y":0,"width":1920,"height":1080,"opacity":1}]'}
        onChange={(event) => {
          const next = event.target.value;
          setDraft(next);
          try {
            const parsed: unknown = JSON.parse(next);
            const validationError = validateSchemaValue(parsed, param.jsonSchema, param.key);
            const rows = Array.isArray(parsed) ? parsed as Record<string, unknown>[] : [];
            if (!validationError && param.key === 'keyframes'
              && rows.some((row, index) => index > 0 && Number(row.at) <= Number(rows[index - 1]?.at))) {
              setError('Keyframe times must increase strictly.');
              return;
            }
            if (!validationError && param.key === 'sourceSegments'
              && (Number(rows[0]?.at) !== 0 || rows.some((row, index) => index > 0 && Number(row.at) <= Number(rows[index - 1]?.at)))) {
              setError('Source segments must start at 0 and increase strictly.');
              return;
            }
            if (validationError) {
              setError(validationError);
              return;
            }
            setError(null);
            onCommit(parsed);
          } catch {
            setError('Enter valid JSON before applying this value.');
          }
        }}
      />
      {error && <div role="alert" className="text-xs text-destructive">{error}</div>}
      {!param.required && value !== undefined && (
        <Button type="button" size="sm" variant="ghost" onClick={onClear} disabled={clearDisabled}>
          Clear
        </Button>
      )}
    </div>
  );
}

const parseAssetKeysInput = (
  value: string,
  registry: ResolvedTimelineConfig['registry'],
): string[] => (
  value
    .split(',')
    .map((item) => item.trim())
    .filter((item) => item.length > 0 && Object.prototype.hasOwnProperty.call(registry, item))
);

export function SequenceParamEditor({
  clipType,
  metadata,
  params,
  registry,
  hideEmptyState = false,
  onChange,
  clipParamsPort,
  current,
  clipId,
}: SequenceParamEditorProps) {
  const [discreteError, setDiscreteError] = useState<string | null>(null);
  const nativeContext = clipParamsPort !== undefined || current !== undefined || clipId !== undefined;
  const nativeAvailable = Boolean(clipParamsPort && current && clipId);

  const submitDiscrete = (key: string, value: unknown, clear = false): boolean => {
    if (!nativeContext) return false;
    if (!nativeAvailable || !clipParamsPort || !current || !clipId) {
      setDiscreteError('Native clip parameter editing is unavailable; the value was not changed.');
      return false;
    }
    try {
      const captured = captureClipParamsEdit(clipParamsPort, current, clipId);
      submitClipParamsEdit(captured, clear
        ? { values: {}, clear: [key] }
        : { values: { [key]: value as JSON }, clear: [] });
      setDiscreteError(null);
      return true;
    } catch (error) {
      setDiscreteError(error instanceof Error ? error.message : String(error));
      return false;
    }
  };
  const resolvedClipType = clipType ?? metadata?.clipType;
  const descriptor = resolvedClipType
    ? getRegisteredClipTypeDescriptor(resolvedClipType)
    : undefined;
  const descriptorParams = getSequenceDescriptorParams(descriptor);
  const sequenceParams = descriptorParams.length > 0 ? descriptorParams : (metadata?.params ?? []);
  const label = descriptor?.label ?? metadata?.label ?? resolvedClipType ?? 'Sequence';
  const description = descriptor?.description ?? metadata?.description ?? 'Sequence parameters.';

  if (sequenceParams.length === 0) {
    if (hideEmptyState) return null;
    return (
      <div className="rounded-xl border border-dashed border-amber-400/40 bg-amber-500/10 p-3 text-sm text-amber-100">
        This clip type does not expose editable sequence params in the current registry view.
      </div>
    );
  }

  return (
    <div className="space-y-3 rounded-xl border border-border bg-card/60 p-3">
      <div>
        <div className="text-sm font-medium text-foreground">{label}</div>
        <div className="text-xs text-muted-foreground">{description}</div>
      </div>
      {nativeContext && !nativeAvailable && (
        <div role="alert" className="text-xs text-muted-foreground">
          Native clip parameter editing is unavailable for this clip; discrete choices are disabled.
        </div>
      )}
      {discreteError && <div role="alert" className="text-xs text-destructive">{discreteError}</div>}

      {sequenceParams.map((param) => {
        const value = params?.[param.key] ?? param.defaultValue ?? (param.kind === 'asset-list' ? [] : '');

        if (param.kind === 'asset-list') {
          const keys = asAssetKeys(value);
          const assetKeyCounts = countAssetKeys(keys);
          const uniqueKeys = assetKeyCounts.map((entry) => entry.key);
          return (
            <div key={param.key} className="space-y-2 rounded-lg border border-border/70 bg-background/60 p-3">
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <div className="text-sm font-medium text-foreground">{param.label}</div>
                  <div className="text-xs text-muted-foreground">{param.description}</div>
                </div>
                {typeof param.maxItems === 'number' && (
                  <div className="shrink-0 text-right text-xs text-muted-foreground">
                    <div>{keys.length}/{param.maxItems} uses</div>
                    {uniqueKeys.length !== keys.length && (
                      <div>{uniqueKeys.length} asset{uniqueKeys.length === 1 ? '' : 's'}</div>
                    )}
                  </div>
                )}
              </div>
              <Input
                value={uniqueKeys.join(', ')}
                placeholder="asset-key-a, asset-key-b"
                disabled={nativeContext && !nativeAvailable}
                onChange={(event) => {
                  const nextKeys = parseAssetKeysInput(event.target.value, registry);
                  const limitedKeys = typeof param.maxItems === 'number' ? nextKeys.slice(0, param.maxItems) : nextKeys;
                  if (!submitDiscrete(param.key, limitedKeys)) {
                    if (!nativeContext) onChange(setParam(params, param.key, limitedKeys));
                  }
                }}
              />
              {keys.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {assetKeyCounts.map(({ key, count }) => (
                    <span
                      key={key}
                      className="max-w-full truncate rounded-md border border-border/70 bg-muted px-2 py-1 text-[11px] text-muted-foreground"
                      title={getAssetDisplayReference(registry[key], key)}
                    >
                      {key}{count > 1 ? ` x${count}` : ''}
                    </span>
                  ))}
                </div>
              )}
            </div>
          );
        }

        if (param.kind === 'json') {
          return <JsonParamField
            key={param.key}
            param={param}
            value={params?.[param.key] ?? param.defaultValue}
            onCommit={(nextValue) => onChange(setParam(params, param.key, nextValue))}
            clearDisabled={nativeContext && !nativeAvailable}
            onClear={() => {
              if (!submitDiscrete(param.key, undefined, true)) {
                if (!nativeContext) onChange(removeParam(params, param.key));
              }
            }}
          />;
        }

        const stringValue = typeof value === 'string' ? value : '';
        return (
          <div key={param.key} className="space-y-2 rounded-lg border border-border/70 bg-background/60 p-3">
            <div>
              <div className="text-sm font-medium text-foreground">
                {param.label}{param.required ? ' *' : ''}
              </div>
              <div className="text-xs text-muted-foreground">{param.description}</div>
            </div>
            {PARAMS_WITH_TEXTAREA.has(param.key) ? (
              <Textarea
                value={stringValue}
                rows={3}
                onChange={(event) => onChange(setParam(params, param.key, event.target.value))}
              />
            ) : (
              <Input
                value={stringValue}
                onChange={(event) => onChange(setParam(params, param.key, event.target.value))}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
