#!/usr/bin/env python3
"""Read-only full graph preflight. Never copies or follows package symlinks."""
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-app-private-clean12-graph'
REPO = Path('/home/user/work/wt/vw-m3-app-private-clean12-graph')
SOURCE = Path('/home/user/work/app/node_modules')
FROZEN = '5117b9da2e17828ec0b3cfbcdf3ff4987dc77ab3'
FLOOR = 10 * 1024**3
BUDGET = 1024**3

def digest(data):
    return hashlib.sha256(data).hexdigest()

def encoded(value):
    return json.dumps(value, separators=(',', ':'), ensure_ascii=False).encode()

def git_bytes(path):
    return subprocess.check_output(['git', 'show', FROZEN + ':' + path], cwd=REPO)

def write(suffix, value):
    Path(str(PREFIX) + suffix).write_text(json.dumps(value, indent=2) + '\n')

def inventory(root):
    entries = []
    def walk(directory):
        for path in sorted(directory.iterdir()):
            info = path.lstat()
            relative = path.relative_to(root).as_posix()
            record = dict(path=relative, mode=stat.S_IMODE(info.st_mode))
            if stat.S_ISDIR(info.st_mode):
                record['kind'] = 'directory'
                entries.append(record)
                walk(path)
                continue
            if stat.S_ISLNK(info.st_mode):
                target = os.readlink(path)
                record.update(kind='symlink', target=target, sha256=digest(target.encode()),
                              mtimeNs=info.st_mtime_ns)
            elif stat.S_ISREG(info.st_mode):
                record.update(kind='executable' if info.st_mode & 0o111 else 'file',
                              bytes=info.st_size, sha256=digest(path.read_bytes()),
                              device=info.st_dev, inode=info.st_ino, links=info.st_nlink)
            else:
                raise AssertionError('Unsupported entry: ' + str(path))
            entries.append(record)
    walk(root)
    return entries

def controller_tree(package, excluded):
    root = SOURCE / package
    rows = []
    for item in pre:
        prefix = package + '/'
        if not item['path'].startswith(prefix) or item['kind'] == 'directory':
            continue
        relative = item['path'][len(prefix):]
        if relative in excluded:
            continue
        rows.append([relative, item['kind'], item['sha256']])
    return dict(sha256=digest(encoded(rows)), fileCount=len(rows))

free_before = os.statvfs(SOURCE).f_bavail * os.statvfs(SOURCE).f_frsize
assert free_before >= FLOOR, 'Standing 10 GiB floor violated; no allocation allowed'
audit = json.loads((ORCH / 'design/handoff-vw-m3-tab-package-additions-audit-REPORT.json').read_text())
peer_reference = json.loads((ORCH / 'design/handoff-vw-m3-app-current-viewer-cut-source.json').read_text())['peer_manifests']
exclusions = {item['package'] + '/' + item['relativeEntry']: item for item in audit['addedEntries']}
pre = inventory(SOURCE)
index = {item['path']: item for item in pre}
for relative, expected in exclusions.items():
    assert index[relative]['kind'] == 'symlink'
    assert index[relative]['target'] == expected['target']

links = [item for item in pre if item['kind'] == 'symlink']
self_links = []
external_links = []
for item in links:
    path = SOURCE / item['path']
    target = Path(os.path.normpath(os.path.join(path.parent, item['target'])))
    if target == path.parent:
        self_links.append(item)
    if not target.is_relative_to(SOURCE):
        external_links.append(item)
retained_self_links = [item for item in self_links if item['path'] not in exclusions]

old_fingerprint = json.loads((ORCH / 'workers/vw-m3-tab-discovery-fix/owned-source-fingerprint.json').read_text())
selected_packages = {}
selected_checks = []
for name, old in old_fingerprint['packages'].items():
    excluded = {exclusions[key]['relativeEntry'] for key in exclusions if exclusions[key]['package'] == name}
    tree = controller_tree(name, excluded)
    meta = json.loads((SOURCE / name / 'package.json').read_bytes())
    selected_packages[name] = dict(version=meta['version'], tree=tree)
    if excluded:
        expected = next(item for item in audit['addedEntries'] if item['package'] == name)
        assert tree == dict(sha256=expected['oldHash'], fileCount=expected['oldFileCount'])
    selected_checks.append(dict(package=name, version=meta['version'], tree=tree))
