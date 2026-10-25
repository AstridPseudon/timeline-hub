#!/usr/bin/env python3
"""Bounded, read-only ownership census for the installed Farm child path.

This diagnostic is deliberately independent of the installed verifier code.  It
reads the installed maker, Store helper, and dependency verifier as source and
uses only bounded stdlib filesystem/archive checks against the supplied inputs.
It never imports or executes an installed file, creates a child, changes Store
state, or treats a failed prerequisite as proof that a later guard ran.
"""

from __future__ import annotations

import argparse
import ast
import base64
import csv
import hashlib
import io
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.parse import unquote, urlparse


DEFAULT_DEADLINE = 20 * 60
MAX_ENTRIES = 100_000
MAX_BYTES = 512 * 1024 * 1024
MAX_OUTPUT = 8 * 1024 * 1024
MAX_FILE = 16 * 1024 * 1024
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA64 = re.compile(r"[0-9a-f]{64}\Z")


class LimitReached(RuntimeError):
    pass


class ExactMissing(RuntimeError):
    pass


class Refusal(RuntimeError):
    pass


@dataclass
class Budget:
    deadline_seconds: int
    max_entries: int = MAX_ENTRIES
    max_bytes: int = MAX_BYTES
    max_output: int = MAX_OUTPUT
    started: float = field(default_factory=time.monotonic)
    entries: int = 0
    bytes: int = 0

    def tick(self) -> None:
        if time.monotonic() - self.started > self.deadline_seconds:
            raise LimitReached("monotonic deadline exceeded")

    def entry(self) -> None:
        self.tick()
        self.entries += 1
        if self.entries > self.max_entries:
            raise LimitReached("entry budget exceeded")

    def charge(self, size: int) -> None:
        self.tick()
        if size < 0 or self.bytes + size > self.max_bytes:
            raise LimitReached("byte budget exceeded")
        self.bytes += size


@dataclass
class Boundary:
    layer: str
    name: str
    status: str
    reason: str | None = None
    detail: Any = None


class Census:
    def __init__(self, budget: Budget) -> None:
        self.budget = budget
        self.boundaries: list[Boundary] = []
        self.missing: list[str] = []
        self.refusals: list[dict[str, Any]] = []
        self.errors: list[dict[str, Any]] = []
        self.skips: list[dict[str, Any]] = []
        self._facts: dict[str, Any] = {}

    def record(self, layer: str, name: str, status: str, reason: str | None = None,
               detail: Any = None) -> None:
        if isinstance(detail, pathlib.Path):
            detail = str(detail)
        boundary = Boundary(layer, name, status, reason, detail)
        self.boundaries.append(boundary)
        row = {"layer": layer, "check": name, "reason": reason}
        if detail is not None:
            row["detail"] = detail
        if status == "refused":
            self.refusals.append(row)
        elif status == "error":
            self.errors.append(row)
        elif status == "skipped":
            self.skips.append(row)

    def missing_input(self, item: str, layer: str | None = None) -> None:
        if item not in self.missing:
            self.missing.append(item)
        if layer:
            self.record(layer, "prerequisite:" + item, "skipped", "EXACTMISSING")

    def check(self, layer: str, name: str, fn: Callable[[], Any],
              *, prerequisites: tuple[str, ...] = ()) -> Any:
        missing = [item for item in prerequisites if item in self.missing]
        if missing:
            self.record(layer, name, "skipped", "prerequisite unavailable", missing)
            return None
        try:
            value = fn()
        except ExactMissing as exc:
            self.missing_input(str(exc), layer)
            self.record(layer, name, "skipped", "EXACTMISSING")
            return None
        except LimitReached as exc:
            self.record(layer, name, "skipped", "INCOMPLETE:" + str(exc))
            return None
        except Refusal as exc:
            self.record(layer, name, "refused", str(exc))
            return None
        except (OSError, ValueError, KeyError, IndexError, TypeError, UnicodeError) as exc:
            self.record(layer, name, "error", type(exc).__name__ + ": " + str(exc))
            return None
        else:
            self.record(layer, name, "visited", detail=value)
            return value

    def skip(self, layer: str, name: str, reason: str, detail: Any = None) -> None:
        self.record(layer, name, "skipped", reason, detail)


def safe_text(value: object, limit: int = 300) -> str:
    text = str(value).replace("\x00", "\\0")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def physical_path(path: pathlib.Path, *, directory: bool = False) -> pathlib.Path:
    if not path.is_absolute() or ".." in path.parts or path != path.resolve():
        raise Refusal("path is not absolute and physical")
    if path.is_symlink():
        raise Refusal("path is symlinked")
    if directory and not path.is_dir():
        raise Refusal("directory is missing")
    return path


def bounded_read(path: pathlib.Path, budget: Budget, *, text: bool = False) -> bytes | str:
    info = path.lstat()
    budget.entry()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise Refusal("not a regular physical file")
    if info.st_size > MAX_FILE:
        raise LimitReached("file budget exceeded")
    budget.charge(info.st_size)
    data = path.read_bytes()
    return data.decode("utf-8") if text else data


