"""Offline controller checks. Never requests a service run or starts a browser."""
import ast
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-root-smoke-central-ready'
controller = Path(str(PREFIX) + '-controller.py')
ast.parse(controller.read_text())
spec = importlib.util.spec_from_file_location('root_smoke_controller', controller)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
c.quiet()

original = (c.SOURCE / 'remotion/__smoke__/bundle.mjs').read_text()
invocation = c.smoke_invocation(original)
start, end = 'const EXPECTED_ALLOWED =', 'const main = async () => {'
assert original.split(start)[1].split(end)[0] == invocation.split(start)[1].split(end)[0]
loop_start = '  for (const fixture of FIXTURES)'
original_loop = original.split(loop_start)[1].split('  console.log(`Smoke bundle OK')[0]
staged_loop = invocation.split(loop_start)[1].split('  const empty =')[0]
assert original_loop == staged_loop.replace('      ...browserOptions,\n', '')
assert original.split('  console.log(`Smoke bundle OK')[1] == invocation.split('  console.log(`Smoke bundle OK')[1]
assert "chromeMode: 'chrome-for-testing'" in invocation
assert 'enableCaching: false' in invocation
assert "if (empty.durationInFrames !== 1)" in invocation
assert 'inputProps' not in invocation.split('  const empty =')[1].split('  });')[0]
print('PASS: original closed snapshots, fixtures, metadata assertions, success/failure paths preserved; empty uses actual Root defaults')

before = json.loads(c.artifact('prepare-pre.json').read_text())
after = json.loads(c.artifact('prepare-finally.json').read_text())
assert before == after
ready = json.loads(c.artifact('READY.json').read_text())
assert ready['controller_hashes'] == c.controller_hashes()
assert ready['pre_manifest_sha256'] == c.digest(c.artifact('prepare-pre.json'))
assert ready['archive_members'] == 77
print('PASS: READY/controller binding; all tracked source, complete borrowed graph, browser installation and Node unchanged')

wrapper = str(c.artifact('READY.sh'))
subprocess.run(['bash', '-n', wrapper], check=True)
refused = subprocess.run(['bash', wrapper], cwd=c.SOURCE, text=True, capture_output=True)
assert refused.returncode == 1 and 'central snapshot required' in refused.stderr
assert not (c.OWN / 'READY_GRANTED').exists()
fake_cwd = Path(tempfile.mkdtemp(prefix='.test-' + c.NAME + '-e2e-viewing-public10-root-smoke-', dir=c.OWN))
try:
    refused = subprocess.run(['bash', wrapper], cwd=fake_cwd, text=True, capture_output=True)
    assert refused.returncode == 1 and 'READY_GRANTED' in refused.stderr and 'FileNotFoundError' in refused.stderr
finally:
    shutil.rmtree(fake_cwd)
assert not (c.OWN / 'ATTEMPT_STARTED').exists()
assert not c.artifact('smoke.log').exists()
assert not list(c.OWN.glob(c.NAME + '-prepare-*'))
assert not list(c.OWN.glob(c.NAME + '-run-*'))
assert not c.git(c.SOURCE, 'status', '--porcelain', '--untracked-files=all')
print('PASS: noncentral invocation refused; missing manager grant refused before source/browser work; no attempt consumed; staging cleaned; repository clean')
