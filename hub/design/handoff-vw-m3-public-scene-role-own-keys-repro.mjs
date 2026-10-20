const root = process.env.ROLE_REPRO_ROOT
  ?? '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-public-scene-role-own-keys/offline-copy';
const {prepareScene, querySceneFrame} = await import(`${root}/typescript/test-dist/src/scene-evaluation.js`);

const track = {id: 'video', kind: 'visual', label: 'Video'};
const frameFor = (id, roles) => querySceneFrame(prepareScene([{
  track,
  clips: [{id, at: 0, hold: 1, track: 'video'}],
  transitions: [null],
}], {assets: {}}, 30, 1920, 1080, {roles}), 0);

for (const id of ['__proto__', 'constructor', 'toString']) {
  const role = frameFor(id, {}).layers[0].role;
  console.log(JSON.stringify({id, roleType: typeof role, role: typeof role === 'string' ? role : String(role)}));
}

console.log(JSON.stringify({
  id: '__proto__',
  ownOverride: frameFor('__proto__', JSON.parse('{"__proto__":"background"}')).layers[0].role,
}));
