"""Real Windows installation journey; no installed-package imports in the driver."""

from __future__ import annotations

import argparse
import functools
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import ntpath
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())) / "X5-windows-journey"
HEALTH_URL = "http://127.0.0.1:17340/api/runtime/v1/health"


def save(name, value):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def run(argv, name, *, env=None, timeout=300, show=True):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    print(f"Running {name}", flush=True)
    try:
        with (EVIDENCE / name).open("w", encoding="utf-8") as log:
            result = subprocess.run([str(arg) for arg in argv], env=env, stdout=log,
                                    stderr=subprocess.STDOUT, timeout=timeout, check=False)
    finally:
        if show:
            print((EVIDENCE / name).read_text(encoding="utf-8", errors="replace"), flush=True)
    if result.returncode:
        raise RuntimeError(f"{name}: exit {result.returncode}")
    return (EVIDENCE / name).read_text(encoding="utf-8-sig", errors="replace")


def powershell(code, name, *, show=True):
    return run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
                "$ErrorActionPreference='Stop'; "
                "[Console]::OutputEncoding=[Text.UTF8Encoding]::new($false); " + code], name, show=show)


def source(repo):
    sha = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError(f"Not a full source commit: {repo}")
    return {"sha": sha, "repo": str(repo.resolve())}


def install_manifest(agent, runtime, app):
    manifest = json.loads((app / "public" / "install-manifest.json").read_text(encoding="utf-8"))
    # Replace the entire source records, including any released schema digest.
    manifest.update(agent=source(agent), runtime=source(runtime))
    return manifest


class ManifestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, document, **kwargs):
        self.document = document
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path != "/install-manifest.json":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(self.document)))
        self.end_headers()
        self.wfile.write(self.document)


def install(shell):
    runtime, app = ROOT / "journey-runtime", ROOT / "journey-app"
    manifest = install_manifest(ROOT, runtime, app)
    save("install-manifest.json", manifest)
    save("sources.json", {"agent": manifest["agent"], "runtime": manifest["runtime"], "app": source(app)})
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(
        ManifestHandler, document=json.dumps(manifest).encode("utf-8")))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    env = dict(os.environ, ASTRID_INSTALL_MANIFEST_URL=
               f"http://127.0.0.1:{server.server_port}/install-manifest.json")
    # Python's standard browser override suppresses the installer's website open.
    env["BROWSER"] = f'"{sys.executable}" -c "pass" %s'
    try:
        run([shell, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
             "-File", app / "public" / "install.ps1"], "bootstrap.log", env=env, timeout=3600)
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    installed = version()
    actual = json.loads((Path(installed["root"]) / "manifest.json").read_text(encoding="utf-8"))
    for name in ("agent", "runtime"):
        if actual[name] != manifest[name]:
            raise RuntimeError(f"Installer did not use the selected {name} source")


def program_root():
    return Path(os.environ["LOCALAPPDATA"]) / "Astrid"


def data_root():
    return Path(os.environ["LOCALAPPDATA"]) / "Astrid Runtime"


def version():
    root = program_root()
    current = (root / "current").read_text(encoding="utf-8").strip()
    return json.loads((root / "versions" / current / "version.json").read_text(encoding="utf-8"))


def cli(module, argv, name, *, timeout=300):
    installed = version()
    env = {key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONHOME"}}
    env.update(installed["env"])
    return run([installed["python"], "-I", "-m", module, *argv], name, env=env, timeout=timeout)


def health():
    request = urllib.request.Request(HEALTH_URL, headers={"Origin": "https://astrid.haus"})
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request, timeout=30) as response:
            value = json.load(response)
    except (OSError, ValueError) as exc:
        save("health-error.json", {"error": str(exc)})
        return None
    save("health.json", value)
    return value


def wait_for(label, probe, *, seconds=900):
    deadline = time.monotonic() + seconds
    while True:
        if probe():
            print(label, flush=True)
            return
        if time.monotonic() >= deadline:
            raise RuntimeError(f"Timed out after {seconds}s: {label}; see journey evidence")
        print(f"Waiting: {label}", flush=True)
        time.sleep(5)


