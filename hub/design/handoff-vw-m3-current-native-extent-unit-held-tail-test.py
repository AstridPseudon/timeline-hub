"""Bounded native layer windows retain the legacy render-clock positive.

This is deliberately a held regression test.  The fixture is a sparse layer
whose selected window is completely before the declared render tail.  Empty
layers and windows that merely have a gap are not represented here: those are
separate, pre-existing failures and are not evidence for this positive.
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

from astrid.core.rendering.contracts import (
    SCHEMA_VERSION,
    FrameWindow,
    RenderProfile,
    RenderRequest,
)
from astrid.core.rendering.service import RenderService
from astrid.core.timeline.duration import (
    timeline_duration_frames,
    timeline_render_duration_frames,
)
from astrid.packs.rendering.rendering.renderers.remotion import run as remotion

_EXTENT_KEY = "astrid_composition_duration_frames"
_ROOT = Path(__file__).resolve().parents[3]
_REMOTION_ROOT = _ROOT / "remotion"
_ROOT_TSX = _REMOTION_ROOT / "src" / "Root.tsx"
_DURATION_CHUNK = "chunk-SE4TPVLW.js"

_ROOT_PROBE = r"""
const fs = require('node:fs');
const assert = require('node:assert/strict');
const ts = require(process.argv[4]);

const [rootPath, durationPath, propsJSON] = process.argv.slice(1, 4);

function compile(filename, modules) {
  const code = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2020,
      jsx: ts.JsxEmit.ReactJSX,
      esModuleInterop: true,
    },
    fileName: filename,
  }).outputText;
  const module = {exports: {}};
  new Function('require', 'module', 'exports', code)(name => {
    assert.ok(name in modules, `Unexpected import: ${name}`);
    return modules[name];
  }, module, module.exports);
  return module.exports;
}

const duration = compile(durationPath, {});
const nil = () => null;
const Composition = () => null;
const Sequence = props => props.children;
const Video = () => null;
const modules = {
  'react/jsx-runtime': {
    Fragment: 'Fragment',
    jsx: (type, props) => ({type, props}),
    jsxs: (type, props) => ({type, props}),
  },
  remotion: {Composition, Sequence, useVideoConfig: () => ({fps: 30})},
  '@remotion/media': {Video},
  '@banodoco/timeline-composition': {
    ...duration,
    TimelineComposition: nil,
    DEFAULT_THEME: {},
  },
  './fonts': {FontProvider: nil},
  './ReviewOverlay': {ReviewOverlay: nil},
  './FrameDiagnostics': {FrameDiagnostics: nil},
  './BoundsProbe': {BoundsProbe: nil},
  './asset-source': {resolveInvocationAsset: file => file},
  './host-registries': {resolveHostRegistries: () => ({})},
};

function walk(node, visit) {
  if (Array.isArray(node)) return node.forEach(child => walk(child, visit));
  if (!node || typeof node !== 'object') return;
  visit(node);
  if (typeof node.type === 'function') walk(node.type(node.props), visit);
  else walk(node.props?.children, visit);
}

