import base64
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from support import MAKER


TRUSTED = {
    'url': 'https://github.com/banodoco/ArtAgents.git',
    'commit': '242f9c4306bf3b501222cb041a9eb246ef47bc85',
    'subdirectory': 'packages/timeline-schema/python',
    'source_tree': '75a5a697f630affee40632e500b3f5b704a9b834',
}
DIST = 'banodoco_timeline_schema-0.0.2.dist-info'
PACKAGE = 'banodoco_timeline_schema'
UNHASHED = {
    f'{DIST}/RECORD',
    f'{PACKAGE}/__pycache__/__init__.cpython-313.pyc',
    f'{PACKAGE}/__pycache__/generated.cpython-313.pyc',
    f'{PACKAGE}/__pycache__/materialize.cpython-313.pyc',
    f'{PACKAGE}/__pycache__/theme.cpython-313.pyc',
    f'{PACKAGE}/__pycache__/validate.cpython-313.pyc',
}
HASHED = [
    f'{DIST}/INSTALLER', f'{DIST}/METADATA', f'{DIST}/REQUESTED',
    f'{DIST}/WHEEL', f'{DIST}/direct_url.json', f'{DIST}/top_level.txt',
    f'{PACKAGE}/__init__.py', f'{PACKAGE}/generated.py',
    f'{PACKAGE}/materialize.py', f'{PACKAGE}/theme.py',
    f'{PACKAGE}/timeline.schema.json', f'{PACKAGE}/validate.py',
]


def record_row(path, data):
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip('=')
    return [path, f'sha256={digest}', str(len(data))]


class SchemaFixture:
    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='d139-schema-installed-')
        self.root = Path(self.temporary.name)
        self.site = self.root / 'site-packages'
        self.dist = self.site / DIST
        self.package = self.site / PACKAGE
        self.dist.mkdir(parents=True)
        self.package.mkdir()
        self.direct = {
            'subdirectory': TRUSTED['subdirectory'],
            'url': TRUSTED['url'],
            'vcs_info': {
                'commit_id': TRUSTED['commit'],
                'requested_revision': TRUSTED['commit'],
                'vcs': 'git',
            },
        }
        metadata = {
            'INSTALLER': b'pip\n',
            'METADATA': b'Metadata-Version: 2.4\nName: banodoco-timeline-schema\nVersion: 0.0.2\n',
            'REQUESTED': b'',
            'WHEEL': b'Wheel-Version: 1.0\nGenerator: test\n',
            'direct_url.json': json.dumps(self.direct, sort_keys=True).encode(),
            'top_level.txt': b'banodoco_timeline_schema\n',
        }
        sources = {
            '__init__.py': b'VALUE = 1\n',
            'generated.py': b'VALUE = 2\n',
            'materialize.py': b'VALUE = 3\n',
            'theme.py': b'VALUE = 4\n',
            'timeline.schema.json': b'{"type":"object"}\n',
            'validate.py': b'VALUE = 5\n',
        }
        for name, data in metadata.items():
            (self.dist / name).write_bytes(data)
        for name, data in sources.items():
            (self.package / name).write_bytes(data)
        for name in ('__init__', 'generated', 'materialize', 'theme', 'validate'):
            (self.package / '__pycache__').mkdir(exist_ok=True)
            (self.package / '__pycache__' / f'{name}.cpython-313.pyc').write_bytes(
                b'\x00\x00\x00\x00synthetic-cache')
        rows = []
        for rel in HASHED:
            path = self.site / rel
            rows.append(record_row(rel, path.read_bytes()))
        rows.extend([[rel, '', ''] for rel in sorted(UNHASHED)])
        with (self.dist / 'RECORD').open('w', newline='') as stream:
            csv.writer(stream).writerows(rows)
        self.manifest = self.root / 'source-manifest.json'
        self.manifest.write_text(json.dumps(TRUSTED, sort_keys=True))

    def close(self):
        self.temporary.cleanup()


def admission_namespace():
    text = MAKER.read_text()
    source = text.split("<<'STORE_PY'\n", 1)[1].split('\nSTORE_PY\n', 1)[0]
    start = source.index('identity = {')
    snippet = source[start:source.index('seed_helper = pathlib.Path(script)')]
    namespace = {
        'agent': 'a' * 40,
        'backend': 'b' * 40,
        'client': 'packages/python/client=' + '0' * 64,
        'schema_required': '1',
        'schema_source': '',
        'schema_manifest': '',
        'schema_installed_distribution': '',
        'context': '',
        'root': '/tmp',
        'tempfile': tempfile,
    }
    prefix = 'import base64, csv, hashlib, io, json, os, pathlib, re, shlex, stat, tempfile\n'
    return source, snippet, prefix, namespace


