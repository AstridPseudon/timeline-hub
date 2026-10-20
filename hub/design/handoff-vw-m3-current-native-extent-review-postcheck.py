from pathlib import Path
import base64, hashlib, json, os, subprocess, tarfile
O=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
P=O/'design/handoff-vw-m3-current-native-extent-review'
W=O/'workers/vw-m3-current-native-extent-review'
C=W/'candidate'
m=json.loads(Path(str(P)+'-all-blobs.json').read_text())
for n,v in m.items():
 p=C/n
 b=os.readlink(p).encode() if p.is_symlink() else p.read_bytes()
 assert hashlib.sha256(b).hexdigest()==v['sha256'],n
refs=subprocess.check_output(['git','rev-parse','tl/vw-m3-current-native-extent-unit','HEAD'],text=True).splitlines()
s=json.loads(Path(str(P)+'-sourcebytes.json').read_text())
assert refs==[s['candidate'],s['base']]
assert not subprocess.check_output(['git','status','--porcelain']).strip()
mods=W/'root-modules/node_modules'
assert not mods.is_symlink()
assert list(p.name for p in mods.iterdir())==['typescript']
assert (mods/'typescript').is_symlink()
assert (mods/'typescript').resolve()==Path('/home/user/work/app/node_modules/typescript')
a=C/'remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz'
lock=json.loads((C/'remotion/package-lock.json').read_text())['packages']['node_modules/@banodoco/timeline-composition']
assert lock['version']=='0.0.10'
assert lock['integrity']=='sha512-'+base64.b64encode(hashlib.sha512(a.read_bytes()).digest()).decode()
with tarfile.open(a) as t:duration=t.extractfile('package/dist/chunk-SE4TPVLW.js').read()
heldoriginal=Path(str(P)+'-held-tail-original.py').read_text()
assert heldoriginal==subprocess.check_output(['git','show','e2d926319:tests/packs/rendering/test_remotion_layer_tail_compat.py'],text=True)
held=Path(str(P)+'-held-tail-test.py').read_text()
expected=heldoriginal.replace('_ROOT = Path(__file__).resolve().parents[3]',"_ROOT = Path(__import__('os').environ['REVIEW_SOURCE_ROOT'])").replace('banodoco-timeline-composition-0.0.12.tgz','banodoco-timeline-composition-0.0.10.tgz')
assert held.startswith(expected)
out={'all_2997_tracked_blobs_equal_after_tests':True,'candidate_ref_still_frozen':refs[0],'reviewer_head':refs[1],'reviewer_checkout_clean':True,'private_modules_exact_leaves':['typescript'],'node_version':subprocess.check_output(['/tmp/vw-m3-agent-gate-node20.19.4/bin/node','--version'],text=True).strip(),'typescript_version':json.loads((mods/'typescript/package.json').read_text())['version'],'typescript_js_sha256':hashlib.sha256((mods/'typescript/lib/typescript.js').read_bytes()).hexdigest(),'composition_pin':'0.0.10','artifact_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'artifact_matches_lock_sha512':True,'extracted_duration_chunk_sha256':hashlib.sha256(duration).hexdigest(),'held_tail_original_sha256':hashlib.sha256(heldoriginal.encode()).hexdigest(),'held_tail_changes':'only source-root location and pinned tarball path; appended legacy-positive test; original three expectations unchanged'}
Path(str(P)+'-postcheck.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
