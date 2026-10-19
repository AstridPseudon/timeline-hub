"""Cooperative cancellation scoped to the foreground startup thread.

Normal daemon operation and background launches have no cancellation scope.
Cleanup runs after leaving the scope so a stop request cannot cancel cleanup.
"""
from contextlib import contextmanager
from contextvars import ContextVar
import time
import urllib.error

_event = ContextVar("runtime_startup_stop", default=None)


class StartupCancelled(RuntimeError):
    pass


def active():
    return _event.get() is not None


def requested():
    event = _event.get()
    return event is not None and event.is_set()


def check():
    if requested():
        raise StartupCancelled("Runtime startup cancelled by a stop request")


def pause(seconds):
    event = _event.get()
    if event is None:
        time.sleep(seconds)
    else:
        event.wait(seconds)
        check()


def retry_timeouts(read, timeout):
    """Poll an idempotent readiness read without shrinking its total budget."""
    if not active():
        return read(timeout)
    deadline = time.monotonic() + timeout
    while True:
        check()
        try:
            result = read(min(0.2, max(0.001, deadline - time.monotonic())))
        except (TimeoutError, urllib.error.URLError) as exc:
            check()
            if isinstance(exc, urllib.error.URLError) and not isinstance(exc.reason, TimeoutError):
                raise
            if time.monotonic() >= deadline:
                raise
        else:
            check()
            return result


@contextmanager
def startup_scope(event):
    token = _event.set(event)
    try:
        check()
        yield
    finally:
        _event.reset(token)


@contextmanager
def cleanup_scope():
    token = _event.set(None)
    try:
        yield
    finally:
        _event.reset(token)
