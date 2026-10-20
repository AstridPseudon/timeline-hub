import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  COMPONENT_MANIFEST_SHA256,
  CONTRACT_VERSION,
  SCHEMA_DIGEST,
} from '../../../../src/integrations/runtime/generated-contract-metadata.ts';

const APP_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
const FULL_SHA = /^[0-9a-f]{40}$/;
const REQUIRED_ENV = ['ASTRID_CHECKOUT', 'ASTRID_RUNTIME_CHECKOUT', 'TIMELINE_BUNDLE_AGENT_HEAD', 'TIMELINE_BUNDLE_RUNTIME_HEAD'] as const;

export type CurrentQualificationEnvironment = {
  agentCheckout: string;
  runtimeCheckout: string;
  agentHead: string;
  runtimeHead: string;
};

export type ContractMetadata = {
  contractVersion: string;
  schemaDigest: string;
  componentManifestSha256: string;
};

type LockFile = {
  files: Record<string, { from: string; sha256: string }>;
  manifest: string;
  producer: string;
  producer_version: string;
  source_commit: string;
};

type ProducerManifest = {
  producer: string;
  version: string;
  artifacts: Record<string, string>;
};

export type AppQualificationAuthority = {
  metadata: ContractMetadata;
  runtimeLock: LockFile;
};

export type SourceIdentity = {
  head: string;
  tree: string;
  status: string;
};

export type CurrentQualificationSources = {
  environment: CurrentQualificationEnvironment;
  app: AppQualificationAuthority;
  agent: { identity: SourceIdentity; metadata: ContractMetadata; runtimeLock: LockFile };
  runtime: { identity: SourceIdentity; metadata: ContractMetadata; manifest: ProducerManifest };
};

function fail(message: string): never {
  throw new Error(`current qualification: ${message}`);
}

function parseJson<T>(text: string, label: string): T {
  try { return JSON.parse(text) as T; }
  catch { return fail(`${label} is not valid JSON`); }
}

