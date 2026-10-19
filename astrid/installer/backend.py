"""Concrete Runtime and tool operations used by the install transaction."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import uuid
import webbrowser
from pathlib import Path

from .core import Version, absolute, current, linked, new_version_id, read_json, write_json
from .service import Service, platform_target, venv_python
from .tools import binary, install_tools, source


class Backend:
    def __init__(self, root: Path, log: Path, uv: Path, *, say=print):
        self.root, self.log, self.uv = root, log, uv
        self.service = Service(root, log, self.run, say=say)

    def run(self, argv, *, extra_env=None, cwd=None, timeout=1800) -> str:
        # Never inherit a developer's Python import path or Runtime connection.
        env = {k: v for k, v in os.environ.items() if k not in {
            "PYTHONPATH", "PYTHONHOME", "ASTRID_WORKSPACE_ENDPOINT",
            "ASTRID_WORKSPACE_CREDENTIAL", "ASTRID_RUNTIME_SOURCE_MANIFEST",
            "ASTRID_RUNTIME_DATA_ROOT", "ASTRID_PACKS_PATH"}}
        env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
        env.update(extra_env or {})
        result = subprocess.run([str(s) for s in argv], cwd=cwd, env=env, check=False,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                encoding="utf-8", errors="replace", timeout=timeout)
        with self.log.open("a", encoding="utf-8") as stream:
            # Do not log inherited environments or credentials.
            stream.write(result.stdout + "\n")
        if result.returncode:
            raise subprocess.CalledProcessError(result.returncode, [str(argv[0])], output=result.stdout)
        return result.stdout.strip()

    def install_remotion_dependencies(self, agent: Path, env: dict[str, str], npm: Path) -> None:
        """Install the renderer's frozen dependencies, reusing an identical lock."""
        remotion = agent / "remotion"
        lock_hash = hashlib.sha256((remotion / "package-lock.json").read_bytes()).hexdigest()
        modules = remotion / "node_modules"
        marker = modules / ".astrid-package-lock.sha256"
        if (modules.is_dir() and marker.is_file()
                and marker.read_text(encoding="ascii").strip() == lock_hash):
            return
        # Node's official archives expose npm through this JavaScript entrypoint
        # on every OS; neither shell shims nor an ambient npm are required.
        self.run([env["ASTRID_NODE_EXECUTABLE"], npm, "ci", "--no-audit", "--no-fund"],
                 cwd=remotion, extra_env=env)
        marker.write_text(lock_hash + "\n", encoding="ascii")

    def runtime(self, version: Version | None, data: Path, *args, profile=False, timeout=1800) -> dict:
        python = version.python if version else Path(sys.executable)
        module = version.env.get("ASTRID_INSTALL_RUNTIME_MODULE", "astrid_runtime") if version else "astrid_runtime"
        if module not in {"astrid_runtime", "banodoco_local"}:
            raise ValueError("Unknown Runtime module in the installation record.")
        argv = [python, "-I", "-m", module, *args, "--data-root", str(data), "--json"]
        if profile and version:
            argv += ["--source-manifest", str(version.profile)]
        result = json.loads(self.run(argv, extra_env=version.env if version else None, timeout=timeout))
        if result.get("ok") is False:
            raise RuntimeError(str(result.get("error") or result))
        return result

    def existing(self, data: Path) -> Version | None:
        record = self.service.recorded()
        if record.get("version"):
            return Version.load(record["version"])
        profile = data / "runtime" / "source-profiles" / "astrid.json"
        value = read_json(profile)
        if not value:
            return None
        environment = absolute(value["runtime_environment"])
        python = venv_python(environment)
        if not python.is_file():
            raise ValueError("The existing Runtime interpreter is missing; its source environment needs recovery.")
        # This is an intentional pre-rename compatibility probe, never a new pin.
        module = self.run([python, "-I", "-c", "import importlib.util; print('astrid_runtime' if importlib.util.find_spec('astrid_runtime') else 'banodoco_local')"]).strip()
        return Version(environment.parent, python, profile,
                       {"PATH": str(python.parent) + os.pathsep + os.defpath,
                        "ASTRID_INSTALL_RUNTIME_MODULE": module})

    def has_workspace(self, data: Path) -> bool:
        # A nonempty selected root is never mistaken for a fresh installation.
        return data.exists() and any(p.name != "logs" for p in data.iterdir())

    def workspace(self, version: Version, data: Path) -> dict:
        value = self.runtime(version, data, "workspace", "inspect")
        if not value.get("realm_id") or not value.get("realm_root"):
            raise ValueError("The selected workspace has no unambiguous identity.")
        absolute(value["realm_root"])
        return value

    def stop(self, version: Version | None, data: Path) -> None:
        self.service.disable()
        if version is not None and (data / "runtime" / "discovery.json").exists():
            self.runtime(version, data, "down", profile=True)
        self.service.stop()
        if (data / "runtime" / "discovery.json").exists():
            # A manager may still be draining after its stop operation.
            if version:
                self.runtime(version, data, "down", profile=True)
            if (data / "runtime" / "discovery.json").exists():
                raise RuntimeError("Astrid did not release its recorded Runtime owner.")

    def _copy(self, source: Path, destination: Path, *, clone=False, support=False) -> None:
        from runtime_protocol.fsclone import clone_or_copy_file

        def copy_file(src, dst):
            src, dst = Path(src), Path(dst)
            if linked(src):
                raise ValueError(f"Backup refused a linked entry: {src}")
            if clone:
                clone_or_copy_file(src, dst)
            else:
                shutil.copy2(src, dst)
            return str(dst)

        def ignore(folder, names):
            parent = Path(folder)
            for name in names:
                entry = parent / name
                if linked(entry):
                    raise ValueError(f"Backup refused a linked entry: {entry}")
            if support and parent == source / "runtime":
                return {"realms", "discovery.json", "instance.lock", "bootstrap.lock"}.intersection(names)
            return set()

        shutil.copytree(source, destination, copy_function=copy_file, ignore=ignore)

    def backup(self, version: Version, data: Path, realm: dict) -> dict:
        from runtime_protocol import platform
        destination = self.root / "backups" / uuid.uuid4().hex[:12]
        platform.private_directory(destination)
        kind = "clone" if self.service.system == "darwin" else "runtime"
        if kind == "clone":
            self._copy(absolute(realm["realm_root"]), destination / "realm", clone=True)
        else:
            # The backup CLI uses authenticated RPC. Start only the neutral
            # daemon (no foreground service supervisor and no browser door).
            try:
                self.runtime(version, data, "up", "--hosted-origin", "off", profile=True)
                self.runtime(version, data, "backup", "--destination", str(destination / "realm"))
            finally:
                self.stop(version, data)
        self._copy(data, destination / "support", clone=kind == "clone", support=True)
        result = {"root": str(destination), "kind": kind}
        write_json(destination / "backup.json", result)
        return result

    def restore(self, old: Version, data: Path, realm: dict, backup: dict) -> None:
        destination = Path(backup["root"])
        realm_root = absolute(realm["realm_root"])
        restored = realm_root.with_name(realm_root.name + ".restore-" + uuid.uuid4().hex[:8])
        if backup["kind"] == "clone":
            self._copy(destination / "realm", restored, clone=True)
        else:
            # The offline restore API is the same authenticated implementation
            # behind `astrid-runtime restore`, without starting a damaged schema.
            script = ("from runtime_protocol.backup import restore_backup; import sys; "
                      "restore_backup(sys.argv[1],sys.argv[2])")
            self.run([old.python, "-I", "-c", script, destination / "realm", restored], extra_env=old.env)
        failed = realm_root.with_name(realm_root.name + ".failed-" + uuid.uuid4().hex[:8])
        os.replace(realm_root, failed)
        try:
            os.replace(restored, realm_root)
        except BaseException:
            os.replace(failed, realm_root)
            raise
        # Restore all support metadata, preserving unselected realms and extras.
        snapshot = destination / "support"
        for item in snapshot.iterdir():
            target = data / item.name
            if item.name == "runtime":
                for entry in target.iterdir():
                    if entry.name != "realms":
                        if entry.is_dir():
                            shutil.rmtree(entry)
                        else:
                            entry.unlink()
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                if target.is_dir():
                    shutil.rmtree(target)
                elif target.exists():
                    target.unlink()
                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)

    def stage(self, manifest: dict, root: Path, data: Path) -> Version:
        if self.run([self.uv, "--version"]).split()[1] != manifest["tools"]["uv"]["version"]:
            raise ValueError("The installer needs the manifest's pinned uv.")
        folder = root / "versions" / new_version_id(manifest)
        folder.mkdir(parents=True)
        agent = source("agent", manifest["agent"]["sha"], folder / "a")
        runtime = source("runtime", manifest["runtime"]["sha"], folder / "r")
        environment = folder / "py"
        self.run([self.uv, "venv", "--python", manifest["tools"]["python"]["version"], environment])
        python = venv_python(environment)
        self.run([self.uv, "pip", "install", "--python", python, runtime,
                  runtime / "packages" / "python", agent / "packages" / "timeline-schema" / "python", agent])
        env = install_tools(manifest, folder / "tools", platform_target(), self.run)
        env.update({"ASTRID_RUNTIME_DATA_ROOT": str(data),
                    "PATH": str(python.parent) + os.pathsep + env["PATH"]})
        npm = binary(folder / "tools" / "node", "npm-cli.js")
        self.install_remotion_dependencies(agent, env, npm)
        profile = folder / "profile.json"
        # Compute the admitted source identity in the installed environment.
        digest = self.run([python, "-I", "-c", "from astrid.core.execution.generic_host import source_checkout_digest; import pathlib,sys; print(source_checkout_digest(pathlib.Path(sys.argv[1])))", agent], extra_env=env)
        write_json(profile, {"profile": "astrid", "runtime_checkout": str(runtime),
                             "source_checkout": str(agent), "runtime_environment": str(environment),
                             "source_digest": digest})
        version = Version(folder, python, profile, env)
        write_json(folder / "version.json", version.document())
        write_json(folder / "manifest.json", manifest)
        return version

    def create(self, version: Version, data: Path) -> dict:
        realm_id = str(uuid.uuid4())
        return self.runtime(version, data, "workspace", "create", "--realm-root",
                            str(data / "runtime" / "realms" / realm_id), "--realm-id", realm_id, profile=True)

    def upgrade(self, version: Version, data: Path) -> None:
        self.runtime(version, data, "upgrade", profile=True)

    def register(self, version: Version, data: Path) -> None:
        self.service.register(version, data)

    def start(self, version: Version, data: Path) -> None:
        if not self.service.start():
            self.service.start_foreground(version, data)

    def verify(self, version: Version, data: Path, realm_id: str) -> None:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        deadline = time.monotonic() + 90
        error = None
        while time.monotonic() < deadline:
            try:
                status = self.runtime(version, data, "status", timeout=3)
                discovery = read_json(data / "runtime" / "discovery.json")
                endpoint = discovery.get("door_endpoint", "")
                if endpoint != "http://127.0.0.1:17340":
                    raise ValueError("Astrid's recorded door is not on the hosted page's loopback port.")
                def get(path):
                    request = urllib.request.Request(endpoint + path, headers={"Origin": "https://astrid.haus"})
                    with opener.open(request, timeout=2) as response:
                        return json.load(response)
                health = get("/api/runtime/v1/health")
                realm = get("/api/runtime/v1/realm")
                if (health.get("status") != "ok" or realm.get("realm_id") != realm_id
                        or discovery.get("active_realm") != realm_id
                        or health.get("runtime_instance_id") != discovery.get("runtime_instance_id")
                        or status.get("discovery", {}).get("runtime_instance_id") != discovery.get("runtime_instance_id")
                        or status.get("support", {}).get("pid_alive") is not True):
                    raise ValueError("The browser door belongs to a different Runtime or workspace.")
                return
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
                error = exc
                time.sleep(0.25)
        raise RuntimeError(f"Astrid's browser door did not become ready: {error}")

    def finish(self, old: Version | None, candidate: Version, backup: dict | None) -> None:
        # Keep the immediately previous program and backup. Failures cleaning an
        # older locked version are residue, not grounds to roll back a good update.
        keep = {candidate.root, old.root if old else candidate.root}
        for path in (self.root / "versions").iterdir():
            if path not in keep:
                try:
                    shutil.rmtree(path)
                except OSError:
                    pass
        if backup:
            for path in (self.root / "backups").iterdir():
                if path != Path(backup["root"]):
                    try:
                        shutil.rmtree(path)
                    except OSError:
                        pass

    def unregister(self) -> None:
        self.service.unregister()

    def remove(self, root: Path, data: Path, *, delete_data: bool) -> list[Path]:
        residue = []
        # Only directories created and marked by this installer are removable.
        if read_json(root / "install.json").get("owner") != "haus.astrid.runtime":
            raise ValueError("Refusing to remove an unowned installation directory.")
        data_targets = [data] if delete_data else []
        if delete_data:
            version = current(root) or self.existing(data)
            if version:
                realm_root = absolute(self.workspace(version, data)["realm_root"])
                if realm_root != data and data not in realm_root.parents:
                    # An attached workspace can live outside the support root.
                    # Inspect its identity before removing the executable.
                    if realm_root in root.parents or root in realm_root.parents:
                        raise ValueError("The attached workspace overlaps the program directory.")
                    data_targets.insert(0, realm_root)
        # Keep the ownership/data-root marker until the last owned file is
        # gone, so rerunning the line can finish removal after a Windows lock.
        for path in root.iterdir():
            if path.name == "install.json":
                continue
            try:
                if path.is_dir() and not linked(path):
                    shutil.rmtree(path)
                else:
                    path.unlink()
            except OSError:
                residue.append(path)
        if not residue:
            (root / "install.json").unlink()
            try:
                root.rmdir()
            except OSError:
                write_json(root / "install.json", {"owner": "haus.astrid.runtime", "data_root": str(data)})
                residue.append(root)
        for data_path in data_targets:
            if not data_path.exists():
                continue
            try:
                shutil.rmtree(data_path)
            except OSError:
                residue.append(data_path)
        return residue

    def open(self) -> None:
        try:
            webbrowser.open("https://astrid.haus/?connect=1")
        except OSError:
            pass  # The printed URL remains usable on headless computers.
