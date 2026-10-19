import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { realpathSync } from 'node:fs';
import { dirname, join } from 'node:path';

const execFileAsync = promisify(execFile);
const DEFAULT_OMP_COMMAND = 'omp';
const DEFAULT_BUN_COMMAND = 'bun';
const MODEL_ROLE_SETTING = 'modelRoles';

export type OmpModel = { id: string; name: string };
export type OmpSafeUsage = { limits: Array<{
  unit?: string; used?: number; limit?: number; remaining?: number; usedFraction?: number;
  remainingFraction?: number; durationMs?: number; resetsAt?: number; status?: 'ok' | 'warning' | 'exhausted' | 'unknown';
}> };
export type OmpProvider = { id: string; name: string; signedIn: boolean; models: OmpModel[]; usage?: OmpSafeUsage };
export type OmpModelCatalog = { providers: OmpProvider[]; currentModel: string | null };
type SafeUsageSnapshot = {
  reports: Array<{ provider: string; limits: OmpSafeUsage['limits'] }>;
  authenticatedProviders: string[];
};
export type OmpModelOptions = {
  command?: string;
  bunCommand?: string;
  cwd: string;
  profile?: string;
};

export class OmpModelSelectionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'OmpModelSelectionError';
  }
}

type JsonRecord = Record<string, unknown>;

function record(value: unknown): JsonRecord | null {
  return value !== null && typeof value === 'object' && !Array.isArray(value) ? value as JsonRecord : null;
}

function parseJson(text: string, description: string): unknown {
  try { return JSON.parse(text); }
  catch { throw new Error(`OMP ${description} returned invalid JSON`); }
}

async function runOmp(options: OmpModelOptions, args: string[]): Promise<string> {
  try {
    const result = await execFileAsync(options.command ?? DEFAULT_OMP_COMMAND, [
      ...(options.profile ? [`--profile=${options.profile}`] : []),
      ...args,
    ], { cwd: options.cwd, encoding: 'utf8', maxBuffer: 8 * 1024 * 1024 });
    return result.stdout;
  } catch {
    // OMP stderr may contain provider diagnostics or credential context. Never
    // include child output in a bridge error response.
    throw new Error('OMP model operation failed');
  }
}

function resolveOmpPackageRoot(command: string): string | null {
  const pathParts = (process.env.PATH ?? '').split(':');
  const executable = command.includes('/')
    ? command
    : pathParts.map(part => join(part, command)).find(path => {
      try { realpathSync(path); return true; } catch { return false; }
    });
  if (!executable) return null;
  try {
    const realExecutable = realpathSync(executable);
    // OMP's supported npm/bun bin points to <package>/dist/cli.js.
    const packageRoot = dirname(dirname(realExecutable));
    return packageRoot;
  } catch { return null; }
}

type OmpProviderMetadata = { providers: Array<{ id: string; name: string; models: OmpModel[] }>; loginProviders: Array<{ id: string; name: string }> };

async function readOmpProviderMetadata(packageRoot: string, bunCommand = DEFAULT_BUN_COMMAND): Promise<OmpProviderMetadata> {
  const code = [
    'import { getOAuthProviders } from "@oh-my-pi/pi-ai/oauth";',
    'import { getBundledProviders, getBundledModels } from "@oh-my-pi/pi-catalog";',
    'const providers = getBundledProviders().map(id => ({id, name:id, models:getBundledModels(id).map(m => ({id:m.id,name:m.name}))}));',
    'const loginProviders = getOAuthProviders().map(({id,name}) => ({id,name}));',
    'process.stdout.write(JSON.stringify({providers,loginProviders}));',
  ].join('\n');
  try {
    const result = await execFileAsync(bunCommand, ['-e', code], {
      cwd: packageRoot, encoding: 'utf8', maxBuffer: 8 * 1024 * 1024,
    });
    const value = record(parseJson(result.stdout, 'provider discovery'));
    if (!Array.isArray(value?.providers) || !Array.isArray(value?.loginProviders)) {
      throw new Error('OMP provider discovery returned an unexpected shape');
    }
    const providers = value.providers.map((entry): OmpProviderMetadata['providers'][number] => {
      const item = record(entry);
      if (!item || typeof item.id !== 'string' || typeof item.name !== 'string' || !Array.isArray(item.models)) {
        throw new Error('OMP provider discovery returned an unexpected shape');
      }
      const models = item.models.map((modelValue): OmpModel => {
        const model = record(modelValue);
        if (!model || typeof model.id !== 'string' || typeof model.name !== 'string') {
          throw new Error('OMP provider discovery returned an unexpected shape');
        }
        return { id: model.id, name: model.name };
      });
      return { id: item.id, name: item.name, models };
    });
    const loginProviders = value.loginProviders.map((entry): OmpProviderMetadata['loginProviders'][number] => {
      const item = record(entry);
      if (!item || typeof item.id !== 'string' || typeof item.name !== 'string') {
        throw new Error('OMP provider discovery returned an unexpected shape');
      }
      return { id: item.id, name: item.name };
    });
    return { providers, loginProviders };
  } catch (error) {
    if (error instanceof Error && /unexpected shape/.test(error.message)) throw error;
    throw new Error('OMP provider discovery failed');
  }
}