def bounded_walk(root: pathlib.Path, budget: Budget) -> list[pathlib.Path]:
    """Walk without following links; every encountered node consumes budget."""
    result: list[pathlib.Path] = []
    pending = [root]
    while pending:
        current = pending.pop()
        budget.entry()
        info = current.lstat()
        result.append(current)
        if stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode):
            children = sorted(current.iterdir(), key=lambda item: item.name, reverse=True)
            pending.extend(children)
    return result


def hash_file(path: pathlib.Path, budget: Budget) -> str:
    data = bounded_read(path, budget)
    assert isinstance(data, bytes)
    return hashlib.sha256(data).hexdigest()


def parse_json_file(path: pathlib.Path, budget: Budget) -> Any:
    data = bounded_read(path, budget, text=True)
    assert isinstance(data, str)
    return json.loads(data)


def git_archive(checkout: pathlib.Path, commit: str, budget: Budget) -> tuple[dict[str, bytes], bytes]:
    if not SHA40.fullmatch(commit):
        raise Refusal("source commit is not a 40-hex identity")
    if not checkout.exists() or checkout.is_symlink():
        raise ExactMissing("authenticated source checkout: " + str(checkout))
    physical_path(checkout, directory=True)
    budget.tick()
    try:
        proc = subprocess.run(
            ["git", "-C", str(checkout), "archive", "--format=tar", commit],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=max(1, min(60, int(budget.deadline_seconds))),
        )
    except subprocess.CalledProcessError as exc:
        raise Refusal("git archive unavailable") from exc
    except subprocess.TimeoutExpired as exc:
        raise LimitReached("git archive deadline exceeded") from exc
    budget.charge(len(proc.stdout))
    archive_hash = hashlib.sha256(proc.stdout).hexdigest()
    files: dict[str, bytes] = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(proc.stdout), mode="r:") as archive:
            for item in archive:
                budget.entry()
                if item.isdir():
                    continue
                if not item.isfile() or not item.name or ".." in pathlib.PurePosixPath(item.name).parts:
                    raise Refusal("unsupported committed source archive entry")
                content = archive.extractfile(item).read()  # type: ignore[union-attr]
                budget.charge(len(content))
                files[item.name] = content
    except (tarfile.TarError, OSError) as exc:
        raise Refusal("committed source archive is unreadable") from exc
    return files, proc.stdout


def ast_inventory(source: str, *, marker: str, end: str) -> dict[str, Any]:
    if marker not in source or end not in source:
        raise Refusal("installed source marker missing")
    body = source.split(marker, 1)[1].split(end, 1)[0]
    tree = ast.parse(body, filename="<installed verifier>")
    fail_calls = [node for node in ast.walk(tree)
                  if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                  and node.func.id == "fail"]
    functions = sorted({node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)})
    return {"fail_sites": len(fail_calls), "functions": functions,
            "source_sha256": hashlib.sha256(body.encode()).hexdigest()}


def call_graph(source: str) -> dict[str, Any]:
    patterns = {
        "Store construction": r"module\.Store\(root, tests\)",
        "Store ensure": r"store\.ensure\(",
        "dependency helper authentication": r"seed_module\(\)",
        "dependency installed verification": r"--installed",
        "embedded STORE_VERIFY execution": r"exec\(compile\(source",
        "embedded STORE_VERIFY staging execution": r"exec\(compile\(source, maker",
        "source carrier archive": r"archive-agent|archive-runtime|\.source-inputs",
    }
    found = {name: bool(re.search(pattern, source)) for name, pattern in patterns.items()}
    return {"found": found, "all_required": all(found.values())}


