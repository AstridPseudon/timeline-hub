"""One direct public13 positive for explicit runtime theme resolution."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from astrid.core.theme import builtin_theme
from astrid.packs.rendering.rendering.renderers.remotion import run


pytestmark = pytest.mark.integration


NORMAL_COMPONENT_SCRIPT = r"""
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import path from 'node:path';
import {TimelineComposition} from '@banodoco/timeline-composition';
import {resolveElementRegistries} from '@banodoco/timeline-composition/registries';
import {createElement as h} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals} from 'remotion';

const packageJson = JSON.parse(readFileSync(
  path.join(process.cwd(), 'node_modules/@banodoco/timeline-composition/package.json'), 'utf8'));
assert.equal(packageJson.version, '0.0.13');
const props = JSON.parse(readFileSync(process.argv[1], 'utf8'));
const theme = props.theme;
assert.equal(theme.id, 'custom-runtime-theme');
assert.deepEqual(theme.visual.color, {
  fg: '#f0ead6', bg: '#102030', accent: '#ff4d6d',
});
assert.deepEqual(theme.visual.type.families, {
  heading: 'Custom Heading', body: 'Custom Body', mono: 'Custom Mono',
});
assert.deepEqual(theme.visual.canvas, {width: 1280, height: 1080, fps: 30});

// The normal component receives the actual custom theme while the built-in
// public13 element registry remains an explicit render input.
const registries = resolveElementRegistries({id: '2rp'});
assert.ok(registries.effects['art-card']);
const metadata = {
  id: 'theme-positive', component: TimelineComposition, defaultProps: {},
  width: 1280, height: 1080, fps: 30, durationInFrames: 30,
  folderName: null, parentFolderName: null, nonce: [], schema: null,
  calculateMetadata: null, stack: null,
};
const html = renderToStaticMarkup(h(
  Internals.CompositionManager.Provider,
  {value: {
    compositions: [metadata], currentCompositionMetadata: null, folders: [],
    canvasContent: {type: 'composition', compositionId: 'theme-positive'},
  }},
  h(Internals.TimelineContext.Provider, {
    value: {
      frame: {'theme-positive': 0}, playing: false,
      imperativePlaying: {current: false}, audioAndVideoTags: {current: []},
    },
  }, h(Internals.CanUseRemotionHooksProvider, null,
    h(TimelineComposition, {...props, registries}))),
));
for (const value of [
  '#102030', '#f0ead6', '#ff4d6d', 'Custom Heading', 'Custom Body', 'Custom Mono',
]) {
  assert.ok(html.includes(value), `normal component omitted ${value}`);
}
"""


def _qualified_public13_runtime() -> tuple[Path, Path]:
    manifest_path = Path(os.environ["ASTRID_PUBLIC13_HOST_MANIFEST"]).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    declared = manifest["env"]
    project = Path(declared["ASTRID_REMOTION_PROJECT_DIR"]).resolve()
    node = Path(declared["ASTRID_NODE_EXECUTABLE"]).resolve()
    assert Path(os.environ["ASTRID_REMOTION_PROJECT_DIR"]).resolve() == project
    assert Path(os.environ["ASTRID_NODE_EXECUTABLE"]).resolve() == node
    assert project.is_dir() and project == Path(declared["ASTRID_REMOTION_PROJECT_DIR"])
    assert node.is_file() and node == Path(declared["ASTRID_NODE_EXECUTABLE"])
    package = project / "node_modules/@banodoco/timeline-composition/package.json"
    assert package.is_file()
    assert json.loads(package.read_text(encoding="utf-8"))["version"] == "0.0.13"
    assert str(project / "node_modules") == str((project / "node_modules").resolve())
    return project, node


def test_public13_normal_component_keeps_custom_runtime_theme_through_prepared_root(
    tmp_path, monkeypatch
):
    """The real prepared Root props reach the pinned public13 normal component unchanged."""
    project, node = _qualified_public13_runtime()
    assert subprocess.run([str(node), "--version"], cwd=project, check=True,
                          capture_output=True, text=True).stdout.strip() == "v20.19.4"

    theme = builtin_theme()
    theme["id"] = "custom-runtime-theme"
    theme["visual"]["color"] = {"fg": "#f0ead6", "bg": "#102030", "accent": "#9b5de5"}
    theme["visual"]["type"]["families"] = {
        "heading": "Custom Heading", "body": "Custom Body", "mono": "Custom Mono",
    }
    theme_path = tmp_path / "theme.json"
    theme_path.write_text(json.dumps(theme), encoding="utf-8")
    timeline = {
        "theme": "stale-authored-slug",
        "theme_overrides": {
            "visual": {
                "color": {"accent": "#ff4d6d"},
                "canvas": {"width": 1280},
            },
        },
        "tracks": [{"id": "v", "kind": "visual", "label": "Visual"}],
        "clips": [{
            "id": "title", "track": "v", "clipType": "art-card", "at": 0, "hold": 1,
            "params": {"title": "Theme proof", "caption": "Caption", "credit": "Credit"},
        }],
    }
    timeline_path = tmp_path / "timeline.json"
    timeline_path.write_text(json.dumps(timeline), encoding="utf-8")
    assets_path = tmp_path / "assets.json"
    assets_path.write_text(json.dumps({"assets": {}}), encoding="utf-8")

    monkeypatch.setattr(run, "_validate_project_dir", lambda _: SimpleNamespace(
        node_executable=node, remotion_cli=project / "node_modules/.bin/remotion",
        node_version="v20.19.4",
    ))
    monkeypatch.setattr(run, "_regenerate_element_registries", lambda *args: None)
    monkeypatch.setattr(run, "_validate_renderer_effect_registry", lambda *args: None)
    monkeypatch.setattr(run, "_effective_registry_state", lambda *args: {})
    monkeypatch.setattr(run, "_available_remotion_port", lambda: 32101)
    monkeypatch.setattr(run, "_stage_effect_assets_for_timeline", lambda *args, **kwargs: {})

    staged_video = tmp_path / "capture" / "unused.mp4"
    with run._prepared_remotion_root(
        timeline_path,
        assets_path,
        staged_video,
        provenance_out_path=staged_video,
        project_dir=project,
        composition_id=run.DEFAULT_COMPOSITION_ID,
        theme_path=theme_path,
        min_free_gb=None,
        staging_parent=tmp_path / "staging",
        frame_numbers=(0,),
        frame_output_dir=tmp_path / "frames",
    ) as prepared:
        props, props_path = prepared[:2]
        expected = {
            **theme,
            "visual": {
                **theme["visual"],
                "color": {**theme["visual"]["color"], "accent": "#ff4d6d"},
                "canvas": {**theme["visual"]["canvas"], "width": 1280},
            },
        }
        assert props["theme"] == expected
        assert props["theme"]["visual"]["color"]["bg"] == "#102030"
        assert props["theme"]["visual"]["type"]["families"] == theme["visual"]["type"]["families"]
        subprocess.run([str(node), "--input-type=module", "-e", NORMAL_COMPONENT_SCRIPT,
                        str(props_path)], cwd=project, check=True, capture_output=True, text=True,
                       timeout=30)
