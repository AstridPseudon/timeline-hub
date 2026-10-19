"""Install transactions. Runtime owns workspace identity, migration and backups."""

from __future__ import annotations

import json
import os
import re
import stat
import uuid
from dataclasses import dataclass
from pathlib import Path


def linked(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        # Path.is_junction is unavailable on the pinned Python 3.11. This
        # also rejects other Windows reparse points before recursive copies.
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT"))
    except FileNotFoundError:
        return False


def absolute(value: str | Path) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ValueError(f"An absolute path is required: {path}")
    path = Path(os.path.abspath(path))
    for entry in (path, *path.parents):
        if linked(entry):
            raise ValueError(f"Managed paths cannot contain links: {entry}")
    return path


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path}")
    return value


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def find_data_root(recorded: Path | None, requested: Path | None,
                   default: Path, legacy: list[Path]) -> tuple[Path, bool]:
    """A recorded selection is authoritative, even if its disk is unavailable."""
    if recorded is not None:
        return absolute(recorded), False
    if requested is not None:
        return absolute(requested), False
    if (default / "runtime" / "catalog.json").exists():
        return absolute(default), False
    candidates = [p for p in legacy if (p / "runtime" / "catalog.json").exists()]
    if len(candidates) > 1:
        raise ValueError("Several old workspaces were found; select one with --data-root.")
    return (absolute(candidates[0]), True) if candidates else (absolute(default), False)


def version_id(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", value):
        raise ValueError("Invalid installation version identifier.")
    return value


@dataclass(frozen=True)
class Version:
    root: Path
    python: Path
    profile: Path
    env: dict[str, str]

    def document(self) -> dict:
        return {"root": str(self.root), "python": str(self.python),
                "profile": str(self.profile), "env": self.env}

    @classmethod
    def load(cls, value: dict) -> "Version":
        python = Path(value["python"])
        absolute(python.parent)  # POSIX venv interpreters themselves are links.
        return cls(absolute(value["root"]), python,
                   absolute(value["profile"]), dict(value["env"]))


def current(root: Path) -> Version | None:
    pointer = root / "current"
    if not pointer.exists():
        return None
    name = version_id(pointer.read_text(encoding="utf-8").strip())
    record = absolute(root / "versions" / name / "version.json")
    # Removal can delete version metadata before a locked pointer is released.
    # The service's retained selection can still finish uninstalling this root.
    if not record.exists() and not linked(record):
        return None
    version = Version.load(read_json(record))
    if version.root != root / "versions" / name:
        raise ValueError("The current version points outside the managed directory.")
    return version


def switch(root: Path, version: Version) -> None:
    name = version_id(version.root.name)
    if version.root != root / "versions" / name:
        raise ValueError("The current pointer must name a managed version.")
    pointer = root / "current.tmp"
    with pointer.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(name + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(pointer, root / "current")


class Installer:
    def __init__(self, root: Path, data: Path, backend, *, say=print):
        self.root, self.data, self.backend, self.say = root, data, backend, say

    def run(self, mode: str, manifest: dict, *, delete_data: bool = False) -> None:
        old = current(self.root) or self.backend.existing(self.data)
        if mode == "uninstall":
            if hasattr(self.backend, "preflight_remove"):
                self.backend.preflight_remove(self.root, self.data, delete_data=delete_data)
            self.backend.stop(old, self.data)
            self.backend.unregister()
            residue = self.backend.remove(self.root, self.data, delete_data=delete_data)
            self.say("Astrid was uninstalled." if not residue else "Astrid was unregistered; some files remain.")
            for path in residue:
                self.say(f"Remaining: {path}")
            if not delete_data:
                self.say(f"Workspace kept at {self.data}.")
            return

        # Repair never provisions tools, installs code, migrates or rewrites data.
        if old and mode != "update":
            realm = self.backend.workspace(old, self.data)
            self.say("Restarting Astrid with the installed version.")
            self.backend.stop(old, self.data)
            self.backend.register(old, self.data)
            self.backend.start(old, self.data)
            self.backend.verify(old, self.data, realm["realm_id"])
            self.backend.open()
            self.say("Open https://astrid.haus")
            return

        realm = self.backend.workspace(old, self.data) if old else None
        if not old and self.backend.has_workspace(self.data):
            raise ValueError("An existing workspace has no usable source profile; repair its profile before installing.")
        backup = None
        candidate = None
        stopped = False
        switched = False
        try:
            if old:
                self.say("Stopping Astrid before the update.")
                # A stop can fail after stopping the manager: recovery must run.
                stopped = True
                self.backend.stop(old, self.data)
                self.say("Backing up your workspace.")
                backup = self.backend.backup(old, self.data, realm)
            self.say("Installing the pinned Astrid version.")
            candidate = self.backend.stage(manifest, self.root, self.data)
            if old:
                self.say("Updating the workspace with Astrid Runtime.")
                self.backend.upgrade(candidate, self.data)
                # upgrade owns its temporary daemon; hand back to the login service.
                self.backend.stop(candidate, self.data)
            else:
                realm = self.backend.create(candidate, self.data)
            switch(self.root, candidate)
            switched = True
            self.say("Starting Astrid at sign-in.")
            self.backend.register(candidate, self.data)
            self.backend.start(candidate, self.data)
            self.backend.verify(candidate, self.data, realm["realm_id"])
            self.backend.finish(old, candidate, backup)
        except (Exception, KeyboardInterrupt) as failure:
            if old and stopped:
                try:
                    self.backend.stop(candidate or old, self.data)
                    if backup is not None:
                        self.backend.restore(old, self.data, realm, backup)
                    if switched and old.root.parent == self.root / "versions":
                        switch(self.root, old)
                    elif switched:
                        (self.root / "current").unlink(missing_ok=True)
                    self.backend.register(old, self.data)
                    self.backend.start(old, self.data)
                    self.backend.verify(old, self.data, realm["realm_id"])
                except (Exception, KeyboardInterrupt) as recovery:
                    raise RuntimeError(f"Update failed ({failure}); recovery also failed ({recovery}).") from failure
            elif candidate is not None:
                self.backend.stop(candidate, self.data)
            raise
        self.backend.open()
        self.say("Open https://astrid.haus")


def new_version_id(manifest: dict) -> str:
    # A retry gets a fresh directory; incomplete/locked versions are never reused.
    return version_id(f"{manifest['agent']['sha'][:8]}-{manifest['runtime']['sha'][:8]}-{uuid.uuid4().hex[:8]}")
