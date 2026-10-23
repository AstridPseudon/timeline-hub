"""Dedicated owned bench lifecycle; stdlib only. No legacy adoption."""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import uuid


class Refused(RuntimeError):
    pass


def check(ok, message):
    if not ok:
        raise Refused(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def sha(value):
    check(isinstance(value, str) and re.fullmatch('[0-9a-f]{40}', value), 'exact commit required')
    return value


def child_key(agent_sha, backend_sha, client_tuple):
    check(isinstance(client_tuple, dict) and bool(client_tuple), 'client tuple required')
    return digest(canonical(['child', sha(agent_sha), sha(backend_sha), client_tuple]))


def runtime_key(remotion_tree):
    return digest(canonical(['runtime', sha(remotion_tree)]))


def key_for(component, identity):
    check(isinstance(identity, dict), 'identity object required')
    if component == 'child':
        check(set(identity) == {'agent_sha', 'backend_sha', 'client_tuple'}, 'child identity schema')
        return child_key(**identity)
    check(component == 'runtime' and set(identity) == {'remotion_tree'}, 'runtime identity schema')
    return runtime_key(**identity)


def physical(path):
    path = Path(path)
    check(path.is_absolute() and '..' not in path.parts and path == path.resolve(), 'physical absolute path required')
    for item in [path, *path.parents]:
        if item.exists():
            info = item.lstat()
            check(stat.S_ISDIR(info.st_mode) and not item.is_symlink(), 'physical directory required')
            check(info.st_uid == os.getuid() or not info.st_mode & 0o022 or bool(info.st_mode & stat.S_ISVTX), 'unsafe directory owner')
    return path


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def read(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        check(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid() and info.st_nlink == 1, 'unsafe metadata file')
        with os.fdopen(fd, 'r', encoding='utf-8', newline='', closefd=False) as stream:
            return stream.read()
    finally:
        os.close(fd)


def atomic(path, value):
    path = Path(path)
    temp = path.with_name('.write-' + uuid.uuid4().hex)
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='', closefd=False) as stream:
            stream.write(value)
            stream.flush()
            os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(temp, path)
    sync_dir(path.parent)


def optional(path):
    return read(path) if path.exists() or path.is_symlink() else None


def inode(path):
    s = path.lstat()
    check(not path.is_symlink() and s.st_uid == os.getuid(), 'unsafe owned path')
    return [s.st_dev, s.st_ino]


class Store:
    # Fixed reserve; adapters cannot bypass retention or reserve via caller flags.
    REPORT_LIMIT = 1024 * 1024
    RESERVE_BYTES = 8 * 1024 * 1024 * 1024

    @classmethod
    def initialize(cls, root, tests_dir):
        root, tests_dir = physical(root), physical(tests_dir)
        check(not root.exists(), 'existing roots are never adopted')
        root.mkdir(mode=0o700)
        for name in ('entries', 'locks', 'staging'):
            (root / name).mkdir(mode=0o700)
        fd = os.open(root / 'mutex', os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
        os.close(fd)
        owner = {'version': 1, 'uid': os.getuid(), 'id': uuid.uuid4().hex,
                 'root': str(root), 'tests': str(tests_dir), 'mutex': inode(root / 'mutex'),
                 'directories': {str(p): inode(p) for p in (root, tests_dir, root / 'entries', root / 'locks', root / 'staging')}}
        atomic(root / 'owner.json', canonical(owner))
        atomic(root / 'index.json', canonical({'version': 1, 'seq': 0, 'entries': {}, 'registrations': {}, 'retired': [], 'retired_suites': []}))
        return cls(root, tests_dir)

    def __init__(self, root, tests_dir):
        self.root, self.tests = physical(root), physical(tests_dir)
        self.owner = json.loads(read(self.root / 'owner.json'))
        check(set(self.owner) == {'version', 'uid', 'id', 'root', 'tests', 'mutex', 'directories'}, 'store owner schema')
        check(self.owner['version'] == 1 and self.owner['uid'] == os.getuid()
              and self.owner['root'] == str(self.root) and self.owner['tests'] == str(self.tests), 'store ownership mismatch')
        for name in ('entries', 'locks', 'staging'):
            physical(self.root / name)
        self.journal = self.root / 'pending.json'

    @contextlib.contextmanager
    def mutex(self, recovery=False):
        expected_dirs = {str(p) for p in (self.root, self.tests, self.root / 'entries', self.root / 'locks', self.root / 'staging')}
        check(set(self.owner['directories']) == expected_dirs, 'directory schema')
        for path, node in self.owner['directories'].items():
            check(inode(physical(path)) == node, 'store directory replaced')
        fd = os.open(self.root / 'mutex', os.O_RDWR | os.O_NOFOLLOW)
        try:
            check(inode(self.root / 'mutex') == self.owner['mutex'] and list((os.fstat(fd).st_dev, os.fstat(fd).st_ino)) == self.owner['mutex'], 'mutex inode changed')
            fcntl.flock(fd, fcntl.LOCK_EX)
            check(inode(self.root / 'mutex') == self.owner['mutex'], 'mutex replaced')
            check(recovery or not self.journal.exists(), 'pending transaction: explicit recover required')
            yield
        finally:
            os.close(fd)

    def _entry_id(self, component, key):
        check(component in ('runtime', 'child') and isinstance(key, str) and re.fullmatch('[0-9a-f]{64}', key), 'entry key schema')
        return component + '-' + key

    def _validate_entry(self, eid, entry, live=True):
        check(set(entry) == {'component', 'key', 'identity', 'path', 'seq', 'lock', 'node', 'owner'}, 'entry schema')
        check(eid == self._entry_id(entry['component'], key_for(entry['component'], entry['identity'])) and entry['key'] == key_for(entry['component'], entry['identity']), 'entry identity mismatch')
        check(entry['path'] == str(self.root / 'entries' / eid) and entry['owner'] == self.owner['id'], 'entry ownership/path mismatch')
        check(isinstance(entry['seq'], int) and entry['seq'] > 0, 'entry sequence')
        check(inode(self.root / 'locks' / eid) == entry['lock'], 'lease inode changed')
        if live:
            self._owned_dir(Path(entry['path']), entry)

    def _owned_dir(self, path, entry):
        check(inode(path) == entry['node'] and path.is_dir(), 'bench inode changed')
        expected = {'owner': self.owner['id'], 'component': entry['component'], 'key': entry['key'], 'identity': entry['identity']}
        check(json.loads(read(path / '.bench-owner.json')) == expected, 'bench marker mismatch')

    def _load(self, live=True):
        index = json.loads(read(self.root / 'index.json'))
        self._validate_index(index, live)
        return index

    def _validate_index(self, index, live):
        check(set(index) == {'version', 'seq', 'entries', 'registrations', 'retired', 'retired_suites'} and index['version'] == 1, 'index schema')
        check(isinstance(index['seq'], int) and isinstance(index['entries'], dict) and isinstance(index['registrations'], dict) and isinstance(index['retired'], list), 'index types')
        for eid, entry in index['entries'].items():
            self._validate_entry(eid, entry, live)
        for name, reg in index['registrations'].items():
            self._name(name)
            check(set(reg) in ({'env', 'suite', 'requires', 'hash'}, {'env', 'suite', 'requires', 'hash', 'report', 'report_sha256'}) and isinstance(reg['env'], str) and isinstance(reg['suite'], str), 'registration schema')
            if 'report' in reg:
                self._report(reg['report'])
                check(bool(reg['report']) and reg['report_sha256'] == digest(reg['report']), 'report hash mismatch')
            check(reg['hash'] == digest(canonical({k: v for k, v in reg.items() if k != 'hash'})), 'registration hash mismatch')
            check(isinstance(reg['requires'], list) and bool(reg['requires']) and len(set(reg['requires'])) == len(reg['requires']), 'registration dependency schema')
            check(all(eid in index['entries'] for eid in reg['requires']), 'registration missing dependency')
            self._suite(reg['suite'])
        for name in index['retired']:
            self._name(name)
        check(isinstance(index['retired_suites'], list) and all(isinstance(pair, list) and len(pair) == 2 and all(isinstance(v, str) and v and not any(c.isspace() for c in v) for v in pair) for pair in index['retired_suites']), 'retired suite schema')

    def _name(self, name):
        check(isinstance(name, str) and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]*', name), 'registration name required')

    def _suite(self, row):
        check(not row or row.endswith('\n') and row.count('\n') == 1 and len(row.split(None, 2)) == 3, 'single full suite row required')

    def _report(self, value):
        check(isinstance(value, str), 'report string required')
        check(len(value.encode('utf-8')) <= self.REPORT_LIMIT, 'report size limit')
        return value

    def _report_path(self, name):
        self._name(name)
        folder = self.tests / 'provision'
        if folder.exists() or folder.is_symlink():
            physical(folder)
            check(folder.stat().st_uid == os.getuid(), 'foreign provision directory')
        return folder / (name + '.txt')

    def _read_report(self, path):
        if not path.exists() and not path.is_symlink():
            return None
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            info = os.fstat(fd)
            check(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid()
                  and info.st_nlink == 1 and info.st_size <= self.REPORT_LIMIT, 'unsafe report file')
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                value = stream.read(self.REPORT_LIMIT + 1)
            check(len(value) <= self.REPORT_LIMIT, 'report size limit')
            return value.decode('utf-8')
        finally:
            os.close(fd)

    def _report_changes(self, before, after):
        result = {}
        for name in set(before['registrations']) | set(after['registrations']):
            old = before['registrations'].get(name, {}).get('report') or None
            new = after['registrations'].get(name, {}).get('report') or None
            if old != new:
                result['provision/' + name + '.txt'] = [old, new]
        return result

    def _verify_pending_reports(self, journal):
        names = {name for name, reg in journal['before']['registrations'].items() if reg.get('report')}
        names.update(name[10:-4] for name in journal['projections'] if name.startswith('provision/'))
        for name in names:
            values = [index['registrations'].get(name, {}).get('report') or None
                      for index in (journal['before'], journal['after'])]
            check(self._read_report(self._report_path(name)) in values, 'report changed while pending')

    def _verify_projection(self, index):
        suites = read(self.tests / 'suites.conf')
        for name, reg in index['registrations'].items():
            if reg.get('report'):
                check(self._read_report(self._report_path(name)) == reg['report'], 'registration report changed: ' + name)
            check(optional(self.tests / (name + '.env')) == (reg['env'] or None), 'registration env changed: ' + name)
            check(not reg['suite'] or suites.splitlines(keepends=True).count(reg['suite']) == 1, 'registration suite changed: ' + name)
            if reg['suite']:
                pair = reg['suite'].split(None, 2)[:2]
                check(sum(row.split(None, 2)[:2] == pair for row in suites.splitlines()) == 1, 'managed suite ambiguity')
        return suites

    def _lock(self, eid, entry, exclusive=False):
        fd = os.open(self.root / 'locks' / eid, os.O_RDWR | os.O_NOFOLLOW)
        try:
            s = os.fstat(fd)
            check([s.st_dev, s.st_ino] == entry['lock'] and inode(self.root / 'locks' / eid) == entry['lock'], 'lease inode replaced')
            fcntl.flock(fd, (fcntl.LOCK_EX | fcntl.LOCK_NB) if exclusive else fcntl.LOCK_SH)
            return fd
        except BaseException:
            os.close(fd)
            raise

    def _save_journal(self, journal):
        atomic(self.journal, canonical(journal))

    def _finish_journal(self):
        self.journal.unlink()
        sync_dir(self.root)

    def _projections(self, before, after):
        suites = self._verify_projection(before)
        rows = suites.splitlines(keepends=True)
        for name, reg in before['registrations'].items():
            if name not in after['registrations'] and reg['suite']:
                rows.remove(reg['suite'])
        for name, reg in after['registrations'].items():
            if name not in before['registrations'] and reg['suite']:
                check(not rows or rows[-1].endswith('\n'), 'unterminated suites file')
                pair = reg['suite'].split(None, 2)[:2]
                check(not any(row.split(None, 2)[:2] == pair for row in rows), 'suite name already owned/unmanaged')
                rows.append(reg['suite'])
        projections = {'suites.conf': [suites, ''.join(rows)]}
        for name in set(before['registrations']) | set(after['registrations']):
            old = before['registrations'].get(name, {}).get('env') or None
            new = after['registrations'].get(name, {}).get('env') or None
            if old != new:
                check(optional(self.tests / (name + '.env')) == old, 'foreign env protected')
                projections[name + '.env'] = [old, new]
        for name, values in self._report_changes(before, after).items():
            check(self._read_report(self._report_path(name[10:-4])) == values[0], 'foreign report protected')
            projections[name] = values
        return projections

    def _apply_projection(self, projections, forward):
        # Validate every target before the first write (including recovery).
        for name, values in projections.items():
            check(name == 'suites.conf' or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*\.env', name) or re.fullmatch(r'provision/[A-Za-z0-9][A-Za-z0-9_-]*\.txt', name), 'journal projection path')
            check(isinstance(values, list) and len(values) == 2 and all(v is None or isinstance(v, str) for v in values), 'journal projection schema')
            if name.startswith('provision/'):
                for value in values:
                    if value is not None:
                        self._report(value)
                current = self._read_report(self._report_path(name[10:-4]))
            else:
                current = optional(self.tests / name)
            check(current in values, 'projection changed while pending')
        for name, values in projections.items():
            path, value = self.tests / name, values[1 if forward else 0]
            if name.startswith('provision/'):
                path = self._report_path(name[10:-4])
                if value is not None and not path.parent.exists():
                    path.parent.mkdir(mode=0o700)
                    sync_dir(self.tests)
            if value is None:
                if path.exists():
                    path.unlink()
                    sync_dir(path.parent)
            else:
                atomic(path, value)
            self._checkpoint('projection:' + name)

    def _checkpoint(self, point):
        """No-op fault-injection seam for private fixtures."""

    def _sync_payload(self, path):
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            for name in os.listdir(fd):
                info = os.stat(name, dir_fd=fd, follow_symlinks=False)
                if stat.S_ISDIR(info.st_mode):
                    self._sync_payload(path / name)
                elif stat.S_ISREG(info.st_mode):
                    leaf = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
                    try:
                        os.fsync(leaf)
                    finally:
                        os.close(leaf)
                else:
                    check(stat.S_ISLNK(info.st_mode), 'unsupported payload inode')
            os.fsync(fd)
        finally:
            os.close(fd)

    def _delete_owned(self, path, entry):
        if not path.exists() and not path.is_symlink():
            return
        self._validate_entry(self._entry_id(entry['component'], entry['key']), entry, False)
        check(path in (Path(entry['path']), self.root / 'staging' / entry['key']), 'deletion path authority')
        check(inode(path) == entry['node'] and path.is_dir(), 'deletion inode authority')
        marker = path / '.bench-owner.json'
        if marker.exists() or marker.is_symlink():
            self._owned_dir(path, entry)
        else:
            check(not list(path.iterdir()), 'missing deletion marker')
        root_fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            root_info = os.fstat(root_fd)
            check([root_info.st_dev, root_info.st_ino] == entry['node'] and root_info.st_uid == os.getuid(), 'deletion directory replaced/foreign')
            # Check the complete owned tree before restoring any directory's write bit.
            def validate_children(directory_fd):
                for name in os.listdir(directory_fd):
                    info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                    check(info.st_dev == root_info.st_dev and info.st_uid == os.getuid(), 'foreign mounted/owned content')
                    if stat.S_ISDIR(info.st_mode):
                        child_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd)
                        try:
                            opened = os.fstat(child_fd)
                            check((opened.st_dev, opened.st_ino) == (info.st_dev, info.st_ino), 'child directory replaced')
                            validate_children(child_fd)
                        finally:
                            os.close(child_fd)
            validate_children(root_fd)
            self._checkpoint('deletion:validated')
            if marker.exists() or marker.is_symlink():
                self._owned_dir(path, entry)
            else:
                check(not os.listdir(root_fd), 'missing deletion marker')
            check(inode(path) == entry['node'], 'deletion root replaced')
            check(inode(self.root / 'locks' / self._entry_id(entry['component'], entry['key'])) == entry['lock'], 'lease inode changed')
            os.fchmod(root_fd, root_info.st_mode | stat.S_IWUSR)
            def delete_children(directory_fd, top=False):
                for name in os.listdir(directory_fd):
                    if top and name == '.bench-owner.json':
                        continue
                    info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                    check(info.st_dev == root_info.st_dev and info.st_uid == os.getuid(), 'foreign mounted/owned content')
                    if stat.S_ISDIR(info.st_mode):
                        child_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd)
                        try:
                            opened = os.fstat(child_fd)
                            check((opened.st_dev, opened.st_ino) == (info.st_dev, info.st_ino), 'child directory replaced')
                            self._checkpoint('deletion:child')
                            check(inode(path) == entry['node'], 'deletion root replaced')
                            current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                            check((current.st_dev, current.st_ino) == (opened.st_dev, opened.st_ino) and opened.st_uid == os.getuid(), 'child directory replaced/foreign')
                            os.fchmod(child_fd, opened.st_mode | stat.S_IWUSR)
                            delete_children(child_fd)
                            current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                            check((current.st_dev, current.st_ino) == (opened.st_dev, opened.st_ino), 'child directory replaced')
                        finally:
                            os.close(child_fd)
                        os.rmdir(name, dir_fd=directory_fd)
                    else:
                        os.unlink(name, dir_fd=directory_fd)  # Never follow leaf symlinks.
                    os.fsync(directory_fd)
                    self._checkpoint('eviction:file')
            delete_children(root_fd, True)
            if marker.exists():
                os.unlink('.bench-owner.json', dir_fd=root_fd)
                os.fsync(root_fd)
            check(inode(path) == entry['node'], 'deletion root replaced')
            path.rmdir()
            sync_dir(path.parent)
            self._checkpoint('eviction:directory')
        finally:
            os.close(root_fd)

    def _evict(self, before, component, incoming, current):
        candidates = sorted(((eid, e) for eid, e in before['entries'].items() if e['component'] == component), key=lambda pair: pair[1]['seq'], reverse=True)
        retained = {eid for eid, _ in candidates[:1 if incoming else 2]} | {current}
        held, victims = [], []
        try:
            for eid, entry in candidates:
                if eid in retained:
                    continue
                try:
                    held.append(self._lock(eid, entry, True))
                    victims.append(eid)
                except BlockingIOError:
                    pass  # All leases are additional to the fixed two latest tuples.
            if not victims:
                return before
            after = json.loads(canonical(before))
            for name, reg in list(after['registrations'].items()):
                if any(eid in reg['requires'] for eid in victims):
                    del after['registrations'][name]
                    if name not in after['retired']:
                        after['retired'].append(name)
                    if reg['suite']:
                        pair = reg['suite'].split(None, 2)[:2]
                        if pair not in after['retired_suites']:
                            after['retired_suites'].append(pair)
            for eid in victims:
                del after['entries'][eid]
            journal = {'version': 1, 'owner': self.owner['id'], 'kind': 'eviction', 'before': before, 'after': after,
                       'projections': self._projections(before, after), 'victims': victims, 'new': None}
            self._save_journal(journal)
            self._checkpoint('eviction:journal')
            self._roll(journal, True)
            return after
        finally:
            for fd in held:
                os.close(fd)

    def _roll(self, journal, forward):
        self._verify_pending_reports(journal)
        self._apply_projection(journal['projections'], forward)
        atomic(self.root / 'index.json', canonical(journal['after'] if forward else journal['before']))
        self._checkpoint('index')
        if journal['kind'] == 'eviction':
            for eid in journal['victims']:
                entry = journal['before']['entries'][eid]
                self._delete_owned(Path(entry['path']), entry)
        elif journal['new']:
            entry = journal['new']
            for path in (Path(entry['path']), self.root / 'staging' / entry['key']):
                self._delete_owned(path, entry)
        self._finish_journal()

    def _validate_transition(self, journal):
        before, after = journal['before'], journal['after']
        for eid in set(before['entries']) & set(after['entries']):
            check(before['entries'][eid] == after['entries'][eid], 'journal rewrites owned entry')
        for name in set(before['registrations']) & set(after['registrations']):
            check(before['registrations'][name] == after['registrations'][name], 'journal rewrites registration')
        if journal['kind'] == 'eviction':
            check(set(after['entries']) <= set(before['entries']), 'eviction cannot create')
            expected = {name: reg for name, reg in before['registrations'].items()
                        if not set(reg['requires']) & set(journal['victims'])}
            check(after['registrations'] == expected, 'eviction registration authority')
        else:
            check(set(before['entries']) <= set(after['entries']) and set(before['registrations']) <= set(after['registrations']), 'creation cannot evict')
        projections = journal['projections']
        if not projections:
            check(before == after, 'missing journal projections')
            return
        check('suites.conf' in projections, 'missing suite baseline')
        old_suites, new_suites = projections['suites.conf']
        check(isinstance(old_suites, str) and isinstance(new_suites, str), 'suite baseline schema')
        rows = old_suites.splitlines(keepends=True)
        expected_projections = {'suites.conf': [old_suites, None]}
        for name, reg in before['registrations'].items():
            if reg['suite']:
                check(rows.count(reg['suite']) == 1, 'journal registration baseline')
            if name not in after['registrations'] and reg['suite']:
                rows.remove(reg['suite'])
        for name, reg in after['registrations'].items():
            if name not in before['registrations'] and reg['suite']:
                rows.append(reg['suite'])
        expected_projections['suites.conf'][1] = ''.join(rows)
        for name in set(before['registrations']) | set(after['registrations']):
            old = before['registrations'].get(name, {}).get('env') or None
            new = after['registrations'].get(name, {}).get('env') or None
            if old != new:
                expected_projections[name + '.env'] = [old, new]
        expected_projections.update(self._report_changes(before, after))
        check(projections == expected_projections, 'journal projection authority/hash mismatch')

    def recover(self):
        with self.mutex(recovery=True):
            if not self.journal.exists():
                return
            journal = json.loads(read(self.journal))
            check(set(journal) == {'version', 'owner', 'kind', 'before', 'after', 'projections', 'victims', 'new'} and journal['version'] == 1 and journal['owner'] == self.owner['id'], 'journal ownership/schema')
            check(journal['kind'] in ('eviction', 'creation'), 'journal kind')
            self._validate_index(journal['before'], False)
            self._validate_index(journal['after'], False)
            self._validate_transition(journal)
            current = json.loads(read(self.root / 'index.json'))
            check(current in (journal['before'], journal['after']), 'pending index changed')
            if journal['kind'] == 'eviction':
                check(journal['new'] is None and set(journal['victims']) == set(journal['before']['entries']) - set(journal['after']['entries']), 'journal eviction authority')
            else:
                check(not journal['victims'], 'creation cannot evict')
                if journal['new']:
                    e = journal['new']
                    new_id = self._entry_id(e['component'], e['key'])
                    self._validate_entry(new_id, e, False)
                    check(new_id not in journal['before']['entries'] and journal['after']['entries'].get(new_id, e) == e, 'creation deletion authority')
            held = []
            try:
                if journal['kind'] == 'eviction':
                    for eid in journal['victims']:
                        held.append(self._lock(eid, journal['before']['entries'][eid], True))
                elif journal['new']:
                    e = journal['new']
                    held.append(self._lock(self._entry_id(e['component'], e['key']), e, True))
                self._roll(journal, journal['kind'] == 'eviction')
            finally:
                for fd in held:
                    os.close(fd)

    def _registration(self, value, entry, index):
        check(isinstance(value, dict) and set(value) <= {'name', 'env', 'suite', 'requires', 'require_names', 'report'} and {'name', 'env', 'suite'} <= set(value), 'registration input schema')
        name = value['name']
        self._name(name)
        check(isinstance(value['env'], str) and isinstance(value['suite'], str), 'registration strings required')
        refs = {self._entry_id(entry['component'], entry['key'])}
        for ref in value.get('requires', []):
            check(isinstance(ref, dict) and set(ref) == {'component', 'key'}, 'dependency schema')
            refs.add(self._entry_id(ref['component'], ref['key']))
        for required in value.get('require_names', []):
            self._name(required)
            check(required in index['registrations'], 'required registration absent')
            refs.update(index['registrations'][required]['requires'])
        check(all(eid in index['entries'] for eid in refs), 'required tuple absent')
        reg = {'env': value['env'].replace('{bench_path}', entry['path']), 'suite': value['suite'].replace('{bench_path}', entry['path']), 'requires': sorted(refs)}
        report = self._report(value.get('report', ''))
        if report:
            check(self._read_report(Path(entry['path']) / '.provision-report') == report, 'report differs from verified entry')
            reg.update(report=report, report_sha256=digest(report))
        self._suite(reg['suite'])
        check(not reg['suite'] or reg['suite'].split(None, 2)[:2] not in index['retired_suites'], 'retired suite immutable')
        reg['hash'] = digest(canonical(reg))
        return name, reg

    def ensure(self, component, identity, registration, build, verify, seal=None):
        key = key_for(component, identity)
        eid = self._entry_id(component, key)
        with self.mutex():
            before = self._load()
            self._verify_projection(before)
            for policy_component in ('child', 'runtime'):
                before = self._evict(before, policy_component, policy_component == component and eid not in before['entries'], eid)
            self._checkpoint('before-build')
            check(shutil.disk_usage(self.root).free >= self.RESERVE_BYTES, 'free-space reserve unavailable')
            reused = eid in before['entries']
            journal = {'version': 1, 'owner': self.owner['id'], 'kind': 'creation', 'before': before, 'after': before,
                       'projections': {}, 'victims': [], 'new': None}
            self._save_journal(journal)
            try:
                after = json.loads(canonical(before))
                if reused:
                    entry = after['entries'][eid]
                else:
                    final, stage = self.root / 'entries' / eid, self.root / 'staging' / key
                    check(not final.exists() and not final.is_symlink() and not stage.exists() and not stage.is_symlink(), 'foreign publication/stage protected')
                    lock = self.root / 'locks' / eid
                    if not lock.exists():
                        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_RDWR | os.O_NOFOLLOW, 0o600)
                        os.close(fd)
                        sync_dir(lock.parent)
                    entry = {'component': component, 'key': key, 'identity': identity, 'path': str(final), 'seq': before['seq'] + 1,
                             'lock': inode(lock), 'node': None, 'owner': self.owner['id']}
                    journal['new'] = entry
                    self._save_journal(journal)
                    stage.mkdir(mode=0o700)
                    entry['node'] = inode(stage)
                    atomic(stage / '.bench-owner.json', canonical({'owner': self.owner['id'], 'component': component, 'key': key, 'identity': identity}))
                    self._save_journal(journal)
                    self._checkpoint('creation:stage')
                    build(stage, final)
                    self._checkpoint('creation:build')
                    self._owned_dir(stage, entry)
                    self._sync_payload(stage)
                    os.rename(stage, final)
                    sync_dir(stage.parent)
                    sync_dir(final.parent)
                    self._checkpoint('creation:publish')
                    self._owned_dir(final, entry)
                    if seal is not None:
                        seal(final)
                    self._owned_dir(final, entry)
                    self._sync_payload(final)
                    self._checkpoint('creation:seal')
                    after['entries'][eid] = entry
                    after['seq'] = entry['seq']
                verify(Path(entry['path']))
                self._owned_dir(Path(entry['path']), entry)
                value = registration(Path(entry['path']), Path(entry['path']), reused) if callable(registration) else registration
                name, reg = self._registration(value, entry, after)
                check(name not in after['registrations'] or after['registrations'][name] == reg, 'registration name immutable')
                check(name not in after['retired'], 'retired registration name immutable')
                after['registrations'][name] = reg
                journal['after'] = after
                journal['projections'] = self._projections(before, after)
                self._save_journal(journal)
                self._apply_projection(journal['projections'], True)
                atomic(self.root / 'index.json', canonical(after))
                self._checkpoint('creation:index')
                self._finish_journal()
                return dict(entry, reused=reused)
            except Exception as error:
                # Eviction was already committed; rollback only this creation.
                if self.journal.exists():
                    try:
                        self._roll(journal, False)
                    except Exception as rollback_error:
                        raise Refused(f'creation failed: {error}; recovery remains pending: {rollback_error}') from error
                raise

    def registered(self, name):
        self._name(name)
        with self.mutex():
            index = self._load()
            self._verify_projection(index)
            check(name not in index['retired'], 'registration was evicted')
            return name in index['registrations']

    def registration_entries(self, name):
        self._name(name)
        with self.mutex():
            index = self._load()
            self._verify_projection(index)
            check(name in index['registrations'], 'registration absent')
            return [dict(index['entries'][eid]) for eid in index['registrations'][name]['requires']]

    def names_for_suite(self, repo, suite, command):
        with self.mutex():
            index = self._load()
            suites = self._verify_projection(index)
            names = []
            for name, reg in index['registrations'].items():
                parts = reg['suite'].rstrip('\n').split(None, 2)
                if parts[:2] == [repo, suite]:
                    check(len(parts) == 3 and parts[2] == command, 'managed suite command mismatch')
                    names.append(name)
            check([repo, suite] not in index['retired_suites'], 'suite registration evicted')
            if not names:
                rows = [row.split(None, 2) for row in suites.splitlines()
                        if row.split(None, 2)[:2] == [repo, suite]]
                check(len(rows) == 1 and len(rows[0]) == 3 and rows[0][2] == command, 'suite absent, ambiguous or changed')
                # Existing custom rows may use any managed environment/path.
                # Acquire all registered dependencies without interpreting shell.
                names = sorted(index['registrations'])
            return names

    @contextlib.contextmanager
    def acquire(self, names):
        held, entries = [], []
        try:
            with self.mutex():
                index = self._load()
                self._verify_projection(index)
                refs = set()
                for name in names:
                    self._name(name)
                    check(name in index['registrations'], 'registration absent')
                    refs.update(index['registrations'][name]['requires'])
                for eid in sorted(refs):
                    entry = index['entries'][eid]
                    fd = self._lock(eid, entry)
                    held.append(fd)
                    os.set_inheritable(fd, True)
                    entries.append(dict(entry, lease_fd=fd))
            yield entries
        finally:
            for fd in held:
                os.close(fd)

    def run(self, names, argv):
        with self.acquire(names) as entries:
            return subprocess.call(argv, pass_fds=tuple(e['lease_fd'] for e in entries))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--tests-dir', required=True)
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('recover')
    key = commands.add_parser('key')
    key.add_argument('component', choices=['child', 'runtime'])
    key.add_argument('--identity', required=True)
    run = commands.add_parser('run')
    run.add_argument('--name', action='append', required=True)
    run.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.action == 'key':
            print(key_for(args.component, json.loads(args.identity)))
            return 0
        store = Store(args.root, args.tests_dir)
        if args.action == 'recover':
            store.recover()
            return 0
        argv = args.command[1:] if args.command[:1] == ['--'] else args.command
        check(bool(argv), 'command required')
        return store.run(args.name, argv)
    except (Refused, OSError, ValueError, TypeError, KeyError) as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
