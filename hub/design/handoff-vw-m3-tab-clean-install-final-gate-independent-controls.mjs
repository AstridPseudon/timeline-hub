import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {appendFileSync,mkdtempSync,readFileSync,rmSync,writeFileSync,realpathSync} from 'node:fs';
import {createRequire} from 'node:module';
import {join,dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {hashTree,FROZEN_PRIVATE_GRAPH} from './source/tests/e2e/timeline/tab-audio-capture.controller.mjs';
const own='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate';
const design=join(own,'../../design');
const audited=JSON.parse(readFileSync(join(design,'handoff-vw-m3-tab-clean-install-final-gate-before.json')));
const fixture=join(own,'tmp/archive-controls-fixture');
try {
 const expected={sha256:audited.compositionCanonical,fileCount:77};
 assert.deepEqual(hashTree(fixture),expected);
 const path=join(fixture,'package.json');const original=readFileSync(path);
 appendFileSync(path,'\n');assert.notEqual(hashTree(fixture).sha256,expected.sha256);assert.equal(hashTree(fixture).fileCount,77);
 writeFileSync(path,original);assert.deepEqual(hashTree(fixture),expected);
 writeFileSync(join(fixture,'added-review-control.txt'),'added');assert.notEqual(hashTree(fixture).sha256,expected.sha256);assert.equal(hashTree(fixture).fileCount,78);
 rmSync(join(fixture,'added-review-control.txt'));assert.deepEqual(hashTree(fixture),expected);
 console.log('PASS independent actual 77-member tar reconstruction; changed-file and added-file controls reject');
} finally {rmSync(fixture,{recursive:true,force:true});}
assert.deepEqual(hashTree(FROZEN_PRIVATE_GRAPH.root),audited.wholeNodeModulesCanonical);
const req=createRequire(join(own,'source/package.json'));
const graphReq=createRequire(join(FROZEN_PRIVATE_GRAPH.root,'../package.json'));
for(const name of ['react','react-dom','remotion','@remotion/media','@remotion/player','@remotion/layout-utils','@banodoco/timeline-composition','@playwright/test','playwright','playwright-core','@remotion/web-renderer']) {
 const manifest=realpathSync(req.resolve(name+'/package.json'));
 assert.equal(manifest,realpathSync(graphReq.resolve(name+'/package.json')));
 assert.ok(manifest.startsWith(FROZEN_PRIVATE_GRAPH.root+'/'));
 if(audited.peers[name])assert.deepEqual(hashTree(dirname(manifest)),audited.peers[name].canonicalTree);
 console.log('PASS private resolution '+name+' '+manifest);
}
for(const name of ['react','react-dom','remotion','@remotion/media','@remotion/player','@remotion/layout-utils','@banodoco/timeline-composition'])await import(name);
const browser=JSON.parse(readFileSync(join(design,'handoff-vw-m3-tab-clean-install-final-gate-browser.json')));
assert.deepEqual(hashTree('/opt/google/chrome'),browser.canonicalTree);
console.log('PASS pure imports, six peer canonical trees, whole graph, exact browser identity');
