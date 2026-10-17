"""Host-owned pins for declared helpers; never constructed from task inputs.

Discovery reads Mach-O load commands, without executing the selected helper.
Only exact installed files and OS shared-cache install names enter the policy.
"""
from __future__ import annotations

from contextvars import ContextVar
from dataclasses import asdict, dataclass
import hashlib
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import threading


class ExecutableAdmissionError(RuntimeError):
    pass


@dataclass(frozen=True)
class FilePin:
    path: Path
    resolved: Path
    aliases: tuple[Path, ...]
    identity: tuple[int, ...]
    sha256: str

    @classmethod
    def measure(cls, path: Path) -> FilePin:
        try:
            if not path.is_absolute() or any(ord(c) < 32 or ord(c) == 127 for c in str(path)):
                raise ValueError("invalid absolute artifact path")
            resolved = path.resolve(strict=True)
            # Seatbelt also sees the physical-parent spelling before following
            # a library's final symlink (Homebrew opt -> Cellar -> versioned lib).
            aliases = [path]
            current = path.parent.resolve(strict=True) / path.name
            visited = set()
            while current not in visited:
                visited.add(current)
                if current not in aliases:
                    aliases.append(current)
                if not current.is_symlink():
                    break
                target = current.readlink()
                target = target if target.is_absolute() else current.parent / target
                current = target.parent.resolve(strict=True) / target.name
            with resolved.open("rb") as stream:
                before = os.fstat(stream.fileno())
                if not stat.S_ISREG(before.st_mode):
                    raise ValueError("artifact is not a regular file")
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
                after = os.fstat(stream.fileno())
            identity = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
            if (identity(before) != identity(after) or identity(resolved.stat()) != identity(after)
                    or path.resolve(strict=True) != resolved):
                raise ValueError("artifact changed during measurement")
            return cls(path, resolved, tuple(aliases), identity(after), "sha256:" + digest)
        except (OSError, ValueError, RuntimeError) as exc:
            raise ExecutableAdmissionError(f"declared executable artifact unavailable: {path}: {exc}") from exc

    def verify(self) -> None:
        if self.measure(self.path) != self:
            raise ExecutableAdmissionError(f"declared executable artifact replaced: {self.path}")


def _system_library(path: Path) -> bool:
    return path.is_absolute() and any(path.is_relative_to(root) for root in (
        Path("/usr/lib"), Path("/System/Library"))) and ".." not in path.parts


# The private caller carries selection provenance, never caller-supplied pins.
_INSPECTION_SELECTION = ContextVar("declared_executable_selection", default=None)


