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
old_guard = (
    b'if test "$AGENT_HEAD" = 57779274a0e4a1ae7defef1a6f7239b79d411d55; '
    b'then test "$(git rev-list --parents -n 1 HEAD)" = '
    b'"57779274a0e4a1ae7defef1a6f7239b79d411d55 '
    b'3769a98d06ea20b6cbb604b496d2a0c21c989609 '
    b'5a612e37833ee43a3376d595ea11bcc3cf3318a9"; '
    b'else test "$(git rev-list --parents -n 1 HEAD)" = '
    b'"$AGENT_HEAD 57779274a0e4a1ae7defef1a6f7239b79d411d55"; fi'
)
new_guard = (
    b'if test "$AGENT_HEAD" = 9502c321b6884235bcd040364d2bc8431caf6a87; '
    b'then test "$(git rev-list --parents -n 1 HEAD)" = '
    b'"9502c321b6884235bcd040364d2bc8431caf6a87 '
    b'cc7c0f1d30ef9c90c35e52d807d17d7f27c0b7f7 '
    b'af1bf20a78c468b553a6673db0ca5ae653202470"; '
    b'else test "$(git rev-list --parents -n 1 HEAD)" = '
    b'"$AGENT_HEAD 9502c321b6884235bcd040364d2bc8431caf6a87"; fi'
)
old_tree = b"c209f6c887eff63174314d037e2fdb5472eea4dc"
new_tree = b"781241f7817337d0bb78f97443a8f63207eebd8f"
target_keys = {
    (b"agent", b"p4-current-becfe-http-3legs"),
    (b"agent", b"final-core"),
    (b"agent", b"p4-preflight-current-9502"),
}
rows = {
    tuple(line.split()[:2]): line
    for line in candidate.read_bytes().splitlines(keepends=True)
    if line.startswith(b"agent ")
}
assert set(rows) == target_keys
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
            assert key not in found
            if line != rows[key]:
                assert line.count(old_tree) == 1
                assert line.count(old_guard) == 1
                updated = line.replace(old_tree, new_tree).replace(old_guard, new_guard)
                assert updated == rows[key]
            else:
                assert key == (b"agent", b"p4-preflight-current-9502")
            found.add(key)
            line = rows[key]
        after_lines.append(line)
    missing = set(rows) - found
    assert missing <= {(b"agent", b"p4-preflight-current-9502")}
    if missing:
        insertion = next(
            index for index, line in enumerate(after_lines)
            if tuple(line.split()[:2]) == (b"agent", b"p4-current-becfe-http-3legs")
        )
        after_lines[insertion + 1:insertion + 1] = [
            rows[(b"agent", b"p4-preflight-current-9502")]
        ]
    assert found | missing == target_keys
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
        return b"".join(
            line for line in entries if tuple(line.split()[:2]) not in target_keys
        )

    assert outside(lines) == outside(after_lines)
    print("backup", backup)
    print("before", expected)
    print("after", hashlib.sha256(after).hexdigest())
    print("outside", hashlib.sha256(outside(lines)).hexdigest(), "byte-identical")
    print("mode 0600; two existing rows refreshed and one preflight row inserted")
