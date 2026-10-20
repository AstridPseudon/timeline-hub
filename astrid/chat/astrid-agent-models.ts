import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { modelCatalogSchema, type AcpModelCatalog } from './modelCatalog.ts';
import { ASTRID_ACP_COMMAND } from './astridAcpLauncher.ts';

const execFileAsync = promisify(execFile);
type UsageLimit = NonNullable<AcpModelCatalog['providers'][number]['usage']>['limits'][number];

/** The documented `astrid agent models --json` v1 response. */
type AstridModelSnapshot = {
  schemaVersion: 1;
  currentModel: string | null;
  providers: Array<{
    id: string;
    name: string;
    signedIn: boolean;
    models: Array<{ id: string; name: string; selector: string }>;
    usage?: Array<{ limits: Array<{
      amount: Omit<UsageLimit, 'durationMs' | 'resetsAt' | 'status'>;
      window?: Pick<UsageLimit, 'durationMs' | 'resetsAt'>;
      status?: UsageLimit['status'];
    }> }>;
  }>;
};

type AstridModelOptions = { command?: string; cwd: string; profile?: string };

async function runAstrid(options: AstridModelOptions, args: string[]): Promise<string> {
  try {
    const result = await execFileAsync(options.command ?? ASTRID_ACP_COMMAND, ['agent', ...args, '--json'], {
      cwd: options.cwd,
      env: { ...process.env, ...(options.profile ? { OMP_PROFILE: options.profile } : {}) },
      encoding: 'utf8',
      timeout: 5_000,
      killSignal: 'SIGKILL',
      maxBuffer: 8 * 1024 * 1024,
    });
    return result.stdout;
  } catch {
    // Child diagnostics can contain private context. Astrid owns discovery,
    // authentication and persistence; the bridge exposes no raw child output.
    throw new Error('Astrid model operation failed. Run `astrid agent models` in a terminal for details.');
  }
}

function modelCatalog(output: string): AcpModelCatalog {
  try {
    const snapshot = JSON.parse(output) as AstridModelSnapshot;
    if (snapshot.schemaVersion !== 1) throw new Error('Unsupported schema');
    return modelCatalogSchema.parse({
      currentModel: snapshot.currentModel,
      providers: snapshot.providers.map(provider => ({
        id: provider.id,
        name: provider.name,
        signedIn: provider.signedIn,
        models: provider.models.map(({ id, name }) => ({ id, name })),
        ...(provider.usage ? { usage: { limits: provider.usage.flatMap(report => report.limits.map(limit => {
          const amount = limit.amount;
          // Adapt the public CLI contract to the existing App usage shape.
          // Only fields already accepted by the browser contract cross over.
          return Object.fromEntries(Object.entries({
            unit: amount.unit, used: amount.used, limit: amount.limit, remaining: amount.remaining,
            usedFraction: amount.usedFraction, remainingFraction: amount.remainingFraction,
            durationMs: limit.window?.durationMs, resetsAt: limit.window?.resetsAt, status: limit.status,
          }).filter(([, value]) => value !== undefined));
        })) } } : {}),
      })),
    });
  } catch {
    throw new Error('Astrid returned an invalid model catalog; expected JSON v1.');
  }
}

export async function getAstridAgentModelCatalog(options: AstridModelOptions): Promise<AcpModelCatalog> {
  return modelCatalog(await runAstrid(options, ['models']));
}