def source_layer(census: Census, args: argparse.Namespace, budget: Budget) -> dict[str, Any]:
    maker = pathlib.Path(args.maker)
    bench = pathlib.Path(args.bench_store or maker.parent / "bench_store.py")
    dependency = pathlib.Path(args.dependency_verifier or maker.parent / "verify_dependency_seed.py")
    paths = {"maker": maker, "bench_store": bench, "dependency_verifier": dependency}
    before: dict[str, str] = {}
    sources: dict[str, str] = {}
    for name, path in paths.items():
        def read_one(path: pathlib.Path = path, name: str = name) -> str:
            if not path.exists() or path.is_symlink():
                raise ExactMissing(name + " source: " + str(path))
            data = bounded_read(path, budget, text=True)
            assert isinstance(data, str)
            before[name] = hashlib.sha256(data.encode()).hexdigest()
            sources[name] = data
            return before[name]
        census.check("installed-source", "read:" + name, read_one)

    static: dict[str, Any] = {"paths": {name: str(path) for name, path in paths.items()},
                              "hashes_before": before}
    if "maker" in sources:
        census.check("installed-source", "embedded-STORE_VERIFY-inventory", lambda: ast_inventory(
            sources["maker"], marker="# STORE_VERIFY_BEGIN\n", end="# STORE_VERIFY_END"))
        static["call_graph"] = call_graph(sources["maker"])
        if not static["call_graph"]["all_required"]:
            census.record("production-call-graph", "maker-to-three-verifiers", "refused",
                          "installed caller pattern incomplete", static["call_graph"])
        else:
            census.record("production-call-graph", "maker-to-three-verifiers", "visited",
                          detail=static["call_graph"])
    if "bench_store" in sources:
        def bench_inventory() -> dict[str, Any]:
            tree = ast.parse(sources["bench_store"], filename="<installed bench_store>")
            calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                     and isinstance(node.func, ast.Name) and node.func.id == "check"]
            methods = sorted(node.name for node in tree.body if isinstance(node, ast.ClassDef)
                             for node in node.body if isinstance(node, ast.FunctionDef))
            return {"check_calls": len(calls), "store_methods": methods,
                    "expected_check_calls": 121, "count_matches_source": len(calls) == 121}
        static["bench_store"] = census.check("installed-source", "bench_store-AST-inventory", bench_inventory)
    if "dependency_verifier" in sources:
        def dependency_inventory() -> dict[str, Any]:
            tree = ast.parse(sources["dependency_verifier"], filename="<installed dependency verifier>")
            calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                     and isinstance(node.func, ast.Name) and node.func.id == "fail"]
            modes = sorted(node.value for node in ast.walk(tree) if isinstance(node, ast.Constant)
                           and isinstance(node.value, str) and node.value.startswith("--")
                           and node.value in {"--installed", "--committed-lock", "--verify-bootstrap", "--verify-farm", "--bootstrap-identity"})
            return {"fail_calls": len(calls), "expected_fail_calls": 143,
                    "count_matches_source": len(calls) == 143, "caller_modes": modes}
        static["dependency_verifier"] = census.check("installed-source", "dependency-verifier-AST-inventory", dependency_inventory)
    after: dict[str, str] = {}
    for name, path in paths.items():
        if not path.exists() or path.is_symlink():
            after[name] = "missing"
            continue
        try:
            after[name] = hash_file(path, budget)
        except (OSError, LimitReached, Refusal) as exc:
            after[name] = type(exc).__name__ + ":" + safe_text(exc)
    static["hashes_after"] = after
    static["hashes_unchanged"] = bool(before) and before == after
    census.record("installed-source", "immutable-installed-source-hashes", "visited" if static["hashes_unchanged"] else "refused",
                  None if static["hashes_unchanged"] else "source changed or could not be re-read", static)
    return static


def root_nodes(root: pathlib.Path, census: Census, budget: Budget, *, staging: bool) -> list[pathlib.Path] | None:
    if not root.exists() or root.is_symlink():
        census.missing_input("Farm retained staged child root: " + str(root), "STORE_VERIFY")
        census.record("STORE_VERIFY", "retained-root", "skipped", "EXACTMISSING")
        return None
    census.check("STORE_VERIFY", "retained-root", lambda: physical_path(root, directory=True))
    try:
        nodes = bounded_walk(root, budget)
    except LimitReached as exc:
        census.record("STORE_VERIFY", "bounded-root-traversal", "skipped", "INCOMPLETE:" + str(exc))
        return None
    except (OSError, ValueError) as exc:
        census.record("STORE_VERIFY", "bounded-root-traversal", "error", type(exc).__name__ + ": " + str(exc))
        return None
    violations: list[str] = []
    uid = os.getuid()
    for path in nodes:
        info = path.lstat()
        mode = info.st_mode
        relative = "." if path == root else path.relative_to(root).as_posix()
        if info.st_uid != uid or (stat.S_ISREG(mode) and info.st_nlink != 1):
            violations.append(relative + ": foreign-or-hardlinked")
        allowed_link = (stat.S_ISLNK(mode) and path == root / "lib64"
                        and path.readlink() == pathlib.Path("lib")
                        and (root / "lib").is_dir() and not (root / "lib").is_symlink())
        if stat.S_ISLNK(mode) and not allowed_link:
            violations.append(relative + ": symlink")
        if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode) or allowed_link):
            violations.append(relative + ": unsupported-type")
        if not staging and mode & 0o222:
            violations.append(relative + ": writable")
    census.record("STORE_VERIFY", "readonly-root-and-all-retained-paths",
                  "refused" if violations else "visited",
                  "ownership/type/mode violation" if violations else None,
                  {"visited_entries": len(nodes), "violations": violations[:1000]})
    return nodes


def expected_site(root: pathlib.Path, census: Census, budget: Budget) -> pathlib.Path | None:
    sites = sorted((root / "lib").glob("python*/site-packages")) if (root / "lib").is_dir() else []
    if len(sites) != 1:
        census.record("STORE_VERIFY", "site-packages-layout", "refused", "layout incomplete or ambiguous", [str(p) for p in sites])
        return None
    site = sites[0]
    try:
        if site.is_symlink() or not site.resolve().is_relative_to(root):
            raise Refusal("site-packages escapes child")
    except OSError as exc:
        census.record("STORE_VERIFY", "site-packages-layout", "error", type(exc).__name__ + ": " + str(exc))
        return None
    census.record("STORE_VERIFY", "site-packages-layout", "visited", detail=str(site))
    return site


