from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import tempfile
import types
from dataclasses import dataclass, field, replace
from pathlib import Path


REPO = "/home/user/peteromallet/astrid-agent"
TARGET = "0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6"


def committed_helper() -> str:
    return subprocess.check_output(
        ["git", "-C", REPO, "show", f"{TARGET}:astrid/core/rendering/window_inputs.py"],
        text=True,
    )


class ProtocolError(RuntimeError):
    pass


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")), encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Request:
    timeline_path: str
    metadata: dict[str, str] = field(default_factory=dict)
    window: object | None = None


@dataclass(frozen=True)
class Window:
    start_frame: int
    end_frame: int
    fps_rational: tuple[int, int]


@dataclass(frozen=True)
class Layer:
    tracks: tuple[str, ...]
    z: int


@dataclass(frozen=True)
class Segment:
    window: Window
    layer: Layer | None = None


@dataclass(frozen=True)
class Manifest:
    capabilities: dict[str, object]


@dataclass(frozen=True)
class Candidate:
    id: str
    manifest: Manifest


def install_stubs() -> None:
    atomic = types.ModuleType("astrid.core.foundation.atomic_io")
    atomic.write_json_atomic = write_json_atomic
    digest = types.ModuleType("astrid.core.foundation.hash")
    digest.sha256_file = sha256_file
    contracts = types.ModuleType("astrid.core.rendering.contracts")
    contracts.RenderRequest = Request
    contracts.RenderSegment = Segment
    errors = types.ModuleType("astrid.core.rendering.errors")

    def raise_protocol_error(**kwargs: object) -> None:
        raise ProtocolError(json.dumps(kwargs, sort_keys=True))

    errors.raise_protocol_error = raise_protocol_error
    registry = types.ModuleType("astrid.core.rendering.registry")
    registry.RenderingCandidate = Candidate

    timeline = types.ModuleType("astrid.core.timeline.banodoco_composer")
    duration = types.ModuleType("astrid.core.timeline.duration")

    class Timeline:
        def __init__(self, data: dict[str, object]):
            self.data = data

        @classmethod
        def from_json_data(cls, data: dict[str, object]) -> "Timeline":
            return cls(data)

        def for_render(self) -> "Timeline":
            return self

        def to_json_data(self) -> dict[str, object]:
            return self.data

    def timeline_render_duration_frames(data: dict[str, object], fps: float) -> int:
        return int(data["duration_frames"])

    timeline.Timeline = Timeline
    duration.timeline_render_duration_frames = timeline_render_duration_frames

    modules = {
        "astrid": types.ModuleType("astrid"),
        "astrid.core": types.ModuleType("astrid.core"),
        "astrid.core.foundation": types.ModuleType("astrid.core.foundation"),
        "astrid.core.rendering": types.ModuleType("astrid.core.rendering"),
        "astrid.core.timeline": types.ModuleType("astrid.core.timeline"),
        "astrid.core.foundation.atomic_io": atomic,
        "astrid.core.foundation.hash": digest,
        "astrid.core.rendering.contracts": contracts,
        "astrid.core.rendering.errors": errors,
        "astrid.core.rendering.registry": registry,
        "astrid.core.timeline.banodoco_composer": timeline,
        "astrid.core.timeline.duration": duration,
    }
    import sys

    sys.modules.update(modules)


def load_materializer():
    tree = ast.parse(committed_helper())
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    module = ast.Module(body=[function], type_ignores=[])
    namespace = {
        "Any": object,
        "Mapping": dict,
        "Path": Path,
        "Callable": object,
        "replace": replace,
        "json": json,
        "write_json_atomic": write_json_atomic,
        "sha256_file": sha256_file,
        "raise_protocol_error": lambda **kwargs: (_ for _ in ()).throw(ProtocolError(kwargs)),
    }
    exec(compile(module, "window_inputs.py", "exec"), namespace)
    return namespace[function.name]


