import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
const { sourceVersions, assertSourceVersionsUnchanged } = await import(pathToFileURL(resolve('tests/e2e/timeline/viewing-parity/harness.ts')).href);
const baseline = await sourceVersions();
const selected = await sourceVersions('native-codec-chrome155');
assert.equal(baseline.playerBrowser.profile, 'chromium141');
assert.equal(selected.playerBrowser.profile, 'native-codec-chrome155');
assert.notEqual(selected.playerBrowserExecutable, baseline.playerBrowserExecutable);
assert.notEqual(selected.playerBrowser.sha256, baseline.playerBrowser.sha256);
assert.throws(() => assertSourceVersionsUnchanged(baseline, selected), /playerBrowser/);
const { playerBrowser: _baselineBrowser, playerBrowserExecutable: _baselineExecutable, ...baselineShared } = baseline;
const { playerBrowser: _selectedBrowser, playerBrowserExecutable: _selectedExecutable, ...selectedShared } = selected;
assert.deepEqual(selectedShared, baselineShared);
console.log(JSON.stringify({ proof: 'offline source identity only; no browser/HTTP/render/parity claim', baseline: baseline.playerBrowser,
  selected: selected.playerBrowser, allOtherSourceVersionFieldsEqual: true,
  compositionFiles: Object.fromEntries(Object.entries(selected.compositionFiles).map(([name, files]) => [name, Object.keys(files).length])),
  renderGraphFiles: Object.fromEntries(Object.entries(selected.renderGraphHashes).map(([name, files]) => [name, Object.keys(files).length])),
  exportBrowserExecutable: selected.browserExecutable, exportBrowserHash: selected.exportBrowserHash, node: selected.node }, null, 2));
