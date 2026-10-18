"""Matched trusted host/relay bootstrap ABI (stdlib only).

This is not a workload descriptor exception. The owner creates the endpoints;
the authenticated trampoline admits their exact identities before exec. Keep
this file byte-identical to Runtime's banodoco_local/hosted_contract.py.
"""
from __future__ import annotations

import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import sys
import tempfile

VERSION = 'runtime.hosted-bootstrap/v1'
LIMIT = 16 * 1024 * 1024
FD_KEY = 'ASTRID_RUNTIME_CUSTODY_HOSTED_FD'
DIGEST_KEY = 'ASTRID_RUNTIME_CUSTODY_HOSTED_DIGEST'
CONSUMER_FD = 'ASTRID_HOSTED_BINDING_FD'
CONSUMER_DIGEST = 'ASTRID_HOSTED_BINDING_DIGEST'


class HostedContractError(RuntimeError):
    pass


def _pipe_identity(fd, direction):
    if type(fd) is not int or fd < 3:
        raise HostedContractError('private pipe descriptor is invalid')
    value = os.fstat(fd)
    if (not stat.S_ISFIFO(value.st_mode) or value.st_nlink != 0
            or fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_ACCMODE != direction):
        raise HostedContractError('private channel is not an anonymous directional pipe')
    return {'fd': fd, 'device': value.st_dev, 'inode': value.st_ino, 'direction': direction}


def _validate_pipe_binding(value):
    if not isinstance(value, list) or len(value) != 2:
        raise HostedContractError('private pipe binding is invalid')
    descriptors = []
    for item, direction in zip(value, (os.O_RDONLY, os.O_WRONLY)):
        if (not isinstance(item, dict) or set(item) != {'fd', 'device', 'inode', 'direction'}
                or any(type(part) is not int for part in item.values())
                or _pipe_identity(item.get('fd'), direction) != item):
            raise HostedContractError('private pipe identity differs')
        descriptors.append(item['fd'])
    if descriptors[0] == descriptors[1]:
        raise HostedContractError('private pipe endpoints collide')
    return tuple(descriptors)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()


def digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def readonly_payload(data):
    if not isinstance(data, bytes) or not data or len(data) > LIMIT:
        raise HostedContractError('hosted binding exceeds its bound')
    fd, name = tempfile.mkstemp(prefix='runtime-hosted-')
    try:
        with os.fdopen(fd, 'wb') as writer:
            os.fchmod(writer.fileno(), 0o600)
            writer.write(data)
            writer.flush()
        result = os.open(name, os.O_RDONLY | os.O_NOFOLLOW)
        os.set_inheritable(result, False)
        return os.fdopen(result, 'rb')
    finally:
        os.unlink(name)


def file_identity(fd):
    value = os.fstat(fd)
    if (type(fd) is not int or fd < 3 or not stat.S_ISREG(value.st_mode)
            or value.st_uid != os.getuid() or value.st_nlink != 0
            or stat.S_IMODE(value.st_mode) != 0o600
            or fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_ACCMODE != os.O_RDONLY
            or value.st_size <= 0 or value.st_size > LIMIT):
        raise HostedContractError('hosted binding is not a bounded private read-only descriptor')
    return {'fd': fd, 'device': value.st_dev, 'inode': value.st_ino, 'size': value.st_size}


def read_payload(fd, expected):
    identity = file_identity(fd)
    data = os.pread(fd, identity['size'] + 1, 0)
    if len(data) != identity['size'] or digest(data) != expected or file_identity(fd) != identity:
        raise HostedContractError('hosted binding digest or identity differs')
    return data


def socket_identity(fd):
    if type(fd) is not int or fd < 3 or not stat.S_ISSOCK(os.fstat(fd).st_mode):
        raise HostedContractError('hosted endpoint is not a private socket')
    value = os.fstat(fd)
    channel = socket.socket(fileno=fd)
    try:
        if (channel.family != socket.AF_UNIX or channel.type != socket.SOCK_STREAM
                or channel.getsockname() or channel.getpeername()):
            raise HostedContractError('hosted endpoint is not an unnamed connected stream')
    finally:
        channel.detach()
    return {'fd': fd, 'device': value.st_dev, 'inode': value.st_ino}


