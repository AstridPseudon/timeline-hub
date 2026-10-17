"""Trusted composition input for reusing one verified Remotion installation.

Never decode this binding from executor payloads or environment. A receipt is
not authority: the host composition supplies its independently admitted digest.
"""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

_PATCHES = {
    '@remotion/renderer/dist/get-cpu-count.js': 'd89ef6b67068fb8f1c0e2f21781a37205b4beb1a8f7ff7997ba82b49c835c2bb',
    '@remotion/renderer/dist/esm/index.mjs': '812dfecb6877a299a9a9b4704bf591baede53aa465eea92cc9b09c69b674050b',
    'remotion/dist/cjs/audio/shared-audio-tags.js': '949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8',
    'remotion/dist/esm/index.mjs': '5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28',
}

_RETAINED_TRANSPORT_PATCHES = {
    'serve-static.js': '94b7c486a0f646a95b297e4bd4eaec7244bef836a28ac6e0e89ff79d7b9e09c9',
    'prepare-server.js': '4bde104699dd7481469b2a7a48645a726e2f8c83b06f1177e5f7e808bacbeb04',
    'open-browser.js': '0dc0ebc6479feaf5db1b6e978c94fefd9efdc279868b859bf2c4d0699f2722a8',
    'browser/BrowserRunner.js': 'd6f8c27c94f64b49da1e501bc1dbbf1d9f6380888e37c12505b6f47201b0e451',
}


_SHA_CACHE = {}
_ROOT_SOURCE_SUFFIXES = frozenset({'.js', '.mjs', '.cjs', '.ts', '.tsx', '.json'})


def _root_sources(project):
    files = set()
    for path in project.iterdir():
        if path.suffix in _ROOT_SOURCE_SUFFIXES and path.is_file():
            if not path.resolve(strict=True).is_relative_to(project):
                raise ValueError('renderer root source contains an escaping file link')
            files.add(path)
    return files


def _sha(path):
    path = Path(path)
    def signature():
        value = path.stat()
        return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_ctime_ns)
    before = signature()
    cached = _SHA_CACHE.get(path)
    if cached is not None and cached[0] == before:
        return cached[1]
    value = hashlib.sha256(path.read_bytes()).hexdigest()
    if signature() != before:
        raise ValueError('renderer closure input changed while hashing')
    if len(_SHA_CACHE) >= 32768:
        _SHA_CACHE.clear()
    _SHA_CACHE[path] = (before, value)
    return value


