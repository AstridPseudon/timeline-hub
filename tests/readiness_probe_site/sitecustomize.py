"""Private subprocess observation; no arguments, headers, bodies or locals recorded."""
import functools
import hashlib
import itertools
import json
import os
from pathlib import Path
import sys
import threading
import time
import traceback

root = Path(os.environ["READINESS_CAPTURE"])
events = (root / f"events-{os.getpid()}.jsonl").open("w", buffering=1)
stacks = (root / f"stacks-{os.getpid()}.txt").open("w", buffering=1)
counter = itertools.count()
active = {}
started = time.monotonic()


def emit(value):
    if events.tell() < 8_000_000:
        events.write(json.dumps({"time": time.monotonic(), **value}) + "\n")


def observe(cls, name):
    original = getattr(cls, name)

    @functools.wraps(original)
    def observed(self, *args, **kwargs):
        number = next(counter)
        thread = threading.get_ident()
        detail = {"call": number, "thread": thread, "method": name}
        if name in ("_dispatch", "_route", "_preflight"):
            detail.update(path=self.path.split("?")[0], http_method=self.command,
                          door=type(self).__name__ == "DoorHandler")
        if name == "commit_timeline":
            detail["commands"] = len(args[2].get("commands", []))
        if name in ("history", "list_timeline_commits"):
            detail.update(limit=kwargs.get("limit"), cursor=kwargs.get("cursor") is not None)
        store = getattr(self, "store", None)
        if store is None and name in ("_dispatch", "_route"):
            store = self.runtime.store
        active[number] = (detail, store)
        begin = time.monotonic()
        emit({"event": "enter", **detail})
        try:
            return original(self, *args, **kwargs)
        finally:
            emit({"event": "exit", "seconds": time.monotonic() - begin, **detail})
            active.pop(number, None)

    setattr(cls, name, observed)


from runtime_protocol.server import RuntimeHandler
from runtime_protocol.door import DoorHandler
from runtime_protocol.timeline_commit_store import TimelineCommitStore
from runtime_protocol.service import RuntimeService
import astrid
import runtime_protocol.server
import astrid.sdk.timeline.commands

for method in ("_dispatch", "_route"):
    observe(RuntimeHandler, method)
observe(DoorHandler, "_preflight")
for method in ("head", "history", "history_entry", "_verify_accepted", "_historical_sequential"):
    observe(TimelineCommitStore, method)
for method in ("commit_timeline", "list_timeline_commits"):
    observe(RuntimeService, method)

origins = {}
for module in (astrid, runtime_protocol.server, astrid.sdk.timeline.commands):
    file = Path(module.__file__).resolve()
    origins[module.__name__] = {"file": str(file), "sha256": hashlib.sha256(file.read_bytes()).hexdigest()}
emit({"event": "origins", "modules": origins, "interpreter": sys.executable})


def sample():
    # Bounded, read-only stack/lock sampling. RLock ownership is observed, never replaced.
    for _ in range(480):
        time.sleep(.25)
        calls = list(active.values())
        if not calls:
            continue
        stacks.write(f"\ntime={time.monotonic()} elapsed={time.monotonic() - started}\n")
        for detail, store in calls:
            lock = repr(store._mutex) if store is not None else "unobserved"
            stacks.write(json.dumps({**detail, "mutex": lock}) + "\n")
        for thread, frame in sys._current_frames().items():
            stacks.write(f"thread={thread}\n")
            stacks.writelines(traceback.format_stack(frame, limit=36))
        if stacks.tell() > 8_000_000:
            break


threading.Thread(target=sample, name="readiness-stack-observer", daemon=True).start()
