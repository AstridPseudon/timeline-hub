"""Replace only the two P4/core launchers using a guarded registry CAS."""

import datetime
import fcntl
import hashlib
import os
import stat
import sys
import tempfile
from pathlib import Path

candidate, registry, evidence = map(Path, sys.argv[1:4])
expected = sys.argv[4]
old_guard = b'test "$(git rev-parse HEAD^)" = 57779274a0e4a1ae7defef1a6f7239b79d411d55; test -z "$(git rev-parse HEAD^2 2>/dev/null || true)"'
new_guard = b'test "$(git rev-list --parents -n 1 HEAD)" = "$AGENT_HEAD 57779274a0e4a1ae7defef1a6f7239b79d411d55"'
rows = {
    tuple(line.split()[:2]): line
    for line in candidate.read_bytes().splitlines(keepends=True)
    if line.startswith(b"agent ")
}
assert set(rows) == {(b"agent", b"p4-current-becfe-http-3legs"), (b"agent", b"final-core")}
assert registry.is_file() and not registry.is_symlink()
assert stat.S_IMODE(registry.stat().st_mode) == 0o600
evidence.mkdir(parents=True, exist_ok=True)
with registry.open("rb") as locked:
    fcntl.flock(locked.fileno(), fcntl.LOCK_EX)
    before = locked.read()
    assert hashlib.sha256(before).hexdigest() == expected
    lines = before.splitlines(keepends=True)
    found = set()
    after_lines = []
    for line in lines:
        key = tuple(line.split()[:2])
        if key in rows:
            assert key not in found and line.count(old_guard) == 1
            assert line.replace(old_guard, new_guard) == rows[key]
            found.add(key)
            line = rows[key]
        after_lines.append(line)
    assert found == set(rows)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    backup = evidence / f"suites.conf.pre-{stamp}.bak"
    with backup.open("xb") as output:
        os.fchmod(output.fileno(), 0o600)
        output.write(before)
        output.flush()
        os.fsync(output.fileno())
    after = b"".join(after_lines)
    fd, temporary = tempfile.mkstemp(prefix=".suites.conf.p4-launch-", dir=registry.parent)
    with os.fdopen(fd, "wb") as output:
        os.fchmod(output.fileno(), 0o600)
        output.write(after)
        output.flush()
        os.fsync(output.fileno())
    assert registry.read_bytes() == before
    os.replace(temporary, registry)
    directory_fd = os.open(registry.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    assert registry.read_bytes() == after
    assert stat.S_IMODE(registry.stat().st_mode) == 0o600
    def outside(entries):
        return b"".join(line for line in entries if tuple(line.split()[:2]) not in rows)

    assert outside(lines) == outside(after_lines)
    print("backup", backup)
    print("before", expected)
    print("after", hashlib.sha256(after).hexdigest())
    print("outside", hashlib.sha256(outside(lines)).hexdigest(), "byte-identical")
    print("mode 0600; only the two snapshot-parent predicates changed")
