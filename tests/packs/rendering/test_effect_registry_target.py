"""Generation is confined to the selected host, including with an installed package."""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_generator_targets_host_and_leaves_installed_package_unchanged(tmp_path):
    installed = tmp_path / "node_modules/@banodoco/timeline-composition/dist"
    installed.mkdir(parents=True)
    sentinel = installed / "effects.generated.js"
    sentinel.write_text("immutable package\n")
    env = {**os.environ, "ASTRID_REMOTION_PROJECT_DIR": str(tmp_path),
           "ASTRID_TIMELINE_COMPOSITION_SRC": str(installed)}
    subprocess.run([sys.executable, str(ROOT / "scripts/gen_effect_registry.py")],
                   env=env, capture_output=True, text=True, check=True)
    for kind in ("effects", "animations", "transitions"):
        assert (tmp_path / "src" / f"{kind}.generated.ts").is_file()
    assert list(installed.iterdir()) == [sentinel]
    assert sentinel.read_text() == "immutable package\n"


def test_generator_refuses_host_staging_linked_into_installed_package(tmp_path):
    installed = tmp_path / "node_modules/@banodoco/timeline-composition/dist"
    installed.mkdir(parents=True)
    (tmp_path / "src").symlink_to(installed, target_is_directory=True)
    result = subprocess.run([sys.executable, str(ROOT / "scripts/gen_effect_registry.py")],
                            env={**os.environ, "ASTRID_REMOTION_PROJECT_DIR": str(tmp_path)},
                            capture_output=True, text=True)
    assert result.returncode != 0
    assert "outside installed packages" in result.stderr
    assert list(installed.iterdir()) == []
