"""Opt-in pytest setup for the elevated Windows hosted runner.

The per-user runtime requires TokenUser-owned files. Hosted Windows runners
can instead default newly created files to the Administrators group, unlike
an ordinary unelevated installation. Set only this test process's TokenOwner
to TokenUser; keep its default DACL and all production security checks intact.

TokenOwner is the documented default owner of newly created objects:
https://learn.microsoft.com/en-us/windows/win32/secauthz/owner-of-a-new-object
Load explicitly with ``python -m pytest -p tests.windows_ci_owner ...``.
"""
from contextlib import contextmanager
import ctypes
from ctypes import wintypes
import sys
import tempfile

from runtime_protocol import windows_security as security


class _TokenOwner(ctypes.Structure):
    _fields_ = [("owner", ctypes.c_void_p)]


@contextmanager
def current_user_creation_owner():
    if sys.platform != "win32":
        raise RuntimeError("the Windows CI owner plugin must only run on Windows")
    adv, kernel = security._api()
    adv.SetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    adv.SetTokenInformation.restype = wintypes.BOOL
    token = wintypes.HANDLE()
    # TOKEN_QUERY | TOKEN_ADJUST_DEFAULT; no privilege enabling or file-owner
    # takeover. TokenUser is always a legal TokenOwner for this same token.
    security._check(adv.OpenProcessToken(kernel.GetCurrentProcess(), 0x0088, ctypes.byref(token)))
    previous = None
    changed = False
    try:
        size = wintypes.DWORD()
        adv.GetTokenInformation(token, 4, None, 0, ctypes.byref(size))
        previous = ctypes.create_string_buffer(size.value)
        security._check(adv.GetTokenInformation(token, 4, previous, size, ctypes.byref(size)))
        old_owner = ctypes.cast(previous, ctypes.POINTER(_TokenOwner)).contents.owner
        user_sid = security._user_sid()
        desired = _TokenOwner(ctypes.cast(user_sid, ctypes.c_void_p))
        print(f"Windows CI creation owner: {security._sid_text(old_owner)} -> {security._sid_text(user_sid)}")
        security._check(adv.SetTokenInformation(token, 4, ctypes.byref(desired), ctypes.sizeof(desired)))
        changed = True
        # Prove ordinary native creation now has the intended owner before any
        # runtime tests run. Do not repair the probe or bypass its validation.
        with tempfile.TemporaryDirectory(prefix="astrid-ci-owner-") as probe:
            with security._handle(probe) as (handle, _info):
                security._validate_handle(handle, owner_only=True)
        yield
    finally:
        try:
            if changed:
                security._check(adv.SetTokenInformation(token, 4, previous, ctypes.sizeof(_TokenOwner)))
        finally:
            kernel.CloseHandle(token)


def pytest_configure(config):
    owner = current_user_creation_owner()
    owner.__enter__()
    config.add_cleanup(lambda: owner.__exit__(None, None, None))
