// Offline path resolution only: no bundler, source evaluation, browser, or sockets.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const graph = '/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules';
const root = path.resolve(process.argv[2]);
const modules = path.join(root, 'remotion/node_modules');
const composition = path.join(modules, '@banodoco/timeline-composition');
const theme = path.join(modules, '@banodoco/timeline-theme-2rp');
const peerRequire = createRequire(`${graph}/typescript/package.json`);
const ts = peerRequire(`${graph}/typescript`);
const {ResolverFactory, CachedInputFileSystem} = peerRequire(`${graph}/enhanced-resolve`);
const {remotionPrimitiveAliasesFor} = await import(pathToFileURL(`${root}/remotion/webpack-alias.mjs`).href);
const configuration = remotionPrimitiveAliasesFor(`${root}/remotion`)({resolve: {}}).resolve;
const resolver = ResolverFactory.createResolver({
  fileSystem: new CachedInputFileSystem(fs, 0), useSyncFileSystemCalls: true,
  extensions: ['.ts', '.tsx', '.web.js', '.js', '.jsx', '.mjs', '.cjs', '.json', '.d.ts'],
  conditionNames: ['remotion', 'import', 'require', 'browser', 'default'],
  mainFields: ['browser', 'module', 'main'],
  alias: configuration.alias, modules: [modules, ...configuration.modules],
});
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const label = (file) => file.startsWith(`${root}/`) ? path.relative(root, file) : file;
const owned = (file) => file.startsWith(`${root}/`) && !file.includes('/node_modules/')
  || file.startsWith(`${composition}/`) || file.startsWith(`${theme}/`);
const registries = ['effects', 'animations', 'transitions']
  .map((name) => `${root}/remotion/src/${name}.generated.ts`);
const queue = [`${root}/remotion/src/index.ts`, ...registries];
const seen = new Set();
const edges = [];
const failures = [];
const nonliteral = [];
while (queue.length) {
  const file = queue.shift();
  if (seen.has(file)) continue;
  seen.add(file);
  const source = ts.createSourceFile(file, fs.readFileSync(file, 'utf8'), ts.ScriptTarget.Latest, true);
  const requests = [];
  const add = (node, value, kind) => {
    if (value && ts.isStringLiteralLike(value)) requests.push({request: value.text, kind});
    else nonliteral.push({importer: label(file), position: node.pos, kind});
  };
  const visit = (node) => {
    if (ts.isImportDeclaration(node) || ts.isExportDeclaration(node)) {
      if (node.moduleSpecifier) add(node, node.moduleSpecifier, 'import/export');
    } else if (ts.isImportTypeNode(node) && ts.isLiteralTypeNode(node.argument)) {
      add(node, node.argument.literal, 'import-type');
    } else if (ts.isCallExpression(node) && (node.expression.kind === ts.SyntaxKind.ImportKeyword
      || ts.isIdentifier(node.expression) && node.expression.text === 'require')) {
      add(node, node.arguments[0], 'dynamic-import/require');
    }
    ts.forEachChild(node, visit);
  };
  visit(source);
  for (const {request, kind} of requests) {
    try {
      const resolved = resolver.resolveSync({}, path.dirname(file), request.split('?')[0]);
      if (!resolved || !fs.statSync(resolved).isFile()) throw new Error('no module file');
      const target = fs.realpathSync(resolved);
      edges.push({importer: label(file), request, kind, target: label(target), sha256: hash(target),
        registry: registries.includes(file), bare: !request.startsWith('.') && !path.isAbsolute(request)});
      if (owned(target) && /\.[cm]?[jt]sx?$/.test(target)) queue.push(target);
    } catch (error) {
      failures.push({importer: label(file), request, kind, error: error.message});
    }
  }
}
const declared = {};
const manifest = JSON.parse(fs.readFileSync(`${root}/remotion/package.json`, 'utf8'));
const lock = JSON.parse(fs.readFileSync(`${root}/remotion/package-lock.json`, 'utf8')).packages;
for (const name of Object.keys({...manifest.dependencies, ...manifest.devDependencies})) {
  try {
    const file = path.join(modules, name, 'package.json');
    const installed = JSON.parse(fs.readFileSync(file, 'utf8'));
    if (installed.version !== lock[`node_modules/${name}`].version) throw new Error('version differs from MAIN lock');
    declared[name] = {version: installed.version, package_json_sha256: hash(file),
      physical_package: fs.realpathSync(path.dirname(file))};
  } catch (error) { failures.push({declared_package: name, error: error.message}); }
}
const generatedBare = edges.filter((edge) => edge.registry && edge.bare);
console.log(JSON.stringify({
  status: failures.length || nonliteral.length ? 'FAIL' : 'PASS',
  method: 'TypeScript AST + enhanced-resolve filesystem only; no compilation or peer module traversal',
  root, registry_files: registries.map((file) => ({path: label(file), sha256: hash(file)})),
  source_files: [...seen].sort().map((file) => ({path: label(file), sha256: hash(file)})),
  generated_registry_bare_imports: generatedBare, edges, declared_main_packages: declared,
  failures, nonliteral,
  scope: 'MAIN index plus ALL four original generated registries, recursively through every owned source import (including types); direct MAIN dependencies/devDependencies lock-version checked. External peers are resolved and hashed but their internals are not traversed.',
  unused_legacy_declaration: {
    package: '@banodoco/timeline-schema', version: '0.0.1',
    declared_by: 'Composition6 package.json', referenced_by_owned_source: edges.some((e) => e.request.startsWith('@banodoco/timeline-schema')),
    staged: fs.existsSync(`${modules}/@banodoco/timeline-schema`),
    note: 'Not imported by this complete owned source graph; not needed for this bundle. No claim of a complete historical npm install or archive integrity for external peers.',
  },
}, null, 2));
if (failures.length || nonliteral.length) process.exitCode = 1;
