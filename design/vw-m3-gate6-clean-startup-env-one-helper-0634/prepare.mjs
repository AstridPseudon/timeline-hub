import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {existsSync,lstatSync,readFileSync,readlinkSync,writeFileSync,realpathSync} from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const out=process.env.PREFLIGHT_DIR;
assert(out && realpathSync(out)===out);
assert.equal(path.dirname(out),path.join(path.dirname(new URL(import.meta.url).pathname),'evidence'));
const app='/home/user/work/wt/app-pin-d00a6613';
const agent='/home/user/work/wt/agt-pin-d0a5072b';
const runtime='/home/user/work/wt/rt-pin-8f105c26';
const composition='/home/user/work/wt/vw-pin-5a4e9b72';
const c=await import(pathToFileURL(path.join(app,'tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs')).href);
const sha=b=>createHash('sha256').update(b).digest('hex');
const hash=b=>'sha256:'+sha(b);
const git=(root,...args)=>execFileSync('git',args,{cwd:root,encoding:'utf8'}).trim();
const runtimePython=process.env.ASTRID_RUNTIME_PYTHON??'/home/user/work/venv-runtime/bin/python';
const agentPython=process.env.ASTRID_PYTHON??'/home/user/work/venv-agent/bin/python';
const pythonEnv={...process.env,
  ASTRID_CHECKOUT:agent,
  ASTRID_RUNTIME_CHECKOUT:runtime,
  ASTRID_RUNTIME_PYTHON:runtimePython,
  ASTRID_PYTHON:agentPython,
  PYTHONDONTWRITEBYTECODE:'1',
  PYTHONUNBUFFERED:'1',
  PYTHONPATH:[runtime,agent].join(path.delimiter),
};
const pythonProbe=`
import importlib.util,json,os,sys
rt,ag=sys.argv[1:3]
def origin(name):
    spec=importlib.util.find_spec(name)
    assert spec is not None,name
    return os.path.realpath(spec.origin or next(iter(spec.submodule_search_locations)))
origins={name:origin(name) for name in ('runtime_protocol','runtime_protocol.cli','astrid_runtime','astrid')}
assert origins['runtime_protocol'].startswith(rt+os.sep),(origins,rt)
assert origins['runtime_protocol.cli'].startswith(rt+os.sep),(origins,rt)
assert origins['astrid_runtime'].startswith(rt+os.sep),(origins,rt)
assert origins['astrid'].startswith(ag+os.sep),(origins,ag)
import runtime_protocol,astrid_runtime,astrid
print(json.dumps({'executable':sys.executable,'origins':origins},sort_keys=True))
`;
function verifyPython(label,executable){
  assert.equal(existsSync(executable),true,`${label} Python missing: ${executable}`);
  const output=execFileSync(executable,['-B','-c',pythonProbe,runtime,agent],{cwd:app,env:pythonEnv,encoding:'utf8'});
  const facts=JSON.parse(output.trim());
  assert.equal(facts.executable,executable,`${label} executable changed`);
  return facts;
}
const python={runtime:verifyPython('Runtime',runtimePython),agent:verifyPython('Agent',agentPython)};
Object.assign(process.env,pythonEnv);
const appSha='d00a66134f330672ea7471dc69db38c1566d94cf';
const appTree='a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba';
assert.equal(git(app,'rev-parse','HEAD'),appSha);assert.equal(git(app,'rev-parse','HEAD^{tree}'),appTree);
assert.equal(git(app,'status','--porcelain'),'');
for(const [root,pin] of [[agent,c.AGENT13],[runtime,c.RUNTIME13]]){
 assert.equal(git(root,'rev-parse','HEAD'),pin.source);assert.equal(git(root,'rev-parse','HEAD^{tree}'),pin.tree);
}
assert.equal(git(composition,'rev-parse','HEAD'),c.COMPOSITION13.source);
assert.equal(git(composition,'rev-parse','HEAD^{tree}'),'13e375534fffd704305eced5686699d2c8c9c948');
assert.equal(git(composition,'status','--porcelain'),'');
assert.equal(git(runtime,'rev-parse',c.RUNTIME13_ARTIFACT.source+'^{tree}'),c.RUNTIME13_ARTIFACT.tree);
const release=JSON.parse(execFileSync('git',['show',c.RUNTIME13_ARTIFACT.source+':contract/artifacts.json'],{cwd:runtime,encoding:'utf8'}));
assert.equal(release.version,c.RUNTIME13_ARTIFACT.version);assert.equal(Object.keys(release.artifacts).length,75);
for(const [name,expected]of Object.entries(release.artifacts))assert.equal(hash(readFileSync(path.join(runtime,name))),expected,'official artifact '+name);
const generated=release.artifacts['packages/typescript/src/generated.ts'];
assert.equal(hash(readFileSync(path.join(app,'src/integrations/runtime/generated.ts'))),generated);
const names=execFileSync('git',['ls-files','-z','--cached','--others','--exclude-standard'],{cwd:app,encoding:'utf8'}).split('\0').filter(Boolean).sort();
const members=names.map(name=>{const p=path.join(app,name),s=lstatSync(p);assert(s.isFile()||s.isSymbolicLink());return[name,s.isSymbolicLink()?'symlink':s.mode&0o111?'executable':'file',hash(s.isSymbolicLink()?Buffer.from(readlinkSync(p)):readFileSync(p))];});
const source=root=>({root,commit:git(root,'rev-parse','HEAD'),tree:git(root,'rev-parse','HEAD^{tree}')});
const agentPeers=Object.fromEntries(Object.entries(c.AGENT13_RUNTIME.peers).map(([p,h])=>[p,'sha256:'+h]));
const appPeers={
 'node_modules/remotion/dist/cjs/audio/shared-audio-tags.js':'sha256:949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8',
 'node_modules/remotion/dist/esm/index.mjs':'sha256:5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28',
 'node_modules/@remotion/player/dist/cjs/use-player-methods.js':'sha256:ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
 'node_modules/@remotion/player/dist/esm/index.mjs':'sha256:d3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
 'node_modules/@remotion/player/dist/cjs/use-playback.js':'sha256:6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
 'node_modules/@remotion/player/dist/cjs/PlayerUI.js':'sha256:5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
};
const tuple={schema:'timeline.viewing.next-five-case/v1',frozen:true,sources:{app:source(app),agent:source(agent),runtime:source(runtime),composition:source(composition)},appSource:{files:members.length,sha256:hash(Buffer.from(JSON.stringify(members)))},remotionProject:c.AGENT13_RUNTIME.project,peers:{app:appPeers,agent:agentPeers},client:{official:true,producerCommit:c.RUNTIME13_ARTIFACT.source,producerTree:c.RUNTIME13_ARTIFACT.tree,producerVersion:release.version,artifactCount:75,files:{'src/integrations/runtime/generated.ts':generated}}};

