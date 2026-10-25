"""Private D77 measurement helper. Import only; no live workload entry point.

Bounds are a prerequisite supplied by the caller, not estimates inferred from
the 1237 lower bound. Unsupported tools must first expose a bounded normal
cancellation seam. This helper never kills unrelated processes or uses SIGKILL.
"""

from dataclasses import dataclass
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time


START_BYTES = 5_200_000_000
PHASE_FLOOR_BYTES = 4_500_000_000
OVERALL_STOP_BYTES = 4_000_000_000
POLL_SECONDS = 0.05
CANCEL_SECONDS = 0.5
MARGIN_BYTES = 50_000_000


@dataclass(frozen=True)
class Bounds:
    # Include ALL writers on this filesystem, plus in-flight writes at cancel.
    rate_bytes_per_second: int
    burst_bytes: int
    normal_cancel_supported: bool

    def reserve(self):
        if (not self.normal_cancel_supported
                or not isinstance(self.rate_bytes_per_second, int)
                or not isinstance(self.burst_bytes, int)
                or self.rate_bytes_per_second <= 0 or self.burst_bytes < 0):
            raise ValueError("a bounded normal cancellation seam is required")
        return (math.ceil(self.rate_bytes_per_second * (POLL_SECONDS + CANCEL_SECONDS))
                + self.burst_bytes + MARGIN_BYTES)


@dataclass(frozen=True)
class Step:
    label: str
    argv: tuple[str, ...]
    cwd: str
    bounds: Bounds | None
    env: dict | None = None
    admission: bool = False


def free_bytes(path):
    stat = os.statvfs(path)
    return stat.f_bavail * stat.f_frsize


def allocated_bytes(paths):
    """Boundary telemetry only; never called while a phase group is live."""
    return sum(int(subprocess.check_output(
        ["du", "-B1", "-s", str(path)], text=True, timeout=5).split()[0])
        for path in paths)


def group_alive(pgid):
    # Linux-only private diagnostic. Ignore dead descendants waiting for reaping.
    for entry in Path('/proc').iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            fields = (entry / 'stat').read_text().rsplit(')', 1)[1].split()
            if int(fields[2]) == pgid and fields[0] not in ('Z', 'X'):
                return True
        except (FileNotFoundError, ProcessLookupError):
            pass
    return False