function normalizedAvailableModels(value: unknown): Array<{ provider: string; id: string; selector?: string; name: string }> {
  const rows = record(value)?.models;
  if (!Array.isArray(rows)) throw new Error('OMP model listing returned an unexpected shape');
  return rows.map((item) => {
    const model = record(item);
    if (!model || typeof model.provider !== 'string' || typeof model.id !== 'string' || typeof model.name !== 'string') {
      throw new Error('OMP model listing returned an unexpected shape');
    }
    return { provider: model.provider, id: model.id, selector: typeof model.selector === 'string' ? model.selector : undefined, name: model.name };
  });
}

function normalizedDefault(value: unknown): string | null {
  const setting = record(value);
  const roles = record(setting?.value);
  if (!roles) throw new Error('OMP model setting returned an unexpected shape');
  const current = roles?.default;
  return typeof current === 'string' && current.includes('/') ? current : null;
}

const SAFE_NUMERIC_USAGE_FIELDS = ['used', 'limit', 'remaining', 'usedFraction', 'remainingFraction', 'durationMs', 'resetsAt'] as const;
const SAFE_USAGE_STATUSES = new Set(['ok', 'warning', 'exhausted', 'unknown']);
const SAFE_USAGE_UNITS = new Set(['percent', 'tokens', 'requests', 'usd', 'minutes', 'bytes', 'unknown']);

export function projectSafeOmpUsage(value: unknown): SafeUsageSnapshot {
  const root = record(value);
  if (!Array.isArray(root?.reports) || !Array.isArray(root.accountsWithoutUsage)) {
    throw new Error('OMP usage report returned an unexpected shape');
  }
  const reports = root.reports.map((entry) => {
    const report = record(entry);
    if (!report || typeof report.provider !== 'string' || !Array.isArray(report.limits)) {
      throw new Error('OMP usage report returned an unexpected shape');
    }
    const limits = report.limits.map((entryLimit) => {
      const limit = record(entryLimit);
      const amount = record(limit?.amount);
      if (!limit || !amount) throw new Error('OMP usage report returned an unexpected shape');
      const projected: OmpSafeUsage['limits'][number] = {};
      for (const key of SAFE_NUMERIC_USAGE_FIELDS) {
        const valueField = amount[key] ?? record(limit.window)?.[key];
        if (valueField !== undefined) {
          if (typeof valueField !== 'number' || !Number.isFinite(valueField)) throw new Error('OMP usage report returned an unexpected shape');
          projected[key] = valueField;
        }
      }
      const unit = amount.unit;
      if (unit !== undefined) {
        if (typeof unit !== 'string' || !SAFE_USAGE_UNITS.has(unit)) throw new Error('OMP usage report returned an unexpected shape');
        projected.unit = unit;
      }
      const status = limit.status;
      if (status !== undefined) {
        if (typeof status !== 'string' || !SAFE_USAGE_STATUSES.has(status)) throw new Error('OMP usage report returned an unexpected shape');
        projected.status = status as OmpSafeUsage['limits'][number]['status'];
      }
      return projected;
    });
    return { provider: report.provider, limits };
  });
  const authenticatedProviders = new Set<string>(reports.map(report => report.provider));
  for (const entry of root.accountsWithoutUsage) {
    const account = record(entry);
    if (!account || typeof account.provider !== 'string') throw new Error('OMP usage report returned an unexpected shape');
    authenticatedProviders.add(account.provider);
  }
  return { reports, authenticatedProviders: [...authenticatedProviders] };
}