def identity_checks(census: Census, args: argparse.Namespace, root: pathlib.Path,
                    site: pathlib.Path, budget: Budget) -> None:
    """Cover the non-RECORD identity guards without importing child modules."""
    executable = shutil.which(args.python)
    child = root / "bin" / "python"
    if executable is None or not pathlib.Path(executable).is_file():
        census.record("STORE_VERIFY", "maker-interpreter-available", "refused", "maker interpreter unavailable")
    elif not child.is_file() or child.is_symlink():
        census.record("STORE_VERIFY", "child-interpreter-identity", "refused", "child bin/python missing or symlinked")
    else:
        try:
            maker_bytes = bounded_read(pathlib.Path(executable), budget)
            child_bytes = bounded_read(child, budget)
            census.record("STORE_VERIFY", "child-interpreter-identity",
                          "visited" if maker_bytes == child_bytes else "refused",
                          None if maker_bytes == child_bytes else "child interpreter differs from maker interpreter")
        except (OSError, Refusal, LimitReached) as exc:
            census.record("STORE_VERIFY", "child-interpreter-identity", "skipped" if isinstance(exc, LimitReached) else "error", safe_text(exc))
    origins_path = root / ".astrid-import-origins"
    expected_names = {"astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client"}
    if args.farm_source:
        expected_names.add("banodoco_timeline_schema")
    try:
        raw = bounded_read(origins_path, budget, text=True)
        assert isinstance(raw, str)
        origins: dict[str, pathlib.Path] = {}
        for line in raw.splitlines():
            name, separator, value = line.partition("=")
            if not separator or name in origins:
                raise Refusal("duplicate or malformed import origin")
            origins[name] = pathlib.Path(value).resolve()
        if set(origins) != expected_names:
            raise Refusal("incomplete import provenance")
        if any(not path.is_file() or not path.is_relative_to(site) for path in origins.values()):
            raise Refusal("import origin escapes site-packages")
        census.record("STORE_VERIFY", "import-origin-provenance", "visited", detail=sorted(origins))
    except (OSError, ValueError, Refusal, LimitReached) as exc:
        census.record("STORE_VERIFY", "import-origin-provenance", "skipped" if isinstance(exc, LimitReached) else "refused", safe_text(exc))
    marker_values = {
        ".astrid-source-commit": args.agent_sha + "\n",
        ".astrid-runtime-source-commit": args.runtime_sha + "\n",
        ".astrid-runtime-client-identity": args.client + "\n",
    }
    for name, wanted in marker_values.items():
        try:
            actual = bounded_read(root / name, budget, text=True)
            census.record("STORE_VERIFY", "identity-marker:" + name,
                          "visited" if actual == wanted else "refused",
                          None if actual == wanted else "marker differs from requested identity")
        except (OSError, Refusal, LimitReached) as exc:
            census.record("STORE_VERIFY", "identity-marker:" + name, "skipped" if isinstance(exc, LimitReached) else "refused", safe_text(exc))


