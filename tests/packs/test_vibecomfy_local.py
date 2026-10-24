from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from astrid.packs.vibecomfy.actions.run.run import _stage_managed_asset_manifest
from astrid.packs.vibecomfy.asset_manifest import read_archive
from astrid.packs.vibecomfy.local import pack_images, scan


class _ComfyHandler(BaseHTTPRequestHandler):
    base_dir: Path
    requested: list[str]

    def do_GET(self) -> None:
        self.requested.append(self.path)
        parsed = urlsplit(self.path)
        if parsed.path == "/system_stats":
            payload = {
                "system": {
                    "comfyui_version": "0.3.32",
                    "python_version": "3.11.8",
                    "embedded_python": False,
                    "argv": ["main.py", "--output-directory", str(self.base_dir / "renders")],
                },
                "devices": [],
            }
        elif parsed.path == "/internal/folder_paths":
            payload = {"custom_nodes": [str(self.base_dir / "custom_nodes")]}
        elif parsed.path == "/userdata":
            assert parse_qs(parsed.query) == {"dir": ["workflows"]}
            payload = ["portrait_flux.json", "nested/wan_i2v.json"]
        else:
            self.send_error(404)
            return
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return


def _server(tmp_path: Path) -> tuple[ThreadingHTTPServer, threading.Thread]:
    custom_nodes = tmp_path / "custom_nodes"
    (custom_nodes / "ComfyUI-Manager").mkdir(parents=True)
    (tmp_path / "venv" / "bin").mkdir(parents=True)
    (tmp_path / "venv" / "bin" / "python").touch()
    _ComfyHandler.base_dir = tmp_path
    _ComfyHandler.requested = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), _ComfyHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def test_scan_reports_local_comfyui_and_endpoint_data(tmp_path: Path) -> None:
    server, thread = _server(tmp_path)
    try:
        result = scan([server.server_address[1]])
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

    assert result["errors"] == []
    assert len(result["servers"]) == 1
    found = result["servers"][0]
    assert found == {
        "url": f"http://127.0.0.1:{server.server_address[1]}",
        "comfyui_version": "0.3.32",
        "python_version": "3.11.8",
        "embedded_python": False,
        "argv": ["main.py", "--output-directory", str(tmp_path / "renders")],
        "folder_paths": {"custom_nodes": [str(tmp_path / "custom_nodes")]},
        "base_dir": str(tmp_path),
        "output_dir": str(tmp_path / "renders"),
        "workflows": ["portrait_flux.json", "nested/wan_i2v.json"],
        "manager_present": True,
        "python": str(tmp_path / "venv" / "bin" / "python"),
    }
    assert _ComfyHandler.requested == [
        "/system_stats",
        "/internal/folder_paths",
        "/userdata?dir=workflows",
    ]


def test_scan_returns_errors_for_unavailable_ports() -> None:
    result = scan([1])
    assert result["servers"] == []
    assert result["errors"]
    assert result["errors"][0]["port"] == 1
    assert result["errors"][0]["endpoint"] == "/system_stats"


def test_pack_images_round_trips_through_manifest_and_run_staging(tmp_path: Path) -> None:
    image = tmp_path / "portrait.png"
    image.write_bytes(b"fake image bytes")
    archive_path = tmp_path / "managed-assets.zip"

    result = pack_images(str(archive_path), [str(image)])

    resolved = read_archive(archive_path)
    assert result == {"zip": str(archive_path), "names": [resolved.manifest["assets"][0]["member"].split("/")[-1]]}
    assert resolved.bindings["image_1"] == result["names"][0]
    output_root = tmp_path / "worker-output"
    staged = _stage_managed_asset_manifest(
        str(archive_path), readiness_profile=None, output_root=output_root
    )
    staged_file = output_root / "engine-input" / result["names"][0]
    assert staged.bindings["image_1"] == result["names"][0]
    assert staged_file.read_bytes() == image.read_bytes()


def test_pack_images_refuses_to_overwrite(tmp_path: Path) -> None:
    image = tmp_path / "still.png"
    image.write_bytes(b"image")
    output = tmp_path / "managed.zip"
    output.write_bytes(b"keep")

    try:
        pack_images(str(output), [str(image)])
    except FileExistsError:
        pass
    else:
        raise AssertionError("existing ZIP must not be overwritten")
    assert output.read_bytes() == b"keep"
