#!/bin/bash
set -eu
app_root=/home/user/work/wt/ap2-m2-private014-first-admission-guard-fix
worker=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-private014-first-admission-guard-fix
overlay="$app_root/.private014-admission"
test ! -e "$overlay"
mkdir "$overlay"
trap 'rm -rf "$overlay"' EXIT HUP INT TERM
export APP_SOURCE="$app_root" PRIVATE_APP="$overlay" WORKER_ROOT="$worker"
python3 - <<'PY'
import hashlib, json, os, shutil, subprocess
from pathlib import Path
source, overlay, worker = [Path(os.environ[key]) for key in ['APP_SOURCE','PRIVATE_APP','WORKER_ROOT']]
for name in subprocess.check_output(['git','-C',str(source),'ls-files','-z']).decode().split('\0'):
    if not name: continue
    target=overlay/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source/name,target,follow_symlinks=False)
shutil.copy2(source/'src/test/threeProductsAuthoring.test.ts',overlay/'src/test/threeProductsAuthoring.test.ts')
shutil.copy2(worker/'native014Admission.test.tsx',overlay/'src/test/native014Admission.test.tsx')
lock=json.loads((overlay/'runtime.lock.json').read_text())
runtime=worker/'sources/runtime'
manifest=json.loads((runtime/'contract/artifacts.json').read_text())
assert manifest['version']=='sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0'
assert hashlib.sha256((runtime/'contract/artifacts.json').read_bytes()).hexdigest()=='ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815'
for name,expected in manifest['artifacts'].items():
    assert 'sha256:'+hashlib.sha256((runtime/name).read_bytes()).hexdigest()==expected,name
for consumer,entry in lock['files'].items():
    data=(runtime/entry['from']).read_bytes()
    entry['sha256']='sha256:'+hashlib.sha256(data).hexdigest()
    assert entry['sha256']==manifest['artifacts'][entry['from']]
    (overlay/consumer).write_bytes(data)
lock['source_commit']='202074110717146fc7f08af2306a8dd7f695b0b1'
lock['producer_version']=manifest['version']
(overlay/'runtime.lock.json').write_text(json.dumps(lock,indent=2)+'\n')
for name,expected in [('generated.ts','c422ce38279e6df9eb93c5b53993d57e68339b0807d34ed69d85b2408ed98be2'),('generated-contract-metadata.ts','9b3b8723a8d86a78d57bf83f43eb82914d1d0cd81ae89ebdf993b1560ddc57dd')]:
    assert hashlib.sha256((overlay/'src/integrations/runtime'/name).read_bytes()).hexdigest()==expected
print('Private Runtime014 sources and manifest verified; public lock untouched.')
PY
graph=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph/node_modules
test "$(realpath "$graph")" = "$graph"
ln -s "$graph" "$overlay/node_modules"
cd "$overlay"
node scripts/vendor-lock.mjs check runtime.lock.json
export NATIVE_ADMISSION_FIXTURE="$worker/native-admission.json"
node --require "$worker/vitest-runner.cjs" node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  "$@"
# Original 137-test invocation also selected the following neighbours:
# src/test/native014Admission.test.tsx src/test/threeProductsAuthoring.test.ts
# # src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts
# # src/integrations/runtime/timelineCommit.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
# # src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx
# # src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx
# # src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