export async function getAstridOmpModelCatalog(options: OmpModelOptions): Promise<OmpModelCatalog> {
  const command = options.command ?? DEFAULT_OMP_COMMAND;
  const [availableOutput, defaultOutput] = await Promise.all([
    runOmp(options, ['models', 'ls', '--json']),
    runOmp(options, ['config', 'get', MODEL_ROLE_SETTING, '--json']),
  ]);
  const packageRoot = resolveOmpPackageRoot(command);
  if (!packageRoot) throw new Error('OMP executable could not be resolved');
  const [metadata, bundledUsage] = await Promise.all([
    readOmpProviderMetadata(packageRoot, options.bunCommand),
    runOmp(options, ['usage', '--json']).then(output => {
      try { return projectSafeOmpUsage(parseJson(output, 'usage report')); }
      catch { return undefined; }
    }).catch(() => undefined),
  ]);
  const bundled = metadata.providers;
  const available = normalizedAvailableModels(parseJson(availableOutput, 'model listing'));
  const defaultSelector = normalizedDefault(parseJson(defaultOutput, 'model setting lookup'));
  const providerNames = new Map<string, string>();
  for (const provider of bundled) {
    providerNames.set(provider.id, provider.name);
  }
  for (const provider of metadata.loginProviders) providerNames.set(provider.id, provider.name);
  const byProvider = new Map<string, OmpProvider>();
  for (const [id, name] of providerNames) {
    const provider = bundled.find(candidate => candidate.id === id);
    byProvider.set(id, { id, name, signedIn: false, models: provider?.models ?? [] });
  }
  for (const model of available) {
    let provider = byProvider.get(model.provider);
    if (!provider) {
      provider = { id: model.provider, name: providerNames.get(model.provider) ?? model.provider, signedIn: false, models: [] };
      byProvider.set(model.provider, provider);
    }
    const wasSignedIn = provider.signedIn;
    provider.signedIn = true;
    if (!wasSignedIn) provider.models = [];
    const known = provider.models.find(candidate => candidate.id === model.id);
    if (!known) provider.models.push({ id: model.id, name: model.name });
    else if (!known.name && model.name) known.name = model.name;
  }
  const usageByProvider = new Map<string, OmpSafeUsage['limits']>();
  for (const report of bundledUsage?.reports ?? []) {
    const limits = usageByProvider.get(report.provider) ?? [];
    limits.push(...report.limits);
    usageByProvider.set(report.provider, limits);
  }
  for (const id of bundledUsage?.authenticatedProviders ?? []) {
    let provider = byProvider.get(id);
    if (!provider) {
      provider = { id, name: providerNames.get(id) ?? id, signedIn: false, models: [] };
      byProvider.set(id, provider);
    }
    if (!provider.signedIn) provider.models = [];
    provider.signedIn = true;
  }
  const providers = [...byProvider.values()]
    .map(provider => ({
      ...provider,
      models: provider.models.map(model => ({ ...model })),
      ...(provider.signedIn && usageByProvider.has(provider.id)
        ? { usage: { limits: usageByProvider.get(provider.id)! } }
        : {}),
    }))
    .sort((left, right) => left.name.localeCompare(right.name));
  const availableCurrent = defaultSelector
    ? available.find(model => model.selector === defaultSelector || `${model.provider}/${model.id}` === defaultSelector)
    : undefined;
  let currentModel = availableCurrent ? `${availableCurrent.provider}/${availableCurrent.id}` : null;
  if (!currentModel && defaultSelector) {
    const slash = defaultSelector.indexOf('/');
    const providerId = slash > 0 ? defaultSelector.slice(0, slash) : '';
    const modelId = slash > 0 ? defaultSelector.slice(slash + 1) : '';
    const bundledMatch = bundled.find(provider => provider.id === providerId)?.models.some(model => model.id === modelId);
    if (bundledMatch) currentModel = `${providerId}/${modelId}`;
  }
  return { providers, currentModel };
}

export async function setAstridOmpDefaultModel(options: OmpModelOptions, model: string): Promise<string> {
  if (!/^[^/\s]+\/.+/.test(model)) throw new OmpModelSelectionError('model must be a provider/model selector');
  const [provider, ...modelParts] = model.split('/');
  const modelId = modelParts.join('/');
  if (!provider || !modelId) throw new OmpModelSelectionError('model must be a provider/model selector');
  const [modelsOutput, rolesOutput] = await Promise.all([
    runOmp(options, ['models', 'ls', '--json']),
    runOmp(options, ['config', 'get', MODEL_ROLE_SETTING, '--json']),
  ]);
  const available = normalizedAvailableModels(parseJson(modelsOutput, 'model listing'));
  const candidate = available.find(item => item.provider === provider && item.id === modelId);
  if (!candidate) throw new OmpModelSelectionError('The requested model is not available');
  const selector = candidate.selector ?? `${candidate.provider}/${candidate.id}`;
  const rolesResult = record(parseJson(rolesOutput, 'model setting lookup'));
  const roles = record(rolesResult?.value);
  if (!roles) throw new Error('OMP model setting returned an unexpected shape');
  await runOmp(options, ['config', 'set', MODEL_ROLE_SETTING, JSON.stringify({ ...roles, default: selector })]);
  return `${candidate.provider}/${candidate.id}`;
}
