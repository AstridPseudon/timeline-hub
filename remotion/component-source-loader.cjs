const fs = require('node:fs');
const path = require('node:path');
const {createHash} = require('node:crypto');

// Verify the actual bytes entering Webpack, after alias setup and before TS
// transpilation. Missing, changed and symlink-escaped sources fail the bundle.
module.exports = function(source) {
  const {root, files} = this.getOptions();
  const filename = this.resourcePath;
  const relative = path.relative(root, fs.realpathSync(filename));
  if (!relative || relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)
    || !Object.hasOwn(files, filename)
    || createHash('sha256').update(source).digest('hex') !== files[filename]) {
    throw new Error(`Changed or escaped staged component: ${filename}`);
  }
  return source;
};
module.exports.raw = true;
