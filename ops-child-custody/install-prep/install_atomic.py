"""Descriptor-bound file operations for the private inventory installer."""

from __future__ import annotations

import os
from pathlib import Path
import stat
import sys


CHUNK = 1024 * 1024


def _regular(info: os.stat_result, uid: int, mode: int) -> None:
    if not stat.S_ISREG(info.st_mode):
        raise RuntimeError("file is not regular")
    if info.st_nlink != 1:
        raise RuntimeError("file is hardlinked")
    if info.st_uid != uid:
        raise RuntimeError("file owner mismatch")
    if stat.S_IMODE(info.st_mode) != mode:
        raise RuntimeError("file mode mismatch")


def copy_reserved(source: Path, destination: Path, uid: int, mode: int) -> None:
    """Copy through an O_EXCL/O_NOFOLLOW descriptor in the receiving parent."""

    parent_fd = os.open(
        destination.parent,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
    )
    source_fd = -1
    destination_fd = -1
    try:
        source_fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW)
        _regular(os.fstat(source_fd), uid, mode)
        destination_fd = os.open(
            destination.name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            mode,
            dir_fd=parent_fd,
        )
        while True:
            data = os.read(source_fd, CHUNK)
            if not data:
                break
            offset = 0
            while offset < len(data):
                offset += os.write(destination_fd, data[offset:])
        os.fchmod(destination_fd, mode)
        os.fsync(destination_fd)
        _regular(os.fstat(destination_fd), uid, mode)
    except BaseException:
        if destination_fd != -1:
            try:
                os.unlink(destination.name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass
        raise
    finally:
        if source_fd != -1:
            os.close(source_fd)
        if destination_fd != -1:
            os.close(destination_fd)
        os.close(parent_fd)


def rename_if_same(
    parent: Path,
    target: str,
    replacement: str,
    expected_device: int,
    expected_inode: int,
    uid: int,
    mode: int,
) -> None:
    """Rename a reserved replacement only if the checked target is unchanged."""

    parent_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        target_info = os.stat(target, dir_fd=parent_fd, follow_symlinks=False)
        if (target_info.st_dev, target_info.st_ino) != (
            expected_device,
            expected_inode,
        ):
            raise RuntimeError("receiving target identity changed")
        _regular(target_info, uid, mode)
        replacement_info = os.stat(
            replacement,
            dir_fd=parent_fd,
            follow_symlinks=False,
        )
        _regular(replacement_info, uid, mode)
        os.replace(
            replacement,
            target,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def main() -> int:
    operation = sys.argv[1]
    if operation == "copy":
        copy_reserved(
            Path(sys.argv[2]),
            Path(sys.argv[3]),
            int(sys.argv[4]),
            int(sys.argv[5], 8),
        )
        return 0
    if operation == "rename":
        rename_if_same(
            Path(sys.argv[2]),
            sys.argv[3],
            sys.argv[4],
            int(sys.argv[5]),
            int(sys.argv[6]),
            int(sys.argv[7]),
            int(sys.argv[8], 8),
        )
        return 0
    raise RuntimeError(f"unknown operation: {operation}")


if __name__ == "__main__":
    raise SystemExit(main())