def main() -> None:
    install_stubs()
    materialize = load_materializer()
    with tempfile.TemporaryDirectory(prefix="timeline-window-review-") as raw:
        root = Path(raw)
        source = root / "timeline.json"
        source_data = {
            "duration_frames": 300,
            "tracks": [{"id": "a"}, {"id": "b"}],
            "clips": [{"id": "a1", "track": "a", "from": 0, "to": 4}],
            "metadata": {"keep": "yes", "astrid_layer": "old"},
        }
        source.write_text(json.dumps(source_data), encoding="utf-8")
        window = Window(63, 65, (30_000, 1_001))

        # Native no-layer path: no materialization, no hook, stale extent stripped.
        hook_calls: list[object] = []
        native = materialize(
            Request(str(source), {"astrid_composition_duration_frames": "99", "x": "1"}),
            candidate=Candidate("native.renderer", Manifest({"supports_windows": True})),
            segment=Segment(window), index=0, workspace=root,
            slice_timeline=lambda *args, **kwargs: hook_calls.append((args, kwargs)),
        )
        assert native[0].timeline_path == str(source)
        assert native[0].metadata == {"x": "1"}
        assert native[1] == {}
        assert hook_calls == []

        # Native layer path: Root-like extent comes from the unfiltered source,
        # then only the requested tracks are materialized and alpha is stamped.
        native_layer = materialize(
            Request(str(source), {"astrid_composition_duration_frames": "99"}, window),
            candidate=Candidate("native.renderer", Manifest({"supports_windows": True})),
            segment=Segment(window, Layer(("a",), 1)), index=1, workspace=root,
            slice_timeline=lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("native layer sliced")),
        )
        materialized = json.loads(Path(native_layer[0].timeline_path).read_text())
        assert native_layer[0].metadata["astrid_composition_duration_frames"] == "300"
        assert native_layer[0].window == window
        assert [track["id"] for track in materialized["tracks"]] == ["a"]
        assert materialized["clips"][0]["id"] == "a1"
        assert materialized["metadata"]["astrid_layer"] == {"z": 1, "alpha": True}
        assert source_data == json.loads(source.read_text())
        assert native_layer[1]["materialized_timeline"] == sha256_file(Path(native_layer[0].timeline_path))

        # Legacy path: the service-owned hook receives the exact window/track
        # selection, and the helper clears the renderer window.
        def slice_hook(data: dict[str, object], got_window: Window, *, tracks: tuple[str, ...] | None):
            hook_calls.append((got_window, tracks))
            return {"tracks": [{"id": "a"}], "clips": [], "metadata": {"source": "slice"}}

        legacy = materialize(
            Request(str(source), {"x": "1"}),
            candidate=Candidate("legacy.renderer", Manifest({"supports_windows": False})),
            segment=Segment(window, Layer(("a",), 0)), index=2, workspace=root,
            slice_timeline=slice_hook,
        )
        legacy_data = json.loads(Path(legacy[0].timeline_path).read_text())
        assert legacy[0].window is None
        assert hook_calls[-1] == (window, ("a",))
        assert legacy_data["metadata"]["astrid_layer"] == {"z": 0, "alpha": False}

        # Malformed and non-object source errors remain structured and do not
        # invoke the hook.
        bad = root / "bad.json"
        bad.write_text("[]", encoding="utf-8")
        try:
            materialize(
                Request(str(bad)), candidate=Candidate("legacy.renderer", Manifest({})),
                segment=Segment(window, Layer(("a",), 0)), index=3, workspace=root, slice_timeline=slice_hook,
            )
        except ProtocolError as exc:
            assert "non-object timeline" in str(exc)
        else:
            raise AssertionError("non-object timeline was accepted")

    print("PASS tiny committed-source window_inputs harness: native/no-layer, native/layer extent+alpha, legacy hook+clear, immutability/hash, structured error")


if __name__ == "__main__":
    main()