const parity = await import(pathToFileURL(path.join(app,'tests/e2e/timeline/viewing-parity/harness.ts')).href);
const local = await import(pathToFileURL(path.join(app,'tests/e2e/local/support/harness.ts')).href);
const setup = await import(pathToFileURL(path.join(app,'tests/e2e/local/global-setup.ts')).href);
const bootstrap = await import(pathToFileURL(path.join(app,'tests/e2e/timeline/viewing-parity/bootstrap.ts')).href);
const {assertDist, availabilityGet} = await import('./dist-availability.mjs');
function exclusive(name,obj) {
 const p=path.join(out,name);
 assert.equal(realpathSync(path.dirname(p)),out);
 writeFileSync(p,JSON.stringify(obj,null,2)+'\n',{flag:'wx',mode:0o600});
 return p;
}
assert.equal(tuple.appSource.sha256,'sha256:76694aa3da39f17ef0945fb50a22f64a86908e2ad94dc46b79c362db22220fa0');
const dist=process.env.ASTRID_APP_DIRECT_DIST;
// The refusal probe only supplies an absent private path; it never edits the retained source.
assertDist(process.argv[2]==='--plant-missing-dist' ? path.join(out,'missing-dist') : dist);
assert.equal(setup.distIsHosted(dist),true,'retained dist must be hosted');
assert.equal(local.harnessUnavailableReason(),null);
process.env.VIEWING_FRAME_SOURCE_TUPLE=exclusive('source-tuple.json',tuple);
c.assertCandidateTuple();c.assertRuntimeArtifact();c.assertOwnerPorts();
c.assertCompletedAppConsumer(app);c.assertExactGraph({appRoot:app,agentRoot:agent,runtimeRoot:runtime});
const freeBytes=c.assertResources(app);c.assertOwnedShortTemp();
const appGraph=c.assertPhysicalPrivateGraph(path.join(app,'node_modules'));
assert.equal(appGraph.sha256,'8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b');
assert.equal(appGraph.fileCount,32393);
const failures=[];
let runtimeGraph;
try { runtimeGraph=c.assertFrozenRuntimeGraph(); }
catch (error) { failures.push({check:'frozen Runtime graph before',error:error.stack}); }
// Read-only diagnostics continue, but any failed guard prevents issuance.
const runtimeContent=c.hashTree(path.join(c.AGENT13_RUNTIME.project,'node_modules'));
assert.equal(runtimeContent.sha256,c.AGENT13_RUNTIME.graph);
assert.equal(runtimeContent.fileCount,c.AGENT13_RUNTIME.graphFileCount);
const node=c.assertNode20();const chrome=c.assertChrome155();
const helper=await bootstrap.resolveReviewedPackHostHelper(agent);
await parity.assertRunBoundary();
const before=await parity.sourceVersions('native-codec-chrome155');
const discovery=c.discover(app);
const normalDiscovery=execFileSync(process.execPath,[path.join(app,'node_modules/@playwright/test/cli.js'),'test','--config','playwright.viewing-parity.normal-profile-native1920.config.ts','--project=native-codec-chrome155','--workers=1','--list'],{cwd:app,encoding:'utf8',timeout:60000});
assert.match(normalDiscovery,/^Total: 5 tests in 1 file$/m);
const availability=await availabilityGet(dist);
await parity.assertRunBoundary();
parity.assertSourceVersionsUnchanged(before,await parity.sourceVersions('native-codec-chrome155'));
assert.deepEqual(c.assertPhysicalPrivateGraph(path.join(app,'node_modules')),appGraph);
try { assert.deepEqual(c.assertFrozenRuntimeGraph(),runtimeGraph); }
catch (error) { failures.push({check:'frozen Runtime graph after',error:error.stack}); }
assert.deepEqual(c.hashTree(path.join(c.AGENT13_RUNTIME.project,'node_modules')),runtimeContent);
await bootstrap.resolveReviewedPackHostHelper(agent);
assert.equal(git(app,'status','--porcelain'),'');
const result={status:failures.length?'BLOCKED':'PASS',failures,runtimeContent,tokenIssued:false,browserLaunched:false,runtimeStarted:false,tuple,dist:assertDist(dist),availability,python,helper,node,chrome,freeBytes,appGraph,runtimeGraph,discovery,normalDiscovery};
exclusive('preflight.json',result);
console.log(JSON.stringify(result,null,2));
if (failures.length) process.exitCode=1;