def _load_commands(path: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
    from .custody_broker import _inventory_load_commands
    selection = _INSPECTION_SELECTION.get()
    result = _inventory_load_commands(selection, path)
    if result.returncode:
        raise ExecutableAdmissionError(f"cannot inspect declared executable library closure: {path}")
    return _parse_load_commands(result.stdout)


def _parse_load_commands(output: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    libraries, rpaths = [], []
    command = ""
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("cmd "):
            command = line[4:]
        elif command in {"LC_LOAD_DYLIB", "LC_LOAD_WEAK_DYLIB", "LC_REEXPORT_DYLIB", "LC_LOAD_UPWARD_DYLIB"} and line.startswith("name "):
            libraries.append(line[5:].rsplit(" (offset ", 1)[0])
        elif command == "LC_RPATH" and line.startswith("path "):
            rpaths.append(line[5:].rsplit(" (offset ", 1)[0])
    return tuple(dict.fromkeys(libraries)), tuple(dict.fromkeys(rpaths))


@dataclass(frozen=True)
class ExecutableBinding:
    name: str
    executable: FilePin
    libraries: tuple[FilePin, ...]
    system_libraries: tuple[Path, ...]
    platform_identity: tuple[str, ...]

    def verify(self) -> None:
        if tuple(os.uname()) != self.platform_identity:
            raise ExecutableAdmissionError("declared executable platform identity changed")
        for pin in (self.executable, *self.libraries):
            pin.verify()
        if not os.access(self.executable.path, os.X_OK):
            raise ExecutableAdmissionError(f"declared executable is not executable: {self.name}")

    def evidence(self) -> dict:
        def pin(value):
            return {**asdict(value), "path": str(value.path), "resolved": str(value.resolved),
                    "aliases": [str(p) for p in value.aliases]}
        return {"name": self.name, "executable": pin(self.executable),
                "libraries": [pin(p) for p in self.libraries],
                "system_libraries": [str(p) for p in self.system_libraries],
                "platform_identity": self.platform_identity}


def _expand_load_path(value: str, loader: Path, executable: FilePin) -> Path:
    for token, base in (("@loader_path", loader.parent), ("@executable_path", executable.resolved.parent)):
        if value == token or value.startswith(token + "/"):
            return Path(os.path.normpath(str(base) + value[len(token):]))
    if not value.startswith("/"):
        raise ExecutableAdmissionError(f"unsupported declared executable load path: {value}")
    return Path(value)


def _dependency_paths(executable: FilePin, loader: Path, inherited: tuple[Path, ...],
                      names: tuple[str, ...], raw_rpaths: tuple[str, ...], approved_roots=None):
    def admit(path):
        if approved_roots is not None:
            normalized = Path(os.path.normpath(path))
            if not _system_library(normalized) and (not any(normalized.is_relative_to(root) for root in approved_roots)
                    or not any(normalized.resolve().is_relative_to(root) for root in approved_roots)):
                raise ExecutableAdmissionError("inspection dependency is outside approved roots")
        return path

    rpaths = tuple(dict.fromkeys((*[_expand_load_path(p, loader, executable) for p in raw_rpaths], *inherited)))
    paths = []
    for value in names:
        if value.startswith("@rpath/"):
            candidates = [admit(p / value[7:]) for p in rpaths]
            path = next((p for p in candidates if p.is_file() or _system_library(p)), None)
            if path is None:
                raise ExecutableAdmissionError(f"unavailable declared executable library: {value}")
        else:
            path = _expand_load_path(value, loader, executable)
        paths.append(admit(path))
    return tuple(paths), rpaths


def _bind(name: str, selected: Path) -> ExecutableBinding:
    executable = FilePin.measure(selected)
    if not os.access(selected, os.X_OK):
        raise ExecutableAdmissionError(f"declared executable is not executable: {name}")
    libraries: dict[Path, FilePin] = {}
    system: set[Path] = set()
    visited: set[tuple[Path, tuple[Path, ...]]] = set()

    def walk(loader: Path, inherited: tuple[Path, ...]) -> None:
        # Non-Darwin readiness still pins files; the required launch backend
        # independently refuses unsupported platforms before workload effects.
        if sys.platform != "darwin":
            return
        key = (loader, inherited)
        if key in visited:
            return
        visited.add(key)
        names, raw_rpaths = _load_commands(loader)
        paths, rpaths = _dependency_paths(executable, loader, inherited, names, raw_rpaths)
        for path in paths:
            if _system_library(path):
                system.add(path)
                continue  # OS shared-cache entries need not exist as files.
            pin = FilePin.measure(path)
            if path in libraries and libraries[path] != pin:
                raise ExecutableAdmissionError(f"declared executable library changed: {path}")
            # Revisit only distinct resolved images, keeping aliases in evidence.
            seen = any(p.resolved == pin.resolved for p in libraries.values())
            libraries[path] = pin
            if not seen:
                walk(pin.resolved, rpaths)

    selection = _INSPECTION_SELECTION.set(name)
    try:
        walk(executable.resolved, ())
    finally:
        _INSPECTION_SELECTION.reset(selection)
    binding = ExecutableBinding(name, executable, tuple(libraries[p] for p in sorted(libraries)),
                                tuple(sorted(system)), tuple(os.uname()))
    binding.verify()
    return binding


class _InspectionAdmission:
    """Launch-owned incremental closure, never populated by request digests."""

    def __init__(self, selections: dict[str, FilePin], roots: tuple[Path, ...]):
        self.platform = tuple(os.uname())
        self.selections = dict(selections)
        self.roots = tuple(p.resolve(strict=True) for p in roots)
        if any(p == Path("/") for p in self.roots):
            raise ExecutableAdmissionError("inspection dependency root is unscoped")
        self.images = {name: {pin.resolved: (pin, {()})} for name, pin in selections.items()}
        self.parents = {name: {pin.resolved: set()} for name, pin in selections.items()}

    def verify(self, name: str, path: str):
        if sys.platform != "darwin" or tuple(os.uname()) != self.platform:
            raise ExecutableAdmissionError("inspection platform changed")
        if not isinstance(name, str) or name not in self.selections or not isinstance(path, str):
            raise ExecutableAdmissionError("inspection selection is unavailable")
        self.selections[name].verify()
        for pin, inherited in self.images[name].values():
            if Path(path) in (pin.path, pin.resolved, *pin.aliases):
                seen = set()
                def verify_ancestry(image):
                    if image in seen:
                        return
                    seen.add(image)
                    self.images[name][image][0].verify()
                    for parent in self.parents[name][image]:
                        verify_ancestry(parent)
                verify_ancestry(pin.resolved)
                return pin, inherited
        raise ExecutableAdmissionError("inspection file has no admitted selection or dependency edge")

    def complete(self, name: str, path: str, output: str) -> None:
        pin, contexts = self.verify(name, path)
        names, rpaths = _parse_load_commands(output)
        additions = []
        for inherited in tuple(contexts):
            paths, resolved_rpaths = _dependency_paths(self.selections[name], pin.resolved, inherited,
                                                     names, rpaths, self.roots)
            for candidate in paths:
                if _system_library(candidate):
                    continue
                # Both the lexical alias and its target must stay within the
                # launch's dependency scopes. Output is an edge, not a root grant.
                if not any(candidate.is_relative_to(root) for root in self.roots):
                    raise ExecutableAdmissionError("inspection dependency is outside approved roots")
                dependency = FilePin.measure(candidate)
                if any(not any(alias.is_relative_to(root) for root in self.roots)
                       for alias in (*dependency.aliases, dependency.resolved)):
                    raise ExecutableAdmissionError("inspection dependency alias escapes approved roots")
                additions.append((dependency, resolved_rpaths))
        pin.verify()
        for dependency, inherited in additions:
            previous = self.images[name].get(dependency.resolved)
            if previous is not None:
                if previous[0].resolved != dependency.resolved or previous[0].identity != dependency.identity:
                    raise ExecutableAdmissionError("inspection dependency changed")
                previous[0].verify()
                previous[1].add(inherited)
            else:
                self.images[name][dependency.resolved] = (dependency, {inherited})
            self.parents[name].setdefault(dependency.resolved, set()).add(pin.resolved)


class _InspectionTool:
    """Non-spawning system developer selection; no PATH/DEVELOPER_DIR override."""

    def __init__(self):
        if sys.platform != "darwin":
            raise ExecutableAdmissionError("inspection requires Darwin")
        self.platform = tuple(os.uname())
        self.alias = FilePin.measure(Path("/usr/bin/otool"))
        self.developer = Path("/var/db/xcode_select_link")
        base, self.selection_identity = self._developer_selection()
        self.base = base
        self.executable = FilePin.measure(base / "usr/bin/otool")
        if not os.access(self.executable.path, os.X_OK):
            raise ExecutableAdmissionError("selected platform otool is not executable")

    def _developer_selection(self):
        if self.developer.exists() or self.developer.is_symlink():
            value = self.developer.lstat()
            identity = (value.st_dev, value.st_ino, value.st_mode, value.st_mtime_ns, value.st_ctime_ns,
                        str(self.developer.readlink()) if self.developer.is_symlink() else None)
            return self.developer.resolve(strict=True), identity
        return Path("/Library/Developer/CommandLineTools"), None

    def verify(self):
        base, identity = self._developer_selection()
        if (sys.platform != "darwin" or tuple(os.uname()) != self.platform
                or base != self.base or identity != self.selection_identity):
            raise ExecutableAdmissionError("inspection platform tool selection changed")
        self.alias.verify()
        self.executable.verify()


class ExecutableAdmission:
    """One host launch's search configuration and immutable first selections."""

    def __init__(self, search_path: str):
        self.search_path = search_path
        self._bindings: dict[str, ExecutableBinding] = {}
        self._lock = threading.RLock()

    def require(self, names: tuple[str, ...]) -> tuple[ExecutableBinding, ...]:
        with self._lock:
            result = []
            for name in names:
                if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.+-]*", name):
                    raise ExecutableAdmissionError("declared executable requires a simple binary name")
                if name not in self._bindings:
                    selected = shutil.which(name, path=self.search_path)
                    if selected is None or not Path(selected).is_absolute():
                        raise ExecutableAdmissionError(f"declared executable unavailable: {name}")
                    self._bindings[name] = _bind(name, Path(selected))
                binding = self._bindings[name]
                binding.verify()
                result.append(binding)
            return tuple(result)
