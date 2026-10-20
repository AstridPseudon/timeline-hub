import collections
import json
import re
import subprocess
from pathlib import Path

repo = Path('/home/user/work/wt/vw-m3-pcm-native-window-resume-r1')
worker = Path(__file__).parent
prefix = worker.parents[1] / 'design/handoff-vw-m3-pcm-native-window-resume-r1'
python = '/home/user/work/venv-agent/bin/python'
paths = subprocess.check_output(['git', 'diff', '--name-only'], cwd=repo, text=True).splitlines()
current = {path: (repo / path).read_bytes() for path in paths}
ruff_command = [python, '-m', 'ruff', 'check', '--no-cache', '--isolated', '--select', 'E4,E7,E9,F,I,BLE', '--output-format', 'json', *paths, 'tests/packs/rendering/test_normal_audio_run.py']
mypy_command = [python, '-m', 'mypy', '--follow-imports=skip', '--no-incremental', '--cache-dir=' + str(worker / 'mypy-cache'), '--hide-error-context', '--no-color-output', '--no-pretty', '--show-error-codes', *paths]

def checks(label):
    ruff = subprocess.run(ruff_command, cwd=repo, capture_output=True, text=True)
    findings = json.loads(ruff.stdout)
    ruff_rows = collections.Counter((Path(row['filename']).relative_to(repo).as_posix(), row['code'], row['message']) for row in findings)
    mypy = subprocess.run(mypy_command, cwd=repo, capture_output=True, text=True)
    mypy_rows = collections.Counter()
    for line in mypy.stdout.splitlines():
        match = re.match(r'(.+?):\d+: error: (.+)', line)
        if match:
            mypy_rows[match.groups()] += 1
    for tool, command, result in [('ruff', ruff_command, ruff), ('mypy', mypy_command, mypy)]:
        Path(str(prefix) + f'-{tool}-{label}.log').write_text('$ ' + ' '.join(command) + '\n' + result.stdout + result.stderr + f'\nexit={result.returncode}\n')
    return {'ruff': ruff_rows, 'mypy': mypy_rows}

now = checks('current')
try:
    for path in paths:
        (repo / path).write_bytes(subprocess.check_output(['git', 'show', '2019d7e69:' + path], cwd=repo))
    base = checks('base')
finally:
    for path, data in current.items():
        (repo / path).write_bytes(data)
result = {tool: {'base_count': sum(base[tool].values()), 'current_count': sum(now[tool].values()),
                 'added': list((now[tool] - base[tool]).elements()),
                 'removed': list((base[tool] - now[tool]).elements())} for tool in now}
Path(str(prefix) + '-static-delta.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
assert all(not value['added'] for value in result.values())
