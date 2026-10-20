import base64, hashlib, io, json, os, stat, subprocess, sys, tarfile
from collections import Counter
from pathlib import Path
D=Path(__file__).parent
W=D.parent/'workers/vw-m3-tab-clean-install-final-gate'
P=D.parent/'workers/vw-m3-app-private12-clean-install/clean-project'
BASE='0ea988bdd2907c876b82fd2620820e3fb6d6ea84'
def sha(b): return hashlib.sha256(b).hexdigest()
def compact(v): return json.dumps(v,ensure_ascii=False,separators=(',',':')).encode()
def filehash(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def snapshot(root):
 rows=[]
 for parent,dirs,files in os.walk(root,followlinks=False):
  for name in dirs+files:
   p=Path(parent)/name;s=p.lstat();r={'path':p.relative_to(root).as_posix(),'mode':stat.S_IMODE(s.st_mode)}
   if stat.S_ISLNK(s.st_mode):r.update(kind='symlink',target=os.readlink(p),sha256=sha(os.readlink(p).encode()))
   elif stat.S_ISDIR(s.st_mode):r.update(kind='directory')
   elif stat.S_ISREG(s.st_mode):r.update(kind='executable' if s.st_mode&0o111 else 'file',bytes=s.st_size,sha256=filehash(p),device=s.st_dev,inode=s.st_ino,links=s.st_nlink)
   else: raise AssertionError(p)
   rows.append(r)
 return sorted(rows,key=lambda r:tuple(r['path'].split('/')))
def tree(rows,prefix,flat):
 tuples=[[r['path'][len(prefix):],r['kind'],r['sha256']] for r in rows if r['path'].startswith(prefix) and r['kind']!='directory']
 if flat:tuples.sort(key=lambda r:r[0])
 return {'sha256':sha(compact(tuples)),'fileCount':len(tuples)}
def git(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd='/home/user/work/app')
def main():
 assert os.statvfs(W).f_bavail*os.statvfs(W).f_frsize>=10*1024**3
 rows=snapshot(P)
 reference=json.loads((D/'handoff-vw-m3-app-private12-clean-install-manifest.json').read_text())
 assert rows==reference['entries'],'physical graph differs from READY'
 assert sha(compact(rows))==reference['sha256']
 links=[r for r in rows if r['kind']=='symlink']
 for r in links:
  p=P/r['path'];target=p.resolve(strict=True)
  assert not os.path.isabs(r['target']) and '.bin' in p.parts and target.is_file() and target.is_relative_to(P/'node_modules')
 regular=[r for r in rows if r['kind'] in ('file','executable')];inos=Counter((r['device'],r['inode']) for r in regular)
 assert all(inos[r['device'],r['inode']]==r['links'] and r['device']==P.stat().st_dev for r in regular)
 assert len(links)==36 and len(rows)==35641
 for rel in ['package.json','package-lock.json','vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz']:
  assert (P/rel).read_bytes()==git(rel)
 lock=json.loads(git('package-lock.json'));manifest=json.loads(git('package.json'))
 artifact=git('vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz')
 assert sha(artifact)=='0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
 assert lock['packages']['node_modules/@banodoco/timeline-composition']['integrity']=='sha512-'+base64.b64encode(hashlib.sha512(artifact).digest()).decode()
 archive=[]
 with tarfile.open(fileobj=io.BytesIO(artifact)) as t:
  for m in t:
   assert m.isfile() and m.name.startswith('package/') and '..' not in Path(m.name).parts
   rel=m.name[len('package/'):];b=t.extractfile(m).read();p=P/'node_modules/@banodoco/timeline-composition'/rel
   assert p.read_bytes()==b and bool(p.stat().st_mode&0o111)==bool(m.mode&0o111)
   archive.append([rel,'executable' if m.mode&0o111 else 'file',sha(b)])
 assert len(archive)==77 and len({r[0] for r in archive})==77
 canonical=sha(compact(sorted(archive,key=lambda r:r[0])))
 assert canonical=='71b44e67e4eeffb0f904bb3a21e24d12ba06c4b2e41d43592a859aced3bb3139'
 assert tree(rows,'node_modules/@banodoco/timeline-composition/',True)=={'sha256':canonical,'fileCount':77}
 meta=json.loads((D/'handoff-vw-m3-app-private12-clean-install-metadata.json').read_text())
 peers={}
 for name,v in meta['peerVersions'].items():
  p=P/'node_modules'/name
  assert json.loads((p/'package.json').read_text())['version']==v
  recursive=tree(rows,'node_modules/'+name+'/',False)
  assert recursive['sha256']==meta['peerTreeSha256'][name]
  peers[name]={'version':v,'recursiveTree':recursive,'canonicalTree':tree(rows,'node_modules/'+name+'/',True),'manifestSha256':filehash(p/'package.json')}
 result={'physicalManifestSha256':reference['sha256'],'entries':len(rows),'regularFiles':len(regular),'symlinks':len(links),'wholeNodeModulesCanonical':tree(rows,'node_modules/',True),'compositionCanonical':canonical,'compositionArchiveMembers':archive,'peers':peers,'freeBytes':os.statvfs(W).f_bavail*os.statvfs(W).f_frsize,'manifestSha256':sha(git('package.json')),'lockSha256':sha(git('package-lock.json'))}
 out=D/('handoff-vw-m3-tab-clean-install-final-gate-'+sys.argv[1]+'.json');out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('compositionArchiveMembers','peers')}))
if __name__=='__main__':main()