class InstalledSchemaControls(unittest.TestCase):
    def run_admission(self, fixture, **changes):
        source, snippet, prefix, namespace = admission_namespace()
        namespace['schema_installed_distribution'] = str(fixture.dist)
        namespace['schema_manifest'] = str(fixture.manifest)
        namespace.update(changes)
        exec(compile(prefix + snippet, '<schema-admission>', 'exec'), namespace)
        return namespace

    def test_pinned_auth_positive_snapshots_exact_record_closure(self):
        fixture = SchemaFixture()
        try:
            (fixture.site / 'unrelated_distribution').mkdir()
            (fixture.site / 'unrelated_distribution' / '__init__.py').write_text('unrelated = True\n')
            namespace = self.run_admission(fixture)
            identity = json.loads(namespace['schema_identity_json'])
            self.assertEqual(identity['input_kind'], 'installed_distribution')
            self.assertEqual(identity['record_rows'], 18)
            self.assertEqual(identity['record_hashed_rows'], 12)
            self.assertEqual(identity['record_unhashed_rows'], sorted(UNHASHED))
            self.assertEqual(identity['tree_tie'], 'UNAVAILABLE')
            snapshot = Path(namespace['schema_source'])
            self.assertEqual(
                {path.relative_to(snapshot).as_posix() for path in snapshot.rglob('*') if path.is_file()},
                set(HASHED) | UNHASHED,
            )
            self.assertTrue(all(path.stat().st_nlink == 1 for path in snapshot.rglob('*') if path.is_file()))
        finally:
            fixture.close()

    def test_metadata_commit_vcs_and_editable_inputs_refuse(self):
        for mutation in ('commit', 'missing-vcs', 'vcs', 'editable'):
            with self.subTest(mutation=mutation):
                fixture = SchemaFixture()
                try:
                    direct = dict(fixture.direct)
                    direct['vcs_info'] = dict(direct['vcs_info'])
                    if mutation == 'commit':
                        direct['vcs_info']['commit_id'] = '0' * 40
                    elif mutation == 'missing-vcs':
                        direct.pop('vcs_info')
                    elif mutation == 'vcs':
                        direct['vcs_info']['vcs'] = 'hg'
                    else:
                        direct = {'url': 'file:///local/schema', 'dir_info': {'editable': True}}
                    (fixture.dist / 'direct_url.json').write_text(json.dumps(direct))
                    with self.assertRaisesRegex(RuntimeError, 'sourceNOT_READY'):
                        self.run_admission(fixture)
                finally:
                    fixture.close()

    def test_record_hash_unhashed_and_unlisted_controls_refuse(self):
        mutations = ('hashed-mismatch', 'unhashed-code', 'unlisted-file')
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                fixture = SchemaFixture()
                try:
                    record = fixture.dist / 'RECORD'
                    rows = list(csv.reader(record.read_text().splitlines()))
                    if mutation == 'hashed-mismatch':
                        rows[0][1] = 'sha256=' + 'A' * 43
                    elif mutation == 'unhashed-code':
                        row = next(row for row in rows if row[0].endswith('/__init__.py'))
                        row[1:] = ['', '']
                    else:
                        extra = fixture.package / 'unlisted.py'
                        extra.write_text('extra = True\n')
                    with record.open('w', newline='') as stream:
                        csv.writer(stream).writerows(rows)
                    with self.assertRaisesRegex(RuntimeError, 'sourceNOT_READY'):
                        self.run_admission(fixture)
                finally:
                    fixture.close()

    def test_each_unhashed_name_is_classified_exactly(self):
        for path in sorted(UNHASHED):
            fixture = SchemaFixture()
            try:
                rows = list(csv.reader((fixture.dist / 'RECORD').read_text().splitlines()))
                changed = next(item for item in sorted(UNHASHED) if item != path)
                for row in rows:
                    if row[0] == changed:
                        row[1:] = record_row(changed, (fixture.site / changed).read_bytes())[1:]
                with (fixture.dist / 'RECORD').open('w', newline='') as stream:
                    csv.writer(stream).writerows(rows)
                with self.assertRaisesRegex(RuntimeError, 'sourceNOT_READY'):
                    self.run_admission(fixture)
            finally:
                fixture.close()

    def test_source_replacement_and_race_refuse_before_snapshot_identity(self):
        fixture = SchemaFixture()
        try:
            target = fixture.package / '__init__.py'
            original = Path.read_bytes
            reads = {'count': 0}

            def raced(path):
                if path == target:
                    reads['count'] += 1
                    if reads['count'] == 2:
                        target.write_text('replaced = True\n')
                return original(path)

            Path.read_bytes = raced
            try:
                with self.assertRaisesRegex(RuntimeError, 'sourceNOT_READY'):
                    self.run_admission(fixture)
            finally:
                Path.read_bytes = original
        finally:
            fixture.close()

    def test_real_cli_refuses_before_store_publication(self):
        fixture = SchemaFixture()
        try:
            direct = dict(fixture.direct)
            direct['vcs_info'] = dict(direct['vcs_info'])
            direct['vcs_info']['commit_id'] = '0' * 40
            (fixture.dist / 'direct_url.json').write_text(json.dumps(direct))
            (fixture.root / 'work').mkdir()
            result = subprocess.run(
                [str(MAKER), 'venv-agent-child-d139-schema-refusal',
                 subprocess.check_output(['git', '-C', '/home/user/work/agent', 'rev-parse', 'HEAD'], text=True).strip(),
                 '--source-carrier', '/home/user/work/agent', '/home/user/work/runtime',
                 subprocess.check_output(['git', '-C', '/home/user/work/runtime', 'rev-parse', 'HEAD'], text=True).strip(),
                 '--schema-installed-distribution', str(fixture.dist),
                 '--schema-source-manifest', str(fixture.manifest)],
                capture_output=True, text=True, check=False,
                env={**os.environ, 'CHILD_VENV_WORK_ROOT': str(fixture.root / 'work')},
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('sourceNOT_READY', result.stderr)
            self.assertNotIn('bench store', result.stderr.lower())
        finally:
            fixture.close()


if __name__ == '__main__':
    unittest.main()