function git(checkout: string, args: string[]): string {
  try {
    return execFileSync('git', ['-C', checkout, ...args], {
      encoding: 'utf8',
      maxBuffer: 8 * 1024 * 1024,
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch {
    return fail(`cannot read git source ${checkout}`);
  }
}

function gitShow(checkout: string, head: string, sourcePath: string): string {
  try {
    return execFileSync('git', ['-C', checkout, 'show', `${head}:${sourcePath}`], {
      encoding: 'utf8',
      maxBuffer: 16 * 1024 * 1024,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
  } catch {
    return fail(`source ${sourcePath} is missing from ${checkout}@${head}`);
  }
}

function sha256(text: string): string {
  return `sha256:${createHash('sha256').update(text).digest('hex')}`;
}

function metadataFromSource(text: string, label: string): ContractMetadata {
  const read = (name: string): string => {
    const match = text.match(new RegExp(`${name}\\s*=\\s*["']([^"']+)["']`));
    return match?.[1] ?? fail(`${label} has no ${name}`);
  };
  return {
    contractVersion: read('CONTRACT_VERSION'),
    schemaDigest: read('SCHEMA_DIGEST'),
    componentManifestSha256: read('COMPONENT_MANIFEST_SHA256'),
  };
}

export function readCommittedAppAuthority(): AppQualificationAuthority {
  const runtimeLock = parseJson<LockFile>(readFileSync(path.join(APP_ROOT, 'runtime.lock.json'), 'utf8'), 'App runtime.lock.json');
  return {
    metadata: {
      contractVersion: CONTRACT_VERSION,
      schemaDigest: SCHEMA_DIGEST,
      componentManifestSha256: COMPONENT_MANIFEST_SHA256,
    },
    runtimeLock,
  };
}

export function requireCurrentQualificationEnvironment(env: NodeJS.ProcessEnv = process.env): CurrentQualificationEnvironment {
  const values = Object.fromEntries(REQUIRED_ENV.map((name) => [name, env[name]])) as Record<typeof REQUIRED_ENV[number], string | undefined>;
  for (const name of REQUIRED_ENV) {
    if (!values[name]) fail(`missing ${name}; the manager must provide an explicit current source pin`);
  }
  if (!path.isAbsolute(values.ASTRID_CHECKOUT!)) fail('ASTRID_CHECKOUT must be an absolute source checkout');
  if (!path.isAbsolute(values.ASTRID_RUNTIME_CHECKOUT!)) fail('ASTRID_RUNTIME_CHECKOUT must be an absolute source checkout');
  if (!FULL_SHA.test(values.TIMELINE_BUNDLE_AGENT_HEAD!)) fail('TIMELINE_BUNDLE_AGENT_HEAD must be a full 40-character SHA');
  if (!FULL_SHA.test(values.TIMELINE_BUNDLE_RUNTIME_HEAD!)) fail('TIMELINE_BUNDLE_RUNTIME_HEAD must be a full 40-character SHA');
  return {
    agentCheckout: values.ASTRID_CHECKOUT!,
    runtimeCheckout: values.ASTRID_RUNTIME_CHECKOUT!,
    agentHead: values.TIMELINE_BUNDLE_AGENT_HEAD!,
    runtimeHead: values.TIMELINE_BUNDLE_RUNTIME_HEAD!,
  };
}

export function assertSourceIdentity(identity: SourceIdentity, expectedHead: string, label: string): void {
  if (identity.head !== expectedHead) fail(`${label} moved: expected ${expectedHead}, got ${identity.head}`);
  if (identity.status !== '') fail(`${label} is dirty: ${identity.status}`);
  if (!FULL_SHA.test(identity.tree)) fail(`${label} has no readable tree identity`);
}

export function assertContractMetadataEqual(expected: ContractMetadata, actual: ContractMetadata, label: string): void {
  if (actual.contractVersion !== expected.contractVersion) fail(`${label} client ${actual.contractVersion} does not match App ${expected.contractVersion}`);
  if (actual.schemaDigest !== expected.schemaDigest) fail(`${label} schema ${actual.schemaDigest} does not match App ${expected.schemaDigest}`);
  if (actual.componentManifestSha256 !== expected.componentManifestSha256) fail(`${label} component artifact ${actual.componentManifestSha256} does not match App ${expected.componentManifestSha256}`);
}

export function assertLockMatchesManifest(lock: LockFile, manifest: ProducerManifest, label: string): void {
  if (lock.manifest !== 'contract/artifacts.json') fail(`${label} manifest ${lock.manifest} is not the official contract artifact manifest`);
  if (lock.producer !== manifest.producer) fail(`${label} producer ${lock.producer} does not match ${manifest.producer}`);
  if (lock.producer_version !== manifest.version) fail(`${label} artifact ${lock.producer_version} does not match ${manifest.version}`);
  for (const [consumerPath, entry] of Object.entries(lock.files)) {
    if (manifest.artifacts[entry.from] !== entry.sha256) {
      fail(`${label} ${consumerPath} does not match official artifact ${entry.from}`);
    }
  }
}

function sourceIdentity(checkout: string): SourceIdentity {
  return {
    head: git(checkout, ['rev-parse', 'HEAD']),
    tree: git(checkout, ['rev-parse', 'HEAD^{tree}']),
    status: git(checkout, ['status', '--porcelain', '--untracked-files=all']),
  };
}

export function readCurrentQualificationSources(env: NodeJS.ProcessEnv = process.env): CurrentQualificationSources {
  const environment = requireCurrentQualificationEnvironment(env);
  const app = readCommittedAppAuthority();
  const agentIdentity = sourceIdentity(environment.agentCheckout);
  const runtimeIdentity = sourceIdentity(environment.runtimeCheckout);
  assertSourceIdentity(agentIdentity, environment.agentHead, 'Agent source');
  assertSourceIdentity(runtimeIdentity, environment.runtimeHead, 'Runtime source');

  const runtimeMetadata = metadataFromSource(
    gitShow(environment.runtimeCheckout, environment.runtimeHead, 'packages/typescript/src/contract-metadata.ts'),
    'Runtime contract metadata',
  );
  const agentMetadata = metadataFromSource(
    gitShow(environment.agentCheckout, environment.agentHead, 'astrid_runtime_client/contract_metadata.py'),
    'Agent contract metadata',
  );
  const runtimeManifest = parseJson<ProducerManifest>(
    gitShow(environment.runtimeCheckout, environment.runtimeHead, 'contract/artifacts.json'),
    'Runtime contract/artifacts.json',
  );
  const agentRuntimeLock = parseJson<LockFile>(
    gitShow(environment.agentCheckout, environment.agentHead, 'runtime.lock.json'),
    'Agent runtime.lock.json',
  );

  assertContractMetadataEqual(app.metadata, runtimeMetadata, 'Runtime');
  assertContractMetadataEqual(app.metadata, agentMetadata, 'Agent');
  assertLockMatchesManifest(app.runtimeLock, runtimeManifest, 'App runtime artifacts');
  assertLockMatchesManifest(agentRuntimeLock, runtimeManifest, 'Agent runtime artifacts');
  if (app.runtimeLock.source_commit !== environment.runtimeHead) fail(`App runtime source ${app.runtimeLock.source_commit} does not match Runtime pin ${environment.runtimeHead}`);
  if (agentRuntimeLock.source_commit !== environment.runtimeHead) fail(`Agent runtime source ${agentRuntimeLock.source_commit} does not match Runtime pin ${environment.runtimeHead}`);
  if (sha256(gitShow(environment.runtimeCheckout, environment.runtimeHead, 'packages/typescript/src/contract-metadata.ts'))
    !== app.runtimeLock.files['src/integrations/runtime/generated-contract-metadata.ts']?.sha256) {
    fail('App generated client metadata is not the official Runtime artifact');
  }

  return {
    environment,
    app,
    agent: { identity: agentIdentity, metadata: agentMetadata, runtimeLock: agentRuntimeLock },
    runtime: { identity: runtimeIdentity, metadata: runtimeMetadata, manifest: runtimeManifest },
  };
}

export function assertCurrentQualificationSources(env: NodeJS.ProcessEnv = process.env): CurrentQualificationSources {
  return readCurrentQualificationSources(env);
}