class Monitor:
    def __init__(self, root, *, free=None, allocation=None, timeout=180,
                 cancel=None):
        if not 0 < timeout <= 1200:
            raise ValueError("timeout must be positive and at most 1200 seconds")
        self.root = Path(root)
        self.free = free or (lambda: free_bytes(self.root))
        self.allocation = allocation
        self.timeout = timeout
        self.cancel = cancel or threading.Event()
        self.used = False
        self.unfinished = []

    def run(self, steps):
        # The caller's normal SIGINT/SIGTERM route reaches the same sticky latch.
        previous = {}
        if threading.current_thread() is threading.main_thread():
            for sig in (signal.SIGINT, signal.SIGTERM):
                previous[sig] = signal.signal(sig, lambda *_: self.cancel.set())
        try:
            return self._run(steps)
        finally:
            for sig, handler in previous.items():
                signal.signal(sig, handler)

    def _run(self, steps):
        if self.used:
            raise RuntimeError("a monitor is single-use, including after cancellation")
        self.used = True
        steps = tuple(steps)
        started = time.monotonic()
        result = dict(status='running', phase_complete=False, cancelled=False,
                      commands=[], samples=[], allocations=[], reason=None,
                      start_bytes=START_BYTES, phase_floor_bytes=PHASE_FLOOR_BYTES,
                      overall_stop_bytes=OVERALL_STOP_BYTES,
                      poll_seconds=POLL_SECONDS, cancel_seconds=CANCEL_SECONDS,
                      margin_bytes=MARGIN_BYTES, measurement_peak_complete=False)

        def stop(reason):
            if result['reason'] is None:
                result['reason'] = reason
            if result['status'] != 'unsupported-normal-cancellation-seam':
                result['status'] = 'cancelled-lower-bound'
            result['cancelled'] = True

        def sample(label, threshold):
            try:
                value = self.free()
                if not isinstance(value, int) or value < 0:
                    raise ValueError('invalid free-space measurement')
            except Exception as exc:
                stop('free-space-unavailable: ' + str(exc))
                return
            result['samples'].append(dict(label=label, monotonic=time.monotonic(),
                                          free_bytes=value,
                                          margin_to_phase_floor=value-PHASE_FLOOR_BYTES))
            if value <= OVERALL_STOP_BYTES:
                stop('overall-stop-floor')
            elif value <= threshold:
                stop('admission' if threshold == START_BYTES else 'phase-reserve')

        def check(label, threshold):
            sample(label, threshold)
            if self.cancel.is_set():
                stop('caller-cancelled')
            if time.monotonic() - started >= self.timeout:
                stop('deadline')

        def allocation(label):
            if self.allocation is not None:
                try:
                    result['allocations'].append(dict(label=label,
                                                      allocated_bytes=self.allocation()))
                except Exception as exc:
                    stop('allocation-unavailable: ' + str(exc))

        # Validate the entire path before any mutator. No guessed live bounds.
        try:
            if sys.platform != 'linux' or not steps:
                raise ValueError('requires Linux and a nonempty finite step list')
            reserves = [step.bounds.reserve() for step in steps]
            if any(not step.argv for step in steps):
                raise ValueError('empty command')
        except (ValueError, AttributeError) as exc:
            result.update(status='unsupported-normal-cancellation-seam', reason=str(exc))
            return result

        check('phase:admission', START_BYTES)
        if not result['cancelled']:
            allocation('phase:before')
        for step, reserve in zip(steps, reserves):
            if result['cancelled']:
                break
            # Recheck after potentially slow boundary du, BEFORE Popen.
            threshold = max(PHASE_FLOOR_BYTES + reserve,
                            START_BYTES if not result['commands'] or step.admission else 0)
            check(step.label + ':before', threshold)
            if result['cancelled']:
                break
            row = dict(label=step.label, argv=list(step.argv), cwd=step.cwd,
                       exit=None, cancelled=False, cleanup_complete=False,
                       reserve_bytes=reserve, cancel_signals=[])
            result['commands'].append(row)
            process = None
            try:
                process = subprocess.Popen(step.argv, cwd=step.cwd, env=step.env,
                                           start_new_session=True,
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
                while True:
                    # Always sample, even if the command exited before our first poll.
                    check(step.label + ':poll', PHASE_FLOOR_BYTES + reserve)
                    code = process.poll()
                    if code is not None:
                        if code != 0:
                            stop('command-failed')
                        if group_alive(process.pid):
                            stop('descendants-after-command-exit')
                    if result['cancelled'] or code is not None:
                        break
                    self.cancel.wait(POLL_SECONDS)
            except (Exception, KeyboardInterrupt) as exc:
                stop('command-interrupted: ' + type(exc).__name__)
            finally:
                if process is not None:
                    if result['cancelled']:
                        row['cancelled'] = True
                        # Signal only our new session's process group. A leader
                        # exiting does not prove its children have stopped.
                        for sig in (signal.SIGINT, signal.SIGTERM):
                            try:
                                os.killpg(process.pid, sig)
                                row['cancel_signals'].append(sig.name)
                            except ProcessLookupError:
                                break
                            until = time.monotonic() + CANCEL_SECONDS / 2
                            while time.monotonic() < until:
                                process.poll()
                                if not group_alive(process.pid):
                                    break
                                time.sleep(0.01)
                            if not group_alive(process.pid):
                                break
                    row['exit'] = process.poll()
                    row['cleanup_complete'] = not group_alive(process.pid)
                    if not row['cleanup_complete']:
                        stop('normal-cancellation-incomplete')
                        result['status'] = 'unsupported-normal-cancellation-seam'
                        # Retain the handle for the caller; never silently lose
                        # ownership or force an uncooperative process to stop.
                        self.unfinished.append(process)
                    check(step.label + ':end', PHASE_FLOOR_BYTES + reserve)
                else:
                    row['cancelled'] = True
            if result['cancelled']:
                break
            allocation(step.label + ':after')
        if not result['cancelled']:
            check('phase:final', PHASE_FLOOR_BYTES + max(reserves))
        complete = (not result['cancelled'] and len(result['commands']) == len(steps)
                    and all(row['exit'] == 0 and not row['cancelled']
                            and row['cleanup_complete'] for row in result['commands']))
        result['phase_complete'] = complete
        if complete:
            result['status'] = 'complete'
        result['observed_min_free_bytes'] = min(
            (row['free_bytes'] for row in result['samples']), default=None)
        result['observed_peak_allocated_bytes_lower_bound'] = max(
            (row['allocated_bytes'] for row in result['allocations']), default=None)
        result['elapsed_seconds'] = time.monotonic() - started
        return result


# Exact 1237 pins/commands; original source retained alongside this helper.
ARCHIVE_SHA = 'a7673f9f9b77d24989a5a84b70380f77af3dd869a7be2b94c8d56de404065ecb'
SOURCE_SHA = '3a84ac8be7d11434de8b22f4f0f1d643582ecc01c644e347bb0e056401da7b2e'
LOCK_SHA = 'f08eab1fd7e0519e8b131697d6a35815fd71d9b0a61a8d70cc57b499bcba53ee'
BUN_SHA = '951ee2aee855f08595aeec6225226a298d3fea83a3dcd6465c09cbccdf7e848f'
NATIVE_SHA = 'f380a65df2a2487b010314872b0d543dbbdc204a97b60551c4aaa5bf0f2dbd2b'
BUN_URL = 'https://github.com/oven-sh/bun/releases/download/bun-v1.3.14/bun-linux-x64.zip'
NATIVE_URL = 'https://registry.npmjs.org/@oh-my-pi/pi-natives-linux-x64/-/pi-natives-linux-x64-17.4.0.tgz'
ABI_PROBE = "import {pathToFileURL} from 'node:url';const b=await import(pathToFileURL(process.argv[1]).href);if(typeof b.__piNativesV17_4_0!=='function')throw Error('OMP native ABI mismatch');"
OMP_LABELS = ('source-extract', 'bun-fetch', 'bun-install', 'lock-after-install',
              'gen-tool-views', 'lock-after-views', 'native-fetch',
              'native-abi-probe', 'bun-link')


def omp_steps(root, archive, bounds, *, python=sys.executable, env=None):
    """Construct only. Does not acquire/reacquire or execute anything.

    root must be a fresh private directory. No fallback for the retained 1229
    archive exists. bounds must cover the whole path BEFORE source extraction.
    The manager must authorize any later live use; this task runs only stubs.
    """
    root = Path(root).resolve()
    archive = Path(archive).resolve()
    if not root.is_dir() or any(root.iterdir()):
        raise ValueError('root must be an existing empty private directory')
    source = root / 'source'
    bun = root / 'bun/bun-linux-x64/bun'
    home = root / 'build-home'
    build_env = {k: v for k, v in (os.environ if env is None else env).items()
                 if not k.startswith('BUN_') and k != 'NODE_OPTIONS'}
    build_env.update({'BUN_INSTALL': str(root), 'BUN_INSTALL_BIN': str(root / 'bin'),
                      'BUN_INSTALL_GLOBAL_DIR': str(root / 'install/global'),
                      'BUN_INSTALL_CACHE_DIR': str(root / 'bun-cache'),
                      'HOME': str(home), 'USERPROFILE': str(home),
                      'XDG_CONFIG_HOME': str(home / 'config'),
                      'npm_config_registry': 'https://registry.npmjs.org',
                      'NPM_CONFIG_REGISTRY': 'https://registry.npmjs.org',
                      'PATH': str(bun.parent) + os.pathsep + build_env.get('PATH', '')})
    worker = (str(python), str(Path(__file__).resolve()), '--omp-step')
    commands = {
        'bun-install': (str(bun), 'install', '--frozen-lockfile', '--ignore-scripts',
                        '--omit', 'optional'),
        'gen-tool-views': (str(bun), 'run', 'gen:tool-views'),
        'native-abi-probe': (str(bun), '-e', ABI_PROBE,
                             str(source / 'packages/natives/native/index.js')),
        'bun-link': (str(bun), 'link', '--frozen-lockfile', '--ignore-scripts', '--no-save'),
    }
    return tuple(Step(label, commands.get(label, worker + (label, str(root), str(archive))),
                      str(source / 'packages/coding-agent' if label == 'bun-link'
                          else source if label in commands else root),
                      bounds.get(label), build_env, label == 'bun-install')
                 for label in OMP_LABELS)


def omp_worker(label, root, archive):
    # Runs ONLY inside Monitor's owned process group, including fetch/extract,
    # directory creation, native moves, chmod, hashes and version verification.
    import hashlib
    import json
    from astrid.installer.tools import extract, fetch_archive, source_tree_sha256

    def sha(path):
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
        return digest.hexdigest()

    def require(actual, expected):
        if actual != expected:
            raise RuntimeError('exact pinned integrity mismatch')

    root, archive = Path(root), Path(archive)
    source = root / 'source'
    metadata = {}
    if label == 'source-extract':
        require(sha(archive), ARCHIVE_SHA)
        extract(archive, source, reject_links=True)
        require(source_tree_sha256(source), SOURCE_SHA)
        require(sha(source / 'bun.lock'), LOCK_SHA)
        (root / 'bun-cache').mkdir()
        (root / 'build-home/config').mkdir(parents=True)
        metadata.update(archive_sha256=ARCHIVE_SHA, source_tree_sha256=SOURCE_SHA,
                        bun_lock_sha256=LOCK_SHA)
    elif label == 'bun-fetch':
        fetch_archive(BUN_URL, root / 'bun', sha256=BUN_SHA, reject_links=True)
        bun = root / 'bun/bun-linux-x64/bun'
        bun.chmod(0o755)
        version = subprocess.check_output([str(bun), '--version'], text=True).strip()
        require(version, '1.3.14')
        metadata['bun_version'] = version
    elif label in ('lock-after-install', 'lock-after-views'):
        require(sha(source / 'bun.lock'), LOCK_SHA)
        metadata['bun_lock_sha256'] = LOCK_SHA
    elif label == 'native-fetch':
        fetch_archive(NATIVE_URL, root / 'native-archive', sha256=NATIVE_SHA)
        dest = source / 'packages/natives/native'
        dest.mkdir(parents=True, exist_ok=True)
        hashes = {}
        for name in ('pi_natives.linux-x64-baseline.node', 'pi_natives.linux-x64-modern.node'):
            src = root / 'native-archive/package' / name
            if not src.is_file():
                raise RuntimeError('missing native ' + name)
            src.replace(dest / name)
            hashes[name] = sha(dest / name)
        metadata['native_files_sha256'] = hashes
    else:
        raise ValueError('unknown private worker step')
    (root / (label + '.json')).write_text(json.dumps(metadata, indent=2) + '\n')


if __name__ == '__main__':
    if len(sys.argv) != 5 or sys.argv[1] != '--omp-step':
        raise SystemExit('Private child helper; import Monitor. No live phase CLI.')
    omp_worker(*sys.argv[2:])
