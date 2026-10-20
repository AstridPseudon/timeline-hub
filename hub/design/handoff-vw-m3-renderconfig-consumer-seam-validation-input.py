"""Stream frozen source to artifact checks; keep no copied source tree."""
from pathlib import Path
import json
import subprocess

prefix = str(Path(__file__)).removesuffix('-validation-input.py')
identity = json.loads(Path(prefix + '-source-identity.json').read_text())
print(json.dumps({name: subprocess.check_output(
    ['git', 'show', identity['base'] + ':' + name],
    cwd='/home/user/work/wt/vw-m3-renderconfig-consumer-seam', text=True,
) for name in identity['sha256']}))
