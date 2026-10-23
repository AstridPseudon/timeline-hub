"""Private exact-byte diagnostic tests; no live proc or handler execution."""
import contextlib
import errno
import hashlib
import io
import os
from pathlib import Path
import stat
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

BASE = Path(sys.argv[3])
BASE.mkdir(parents=True, exist_ok=True)
SOURCE_PATH, COMMAND_PATH = Path(sys.argv[1]), Path(sys.argv[2])
SOURCE = SOURCE_PATH.read_bytes()
COMMAND = COMMAND_PATH.read_bytes()
assert COMMAND == b"python3 - <<'PY'\n" + SOURCE + b"PY\n"
CODE = compile(SOURCE, str(SOURCE_PATH), 'exec')
ROOT = str(BASE / 'mock-proc')
SECRET = 'SECRET_ARG_CREDENTIAL_MOUNT_EXE_1840'
ALLOWED = set('proc_root_visible proc_root_readable proc_entries_visible mountinfo_visible mountinfo_readable pid_ns_self_visible pid_ns_init_visible pid_ns_same pid pid_exists_before pid_exists_after_cmdline pid_exists_after_exe cmdline_empty cmdline_bytes exe_errno race classification result observation'.split())

class InjectedError(OSError):
    pass

class Model:
    def __init__(self, payload=b'arg\0' + SECRET.encode(), exe_error=None, inject=None, error=None, race=None, hidden=False, names=None):
        self.payload, self.exe_error = payload, exe_error
        self.inject, self.error, self.race, self.hidden = inject, error, race, hidden
        self.names = names if names is not None else ['42', '43']
        self.trace, self.denied, self.offset, self.nextfd = [], False, {}, 10
    def step(self, op, path):
        assert not self.denied, 'SENTINEL: observation after denial'
        self.trace.append((op, path))
        if len(self.trace) - 1 == self.inject:
            self.denied = True
            raise self.error
        if self.race == (op, path):
            raise FileNotFoundError(errno.ENOENT, SECRET)
    def stat(self, path):
        self.step('stat', path)
        if self.hidden and path == ROOT:
            raise FileNotFoundError(errno.ENOENT, SECRET)
        return SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_dev=1, st_ino=2, st_size=0)
    def open(self, path, flags):
        self.step('open', path)
        self.nextfd += 1
        self.offset[self.nextfd] = (path, 0)
        return self.nextfd
    def close(self, fd):
        pass
    def read(self, fd, length):
        path, pos = self.offset[fd]
        self.step('read', path)
        data = self.payload[pos:pos+length]
        self.offset[fd] = (path, pos + len(data))
        return data
    def readlink(self, path):
        self.step('readlink', path)
        if self.exe_error:
            raise OSError(self.exe_error, SECRET)
        return '/private/target/' + SECRET
    def scandir(self, path):
        self.step('scandir', path)
        model = self
        class Entries:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def __iter__(self):
                model.step('iterate', path)
                return iter(SimpleNamespace(name=n) for n in model.names)
        return Entries()

def run(model):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.dict(os.environ, TL_RETIRE_DIAG_PROC_ROOT=ROOT))
        for name in ('stat', 'open', 'read', 'close', 'readlink', 'scandir'):
            stack.enter_context(patch.object(os, name, getattr(model, name)))
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                exec(CODE, {'__name__': '__main__'})
            except SystemExit as exc:
                status = exc.code
            else:
                status = 0
    output = out.getvalue()
    assert not err.getvalue(), err.getvalue()
    assert SECRET not in output and ROOT not in output and '/private/target' not in output
    values = set('yes no not-observed permission-denied unknown stop-permission-denied stop-tool-refusal none no-failing-exe-observed observed-empty-cmdline-exe-failure handler-continues-exe-branch executable-unreadable refused unknown-race pid-vanished pid-or-metadata-unavailable pid-entry-changed unknown-cmdline-limit unknown-scan-limit stop-proc-root-unavailable ENOENT EIO EACCES EPERM UNKNOWN'.split())
    observations = set('proc-root-stat proc-root-open mountinfo-stat mountinfo-open pid-ns-self-stat pid-ns-self-open pid-ns-init-stat pid-ns-init-open proc-root-scan pid-before cmdline-open cmdline-read pid-after-cmdline exe-readlink pid-after-exe'.split())
    assert len(output.splitlines()) <= 2, output
    for line in output.splitlines():
        assert all(pair.split('=', 1)[0] in ALLOWED for pair in line.split()), output
        assert all(len(pair.split('=', 1)) == 2 for pair in line.split()), output
        for pair in line.split():
            key, value = pair.split('=', 1)
            assert value.isdecimal() or value in (observations if key == 'observation' else values), pair
    return status, output

