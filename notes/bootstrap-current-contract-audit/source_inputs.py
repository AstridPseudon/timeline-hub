"""Read Git objects without Node subprocess/signal restrictions; no source mutation."""
import json
import os
from pathlib import Path
import subprocess

app = '/home/user/work/app'
agent = '/home/user/work/agent'
runtime = '/home/user/work/runtime'
base = '7bb885b638838588a0dff81b64b7c34960ac07f3'
stage = 'f0112b846c1084b0902cdba091442cc840d8e88d'
fixed = '3a1d9c8524f37a2960d37d1b892d041b4c19ed0b'
entries = []
for sha in [base, stage, fixed, '44f0b9ca9d0247d909f86f56955a04ef6c18a2aa']:
    for file in ['src/integrations/runtime/createDefaultTimeline.ts', 'src/integrations/runtime/createDefaultTimeline.test.ts']:
        entries.append((app, sha, file))
for sha in ['31d02d45ad21f452724091b94b285478d00c9c21', 'a2ba1bca3cb68a15abb62a1260162c4cb73903af', '26ef2bbb31b4892fdd7c15ee5b20700bd40cb933', '487ca1e0d74edf4aecdd2b4e045294ab089fc273']:
    entries.append((agent, sha, 'astrid/core/timeline/schema/edit-command.schema.json'))
entries.append((runtime, 'f7081c14efd9a5b834987e7a1e2abf597b66313b', 'contract/schemas/edit-command.json'))
entries.append((app, stage, 'src/tools/video-editor/commands/fixtures/recipe_m2_app_bootstrap.json'))
blobs = {json.dumps(entry, separators=(',', ':')): subprocess.check_output(['git', '-C', entry[0], 'show', f'{entry[1]}:{entry[2]}'], text=True) for entry in entries}
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
(Path(os.environ['AUDIT_NOTES']) / 'source-inputs.json').write_text(json.dumps({'head': head, 'blobs': blobs}))
print('PASS exact Git source inputs read')
