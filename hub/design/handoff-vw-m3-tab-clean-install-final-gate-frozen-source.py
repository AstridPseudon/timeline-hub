import hashlib,json,subprocess
from pathlib import Path
O=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch');D=O/'design';W=O/'workers/vw-m3-tab-clean-install-final-gate';R='/home/user/work/app'
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
sha=git('rev-parse','tl/vw-m3-tab-clean-install-source-compose').decode().strip();base='0ea988bdd2907c876b82fd2620820e3fb6d6ea84'
meta=json.loads((D/'handoff-vw-m3-tab-clean-install-source-compose-metadata.json').read_text())
changes=git('diff','--name-status',base,sha).decode().splitlines();assert set(changes)=={'A\t'+p for p in meta['files']}
entries=[]
for row in git('ls-tree','-rz','--full-tree',sha).split(b'\0'):
 if row:
  header,name=row.split(b'\t');mode,kind,blob=header.decode().split();assert kind=='blob';entries.append((name.decode(),blob))
entries.sort();batch=subprocess.run(['git','cat-file','--batch'],cwd=R,input=('\n'.join(b for p,b in entries)+'\n').encode(),capture_output=True,check=True).stdout
full=hashlib.sha256();inputs=hashlib.sha256();position=0;fingerprint=json.loads((D/'handoff-vw-m3-tab-clean-install-final-gate-fingerprint.json').read_text());selected=set(fingerprint['inputFiles'])
for path,blob in entries:
 end=batch.index(b'\n',position);header=batch[position:end].split();size=int(header[2]);data=batch[end+1:end+1+size];position=end+size+2
 assert header[0].decode()==blob and len(data)==size
 if path=='CLAUDE.md': data=git('show',sha+':'+data.decode())
 framed=path.encode()+b'\0'+data+b'\0';full.update(framed)
 if path in selected:inputs.update(framed)
 if path in meta['files']:
  assert hashlib.sha256(data).hexdigest()==meta['files'][path]
  assert data==(D/('handoff-vw-m3-tab-clean-install-source-compose-'+Path(path).name)).read_bytes()
  target=W/'source'/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
print('reconstructed',full.hexdigest(),inputs.hexdigest(),'expected',meta['fullTrackedHash'],meta['inputHash'],'count',len(entries),flush=True)
assert full.hexdigest()==meta['fullTrackedHash'] and inputs.hexdigest()==meta['inputHash']
(W/'source/node_modules').symlink_to(O/'workers/vw-m3-app-private12-clean-install/clean-project/node_modules',target_is_directory=True)
result={'sourceSha':sha,'sourceTree':git('rev-parse',sha+'^{tree}').decode().strip(),'baseSha':base,'changes':changes,'files':meta['files'],'fullTrackedHash':full.hexdigest(),'inputHash':inputs.hexdigest(),'trackedFileCount':len(entries),'flatSourcesMatchCommit':True,'emptyGrantTemplateBytes':(D/'handoff-vw-m3-tab-clean-install-source-compose-manager-only-grant-template.json').stat().st_size}
assert result['emptyGrantTemplateBytes']==0
(D/'handoff-vw-m3-tab-clean-install-final-gate-frozen-source.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
