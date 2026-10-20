import { defineConfig } from '/home/user/work/app/node_modules/vitest/dist/config.js';
import path from 'node:path';
const orch='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch';
const work=path.join(orch,'workers/vw-m3-app-delivered-theme-seam');
const root=path.join(work,'offline-app');
const modules='/home/user/work/app/node_modules';
export default defineConfig({
 plugins:[{name:'offline-empty-admissions',resolveId(id){if(id==='virtual:astrid-element-admissions')return '\0offline-admissions';},load(id){if(id==='\0offline-admissions')return 'export const configured=false; export const projectId=null; export const selectionDigest="empty"; export const realmId=null; export const projects=[]; export const elements=[]; export const components={};';}}],
 server:{fs:{allow:[root,work,path.join(work,'agent-source'),modules]}},
 root, cacheDir:path.join(work,'vite-cache'),
 oxc:{jsx:{runtime:'automatic'}},
 resolve:{alias:[
  {find:/^@banodoco\/timeline-composition$/,replacement:path.join(work,'public10/package/dist/index.js')},
  {find:/^@banodoco\/timeline-composition\/(.*)$/,replacement:path.join(work,'public10/package/dist/$1.js')},
  {find:'@astrid/editor-sdk',replacement:path.join(root,'src/sdk/index.ts')},
  {find:'@astrid',replacement:path.join(work,'agent-source/astrid')},
  {find:'@test-react-refresh',replacement:path.join(modules,'@vitejs/plugin-react-swc/refresh-runtime.js')},
  {find:'@',replacement:path.join(root,'src')},
  {find:'fake-indexeddb',replacement:path.join(root,'vendor/fake-indexeddb/index.js')},
  {find:'@banodoco/timeline-schema',replacement:path.join(root,'src/test/shims/banodoco/timeline-schema.ts')},
  ...['react','react-dom','remotion','@remotion/layout-utils','@remotion/media'].map(name=>({find:name,replacement:path.join(modules,name)})),
 ],dedupe:['react','react-dom','remotion','@remotion/media','@remotion/layout-utils']},
 test:{globals:true,environment:'jsdom',include:['src/**/*.test.{ts,tsx}'],setupFiles:[path.join(root,'src/test/reactRefreshSetup.ts'),path.join(root,'src/test/setup.ts')],maxWorkers:1,minWorkers:1,testTimeout:30000},
});
