// Parse source with TypeScript; resolve paths only. No source module is imported.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const requirePeer = createRequire('/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules/typescript/package.json');
const ts = requirePeer('typescript');
const {ResolverFactory} = requirePeer('enhanced-resolve');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const root = '/__readonly_main__';
const graph = '/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules';
const files = new Map(Object.entries(input.files).map(([name, text]) => [`${root}/${name}`, text]));
const dirs = new Set();
for (const name of files.keys()) {
  for (let parent = path.dirname(name); parent !== '/'; parent = path.dirname(parent)) dirs.add(parent);
}
const stats = (directory) => ({isFile: () => !directory, isDirectory: () => directory, isSymbolicLink: () => false});
const virtual = (value) => typeof value === 'string' && value.startsWith(`${root}/`);
const missing = (name) => Object.assign(new Error(`ENOENT ${name}`), {code: 'ENOENT'});
const fileSystem = {
  readFileSync(name, options) {
    if (!virtual(name)) return fs.readFileSync(name, options);
    if (!files.has(name)) throw missing(name);
    return options ? files.get(name) : Buffer.from(files.get(name));
  },
  statSync(name) {
    if (!virtual(name)) return fs.statSync(name);
    if (files.has(name)) return stats(false);
    if (dirs.has(name)) return stats(true);
    throw missing(name);
  },
  lstatSync(name) { return this.statSync(name); },
  readlinkSync(name) {
    if (!virtual(name)) return fs.readlinkSync(name);
    throw Object.assign(new Error('not a symlink'), {code: 'EINVAL'});
  },
  realpathSync(name) {
    if (!virtual(name)) return fs.realpathSync(name);
    if (files.has(name) || dirs.has(name)) return name;
    throw missing(name);
  },
};
const aliases = Object.fromEntries(Object.entries(input.aliases).map(([key, value]) => [key, `${root}/${value}`]));
const resolver = ResolverFactory.createResolver({
  fileSystem, useSyncFileSystemCalls: true, extensions: ['.tsx', '.ts', '.jsx', '.js', '.mjs', '.cjs', '.json'],
  conditionNames: ['remotion', 'browser', 'import', 'default'], mainFields: ['browser', 'module', 'main'],
  alias: aliases, modules: [`${root}/remotion/node_modules`, graph], symlinks: true,
});
const edges = [];
const pending = [...files.keys()].filter((name) => name === `${root}/remotion/src/index.ts`
  || /\/typescript\/src\/(registry|effects|animations|transitions)\.generated\.ts$/.test(name));
const visited = new Set();
while (pending.length) {
  const name = pending.shift();
  if (visited.has(name)) continue;
  visited.add(name);
  const text = files.get(name);
  if (!/\.(tsx?|m?js)$/.test(name)) continue;
  const ast = ts.createSourceFile(name, text, ts.ScriptTarget.Latest, true);
  const collect = (node) => {
    if ((ts.isImportDeclaration(node) || ts.isExportDeclaration(node)) && node.moduleSpecifier && ts.isStringLiteral(node.moduleSpecifier)) {
      // Pure type imports have no bundling/runtime dependency.
      if (!node.isTypeOnly && !node.importClause?.isTypeOnly) {
        const specifier = node.moduleSpecifier.text;
        if (!specifier.startsWith('node:')) {
          const resolved = resolver.resolveSync({}, path.dirname(name), specifier.split('?')[0]);
          if (!resolved) throw new Error(`unresolved ${name}: ${specifier}`);
          edges.push({from: name.slice(root.length + 1), specifier, resolved});
          if (files.has(resolved)) pending.push(resolved);
        }
      }
    }
    ts.forEachChild(node, collect);
  };
  collect(ast);
}
console.log(JSON.stringify({available_files: files.size, parsed_files: visited.size,
  visited: [...visited], resolved_imports: edges.length, edges}, null, 2));