baseline = Model()
assert run(baseline)[0] == 0
# Every read/stat/probe/iteration in a successful two-PID trace is denied
# independently; any later observation raises the sentinel assertion.
for index, observation in enumerate(baseline.trace):
    for error in (PermissionError(SECRET), InjectedError(errno.EACCES, SECRET), InjectedError(errno.EPERM, SECRET)):
        model = Model(inject=index, error=error)
        status, output = run(model)
        assert status == 3 and 'result=stop-permission-denied' in output, (index, output)
        assert model.denied and len(model.trace) == index + 1
print(f'PASS permission matrix: {len(baseline.trace)} observations x 3 denial forms; no next-observation sentinel reached')
# Also deny the existence check reached after an exe failure.
model = Model(payload=b'', exe_error=errno.ENOENT)
assert run(model)[0] == 0
for error in (PermissionError(SECRET), InjectedError(errno.EACCES, SECRET), InjectedError(errno.EPERM, SECRET)):
    denied = Model(payload=b'', exe_error=errno.ENOENT, inject=len(model.trace)-1, error=error)
    assert run(denied)[0] == 3 and denied.denied
print('PASS exe-error post-existence denial x 3')
for label in ('pid-after-cmdline', 'pid-after-exe'):
    # Trace indexes distinguish repeated stats of the same PID directory.
    index = 14 if label == 'pid-after-cmdline' else 16
    assert baseline.trace[index] == ('stat', ROOT+'/42'), baseline.trace
    raced = Model(inject=index, error=FileNotFoundError(errno.ENOENT, SECRET))
    status, output = run(raced)
    assert status == 4 and 'unknown-race' in output
    print('PASS', label, 'race exit 4')
checks = [
    ('empty-ENOENT', Model(payload=b'', exe_error=errno.ENOENT), 0, 'handler-continues-exe-branch'),
    ('nonempty-ENOENT', Model(exe_error=errno.ENOENT), 2, 'executable-unreadable'),
    ('hidden-root', Model(hidden=True), 3, 'stop-tool-refusal'),
    ('cmdline-ENOENT', Model(race=('open', ROOT+'/42/cmdline')), 4, 'unknown-race'),
    ('pid-exit-race', Model(race=('stat', ROOT+'/42')), 4, 'unknown-race'),
    ('readable-target-use-unqualified', Model(), 0, 'no-failing-exe-observed'),
    ('empty-table', Model(names=[]), 0, 'no-failing-exe-observed'),
    ('cmdline-limit', Model(payload=b'x'*1048577), 3, 'unknown-cmdline-limit'),
    ('unknown-exe-error', Model(exe_error=errno.EIO), 2, 'executable-unreadable'),
    ('pid-scan-limit', Model(names=[str(n) for n in range(2, 4099)]), 3, 'unknown-scan-limit'),
    ('mountinfo-ENOENT', Model(inject=2, error=FileNotFoundError(errno.ENOENT, SECRET)), 3, 'stop-tool-refusal'),
    ('namespace-EIO', Model(inject=4, error=InjectedError(errno.EIO, SECRET)), 3, 'stop-tool-refusal'),
]
for label, model, expected, phrase in checks:
    status, output = run(model)
    assert status == expected and phrase in output, (label, status, output)
    print('PASS', label, 'exit', status)
# Successful reads use actual byte count, even when stat metadata is zero.
assert f'cmdline_bytes={len(b"arg"+bytes([0])+SECRET.encode())}' in run(Model(exe_error=errno.ENOENT))[1]
print('PASS proc-st_size-zero does not imply empty argv; allowlist and secret sentinels on every model run')
# Exact self-contained shell command on real PRIVATE files and symlinks only.
root = BASE / 'disk-proc'
(root/'self/ns').mkdir(parents=True, exist_ok=True)
(root/'1/ns').mkdir(parents=True, exist_ok=True)
(root/'self/mountinfo').write_text(SECRET)
(root/'self/ns/pid').write_text(SECRET)
(root/'1/ns/pid').write_text(SECRET)
(root/'1/cmdline').write_bytes(b'arg\0'+SECRET.encode())
if not (root/'1/exe').is_symlink():
    (root/'1/exe').symlink_to(BASE / SECRET)
result = subprocess.run(['bash', str(COMMAND_PATH)], env=dict(os.environ, TL_RETIRE_DIAG_PROC_ROOT=str(root)), capture_output=True, text=True)
assert result.returncode == 0 and 'no-failing-exe-observed' in result.stdout
assert not result.stderr and SECRET not in result.stdout and str(root) not in result.stdout
print('PASS exact command private disk fixture with dangling exe symlink and secret mountinfo/cmdline/namespace contents; exit 0')
print('PASS script sha256', hashlib.sha256(SOURCE).hexdigest())
print('PASS command sha256', hashlib.sha256(COMMAND).hexdigest())
