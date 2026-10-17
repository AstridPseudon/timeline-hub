"""The Host and Runtime must agree on native birth without relaxing equality."""
import os
import sys
import time
import pytest
from banodoco_local import custody_broker as custody


@pytest.mark.parametrize("zone", ["Europe/Berlin", "UTC", "Pacific/Honolulu"])
def test_darwin_birth_is_fixed_english_utc(tmp_path, monkeypatch, zone):
    row = dict(pid=123, uid=501, parent_pid=12, start_sec=1792202400)
    monkeypatch.setattr(custody, "_read_darwin_process_info", lambda pid: dict(row))
    monkeypatch.setattr(time, "localtime", lambda *a: pytest.fail("birth depended on local timezone"))
    monkeypatch.setattr(time, "strftime", lambda *a: pytest.fail("birth depended on locale"))
    monkeypatch.setenv("TZ", zone)
    observed = custody._darwin_process_identity(123, timeout=1)
    assert observed["birth_id"] == "ps-lstart:Sat Oct 17 02:00:00 2026"
    assert observed == dict(pid=123, uid=501, parent_pid=12, birth_id=observed["birth_id"])


@pytest.mark.skipif(sys.platform != "darwin", reason="native Darwin identity")
def test_native_custody_and_authenticated_private_peer_agree():
    import socket
    left, right = socket.socketpair()
    try:
        own = custody.AuthenticatedCleanupActor.current().verify()
        peer = custody.AuthenticatedCleanupActor.private_peer(right).verify()
        assert own == peer
        assert own["birth_id"] == custody.default_process_identity(os.getpid())["birth_id"]
    finally:
        left.close(); right.close()