filtered_11_hash = digest(encoded(selected_packages))
assert filtered_11_hash == audit['diagnosticExclusion']['filteredPackageGraphHash']

frozen_manifest = git_bytes('package.json')
frozen_lock = git_bytes('package-lock.json')
lock = json.loads(frozen_lock)
artifact_path = 'vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz'
artifact = git_bytes(artifact_path)
assert digest(artifact) == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
composition_lock = lock['packages']['node_modules/@banodoco/timeline-composition']
assert composition_lock['version'] == '0.0.12'
assert composition_lock['integrity'] == 'sha512-' + base64.b64encode(hashlib.sha512(artifact).digest()).decode()
assert composition_lock['resolved'] == 'file:' + artifact_path
members = []
with tarfile.open(fileobj=io.BytesIO(artifact)) as archive:
    for member in archive.getmembers():
        assert member.isfile() and member.name.startswith('package/') and '..' not in Path(member.name).parts
        members.append(dict(path=member.name.removeprefix('package/'), bytes=member.size,
                            sha256=digest(archive.extractfile(member).read())))
assert len(members) == 77
peers = {}
for name, expected in peer_reference.items():
    data = (SOURCE / name / 'package.json').read_bytes()
    version = json.loads(data)['version']
    assert digest(data) == expected['manifest_sha256'] and version == expected['version']
    peers[name] = dict(version=version, manifestSha256=digest(data),
                       tree=controller_tree(name, {exclusions[key]['relativeEntry'] for key in exclusions if exclusions[key]['package'] == name}))

versions = []
for item in pre:
    if item['path'].endswith('/package.json') and item['kind'] in ('file', 'executable'):
        data = json.loads((SOURCE / item['path']).read_bytes())
        versions.append(dict(path=item['path'], name=data.get('name'), version=data.get('version'),
                             manifestSha256=item['sha256']))
post = inventory(SOURCE)
assert post == pre, 'Source graph changed during read-only preflight'
free_after = os.statvfs(SOURCE).f_bavail * os.statvfs(SOURCE).f_frsize
assert free_after >= FLOOR, 'Standing 10 GiB floor violated'
write('-source-manifest.json', dict(root=str(SOURCE), entries=pre, sha256=digest(encoded(pre))))
write('-unexpected-self-links.json', retained_self_links)
write('-frozen12-members.json', members)
write('-package-versions.json', versions)
report = dict(status='BLOCKED', ready=False, privateRoot=None,
    reason='147 self-targeting package symlinks remain after ONLY the six authorized exclusions; cannot retain safely or remove within scope',
    sourceRoot=str(SOURCE), sourcePrePostEqual=True, sourceManifestSha256=digest(encoded(pre)),
    sourceFileBytes=sum(item.get('bytes', 0) for item in pre), sourceEntryCount=len(pre),
    symlinkCount=len(links), selfTargetingLinkCount=len(self_links), retainedSelfTargetingLinkCount=len(retained_self_links),
    authorizedExclusions=list(exclusions), externalLinks=external_links,
    selected11PackageChecks=selected_checks, selected11FilteredHash=filtered_11_hash,
    selected11HashIsWholePhysicalGraph=False, frozenSource=FROZEN,
    frozenManifestSha256=digest(frozen_manifest), frozenLockSha256=digest(frozen_lock),
    artifact=dict(path=artifact_path, bytes=len(artifact), sha256=digest(artifact), members=len(members), lock=composition_lock),
    sixPeerChecks=peers, floorBytes=FLOOR, ownAllocationBudgetBytes=BUDGET,
    freeBeforeBytes=free_before, freeAfterBytes=free_after, allocatedPrivateGraphs=0,
    notPerformed=['dependency copy', 'own extraction', 'private imports', 'install', 'network', 'browser', 'render', 'listener', 'full suite', 'central request', 'git mutation', 'shared dependency write', 'product edit'])
write('-REPORT.json', report)
print(json.dumps({key: report[key] for key in ['status', 'sourcePrePostEqual', 'sourceEntryCount', 'sourceFileBytes', 'symlinkCount', 'selfTargetingLinkCount', 'retainedSelfTargetingLinkCount', 'selected11FilteredHash', 'freeAfterBytes']}, indent=2))
raise SystemExit(2)