@dataclass(frozen=True)
class RemotionClosureBinding:
    project: Path
    installed_project: Path
    receipt: Path
    receipt_digest: str
    manifest_digest: str
    lock_digest: str
    files: tuple[tuple[Path, str], ...]

    @classmethod
    def admit(cls, *, project, installed_project, verification_receipt, receipt_sha256,
              manifest_sha256, lock_sha256):
        """Bind explicit host-selected roots to an admitted SRI verification.

        The source lock/manifest, verified installed package graph, CPU/audio
        postimages and packed local Composition bytes all remain pinned.
        """
        project, installed, receipt = map(lambda p: Path(p).resolve(strict=True),
                                          (project, installed_project, verification_receipt))
        if _sha(receipt) != receipt_sha256:
            raise ValueError('renderer closure verification receipt changed')
        report = json.loads(receipt.read_bytes())
        if (report.get('passed') is not True or report.get('issues')
                or report.get('installed_sri_missing') or report.get('installed_sri_bad')
                or report.get('source', {}).get('manifest_sha256') != manifest_sha256
                or report.get('source', {}).get('lock_sha256') != lock_sha256
                or report.get('counts', {}).get('lock_sri_records_bad') != 0
                or report.get('counts', {}).get('lock_sri_records_missing_or_unverified') != 0):
            raise ValueError('renderer closure lacks the admitted SRI verification')
        for root in (project, installed):
            if _sha(root/'package.json') != manifest_sha256 or _sha(root/'package-lock.json') != lock_sha256:
                raise ValueError('renderer project differs from admitted manifest or lock')
        modules = installed/'node_modules'
        if modules.resolve(strict=True) != modules or not modules.is_dir():
            raise ValueError('installed renderer root must be a canonical directory')
        if (project/'node_modules').resolve(strict=True) != modules:
            raise ValueError('renderer dependency link differs from the admitted installation')
        lock = json.loads((project/'package-lock.json').read_bytes())
        files = {receipt: receipt_sha256}
        for root in (project, installed):
            files[root/'package.json'] = manifest_sha256
            files[root/'package-lock.json'] = lock_sha256
        versions = report.get('versions', {})
        for relative, version in versions.items():
            path = Path(relative)
            if path.is_absolute() or not path.parts or '..' in path.parts:
                raise ValueError('renderer receipt has an invalid package path')
            if path.parts[0] != 'node_modules':
                # The immutable checker also records package-name aliases.
                path = Path('node_modules')/path
            record = lock['packages'].get(path.as_posix(), {})
            if record.get('link') is True:
                if path.as_posix() != 'node_modules/@banodoco/timeline-composition' or record.get('resolved') != 'vendor/timeline-composition':
                    raise ValueError('renderer receipt contains an unadmitted local package')
                record = lock['packages'].get('vendor/timeline-composition', {})
            manifest = installed/path/'package.json'
            actual = json.loads(manifest.read_bytes())
            if actual.get('version') != version or record.get('version') != version:
                raise ValueError('renderer installed package differs from admitted lock')
            files[manifest] = _sha(manifest)
        for name in ('remotion', '@remotion/renderer', '@remotion/cli', '@remotion/bundler'):
            if versions.get('node_modules/'+name) != '4.0.509':
                raise ValueError('renderer requires exact Remotion 4.0.509')
        for relative, expected in _PATCHES.items():
            path = modules/relative
            if _sha(path) != expected:
                raise ValueError('admitted renderer CPU/audio postimage differs')
            files[path] = expected
        # The local package is not SRI-backed. Compare every shipped byte with
        # the selected source rather than trusting its version or symlink.
        source = project/'vendor/timeline-composition'
        packed = modules/'@banodoco/timeline-composition'
        for path in sorted(packed.rglob('*')):
            if path.is_file():
                relative = path.relative_to(packed)
                if not (source/relative).is_file() or _sha(path) != _sha(source/relative):
                    raise ValueError('installed Composition differs from selected source')
                files[path] = _sha(path)
                files[source/relative] = _sha(path)
        for relative in ('@remotion/cli/remotion-cli.js', '@remotion/renderer/package.json'):
            path = modules/relative
            files[path] = _sha(path)
        # Freeze the actual installed bytes after checking the immutable SRI
        # receipt and required postimages. Subsequent leases/requests recheck
        # this snapshot, including the exact file inventory.
        for path in sorted(modules.rglob('*')):
            if path.is_file():
                if not path.resolve(strict=True).is_relative_to(modules):
                    raise ValueError('renderer installation contains an escaping file link')
                files[path] = _sha(path)
        for directory in ('src', 'vendor/timeline-composition'):
            for path in sorted((project/directory).rglob('*')):
                if path.is_file():
                    if not path.resolve(strict=True).is_relative_to(project):
                        raise ValueError('renderer source contains an escaping file link')
                    files[path] = _sha(path)
        # The config imports root helpers such as webpack-alias.mjs. Their
        # admitted code and inventory are part of the same renderer closure.
        for path in sorted(_root_sources(project)):
            files[path] = _sha(path)
        binding = cls(project, installed, receipt, receipt_sha256, manifest_sha256, lock_sha256,
                      tuple(sorted(files.items(), key=lambda item: str(item[0]))))
        binding.validate(project)
        return binding

    def validate(self, project):
        project = Path(project)
        if project != self.project or (project/'node_modules').resolve(strict=True) != self.installed_project/'node_modules':
            raise ValueError('renderer project or dependency root changed after admission')
        modules = self.installed_project/'node_modules'
        expected_modules = {path for path, _ in self.files if path.is_relative_to(modules)}
        actual_modules = {path for path in modules.rglob('*') if path.is_file()}
        if actual_modules != expected_modules:
            raise ValueError('admitted renderer installation file inventory changed')
        expected_root = {p for p, _ in self.files if p.parent == project and p.suffix in _ROOT_SOURCE_SUFFIXES}
        if _root_sources(project) != expected_root:
            raise ValueError('admitted renderer root source inventory changed')
        for directory in ('src', 'vendor/timeline-composition'):
            root = self.project/directory
            expected_source = {p for p, _ in self.files if p.is_relative_to(root)}
            actual_source = {p for p in root.rglob('*') if p.is_file()}
            if actual_source != expected_source:
                raise ValueError('admitted renderer source file inventory changed')
        for path, expected in self.files:
            if not path.is_file() or _sha(path) != expected:
                raise ValueError('admitted renderer closure input changed')
        return self.installed_project/'node_modules/@remotion/cli/remotion-cli.js'

    def require_retained_transport(self):
        self.validate(self.project)
        root = self.installed_project / 'node_modules/@remotion/renderer/dist'
        pinned = dict(self.files)
        if any(pinned.get(root / name) != expected or _sha(root / name) != expected
               for name, expected in _RETAINED_TRANSPORT_PATCHES.items()):
            raise ValueError('renderer closure lacks the qualified retained transport postimages')