(async () => {
  const props = JSON.parse(propsJSON);
  const root = compile(rootPath, modules).Root();
  const compositions = root.props.children.filter(element => element.type === Composition);
  assert.equal(compositions.length, 2);
  const metadata = await Promise.all(
    compositions.map(element => element.props.calculateMetadata({props})),
  );
  assert.deepEqual(metadata[0], metadata[1]);
  const sequences = [];
  const videos = [];
  walk(compositions[0].props.component(props), element => {
    if (element.type === Sequence) sequences.push(element.props);
    if (element.type === Video) videos.push(element.props);
  });
  process.stdout.write(JSON.stringify({
    metadata: metadata[0],
    sequence: sequences[0] ?? null,
    video: videos[0] ?? null,
  }));
})().catch(error => {
  process.stdout.write(JSON.stringify({error: String(error && error.message || error)}));
  process.exitCode = 0;
});
"""


def _profile() -> RenderProfile:
    return RenderProfile(320, 180, (30, 1), (1, 90000), "h264", "yuv420p")


def _clock() -> dict[str, object]:
    return {
        "authored_duration_frames": 300,
        "render_duration_frames": 330,
        "tail": {
            "policy": "unmapped_excess_rendered_region",
            "source_asset": "tail",
            "start_frame": 300,
            "end_frame": 330,
            "source_start_frame": 300,
            "source_end_frame": 330,
        },
    }


def _timeline() -> dict[str, object]:
    return {
        "theme": "banodoco-default",
        "theme_overrides": {"visual": {"canvas": {"width": 320, "height": 180, "fps": 30}}},
        "tracks": [
            {"id": "bottom", "kind": "visual", "label": "Bottom"},
            {"id": "top", "kind": "visual", "label": "Top"},
        ],
        "clips": [
            {"id": "base", "track": "bottom", "asset": "base", "at": 0, "from": 0, "to": 10},
            # This clip covers the whole selected [0, 1s) window.  It is not
            # an empty layer or a gap: the bounded positive is explicit.
            {"id": "top", "track": "top", "asset": "base", "at": 0, "from": 0, "to": 1},
        ],
        "app": {"astrid_render_clock": _clock()},
    }


def _props(timeline: dict[str, object], *, extent: int | None = None) -> dict[str, object]:
    props: dict[str, object] = {
        "timeline": timeline,
        "assets": {"assets": {"base": {"file": "base.mp4"}, "tail": {"file": "tail.mp4"}}},
        "theme": {},
    }
    if extent is not None:
        props["astridCompositionDurationInFrames"] = extent
    return props


def _root_probe(tmp_path: Path, props: dict[str, object]) -> dict[str, object]:
    archive = _REMOTION_ROOT / "artifacts" / "banodoco-timeline-composition-0.0.12.tgz"
    duration_path = tmp_path / _DURATION_CHUNK
    extract = subprocess.run(
        ["tar", "-xOf", str(archive), f"package/dist/{_DURATION_CHUNK}"],
        check=True,
        capture_output=True,
    )
    duration_path.write_bytes(extract.stdout)
    node = shutil.which("node")
    assert node is not None, "Root callback probe requires Node"
    typescript = "/home/user/work/app/node_modules/typescript/lib/typescript.js"
    assert Path(typescript).is_file(), "Root callback probe requires TypeScript"
    completed = subprocess.run(
        [
            node,
            "-e",
            _ROOT_PROBE,
            str(_ROOT_TSX),
            str(duration_path),
            json.dumps(props),
            typescript,
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == "", completed.stderr
    return json.loads(completed.stdout)


def _segment(tmp_path: Path) -> tuple[RenderRequest, RenderRequest, dict[str, object]]:
    timeline_path = tmp_path / "timeline.json"
    raw = _timeline()
    timeline_path.write_text(json.dumps(raw), encoding="utf-8")
    window = FrameWindow(0, 30, (30, 1))
    request = RenderRequest(SCHEMA_VERSION, str(timeline_path), "out.mp4", window=window)
    adapted, _ = RenderService._segment_request(
        object.__new__(RenderService),
        request,
        candidate=SimpleNamespace(
            id="remotion",
            manifest=SimpleNamespace(capabilities={"supports_windows": True}),
        ),
        segment=SimpleNamespace(window=window, layer=SimpleNamespace(tracks=("top",), z=1)),
        index=0,
        workspace=tmp_path,
    )
    selected = remotion._serialize_timeline(Path(adapted.timeline_path))
    return request, adapted, selected


def test_fully_covered_pre_tail_layer_window_keeps_legacy_native_positive(tmp_path: Path) -> None:
    """The current filtered-native route must retain the old bounded positive.

    The legacy route is the frozen 2019d7e69 behavior: it slices this exact
    layer/window, clears the native window, and Root accepts the source-window
    metadata with a 30-frame composition.  The current route retains the
    original clock and uses native bounds, so it must accept the same request
    without treating the filtered clip extent as authored clock authority.
    """

    request, adapted, selected = _segment(tmp_path)
    raw = _timeline()
    assert timeline_duration_frames(raw, 30) == 300
    assert timeline_render_duration_frames(raw, 30) == 330
    assert timeline_duration_frames(selected, 30) == 30
    assert selected["app"]["astrid_render_clock"] == _clock()
    assert adapted.metadata[_EXTENT_KEY] == "330"
    assert adapted.window is request.window

    legacy = RenderService._window_timeline(raw, request.window, tracks=("top",))
    legacy.setdefault("metadata", {})["astrid_layer"] = {"z": 1, "alpha": True}
    assert legacy["clips"] == [
        {"id": "top_0_30", "track": "top", "asset": "base", "at": 0.0, "from": 0.0, "to": 1.0}
    ]
    assert timeline_duration_frames(legacy, 30) == 30
    assert remotion._native_window_argument(None, legacy, _profile()) is None
    legacy_tree = _root_probe(tmp_path, _props(legacy))
    assert legacy_tree["metadata"] == {
        "width": 320,
        "height": 180,
        "fps": 30,
        "durationInFrames": 30,
    }
    assert legacy_tree["sequence"]["from"] == 30
    assert legacy_tree["video"]["trimBefore"] == 300
    assert legacy_tree["video"]["trimAfter"] == 330

    # This is the held red assertion.  The current branch raises before it
    # can produce the equivalent absolute native request.
    native = remotion._native_window_argument(
        adapted.window,
        selected,
        _profile(),
        composition_duration_frames=remotion._composition_duration_from_request(adapted),
    )
    assert native == "--frames=0-29"


def test_fully_covered_pre_tail_root_callback_accepts_native_extent(tmp_path: Path) -> None:
    """Root's real callbacks must accept the service's original extent grant."""

    _, adapted, selected = _segment(tmp_path)
    tree = _root_probe(
        tmp_path,
        _props(selected, extent=remotion._composition_duration_from_request(adapted)),
    )
    # The selected clip covers the native request; the tail starts at the
    # exclusive end and therefore contributes no frames to [0, 30).
    assert tree.get("error") is None, tree
    assert tree["metadata"]["durationInFrames"] == 330
    assert tree["sequence"]["from"] == 30
    assert tree["video"]["trimBefore"] == 300
    assert tree["video"]["trimAfter"] == 330


def test_ordinary_full_tail_and_no_clock_controls_remain_distinct(tmp_path: Path) -> None:
    """The bounded regression does not broaden ordinary tail behavior."""

    raw = _timeline()
    ordinary = _root_probe(tmp_path, _props(raw))
    assert ordinary["metadata"]["durationInFrames"] == 330
    assert ordinary["sequence"]["from"] == 300
    assert ordinary["video"]["trimBefore"] == 300
    assert ordinary["video"]["trimAfter"] == 330

    no_clock = copy.deepcopy(raw)
    del no_clock["app"]
    no_tail = copy.deepcopy(_props(no_clock))
    no_tail["assets"] = {"assets": {"base": {"file": "base.mp4"}}}
    ordinary_no_tail = _root_probe(tmp_path, no_tail)
    assert ordinary_no_tail["metadata"]["durationInFrames"] == 300
    assert ordinary_no_tail["sequence"] is None
    assert ordinary_no_tail["video"] is None