def healthy():
    value = health()
    if not value or value.get("status") != "ok":
        return False
    try:
        discovery = json.loads((data_root() / "runtime" / "discovery.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return bool(value.get("runtime_instance_id") and
                value["runtime_instance_id"] == discovery.get("runtime_instance_id"))


def host_ready():
    value = health()
    if not value or value.get("status") != "ok":
        return False
    service = next((row for row in value.get("services", []) if row.get("name") == "pack-host"), {})
    ready_path = data_root() / "runtime" / "generic-host.ready.json"
    if service.get("state") != "running" or not ready_path.is_file():
        return False
    try:
        ready = json.loads(ready_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    save("pack-host-ready.json", ready)
    return (ready.get("status") == "ready" and bool(value.get("runtime_instance_id")) and
            ready.get("runtime_instance_id") == value["runtime_instance_id"])


def task():
    project = "windows-journey"
    created = json.loads(cli("astrid", ["projects", "create", project, "--name", "Windows journey", "--json"],
                             "project.json"))
    if created.get("ok") is not True:
        raise RuntimeError("Project creation failed")
    spec = {"capability_id": "chiptune.sfx", "kind": "executor", "inputs": {
        "kind": "blip", "variant": 1, "pitch": 0, "duration_s": 0.1}, "outputs": {}, "extra_pack_roots": []}
    admitted = json.loads(cli("astrid", ["tasks", "create", "--project", project, "--capability", "chiptune.sfx",
                              "--spec", json.dumps(spec), "--json"], "task-created.json"))
    if admitted.get("ok") is not True:
        raise RuntimeError("Task admission failed")
    task_id = admitted["data"]["task_id"]
    cli("astrid", ["tasks", "follow", task_id, "--project", project, "--poll-seconds", "2",
                   "--timeout-seconds", "900", "--json"], "task-follow.jsonl", timeout=960)
    settled = json.loads(cli("astrid", ["tasks", "show", task_id, "--project", project, "--json"], "task-settled.json"))
    row = settled.get("data") or {}
    outputs = {item.get("name"): item for item in (row.get("result") or {}).get("outputs", [])}
    if (settled.get("ok") is not True or row.get("state") != "succeeded" or
            not {"sfx", "sfx_meta"} <= outputs.keys() or any(
                not re.fullmatch(r"sha256:[0-9a-f]{64}", outputs[name].get("digest", "")) or
                outputs[name].get("size", 0) <= 0 for name in ("sfx", "sfx_meta"))):
        raise RuntimeError("Task did not settle successfully with outputs")


def process_key(row):
    return (row["pid"], row["created"])


def astrid_processes(rows, roots, tracked=()):
    roots = [ntpath.normcase(str(root)).rstrip("\\/") + "\\" for root in roots]
    selected = {process_key(row) for row in rows if process_key(row) in tracked or
                any(root in ntpath.normcase(row.get("exe") or "") or
                    root in ntpath.normcase(row.get("command") or "") for root in roots) or
                re.search(r"\b(?:astrid_runtime|runtime_protocol)\b|(?:^|\s)-m\s+astrid\b|"
                          r"\bastrid\.core\.execution\b|astrid-install-", row.get("command") or "")}
    by_pid = {row["pid"]: row for row in rows}
    while True:
        added = set()
        for row in rows:
            parent = by_pid.get(row["ppid"])
            if parent and parent["created"] <= row["created"] and process_key(parent) in selected:
                added.add(process_key(row))
        if added <= selected:
            return [row for row in rows if process_key(row) in selected]
        selected.update(added)


def snapshot(name):
    # There is no public enumeration of arbitrary Job handles. Track process
    # incarnations and descendants before down, including generic Job children.
    value = json.loads(powershell("""
$rows = @(Get-CimInstance Win32_Process | ForEach-Object {
    [pscustomobject]@{pid=[int]$_.ProcessId; ppid=[int]$_.ParentProcessId;
        created=$(if ($_.CreationDate) { $_.CreationDate.ToUniversalTime().ToString('o') } else { '' });
        exe=[string]$_.ExecutablePath; command=[string]$_.CommandLine}
})
ConvertTo-Json -InputObject @{collector_pid=$PID; processes=$rows} -Depth 4
""", name, show=False))
    rows = [row for row in value["processes"] if row["pid"] not in {os.getpid(), value["collector_pid"]}]
    tracked_file = EVIDENCE / "tracked-processes.json"
    tracked = json.loads(tracked_file.read_text(encoding="utf-8")) if tracked_file.exists() else []
    selected = astrid_processes(rows, [program_root(), data_root(), program_root().parent / "Astrid Installer"],
                               {process_key(row) for row in tracked})
    save("tracked-processes.json", list({process_key(row): row for row in tracked + selected}.values()))
    save(name, {"processes": rows, "astrid_processes": selected})
    return selected


def down():
    snapshot("processes-before-down.json")
    powershell("Get-ScheduledTask | Where-Object { $_.TaskName -eq 'Astrid Runtime' -and $_.TaskPath -eq '\\' } "
               "| Disable-ScheduledTask | Out-Null", "disable-scheduled-task.log")
    if (program_root() / "current").is_file():
        installed = version()
        cli("astrid_runtime", ["down", "--profile", "astrid", "--data-root", str(data_root()),
                              "--source-manifest", installed["profile"], "--json"], "down.json", timeout=900)
    else:
        print("No installed current version; checking for partial-install leftovers.")


def collect():
    logs = data_root() / "logs"
    errors = []
    for path in logs.glob("*.log"):
        try:
            shutil.copyfile(path, EVIDENCE / path.name)
        except OSError as exc:
            errors.append(f"{path.name}: {exc}")
    value = health()
    save("health-final.json", value or {"error": "Runtime health unavailable; see health-error.json"})
    if not (EVIDENCE / "health.json").exists():
        save("health.json", {"error": "Runtime never reported health; see health-error.json"})
    try:
        snapshot("processes-final.json")
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        errors.append(f"Process snapshot: {exc}")
    save("collection.json", {"errors": errors, "logs_found": sorted(path.name for path in logs.glob("*.log"))})
    if errors:
        raise RuntimeError("Evidence collection was incomplete; see collection.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=("install", "start", "health", "host", "task", "down", "stopped", "collect"))
    parser.add_argument("--installer-shell", choices=("powershell.exe", "pwsh.exe"))
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("This journey must run on Windows")
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if args.step == "install":
        if not args.installer_shell:
            parser.error("install requires --installer-shell")
        install(args.installer_shell)
    elif args.step == "start":
        powershell("Start-ScheduledTask -TaskName 'Astrid Runtime' -TaskPath '\\'", "start.log")
    elif args.step == "health":
        wait_for("Runtime health is ok and belongs to this installation", healthy)
    elif args.step == "host":
        wait_for("pack-host is running with its current ready file", host_ready)
        snapshot("processes-host-ready.json")
    elif args.step == "task":
        task()
    elif args.step == "down":
        down()
    elif args.step == "stopped":
        wait_for("No Astrid/Runtime processes remain", lambda: not snapshot("processes-after-down.json"), seconds=300)
    else:
        collect()


if __name__ == "__main__":
    main()