def parse_client(value: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in value.splitlines():
        if "=" not in line:
            raise Refusal("client tuple line has no equals")
        name, digest = line.split("=", 1)
        rel = name.removeprefix("packages/python/")
        if not rel or not SHA64.fullmatch(digest) or rel in result:
            raise Refusal("client tuple schema")
        result[rel] = digest
    if not result:
        raise Refusal("client tuple is empty")
    return result


def source_manifest_checks(census: Census, args: argparse.Namespace, root: pathlib.Path,
                           site: pathlib.Path, budget: Budget) -> dict[str, Any]:
    checkouts = {
        "astrid": (pathlib.Path(args.agent_checkout), args.agent_sha),
        "astrid-runtime": (pathlib.Path(args.runtime_checkout), args.runtime_sha),
    }
    if args.farm_source:
        checkouts["banodoco-timeline-schema"] = (pathlib.Path(args.farm_source), "242f9c4306bf3b501222cb041a9eb246ef47bc85")
    source_info: dict[str, Any] = {"carrier_allowlist": {
        "directory": ".child-venv-source-*/{agent,runtime,schema}",
        "archive": ".source-inputs/{agent,runtime,schema}.tar",
        "rule": "only committed manifest files and their parent directories are owned",
    }}
    archives: dict[str, tuple[dict[str, bytes], bytes]] = {}
    for name, (checkout, commit) in checkouts.items():
        label = "source-archive:" + name
        def archive_one(checkout: pathlib.Path = checkout, commit: str = commit,
                        name: str = name) -> dict[str, Any]:
            files, raw = git_archive(checkout, commit, budget)
            archives[name] = (files, raw)
            return {"files": len(files), "archive_sha256": hashlib.sha256(raw).hexdigest()}
        census.check("STORE_VERIFY", label, archive_one)
    snapshots = sorted(p for p in root.glob(".child-venv-source-*") if p.is_dir() and not p.is_symlink())
    if len(snapshots) != 1:
        census.record("STORE_VERIFY", "retained-source-snapshot", "refused", "snapshot count is not one", len(snapshots))
        return source_info
    snapshot = snapshots[0]
    for name, (files, raw) in archives.items():
        short = {"astrid": "agent", "astrid-runtime": "runtime", "banodoco-timeline-schema": "schema"}[name]
        source = snapshot / short
        dist_name = name
        dist_dirs = []
        for candidate in site.glob("*.dist-info"):
            metadata = candidate / "METADATA"
            if metadata.is_file() and re.search(r"^Name:\s*" + re.escape(dist_name) + r"\s*$", metadata.read_text(errors="replace"), re.MULTILINE | re.IGNORECASE):
                dist_dirs.append(candidate)
        if len(dist_dirs) != 1:
            census.record("STORE_VERIFY", "distribution:" + name, "refused", "missing or ambiguous distribution", len(dist_dirs))
            continue
        dist = dist_dirs[0]
        direct_path = dist / "direct_url.json"
        try:
            direct = json.loads(bounded_read(direct_path, budget, text=True))
            parsed = urlparse(direct.get("url", ""))
            carrier = pathlib.Path(unquote(parsed.path))
            if parsed.scheme != "file" or parsed.netloc not in ("", "localhost") or parsed.query or parsed.fragment:
                raise Refusal("invalid source URL")
            if carrier.is_symlink() or carrier != carrier.resolve() or not carrier.is_relative_to(root):
                raise Refusal("source carrier escapes retained child root")
            if "archive_info" in direct:
                expected = root / ".source-inputs" / (short + ".tar")
                if carrier != expected or hashlib.sha256(bounded_read(carrier, budget)).hexdigest() != hashlib.sha256(raw).hexdigest():
                    raise Refusal("source archive differs from requested commit")
            else:
                info = direct.get("dir_info")
                if (carrier != source or carrier.is_symlink() or not carrier.is_dir()
                        or not isinstance(info, dict) or info.get("editable", False) is not False):
                    raise Refusal("source is not a noneditable directory install")
            source_info.setdefault("carriers", {})[name] = {"path": str(carrier), "kind": "archive" if "archive_info" in direct else "directory"}
            for rel, content in files.items():
                target = source / rel
                if not target.is_file() or target.is_symlink() or bounded_read(target, budget) != content:
                    raise Refusal("retained source differs from requested commit: " + name + "/" + rel)
            expected_dirs = {source}
            for rel in files:
                expected_dirs.update((root / (snapshot.relative_to(root) / short / rel)).parents)
            for path in bounded_walk(source, budget):
                rel = path.relative_to(root).as_posix()
                if path.is_dir() and path not in expected_dirs:
                    raise Refusal("unowned retained source directory: " + rel)
                if path.is_file() and rel not in {str((snapshot.relative_to(root) / short / item).as_posix()) for item in files}:
                    raise Refusal("unowned retained source file: " + rel)
            census.record("STORE_VERIFY", "source-carrier-and-allowlist:" + name, "visited",
                          detail=source_info.get("carriers", {}).get(name))
        except (OSError, ValueError, KeyError, UnicodeError, Refusal, LimitReached) as exc:
            status = "skipped" if isinstance(exc, LimitReached) else "refused"
            census.record("STORE_VERIFY", "source-carrier-and-allowlist:" + name, status, safe_text(exc))
    return source_info


def record_checks(census: Census, args: argparse.Namespace, root: pathlib.Path,
                  site: pathlib.Path, budget: Budget) -> dict[str, Any]:
    expected_client = parse_client(args.client)
    distributions = sorted(p for p in site.glob("*.dist-info") if p.is_dir() and not p.is_symlink())
    rows_by_dist: dict[str, dict[str, str]] = {}
    all_rows: dict[str, str] = {}
    details: dict[str, Any] = {"distributions": [str(p.relative_to(site)) for p in distributions]}
    for dist in distributions:
        metadata = bounded_read(dist / "METADATA", budget, text=True)
        assert isinstance(metadata, str)
        match = re.search(r"^Name:\s*(.+?)\s*$", metadata, re.MULTILINE | re.IGNORECASE)
        name = match.group(1).strip() if match else dist.name.removesuffix(".dist-info")
        record = dist / "RECORD"
        rows: dict[str, str] = {}
        try:
            raw = bounded_read(record, budget, text=True)
            assert isinstance(raw, str)
            for row in csv.reader(io.StringIO(raw), strict=True):
                if len(row) != 3 or not row[0] or "\\" in row[0] or "\x00" in row[0]:
                    raise Refusal("malformed RECORD row")
                rel, encoded, size = row
                pure = pathlib.PurePosixPath(rel)
                target = (site / rel).resolve()
                if pure.is_absolute() or str(pure) != rel or rel in rows or not target.is_relative_to(root):
                    raise Refusal("unsafe or duplicate RECORD path")
                info = target.lstat()
                if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
                    raise Refusal("RECORD target is not a physical regular file")
                content = bounded_read(target, budget)
                assert isinstance(content, bytes)
                if not encoded and not size:
                    if target != record and not (rel.endswith(".pyc") and "__pycache__" in pure.parts):
                        raise Refusal("unhashed non-RECORD/non-pyc row")
                else:
                    digest = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
                    if encoded != "sha256=" + digest or size != str(len(content)):
                        raise Refusal("RECORD digest/size mismatch: " + rel)
                rows[rel] = encoded
                if rel in all_rows:
                    raise Refusal("overlapping RECORD ownership: " + rel)
                all_rows[rel] = name
            rows_by_dist[name] = rows
            census.record("STORE_VERIFY", "RECORD:" + name, "visited", detail={"rows": len(rows)})
        except (OSError, ValueError, csv.Error, Refusal, LimitReached) as exc:
            census.record("STORE_VERIFY", "RECORD:" + name, "skipped" if isinstance(exc, LimitReached) else "refused", safe_text(exc))
    client_rows = {rel for rel in all_rows if rel.startswith("astrid_runtime_client/") and not rel.endswith(".pyc")}
    client_ok = client_rows == set(expected_client)
    if client_ok:
        for rel, wanted in expected_client.items():
            target = site / rel
            if not target.is_file() or hash_file(target, budget) != wanted:
                client_ok = False
                break
    census.record("STORE_VERIFY", "canonical-client-ownership", "visited" if client_ok else "refused",
                  None if client_ok else "client RECORD/file set or digest mismatch", {"rows": sorted(client_rows)})
    details["rows"] = {name: len(rows) for name, rows in rows_by_dist.items()}
    return details


def store_layer(census: Census, args: argparse.Namespace, root: pathlib.Path,
                budget: Budget) -> dict[str, Any]:
    store = pathlib.Path(args.work_root) / "bench-store"
    tests = pathlib.Path(args.work_root) / "tests"
    result = {"store_root": str(store), "tests_root": str(tests), "production_constructor": "Store(root, tests)",
              "production_operations": ["Store.__init__", "ensure", "_validate_index", "_owned_dir", "registration", "projection"]}
    if not store.exists() or store.is_symlink():
        census.missing_input("bench-store root: " + str(store), "bench_store")
        census.record("bench_store", "store-root", "skipped", "EXACTMISSING")
        return result
    census.check("bench_store", "store-root", lambda: physical_path(store, directory=True))
    try:
        owner = parse_json_file(store / "owner.json", budget)
        expected = {"version", "uid", "id", "root", "tests", "mutex", "directories"}
        if set(owner) != expected or owner["root"] != str(store) or owner["tests"] != str(tests) or owner["uid"] != os.getuid():
            raise Refusal("store owner schema/identity mismatch")
        census.record("bench_store", "owner-schema-and-identity", "visited")
        for name in ("entries", "locks", "staging"):
            child = store / name
            if child.is_symlink() or not child.is_dir():
                raise Refusal("store directory missing or symlinked: " + name)
        index = parse_json_file(store / "index.json", budget)
        if set(index) != {"version", "seq", "entries", "registrations", "retired", "retired_suites"} or index["version"] != 1:
            raise Refusal("index schema")
        entry_count = 0
        for eid, entry in index["entries"].items():
            budget.entry()
            entry_count += 1
            if set(entry) != {"component", "key", "identity", "path", "seq", "lock", "node", "owner"}:
                raise Refusal("entry schema")
            if entry["owner"] != owner["id"] or entry["path"] != str(store / "entries" / eid):
                raise Refusal("entry ownership/path mismatch")
            entry_path = pathlib.Path(entry["path"])
            if entry_path.exists():
                marker = parse_json_file(entry_path / ".bench-owner.json", budget)
                if marker.get("owner") != owner["id"]:
                    raise Refusal("entry marker owner mismatch")
        census.record("bench_store", "index-entry-registration-ownership", "visited", {"entries": entry_count, "registrations": len(index["registrations"])})
        if root.exists():
            matching = [entry for entry in index["entries"].values() if entry.get("path") == str(root)]
            census.record("bench_store", "retained-root-index-binding", "visited" if len(matching) == 1 else "refused",
                          None if len(matching) == 1 else "retained root is not exactly one indexed entry", len(matching))
    except (OSError, ValueError, KeyError, TypeError, Refusal, LimitReached) as exc:
        census.record("bench_store", "store-read-only-census", "skipped" if isinstance(exc, LimitReached) else "refused", safe_text(exc))
    return result


def dependency_layer(census: Census, args: argparse.Namespace, root: pathlib.Path,
                     budget: Budget) -> dict[str, Any]:
    seed = pathlib.Path(args.dependency_seed) if args.dependency_seed else None
    retained = root / ".dependency-wheelhouse"
    result: dict[str, Any] = {"installed_verifier": str(args.dependency_verifier or pathlib.Path(args.maker).parent / "verify_dependency_seed.py"),
                              "production_modes": ["--bootstrap-identity", "--verify-bootstrap", "wheelhouse", "--installed", "--verify-farm"],
                              "read_only": True}
    if not root.exists():
        census.missing_input("dependency verifier child root: " + str(root), "verify_dependency_seed")
        census.record("verify_dependency_seed", "dependency-root", "skipped", "EXACTMISSING")
        return result
    if seed is None and not retained.exists():
        census.skip("verify_dependency_seed", "dependency-seed-path", "NOT_REQUIRED: no caller seed and no retained seed")
        return result
    if seed is None and retained.exists():
        census.record("verify_dependency_seed", "dependency-seed-binding", "refused", "retained seed exists without caller-bound dependency seed")
        return result
    assert seed is not None
    if not seed.exists() or seed.is_symlink():
        census.missing_input("dependency wheelhouse: " + str(seed), "verify_dependency_seed")
        census.record("verify_dependency_seed", "dependency-wheelhouse", "skipped", "EXACTMISSING")
        return result
    census.check("verify_dependency_seed", "dependency-wheelhouse-physical", lambda: physical_path(seed, directory=True))
    requirements = pathlib.Path(args.dependency_requirements) if args.dependency_requirements else seed / "requirements.txt"
    if not requirements.exists() or requirements.is_symlink():
        census.missing_input("dependency requirements: " + str(requirements), "verify_dependency_seed")
        census.record("verify_dependency_seed", "dependency-requirements", "skipped", "EXACTMISSING")
        return result
    data = bounded_read(requirements, budget)
    assert isinstance(data, bytes)
    names = sorted(path.name for path in seed.iterdir() if path.is_file() and not path.is_symlink())
    unsupported = [name for name in names if name != "requirements.txt" and not name.endswith(".whl")]
    census.record("verify_dependency_seed", "wheelhouse-contents", "refused" if unsupported else "visited",
                  "unsupported artifact" if unsupported else None, {"files": names[:1000], "unsupported": unsupported[:100]})
    census.record("verify_dependency_seed", "dependency-missing-probe-boundary", "visited",
                  detail={"requirements_bytes": len(data), "wheel_count": len([n for n in names if n.endswith(".whl")])})
    return result


def private_probe(census: Census, budget: Budget) -> dict[str, Any]:
    """Small local fixture: proves simultaneous root failures and missing seed."""
    base = pathlib.Path(tempfile.mkdtemp(prefix="farm-census-1516-"))
    root = base / "readonly-case"
    root.mkdir()
    (root / "hard-a").write_bytes(b"x")
    os.link(root / "hard-a", root / "hard-b")
    (root / "writable").mkdir()
    (root / "writable" / "marker").write_bytes(b"x")
    os.chmod(root / "writable", 0o755)
    (root / "link").symlink_to("hard-a")
    violations: list[str] = []
    for path in bounded_walk(root, budget):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if info.st_nlink != 1:
            violations.append("hardlink:" + rel)
        if stat.S_ISLNK(info.st_mode):
            violations.append("symlink:" + rel)
        if info.st_mode & 0o222:
            violations.append("writable:" + rel)
    missing = base / "missing-wheelhouse"
    result = {"fixture_root": str(base), "multiple_failures": sorted(set(item.split(":", 1)[0] for item in violations)),
              "observed_violation_count": len(violations),
              "dependency_missing": {"path": str(missing), "status": "EXACTMISSING"},
              "status": "PASS_LIMITED" if {"hardlink", "symlink", "writable"} <= set(item.split(":", 1)[0] for item in violations) else "FAIL"}
    census.record("private-probe", "simultaneous-hardlink-writable-symlink", "visited", detail=result)
    census.record("private-probe", "missing-dependency-prerequisite", "visited", detail=result["dependency_missing"])
    return result


def final_status(census: Census, static: dict[str, Any], root: pathlib.Path) -> str:
    if census.missing:
        return "EXACTMISSING"
    if any(row.status == "skipped" and (row.reason or "").startswith("INCOMPLETE") for row in census.boundaries):
        return "INCOMPLETE"
    if census.errors or census.refusals:
        return "INCOMPLETE"
    if not root.exists():
        return "EXACTMISSING"
    if not static.get("hashes_unchanged"):
        return "INCOMPLETE"
    if any(row.status == "skipped" for row in census.boundaries if row.layer in {"STORE_VERIFY", "bench_store", "verify_dependency_seed"}):
        return "INCOMPLETE"
    return "COMPLETE"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    budget = Budget(max(1, min(int(args.deadline_seconds), DEFAULT_DEADLINE)))
    census = Census(budget)
    root = pathlib.Path(args.root)
    static = source_layer(census, args, budget)
    nodes = root_nodes(root, census, budget, staging=args.staging)
    site = None
    if nodes is not None:
        site = expected_site(root, census, budget)
        if site is not None:
            census.check("STORE_VERIFY", "interpreter-import-marker-identity",
                         lambda: identity_checks(census, args, root, site, budget))
            census.check("STORE_VERIFY", "distribution-record-ownership", lambda: record_checks(census, args, root, site, budget))
            census.check("STORE_VERIFY", "source-carrier-directory-allowlist", lambda: source_manifest_checks(census, args, root, site, budget))
        else:
            census.skip("STORE_VERIFY", "distribution-record-ownership", "site-packages prerequisite unavailable")
            census.skip("STORE_VERIFY", "source-carrier-directory-allowlist", "site-packages prerequisite unavailable")
    store = store_layer(census, args, root, budget)
    dependency = dependency_layer(census, args, root, budget)
    probe = private_probe(census, budget)
    # Re-read installed source after all checks.  This is intentionally last so
    # any source mutation is visible even if a prior independent check refused.
    if static.get("paths"):
        paths = {name: pathlib.Path(path) for name, path in static["paths"].items()}
        after: dict[str, str] = {}
        for name, path in paths.items():
            try:
                after[name] = hash_file(path, budget)
            except (OSError, LimitReached, Refusal) as exc:
                after[name] = type(exc).__name__ + ":" + safe_text(exc)
        static["hashes_after_final"] = after
        static["hashes_unchanged"] = static.get("hashes_before", {}) == after
    status = final_status(census, static, root)
    report = {
        "task": "rt-OPS-Farm-census-return-1516",
        "result": status,
        "diagnostic_fitness": "READY_FOR_REVIEW" if status != "COMPLETE" else "COMPLETE_READ_ONLY_CENSUS",
        "mode": "independent-bounded-read-only",
        "production_caller": {
            "maker": str(pathlib.Path(args.maker)),
            "sequence": ["source authentication", "optional dependency/farm authority", "Store(root, tests)", "Store.ensure", "embedded STORE_VERIFY", "dependency --installed when seed-bound", "registration/projection"],
            "installed_checks_unchanged": True,
        },
        "limits": {"deadline_seconds": budget.deadline_seconds, "max_entries": budget.max_entries,
                   "max_bytes": budget.max_bytes, "max_output_bytes": budget.max_output,
                   "stop_on_limit": "INCOMPLETE", "no_heavy_or_network": True},
        "inputs": {"root": str(root), "root_observed": root.exists() and not root.is_symlink(),
                   "work_root": str(pathlib.Path(args.work_root)), "staging": bool(args.staging),
                   "agent_sha": args.agent_sha, "runtime_sha": args.runtime_sha,
                   "farm_source": args.farm_source},
        "missing": sorted(census.missing),
        "installed_source": static,
        "store_layer": store,
        "dependency_layer": dependency,
        "source_carrier_allowlist": {"from_exact_e62f": True,
            "allowed": [".child-venv-source-*/agent|runtime|schema committed files", ".source-inputs/agent|runtime|schema.tar"],
            "directory_rule": "only authenticated manifest parent directories; no extra retained source directory",
            "proposed_fix": "none proved; the observed flat refusal has no path and the installed rule is already strict",
            "required_for_review": "exact retained source tree plus authenticated source manifest"},
        "private_probe": probe,
        "boundaries": [{"layer": row.layer, "check": row.name, "status": row.status,
                         "reason": row.reason, **({"detail": row.detail} if row.detail is not None else {})}
                        for row in census.boundaries],
        "counts": {"visited": sum(row.status == "visited" for row in census.boundaries),
                    "refused": len(census.refusals), "skipped": len(census.skips),
                    "errors": len(census.errors), "entries": budget.entries, "bytes": budget.bytes},
        "refusals": census.refusals,
        "skips": census.skips,
        "errors": census.errors,
        "safety": {"executed_installed_content": False, "writes_to_inputs": False,
                    "production_mutations": [], "source_hashes_checked_before_after": True},
    }
    encoded = json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True).encode()
    if len(encoded) > budget.max_output:
        raise LimitReached("report output budget exceeded")
    return report


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--maker", required=True)
    p.add_argument("--root", required=True)
    p.add_argument("--client", required=True)
    p.add_argument("--agent-checkout", required=True)
    p.add_argument("--agent-sha", required=True)
    p.add_argument("--runtime-checkout", required=True)
    p.add_argument("--runtime-sha", required=True)
    p.add_argument("--work-root", required=True)
    p.add_argument("--python", required=True)
    p.add_argument("--farm-source")
    p.add_argument("--bench-store")
    p.add_argument("--dependency-verifier")
    p.add_argument("--dependency-seed")
    p.add_argument("--dependency-requirements")
    p.add_argument("--staging", action="store_true")
    p.add_argument("--deadline-seconds", type=int, default=DEFAULT_DEADLINE)
    p.add_argument("--output", required=True)
    return p


def main() -> int:
    args = parser().parse_args()
    output = pathlib.Path(args.output)
    if not output.is_absolute() or output.is_symlink() or ".." in output.parts:
        print("REFUSED: output must be an absolute non-symlink path", file=sys.stderr)
        return 2
    try:
        report = build_report(args)
        output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except LimitReached as exc:
        report = {"task": "rt-OPS-Farm-census-return-1516", "result": "INCOMPLETE",
                  "diagnostic_fitness": "INCOMPLETE", "fatal_boundary": safe_text(exc),
                  "writes_to_inputs": False}
        output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return 2
    except (OSError, ValueError, Refusal, ExactMissing) as exc:
        report = {"task": "rt-OPS-Farm-census-return-1516", "result": "INCOMPLETE",
                  "diagnostic_fitness": "INCOMPLETE", "fatal_boundary": type(exc).__name__ + ": " + safe_text(exc),
                  "writes_to_inputs": False}
        output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return 2
    return 0 if report["result"] in {"EXACTMISSING", "COMPLETE", "INCOMPLETE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
