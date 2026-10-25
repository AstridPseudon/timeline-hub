"""One private diagnostic around the unchanged P4 test; no request substitution."""
import collections
import faulthandler
import hashlib
import json
import os
import selectors
from pathlib import Path
import subprocess
import sys
import threading
import time


OUT = None
EVENTS = None
DUMPS = None
START = time.monotonic()
MAIN = threading.get_ident()
HZ = os.sysconf('SC_CLK_TCK')
LOCK = threading.RLock()
CHILDREN = {}
STOP = threading.Event()
TEST_START = None
COUNTS = collections.Counter()
SAMPLES = []
ERRORS = []
ORIGINAL_POLLS = {}


def event(kind, **data):
    with LOCK:
        row = dict(data)
        row.setdefault('elapsed', time.monotonic() - START)
        row.update(kind=kind, pid=os.getpid())
        EVENTS.write(json.dumps(row) + '\n')
        EVENTS.flush()


def stat(pid, tid=None):
    try:
        path = f'/proc/{pid}/stat' if tid is None else f'/proc/{pid}/task/{tid}/stat'
        fields = Path(path).read_text().rsplit(')', 1)[1].split()
        return dict(state=fields[0], ppid=int(fields[1]), user=float(fields[11]) / HZ,
                    system=float(fields[12]) / HZ, birth_ticks=int(fields[19]))
    except (OSError, ValueError):
        return None


def stack(frame):
    result = []
    while frame is not None:
        result.append([frame.f_code.co_filename, frame.f_code.co_name, frame.f_lineno])
        frame = frame.f_back
    return result


def phase(frame):
    while frame is not None:
        if frame.f_code.co_name == 'test_http_ten_note_commit_per_step_inverse_and_redo':
            line = frame.f_lineno
            stage = ('setup' if line < 305 else 'author' if line < 326 else
                     'commit_readback' if line < 422 else 'restart_open' if line < 428 else
                     'undo' if line < 455 else 'redo')
            note = frame.f_locals.get('note')
            ordinal = note.get('ordinal') if isinstance(note, dict) else None
            return dict(stage=stage, line=line, note=ordinal if isinstance(ordinal, int) else None)
        frame = frame.f_back
    return dict(stage='fixture_or_framework', line=None, note=None)


ORIGINAL_INIT = subprocess.Popen.__init__


def observed_init(self, *args, **kwargs):
    before = time.monotonic()
    ORIGINAL_INIT(self, *args, **kwargs)
    argv = args[0] if args else kwargs.get('args')
    entry = dict(process=self, executable=Path(str(argv[0])).name if isinstance(argv, (list, tuple)) else 'UNKNOWN',
                 start=before, last=stat(self.pid), ended=False)
    with LOCK:
        CHILDREN[self.pid] = entry
    event('spawn', child=self.pid, executable=entry['executable'], spawn_wall=time.monotonic() - before,
          process_stat=entry['last'])


ORIGINAL_SLEEP = time.sleep


def observed_sleep(seconds):
    before = time.monotonic()
    caller = sys._getframe(1)
    where = [caller.f_code.co_filename, caller.f_code.co_name, caller.f_lineno]
    try:
        return ORIGINAL_SLEEP(seconds)
    finally:
        event('sleep', requested=seconds, wall=time.monotonic() - before,
              tid=threading.get_native_id(), caller=where)




ORIGINAL_WAIT = subprocess.Popen.wait


def observed_wait(self, *args, **kwargs):
    before = time.monotonic()
    try:
        return ORIGINAL_WAIT(self, *args, **kwargs)
    finally:
        entry = CHILDREN.get(self.pid)
        if entry is not None and self.returncode is not None and not entry['ended']:
            entry['ended'] = True
            event('child_exit_observed', child=self.pid, code=self.returncode,
                  lifespan_upper_bound=time.monotonic() - entry['start'],
                  wait_wall=time.monotonic() - before, last_process_stat=entry['last'],
                  cpu_limit='last observed proc stat; final CPU UNKNOWN after reap')


