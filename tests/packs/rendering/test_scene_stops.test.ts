// @vitest-environment node
import {describe,expect,it,vi} from 'vitest';
import {SceneFrameHost,sanitizeSceneStops,sceneDocument,validateScenePackage,type ValidatedScenePackage} from '../../../astrid/packs/rendering/ui/threejs-live-editor/runtime';

const DIGEST=`sha256:${'0'.repeat(64)}`;
function pkg(duration=60): ValidatedScenePackage {
  const entry={object_id:'e',digest:DIGEST,media_type:'text/html',size:1,filename:'scene.html'};
  const manifest={formatVersion:1,entry:'scene.html',duration,authoredFps:30};
  return validateScenePackage({revision:DIGEST,source:{objectId:'p',revision:DIGEST},packageBody:JSON.stringify({manifest,entry,assets:[]}),html:'<html><head></head><body></body></html>'});
}

describe('sanitizeSceneStops',()=>{
  it('keeps valid entries trimmed and sorted by time',()=>{
    expect(sanitizeSceneStops([{time:5,name:' Bridge '},{time:0,name:'Start'},{time:2.5,name:'Lake',extra:1}]))
      .toEqual([{time:0,name:'Start'},{time:2.5,name:'Lake'},{time:5,name:'Bridge'}]);
  });
  it('drops invalid entries instead of failing',()=>{
    const long='x'.repeat(81);
    expect(sanitizeSceneStops([
      null,'s',{time:1},{name:'a'},{time:'1',name:'a'},{time:NaN,name:'a'},{time:Infinity,name:'a'},{time:-1,name:'a'},
      {time:1,name:'   '},{time:1,name:7},{time:1,name:long},{time:1,name:'x'.repeat(80)},{time:2,name:'ok'},
    ])).toEqual([{time:1,name:'x'.repeat(80)},{time:2,name:'ok'}]);
  });
  it('drops stops after the known duration',()=>{
    expect(sanitizeSceneStops([{time:10,name:'end'},{time:10.1,name:'past'}],10)).toEqual([{time:10,name:'end'}]);
  });
  it('treats absent, non-array and oversized lists as empty',()=>{
    for(const value of [undefined,null,{},'x',3]) expect(sanitizeSceneStops(value)).toEqual([]);
    const many=Array.from({length:65},(_,i)=>({time:i,name:`s${i}`}));
    expect(sanitizeSceneStops(many)).toEqual([]);
    expect(sanitizeSceneStops(many.slice(0,64))).toHaveLength(64);
  });
});

describe('SceneFrameHost stops',()=>{
  const host=(duration=60)=>{
    const sent: Record<string,unknown>[]=[];
    const h=new SceneFrameHost(pkg(duration),'i',m=>sent.push(m),()=>{});
    const ack=(extra:Record<string,unknown>)=>h.receive({protocol:'astrid.scene/1',instance:'i',revision:DIGEST,kind:'initialized',...extra});
    return {h,ack};
  };
  it('is empty until initialized and when the field is absent',()=>{
    const {h,ack}=host();
    expect(h.stops).toEqual([]);ack({});expect(h.stops).toEqual([]);h.dispose(false);
  });
  it('re-validates what the child sent against the manifest duration',()=>{
    const {h,ack}=host(10);
    ack({stops:[{time:9,name:'b'},{time:11,name:'late'},{time:1,name:' a '},{time:2,name:''}]});
    expect(h.stops).toEqual([{time:1,name:'a'},{time:9,name:'b'}]);h.dispose(false);
  });
});

describe('bridge in sceneDocument',()=>{
  // Runs the injected bridge against a stub iframe window.
  async function run(sceneStops: unknown, duration=60) {
    const html=sceneDocument(pkg(duration),'i');
    const script=/<script>([\s\S]*)<\/script><\/body>/.exec(html)![1];
    const posted: Record<string,unknown>[]=[];
    const parent={postMessage:(m:Record<string,unknown>)=>posted.push(m)};
    let listener:(e:unknown)=>void=()=>{};
    const scene:Record<string,unknown>={initialize:async()=>{},render:async()=>{},dispose:()=>{}};
    if (sceneStops!=='absent') Object.defineProperty(scene,'stops',{get:()=>{ if (sceneStops instanceof Error) throw sceneStops; return sceneStops; }});
    const win={astridScene:scene};
    new Function('window','document','parent','addEventListener',script)(
      win,{fonts:{ready:Promise.resolve(),status:'loaded'},images:[]},parent,(type:string,fn:(e:unknown)=>void)=>{ if(type==='message') listener=fn; });
    listener({source:parent,data:{protocol:'astrid.scene/1',instance:'i',revision:DIGEST,kind:'initialize'}});
    await vi.waitFor(()=>expect(posted.length).toBeGreaterThan(0));
    return posted[0];
  }
  it('adds sanitized stops to the existing initialized acknowledgement',async()=>{
    const ack=await run([{time:3,name:' B '},{time:1,name:'A'},{time:99,name:'past'},{time:2,name:''}],10);
    expect(ack).toEqual({protocol:'astrid.scene/1',instance:'i',revision:DIGEST,kind:'initialized',stops:[{time:1,name:'A'},{time:3,name:'B'}]});
  });
  it('sends an empty list when stops are absent, invalid or throw',async()=>{
    for(const value of ['absent','nope',null,new Error('boom'),Array.from({length:65},(_,i)=>({time:i,name:'s'}))]) {
      expect(await run(value)).toMatchObject({kind:'initialized',stops:[]});
    }
  });
});
