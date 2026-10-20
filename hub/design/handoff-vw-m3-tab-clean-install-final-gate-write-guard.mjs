import fs from 'node:fs';
import fsp from 'node:fs/promises';
import {syncBuiltinESMExports} from 'node:module';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import net from 'node:net';
const own='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-clean-install-final-gate';
function allowed(p) {
 if (typeof p === 'number') return;
 const path=resolve(p instanceof URL ? fileURLToPath(p) : String(p));
 if (path !== own && !path.startsWith(own+'/')) throw new Error('Reviewer write boundary: '+path);
}
for (const [object,names] of [[fs,['writeFileSync','appendFileSync','rmSync','unlinkSync','chmodSync','truncateSync']],[fsp,['writeFile','appendFile','rm','unlink','chmod','truncate']]]) {
 for (const name of names) {const original=object[name];object[name]=function(p,...args){allowed(p);return original.call(this,p,...args);};}
}
for (const [object,name] of [[fs,'mkdirSync'],[fsp,'mkdir']]) {
 const original=object[name];object[name]=function(p,...args){
  // Frozen config ensures its state directories exist. Existing directories need no write.
  if (fs.existsSync(p) && fs.statSync(p).isDirectory()) return object===fsp ? Promise.resolve(undefined) : undefined;
  allowed(p);return original.call(this,p,...args);
 };
}
net.Server.prototype.listen=function(){throw new Error('Listeners forbidden in reviewer discovery');};
syncBuiltinESMExports();