def observed_poll(original):
    def poll(self, timeout=None):
        before = time.monotonic()
        caller = sys._getframe(1)
        try:
            return original(self, timeout)
        finally:
            event('poll', timeout=timeout, wall=time.monotonic() - before,
                  caller=[caller.f_code.co_filename, caller.f_code.co_name, caller.f_lineno],
                  tid=threading.get_native_id())
    return poll


def child_snapshot():
    live = []
    with LOCK:
        entries = list(CHILDREN.items())
    for pid, entry in entries:
        current = stat(pid)
        if current is not None:
            entry['last'] = current
        code = entry['process'].poll()
        if code is None:
            live.append(dict(pid=pid, executable=entry['executable'], process_stat=current, main_cpu=stat(pid, pid)))
        elif not entry['ended']:
            entry['ended'] = True
            event('child_exit_observed', child=pid, code=code,
                  wall_upper_bound=time.monotonic() - entry['start'],
                  last_process_stat=entry['last'])
    pending = [os.getpid()]
    seen = set(pending)
    while pending:
        parent = pending.pop()
        try:
            tasks = Path(f'/proc/{parent}/task').iterdir()
            descendants = {int(pid) for task in tasks
                           for pid in (task / 'children').read_text().split()}
        except OSError:
            descendants = set()
        for pid in descendants - seen:
            seen.add(pid)
            pending.append(pid)
            if pid not in CHILDREN:
                live.append(dict(pid=pid, process_stat=stat(pid), main_cpu=stat(pid, pid),
                                 origin='descendant_scan'))
    return live


def collect_samples():
    next_dump = 0
    previous_phase = None
    sampler_cpu = 0.0
    while not STOP.wait(0.1):
        cpu_before = time.thread_time()
        now = time.monotonic()
        frames = sys._current_frames()
        main = frames.get(MAIN)
        trace = stack(main)
        current_phase = phase(main)
        row = dict(elapsed=now - START, test_elapsed=None if TEST_START is None else now - TEST_START,
                   process=stat(os.getpid()), main_cpu=stat(os.getpid(), os.getpid()),
                   main_stack=trace, phase=current_phase, children=child_snapshot())
        SAMPLES.append(row)
        if trace:
            COUNTS[tuple(trace[0])] += 1
        if current_phase != previous_phase:
            event('phase', **current_phase)
            previous_phase = current_phase
        event('sample', **row)
        while TEST_START is not None and next_dump < 3 and now - TEST_START >= (10, 25, 40)[next_dump]:
            target = (10, 25, 40)[next_dump]
            DUMPS.write(f'\nTARGET {target} ACTUAL {now - TEST_START:.6f} PID {os.getpid()} MAIN_IDENT {MAIN}\n')
            DUMPS.flush()
            faulthandler.dump_traceback(file=DUMPS, all_threads=True)
            DUMPS.flush()
            os.fsync(DUMPS.fileno())
            event('checkpoint', target=target, test_elapsed=now - TEST_START,
                  process=stat(os.getpid()), main_cpu=stat(os.getpid(), os.getpid()),
                  threads=[dict(ident=ident, stack=stack(frame)) for ident, frame in frames.items()],
                  children=row['children'])
            os.fsync(EVENTS.fileno())
            next_dump += 1
        sampler_cpu += time.thread_time() - cpu_before
    event('sampler_end', cpu=sampler_cpu)


def sample_loop():
    try:
        collect_samples()
    except BaseException as error:
        ERRORS.append(type(error).__name__)
        event('sampler_error', error_type=type(error).__name__)
        os.fsync(EVENTS.fileno())


def origins():
    result = []
    for name, module in list(sys.modules.items()):
        if name.startswith(('astrid', 'runtime_protocol', 'tests.editing_conformance.test_p4')):
            filename = getattr(module, '__file__', None)
            if filename and Path(filename).is_file():
                result.append(dict(module=name, path=filename,
                                   sha256=hashlib.sha256(Path(filename).read_bytes()).hexdigest()))
    (OUT / 'loaded-origins.json').write_text(json.dumps(result, indent=2) + '\n')


