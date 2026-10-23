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
        with os.fdopen(fd, 'r', closefd=False) as stream:
            return stream.read()
    finally:
        os.close(fd)


def atomic(path, value):
    path = Path(path)
    temp = path.with_name('.write-' + uuid.uuid4().hex)
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, 'w', closefd=False) as stream:
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
    RESERVE_BYTES = 8 * 1024 * 1024

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
                 'root': str(root), 'tests': str(tests_dir), 'mutex': inode(root / 'mutex')}
        atomic(root / 'owner.json', canonical(owner))
        atomic(root / 'index.json', canonical({'version': 1, 'seq': 0, 'entries': {}, 'registrations': {}, 'retired': [], 'retired_suites': []}))
        return cls(root, tests_dir)

    def __init__(self, root, tests_dir):
        self.root, self.tests = physical(root), physical(tests_dir)
        self.owner = json.loads(read(self.root / 'owner.json'))
        check(set(self.owner) == {'version', 'uid', 'id', 'root', 'tests', 'mutex'}, 'store owner schema')
        check(self.owner['version'] == 1 and self.owner['uid'] == os.getuid()
              and self.owner['root'] == str(self.root) and self.owner['tests'] == str(self.tests), 'store ownership mismatch')
        for name in ('entries', 'locks', 'staging'):
            physical(self.root / name)
        self.journal = self.root / 'pending.json'

    @contextlib.contextmanager
    def mutex(self, recovery=False):
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
            check(set(reg) == {'env', 'suite', 'requires', 'hash'} and isinstance(reg['env'], str) and isinstance(reg['suite'], str), 'registration schema')
            check(reg['hash'] == digest(canonical({k: reg[k] for k in ('env', 'suite', 'requires')})), 'registration hash mismatch')
            check(isinstance(reg['requires'], list) and bool(reg['requires']) and len(set(reg['requires'])) == len(reg['requires']), 'registration dependency schema')
            check(all(eid in index['entries'] for eid in reg['requires']), 'registration missing dependency')
            self._suite(reg['suite'])
        for name in index['retired']:
            self._name(name)

    def _name(self, name):
        check(isinstance(name, str) and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]*', name), 'registration name required')

    def _suite(self, row):
        check(not row or row.endswith('\n') and row.count('\n') == 1 and len(row.split(None, 2)) == 3, 'single full suite row required')

    def _verify_projection(self, index):
        suites = read(self.tests / 'suites.conf')
        for name, reg in index['registrations'].items():
            check(optional(self.tests / (name + '.env')) == (reg['env'] or None), 'registration env changed: ' + name)
            check(not reg['suite'] or suites.splitlines(keepends=True).count(reg['suite']) == 1, 'registration suite changed: ' + name)
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
        return projections

    def _apply_projection(self, projections, forward):
        # Validate every target before the first write (including recovery).
        for name, values in projections.items():
            check(name == 'suites.conf' or re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]*\.env', name), 'journal projection path')
            check(isinstance(values, list) and len(values) == 2 and all(v is None or isinstance(v, str) for v in values), 'journal projection schema')
            check(optional(self.tests / name) in values, 'projection changed while pending')
        for name, values in projections.items():
            path, value = self.tests / name, values[1 if forward else 0]
            if value is None:
                if path.exists():
                    path.unlink()
                    sync_dir(path.parent)
            else:
                atomic(path, value)
            self._checkpoint('projection:' + name)

    def _checkpoint(self, point):
        """No-op fault-injection seam for private fixtures."""

    def _delete_owned(self, path, entry):
        if not path.exists() and not path.is_symlink():
            return
        check(path in (Path(entry['path']), self.root / 'staging' / entry['key']), 'deletion path authority')
        check(inode(path) == entry['node'] and path.is_dir(), 'deletion inode authority')
        marker = path / '.bench-owner.json'
        if marker.exists() or marker.is_symlink():
            self._owned_dir(path, entry)
        else:
            check(not list(path.iterdir()), 'missing deletion marker')
        device = path.lstat().st_dev
        def delete_children(directory):
            for item in directory.iterdir():
                if item == marker:
                    continue
                info = item.lstat()
                check(info.st_dev == device and info.st_uid == os.getuid(), 'foreign mounted/owned content')
                if stat.S_ISDIR(info.st_mode):
                    delete_children(item)
                    item.rmdir()
                else:
                    item.unlink()  # Leaf symlinks are unlinked, never followed.
                sync_dir(directory)
                self._checkpoint('eviction:file')
        delete_children(path)
        if marker.exists():
            marker.unlink()
            sync_dir(path)
        path.rmdir()
        sync_dir(path.parent)
        self._checkpoint('eviction:directory')

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

    def recover(self):
        with self.mutex(recovery=True):
            if not self.journal.exists():
                return
            journal = json.loads(read(self.journal))
            check(set(journal) == {'version', 'owner', 'kind', 'before', 'after', 'projections', 'victims', 'new'} and journal['version'] == 1 and journal['owner'] == self.owner['id'], 'journal ownership/schema')
            check(journal['kind'] in ('eviction', 'creation'), 'journal kind')
            self._validate_index(journal['before'], False)
            self._validate_index(journal['after'], False)
            current = json.loads(read(self.root / 'index.json'))
            check(current in (journal['before'], journal['after']), 'pending index changed')
            if journal['kind'] == 'eviction':
                check(journal['new'] is None and set(journal['victims']) == set(journal['before']['entries']) - set(journal['after']['entries']), 'journal eviction authority')
            else:
                check(not journal['victims'], 'creation cannot evict')
                if journal['new']:
                    e = journal['new']
                    self._validate_entry(self._entry_id(e['component'], e['key']), e, False)
            self._roll(journal, journal['kind'] == 'eviction')

    def _registration(self, value, entry, index):
        check(isinstance(value, dict) and set(value) <= {'name', 'env', 'suite', 'requires', 'require_names'} and {'name', 'env', 'suite'} <= set(value), 'registration input schema')
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
        self._suite(reg['suite'])
        check(not reg['suite'] or reg['suite'].split(None, 2)[:2] not in index['retired_suites'], 'retired suite immutable')
        reg['hash'] = digest(canonical(reg))
        return name, reg

    def ensure(self, component, identity, registration, build, verify):
        key = key_for(component, identity)
        eid = self._entry_id(component, key)
        with self.mutex():
            before = self._load()
            self._verify_projection(before)
            before = self._evict(before, component, eid not in before['entries'], eid)
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
                    stage.mkdir(mode=0o700)
                    entry = {'component': component, 'key': key, 'identity': identity, 'path': str(final), 'seq': before['seq'] + 1,
                             'lock': inode(lock), 'node': inode(stage), 'owner': self.owner['id']}
                    atomic(stage / '.bench-owner.json', canonical({'owner': self.owner['id'], 'component': component, 'key': key, 'identity': identity}))
                    journal['new'] = entry
                    self._save_journal(journal)
                    build(stage, final)
                    self._owned_dir(stage, entry)
                    os.rename(stage, final)
                    sync_dir(stage.parent)
                    sync_dir(final.parent)
                    self._checkpoint('creation:publish')
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
            except Exception:
                # Eviction was already committed; rollback only this creation.
                if self.journal.exists():
                    self._roll(journal, False)
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
            self._verify_projection(index)
            names = []
            for name, reg in index['registrations'].items():
                parts = reg['suite'].rstrip('\n').split(None, 2)
                if parts[:2] == [repo, suite]:
                    check(len(parts) == 3 and parts[2] == command, 'managed suite command mismatch')
                    names.append(name)
            check([repo, suite] not in index['retired_suites'], 'suite registration evicted')
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
