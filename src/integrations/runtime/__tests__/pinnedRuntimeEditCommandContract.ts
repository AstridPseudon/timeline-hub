import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import type { EditCommand } from '../timeline-commit-types.ts';

type JsonObject = { [key: string]: unknown };

function walk(value: unknown, visit: (value: JsonObject) => void): void {
  if (Array.isArray(value)) {
    value.forEach((item) => walk(item, visit));
    return;
  }
  if (!value || typeof value !== 'object') return;
  const object = value as JsonObject;
  visit(object);
  Object.values(object).forEach((item) => walk(item, visit));
}

function runtimeBundlePath(): string {
  const checkout = process.env.ASTRID_RUNTIME_CHECKOUT?.trim() || resolve(process.cwd(), '../../runtime');
  return resolve(checkout, 'runtime_protocol/schemas/timeline-commit-bundle.json');
}

function pinnedEditCommandSchema(): JsonObject {
  const bundle = JSON.parse(readFileSync(runtimeBundlePath(), 'utf8')) as JsonObject;
  const resources = bundle.resources;
  if (!resources || typeof resources !== 'object' || Array.isArray(resources)) {
    throw new Error('Pinned Runtime commit bundle has no resources');
  }
  const resource = Object.values(resources as JsonObject).find((candidate) => (
    candidate && typeof candidate === 'object' && !Array.isArray(candidate)
      && (candidate as JsonObject).$id === 'https://astrid.local/schemas/timeline/edit-command.schema.json'
  ));
  if (!resource || typeof resource !== 'object' || Array.isArray(resource)) {
    throw new Error('Pinned Runtime commit bundle has no EditCommand schema resource');
  }
  return resource as JsonObject;
}

/** Derive operation membership from the Runtime's normal pinned schema bundle. */
export function pinnedRuntimeEditCommandOps(): ReadonlySet<string> {
  const schema = pinnedEditCommandSchema();
  const defs = schema.$defs;
  const editCommand = defs && typeof defs === 'object' && !Array.isArray(defs)
    ? (defs as JsonObject).EditCommand : undefined;
  if (!editCommand) throw new Error('Pinned Runtime EditCommand schema has no EditCommand definition');

  const operations = new Set<string>();
  walk(editCommand, (value) => {
    const op = value.op;
    if (!op || typeof op !== 'object' || Array.isArray(op)) return;
    const constant = (op as JsonObject).const;
    if (typeof constant === 'string') operations.add(constant);
  });
  if (!operations.size) throw new Error('Pinned Runtime EditCommand schema declares no operations');
  return operations;
}

export function assertPinnedRuntimeEditCommandOps(commands: readonly EditCommand[]): void {
  const supported = pinnedRuntimeEditCommandOps();
  const unknown = [...new Set(commands.map((command) => command.op))]
    .filter((op) => !supported.has(op));
  if (unknown.length) {
    throw new Error(`Pinned Runtime EditCommand schema rejects unknown operation(s): ${unknown.join(', ')}`);
  }
}
