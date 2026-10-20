import json, os, subprocess, sys
from pathlib import Path
base=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
w=base/'workers/vw-m3-tab-clean-install-source-compose'
repo=Path('/home/user/work/wt/vw-m3-tab-clean-install-source-compose')
node='/tmp/vw-m3-agent-gate-node20.19.4/bin/node'
env=dict(os.environ, TMPDIR=str(w/'tmp'), TMP=str(w/'tmp'), TEMP=str(w/'tmp'), XDG_CACHE_HOME=str(w/'cache'), XDG_CONFIG_HOME=str(w/'config'), PWTEST_CACHE_DIR=str(w/'playwright-transform'), PLAYWRIGHT_OUTPUT_DIR=str(w/'playwright-output'), NODE_PATH='')
env['PATH']=str(Path(node).parent)+':'+env['PATH']
commands=[
 [node, 'tests/e2e/timeline/tab-audio-capture.analysis.test.mjs'],
 [node, 'tests/e2e/timeline/tab-audio-capture.controller.test.mjs'],
 [node, 'tests/e2e/timeline/tab-audio-capture.environment.test.mjs'],
 [node, 'node_modules/typescript/bin/tsc', '--noEmit', '--target', 'ES2022', '--lib', 'ES2023,DOM', '--module', 'ESNext', '--moduleResolution', 'bundler', '--strict', '--skipLibCheck', '--allowJs', '--resolveJsonModule', '--types', 'node', 'tests/e2e/timeline/tab-audio-capture.probe.ts', 'tests/e2e/timeline/tab-audio-capture.config.ts'],
 [node, 'node_modules/eslint/bin/eslint.js', '--no-cache', *['tests/e2e/timeline/'+p for p in ['tab-audio-capture.probe.ts','tab-audio-capture.config.ts','tab-audio-capture.analysis.mjs','tab-audio-capture.analysis.test.mjs','tab-audio-capture.controller.mjs','tab-audio-capture.controller.test.mjs','tab-audio-capture.environment.test.mjs']], '--max-warnings', '0'],
 [node, 'node_modules/vitest/vitest.mjs', 'run', '--config', str(w/'pure-preflight.config.mjs'), '--configLoader=runner', '--no-cache', 'src/tools/video-editor/compositions/playerEvaluation.test.ts'],
 ['bash', '-n', 'tests/e2e/timeline/setup-tab-audio-capture.sh'],
]
results=[]
with (base/'design/handoff-vw-m3-tab-clean-install-source-compose-static.log').open('w') as log:
 for command in commands:
  print('RUN', ' '.join(command), flush=True)
  log.write('COMMAND '+json.dumps(command)+'\n'); log.flush()
  result=subprocess.run(command,cwd=repo,env=env,stdout=log,stderr=subprocess.STDOUT)
  results.append({'command':command,'exit':result.returncode})
  log.write('EXIT '+str(result.returncode)+'\n'); log.flush()
  print('EXIT', result.returncode, flush=True)
(base/'design/handoff-vw-m3-tab-clean-install-source-compose-tests.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(int(any(r['exit'] for r in results)))
