"""Tiny committed fixture sources; never reads or copies a product checkout."""
import os
from pathlib import Path
import subprocess

CAP = 100 * 1024 * 1024

def footprint(label):
    root = Path(os.environ['TMPDIR']).resolve()
    size = sum(p.lstat().st_size for p in root.rglob('*'))
    allocated = sum(p.lstat().st_blocks * 512 for p in root.rglob('*'))
    print(f'FOOTPRINT {label} logical={size} allocated={allocated} cap={CAP}', flush=True)
    assert max(size, allocated) <= CAP, 'fixture expansion stopped: 100 MiB cap'
    return size, allocated

def make_sources(root):
    footprint('before-source-group')
    common = '[project]\nname = "{name}"\nversion = "0.1.0"\n[tool.setuptools.packages.find]\ninclude = {include}\n'
    client = {'astrid_runtime_client/__init__.py': b'"""Fixture generated client."""\n', 'astrid_runtime_client/generated.py': b'CLIENT_VERSION = 1\n'}
    data = {
        'agent': {'pyproject.toml': common.format(name='astrid', include='["astrid*"]').encode(), 'astrid/__init__.py': b'VERSION = "0.1.0"\n', 'astrid/nested/__init__.py': b'', 'astrid/nested/command.py': b'def command(): return 1\n', 'README.md': b'Tiny Agent source completeness sentinel\n', **client},
        'runtime': {'pyproject.toml': common.format(name='astrid-runtime', include='["astrid_runtime*", "runtime_protocol*"]').encode(), 'astrid_runtime/__init__.py': b'VERSION = "0.1.0"\n', 'runtime_protocol/__init__.py': b'VERSION = 1\n', 'README.md': b'Tiny Runtime source completeness sentinel\n', **{'packages/python/' + p: content for p, content in client.items()}},
    }
    repos = {}
    for name, files in data.items():
        repo = root / ('checkout-' + name)
        repo.mkdir()
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)
        # fast-import makes fixture commits without any git commit command or
        # touching real repository refs, indexes, or configuration.
        stream = b'commit refs/heads/fixture\ncommitter Fixture <fixture@example.invalid> 1 +0000\ndata 7\nfixture\n'
        for rel, content in sorted(files.items()):
            stream += f'M 100644 inline {rel}\ndata {len(content)}\n'.encode() + content + b'\n'
        stream += b'\ndone\n'
        subprocess.run(['git', '-C', str(repo), 'fast-import', '--quiet'], input=stream, check=True)
        # Set HEAD only in this tiny synthetic repository via normal Git API.
        subprocess.run(['git', '-C', str(repo), 'symbolic-ref', 'HEAD', 'refs/heads/fixture'], check=True)
        subprocess.run(['git', '-C', str(repo), 'reset', '--hard', '--quiet', 'HEAD'], check=True)
        repos[name] = repo
    footprint('after-source-group')
    return repos['agent'], repos['runtime']