class Diagnostic:
    def pytest_collection_finish(self, session):
        event('collection_finished', items=[item.nodeid for item in session.items],
              modules=len(sys.modules), process=stat(os.getpid()))
        module = sys.modules.get('tests.editing_conformance.test_p4_ten_note_v2_runtime')
        if module is not None:
            original = module._run_cli

            def inline_cli(*args, **kwargs):
                before = time.monotonic()
                event('inline_cli_start')
                try:
                    return original(*args, **kwargs)
                finally:
                    event('inline_cli_end', wall=time.monotonic() - before)

            module._run_cli = inline_cli
        sync = sys.modules.get('astrid.sdk.timeline.sync')
        if sync is not None:
            original_undo = sync.TimelineSession.undo

            def inverse(*args, **kwargs):
                before = time.monotonic()
                cpu = time.thread_time()
                position = phase(sys._getframe(1))
                event('inverse_start', **position)
                try:
                    return original_undo(*args, **kwargs)
                finally:
                    event('inverse_end', wall=time.monotonic() - before,
                          cpu=time.thread_time() - cpu, **position)

            sync.TimelineSession.undo = inverse

    def pytest_runtest_logstart(self, nodeid, location):
        global TEST_START
        TEST_START = time.monotonic()
        event('test_start', nodeid=nodeid, process=stat(os.getpid()),
              main_cpu=stat(os.getpid(), os.getpid()))

    def pytest_runtest_logreport(self, report):
        event('test_report', when=report.when, outcome=report.outcome, duration=report.duration,
              process=stat(os.getpid()), main_cpu=stat(os.getpid(), os.getpid()))


def main():
    global OUT, EVENTS, DUMPS, START
    os.umask(0o077)
    OUT = Path(os.environ['P4_SAMPLE_OUTPUT'])
    OUT.mkdir(parents=True, exist_ok=True)
    EVENTS = (OUT / 'events.jsonl').open('w', buffering=1)
    DUMPS = (OUT / 'faulthandler.txt').open('w', buffering=1)
    START = time.monotonic()
    subprocess.Popen.__init__ = observed_init
    subprocess.Popen.wait = observed_wait
    time.sleep = observed_sleep
    for cls in {selectors.SelectSelector, selectors.PollSelector, selectors.EpollSelector}:
        ORIGINAL_POLLS[cls] = cls.select
        cls.select = observed_poll(cls.select)
    event('bootstrap', executable=sys.executable, process=stat(os.getpid()),
          main_cpu=stat(os.getpid(), os.getpid()), modules=len(sys.modules))
    sampler = threading.Thread(target=sample_loop, name='p4-private-sampler', daemon=True)
    sampler.start()
    try:
        import pytest
        event('pytest_imported', modules=len(sys.modules), process=stat(os.getpid()))
        result = pytest.main(sys.argv[1:], plugins=[Diagnostic()])
    finally:
        STOP.set()
        sampler.join(timeout=2)
        if sampler.is_alive():
            ERRORS.append('sampler_join_timeout')
        child_snapshot()
        origins()
        event('diagnostic_end', process=stat(os.getpid()), main_cpu=stat(os.getpid(), os.getpid()),
              samples=len(SAMPLES), observed_children=len(CHILDREN), sampler_errors=ERRORS)
        os.fsync(EVENTS.fileno())
        subprocess.Popen.__init__ = ORIGINAL_INIT
        subprocess.Popen.wait = ORIGINAL_WAIT
        time.sleep = ORIGINAL_SLEEP
        for cls, original in ORIGINAL_POLLS.items():
            cls.select = original
        EVENTS.close()
        DUMPS.close()
    return 3 if ERRORS else result


if __name__ == '__main__':
    raise SystemExit(main())