def descriptor_set():
    if sys.platform != 'darwin':
        raise HostedContractError('hosted descriptor census requires Darwin')
    class FDInfo(ctypes.Structure):
        _fields_ = [('fd', ctypes.c_int32), ('kind', ctypes.c_uint32)]
    library = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
    library.proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
    library.proc_pidinfo.restype = ctypes.c_int
    size = library.proc_pidinfo(os.getpid(), 1, 0, None, 0)
    if size <= 0:
        raise HostedContractError('hosted descriptor census unavailable')
    entries = (FDInfo * (size // ctypes.sizeof(FDInfo) + 128))()
    used = library.proc_pidinfo(os.getpid(), 1, 0, ctypes.byref(entries), ctypes.sizeof(entries))
    if used <= 0 or used >= ctypes.sizeof(entries) or used % ctypes.sizeof(FDInfo):
        raise HostedContractError('hosted descriptor census incomplete')
    return {entry.fd for entry in entries[:used // ctypes.sizeof(FDInfo)] if entry.fd > 2}


class _BSD(ctypes.Structure):
    _fields_ = [(name, ctypes.c_uint32) for name in (
        'flags', 'status', 'xstatus', 'pid', 'ppid', 'uid', 'gid', 'ruid', 'rgid', 'svuid', 'svgid', 'reserved')
    ] + [('comm', ctypes.c_char * 16), ('name', ctypes.c_char * 32)] + [
        (name, ctypes.c_uint32) for name in ('nfiles', 'pgid', 'jobc', 'tdev', 'tpgid')
    ] + [('nice', ctypes.c_int32), ('start_sec', ctypes.c_uint64), ('start_usec', ctypes.c_uint64)]


class _Usage(ctypes.Structure):
    _fields_ = [('uuid', ctypes.c_uint8 * 16)] + [(name, ctypes.c_uint64) for name in (
        'user', 'system', 'idle', 'interrupt', 'pageins', 'wired', 'resident', 'footprint', 'start_abstime', 'exit_abstime')]


def incarnation(pid):
    if sys.platform != 'darwin' or type(pid) is not int or pid <= 0:
        raise HostedContractError('hosted process incarnation requires Darwin')
    library = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
    library.proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
    library.proc_pidinfo.restype = ctypes.c_int
    library.proc_pid_rusage.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    library.proc_pid_rusage.restype = ctypes.c_int
    bsd, usage = _BSD(), _Usage()
    if (library.proc_pidinfo(pid, 3, 0, ctypes.byref(bsd), ctypes.sizeof(bsd)) != ctypes.sizeof(bsd)
            or library.proc_pid_rusage(pid, 0, ctypes.byref(usage)) != 0
            or bsd.pid != pid or bsd.status not in {1, 2, 3, 4}
            or not usage.start_abstime or usage.exit_abstime):
        raise HostedContractError('hosted process incarnation is unavailable')
    return {'pid': pid, 'uid': int(bsd.uid), 'start_sec': int(bsd.start_sec),
            'start_usec': int(bsd.start_usec), 'start_abstime': int(usage.start_abstime)}


def birth_fence(process):
    library = ctypes.CDLL('/usr/lib/libSystem.B.dylib')
    library.mach_absolute_time.argtypes = []
    library.mach_absolute_time.restype = ctypes.c_uint64
    if int(library.mach_absolute_time()) <= process['start_abstime']:
        raise HostedContractError('hosted incarnation has no strict monotonic birth fence')


def validate(value, *, role, argv=None):
    fields = {'version', 'purpose', 'role', 'run_id', 'owner_epoch', 'generation', 'operation_id',
              'channel_id', 'profile_digest', 'scope', 'argv_digest', 'sockets', 'launch_binding'}
    if (not isinstance(value, dict) or set(value) - fields - {'inspection_pipes'} or not fields <= set(value) or value['version'] != VERSION
            or role not in {'host', 'relay'} or value['role'] != role
            or value['purpose'] != 'runtime-' + role + '-control/v1'
            or type(value['generation']) is not int or value['generation'] < 1
            or any(not isinstance(value[k], str) or not value[k] or len(value[k]) > 4096
                   for k in ('run_id', 'owner_epoch', 'operation_id', 'channel_id', 'profile_digest', 'scope', 'argv_digest'))
            or set(value['sockets']) != ({'control', 'activation'} if role == 'host' else {'control'})
            or argv is not None and value['argv_digest'] != digest(canonical(argv))):
        raise HostedContractError('hosted purpose, role or launch binding differs')
    fds = []
    for item in value['sockets'].values():
        if not isinstance(item, dict) or socket_identity(item['fd']) != item:
            raise HostedContractError('hosted socket descriptor identity differs')
        fds.append(item['fd'])
    if 'inspection_pipes' in value:
        if role != 'host':
            raise HostedContractError('inspection pipes require the selected Host')
        fds.extend(_validate_pipe_binding(value['inspection_pipes']))
    binding = value['launch_binding']
    if binding is not None:
        if role != 'host' or set(binding) != {'identity', 'digest'} or file_identity(binding['identity']['fd']) != binding['identity']:
            raise HostedContractError('hosted launcher descriptor differs')
        read_payload(binding['identity']['fd'], binding['digest'])
        fds.append(binding['identity']['fd'])
    if len(set(fds)) != len(fds):
        raise HostedContractError('hosted descriptors collide')
    return set(fds)


class HostedLaunch:
    """Owned endpoints for exactly one broker admission; no supplied sockets."""

    def __init__(self, broker, preparation):
        if (broker.role not in {'host', 'relay'} or broker.owner_epoch != preparation['owner_epoch']
                or broker.authority_scope_root is None or str(broker.authority_scope_root) != preparation['custody_scope']):
            raise HostedContractError('hosted owner or role differs')
        self.broker, self.preparation = broker, preparation
        self.parents, self.children = {}, {}
        self.binding = None
        self.value = None
        try:
            for name in ('control', 'activation') if broker.role == 'host' else ('control',):
                self.parents[name], self.children[name] = socket.socketpair()
        except BaseException:
            self.close()
            raise

    def environment(self, argv, *, launch_binding=None):
        if self.value is not None:
            raise HostedContractError('hosted launch was already selected')
        broker, preparation = self.broker, self.preparation
        profile = preparation['profile']
        executable = profile['host_executable' if broker.role == 'host' else 'worker_executable']
        if argv[0] != executable:
            raise HostedContractError('hosted executable differs from selected profile')
        if broker.role == 'relay':
            if (len(argv) != 6 or argv[1:3] != ['-I', '-S']
                    or Path(argv[3]).name != 'local_execution_supervisor.py'
                    or argv[4:] != ['--prepared-control-fd', str(self.children['control'].fileno())]):
                raise HostedContractError('relay target is not the matched consumer')
        elif launch_binding is not None:
            if (len(argv) != 6 or argv[1:3] != ['-I', '-S']
                    or not Path(argv[3]).is_absolute()
                    or argv[4:] != ['--binding-fd', str(launch_binding.fileno())]):
                raise HostedContractError('host target is not the verified binding launcher')
        else:
            if argv[1:3] != ['-m', 'astrid.core.execution.generic_host']:
                raise HostedContractError('host target is not GenericHost')
            for flag, selected in (
                    ('--host-control-fd', str(self.children['control'].fileno())),
                    ('--activation-fd', str(self.children['activation'].fileno())),
                    ('--activation-operation-id', preparation['operation_id']),
                    ('--activation-channel-id', preparation['channel_id'])):
                if argv.count(flag) != 1 or argv[argv.index(flag) + 1] != selected:
                    raise HostedContractError('host target channels differ from owned endpoints')
        self.value = {'version': VERSION, 'role': broker.role, 'purpose': 'runtime-' + broker.role + '-control/v1',
            'run_id': broker.run_id, 'owner_epoch': broker.owner_epoch, 'generation': broker.custody_generation,
            'operation_id': preparation['operation_id'], 'channel_id': preparation['channel_id'],
            'profile_digest': digest(canonical(preparation['profile'])), 'scope': str(broker.authority_scope_root),
            'argv_digest': digest(canonical(argv)),
            'sockets': {name: socket_identity(channel.fileno()) for name, channel in self.children.items()},
            'launch_binding': None if launch_binding is None else {
                'identity': file_identity(launch_binding.fileno()), 'digest': digest(os.pread(launch_binding.fileno(), LIMIT + 1, 0))}}
        if getattr(broker, 'child_pipe_binding', None):
            if broker.role != 'host' or profile.get('execution_mode') != 'host_only_cpu':
                raise HostedContractError('inspection requires the selected CPU Host')
            launch = profile.get('host_launch') or {}
            if not launch.get('renderer_selection'):
                # Parent-side static discovery only. The stdlib trampoline and
                # consumer validate the sealed descriptors without SDK imports.
                if profile.get('session_config_digest') != digest(canonical(launch)):
                    raise HostedContractError('inspection launch differs from selected profile')
                from astrid.core.execution.generic_host import _launch_needs_command_inspection
                roots = (Path(launch['pack_root']),
                         *(Path(root['path']) for root in launch.get('additional_pack_roots', [])))
                matrix = Path(launch['capability_matrix']) if launch.get('capability_matrix') else None
                if not _launch_needs_command_inspection(roots, matrix):
                    raise HostedContractError('inspection requires selected binary declarations')
            self.value['inspection_pipes'] = broker.child_pipe_binding
        validate(self.value, role=broker.role, argv=argv)
        data = canonical(self.value)
        self.binding = readonly_payload(data)
        return {FD_KEY: str(self.binding.fileno()), DIGEST_KEY: digest(data)}

    @property
    def pass_fds(self):
        return tuple(sorted(validate(self.value, role=self.broker.role) | {self.binding.fileno()}))

    def close_children(self):
        for child in self.children.values():
            child.close()
        if self.binding is not None:
            self.binding.close()

    def close(self):
        self.close_children()
        for parent in self.parents.values():
            parent.close()


def bootstrap(environment, argv):
    role = environment.get('ASTRID_RUNTIME_CUSTODY_ROLE')
    if CONSUMER_FD in environment or CONSUMER_DIGEST in environment:
        raise HostedContractError('hosted consumer binding cannot be supplied before bootstrap')
    fd = int(environment[FD_KEY])
    try:
        data = read_payload(fd, environment[DIGEST_KEY])
        value = json.loads(data)
        fds = validate(value, role=role, argv=argv)
        if (value['run_id'] != environment['ASTRID_RUNTIME_CUSTODY_RUN_ID']
                or descriptor_set() != fds | {fd}):
            raise HostedContractError('hosted launch has missing or unexpected descriptors')
        for descriptor in fds:
            os.set_inheritable(descriptor, False)
        return value, incarnation(os.getpid())
    finally:
        os.close(fd)


def publish_consumer(value, process):
    proof = readonly_payload(canonical({'binding': value, 'process': process}))
    os.set_inheritable(proof.fileno(), True)
    for item in value['sockets'].values():
        os.set_inheritable(item['fd'], True)
    if value['launch_binding'] is not None:
        os.set_inheritable(value['launch_binding']['identity']['fd'], True)
    for item in value.get('inspection_pipes', []):
        os.set_inheritable(item['fd'], True)
    return proof, {CONSUMER_FD: str(proof.fileno()), CONSUMER_DIGEST: digest(proof.read())}


def consume(role, sockets):
    fd = int(os.environ.pop(CONSUMER_FD))
    expected = os.environ.pop(CONSUMER_DIGEST)
    try:
        proof = json.loads(read_payload(fd, expected))
    finally:
        os.close(fd)
    value = proof['binding']
    # The selected launcher has consumed its own file before importing the host.
    copied = {**value, 'launch_binding': None}
    validate(copied, role=role)
    if (set(proof) != {'binding', 'process'} or proof['process'] != incarnation(os.getpid())
            or {name: item['fd'] for name, item in value['sockets'].items()} != sockets
            or descriptor_set() != set(sockets.values()) | {p['fd'] for p in value.get('inspection_pipes', [])}):
        raise HostedContractError('hosted consumer role, descriptors or process incarnation differs')
    if value.get('inspection_pipes'):
        selected = json.loads(os.environ.get('ASTRID_COMMAND_CONTROL_FD', 'null'))
        if selected != value['inspection_pipes']:
            raise HostedContractError('inspection consumer descriptor binding differs')
        for descriptor in _validate_pipe_binding(selected):
            os.set_inheritable(descriptor, False)
    for descriptor in sockets.values():
        os.set_inheritable(descriptor, False)
    return value


def verify_preparation(value, preparation, authority, *, actor):
    if (any(value[k] != preparation[k] for k in ('operation_id', 'channel_id', 'owner_epoch'))
            or value['profile_digest'] != digest(canonical(preparation['profile']))
            or value['scope'] != preparation['custody_scope']):
        raise HostedContractError('hosted preparation differs from authenticated launch')
    reference = authority.reference()
    if (reference['generation'] != value['generation']
            or reference['target']['pid'] != os.getpid()):
        raise HostedContractError('hosted generation or process designation differs')
    authority.verify_reference(reference, expected_actor=actor.verify(), owner_epoch=value['owner_epoch'])
