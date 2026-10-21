"""GenericPackHost acceptance for the real Remotion render capability.

The test is intentionally opt-in through a provisioned dependency tree.  A
normal source checkout does not carry ``remotion/node_modules``; when the
tree is available, the test copies it into the temporary workspace so the
host's preflight and the Remotion CLI both see an owned runtime.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DEPENDENCY_ROOT = Path(
    os.environ.get(
        "ASTRID_TEST_REMOTION_DEPENDENCY_ROOT",
        str(ROOT.parent / "Astrid-beta-convergence" / "remotion" / "node_modules"),
    )
).expanduser()

if not DEPENDENCY_ROOT.is_dir():
    pytest.skip(
        "provisioned Remotion dependency root is unavailable; set "
        "ASTRID_TEST_REMOTION_DEPENDENCY_ROOT",
        allow_module_level=True,
    )

from astrid.core.execution.generic_host import (  # noqa: E402
    GenericPackHost,
    HostError,
    RuntimeProtocolClient,
)
from astrid.core.theme import builtin_theme  # noqa: E402
from astrid.packs.rendering.rendering.renderers.remotion.root_preparation import (  # noqa: E402
    _prepared_remotion_root,
)
from astrid.packs.rendering.shared.rendering_backend import (  # noqa: E402
    _resolved_theme_for_render,
)
from astrid.sdk.client import AstridClient  # noqa: E402
from astrid_runtime_client import WorkspaceClient  # noqa: E402

pytestmark = pytest.mark.integration  # needs the Runtime from a second checkout (real_runtime fixture)


def _make_media(root: Path) -> tuple[Path, Path]:
    media = root / "media"
    media.mkdir()
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=160x90:r=10:d=2",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(media / "black.mp4"),
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=48000:cl=stereo",
            "-t",
            "2",
            "-c:a",
            "aac",
            "-b:a",
            "64k",
            str(media / "silence.m4a"),
        ],
        check=True,
        capture_output=True,
    )
    black = (media / "black.mp4").read_bytes()
    silence = (media / "silence.m4a").read_bytes()
    (media / "assets.json").write_text(
        json.dumps(
            {
                "assets": {
                    "black": {
                        "media_id": "runtime-black",
                        "content_sha256": hashlib.sha256(black).hexdigest(),
                        "type": "video/mp4",
                        "duration": 2.0,
                        "resolution": "160x90",
                        "fps": 10,
                    },
                    "silence": {
                        "media_id": "runtime-silence",
                        "content_sha256": hashlib.sha256(silence).hexdigest(),
                        "type": "audio/mp4",
                        "duration": 2.0,
                    },
                }
            }
        ),
        encoding="utf-8",
    )
    timeline = {
        "theme": "banodoco-default",
        "theme_overrides": {
            "visual": {
                "canvas": {"width": 160, "height": 90, "fps": 10},
                "color": {"fg": "#ffffff", "bg": "#000000", "accent": "#ffffff"},
            }
        },
        "tracks": [
            {"id": "source", "kind": "visual", "label": "Source"},
            {"id": "audio", "kind": "audio", "label": "Audio"},
        ],
        "clips": [
            {
                "id": "source_black",
                "at": 0,
                "track": "source",
                "clipType": "media",
                "asset": "black",
                "from": 0,
                "to": 0.6,
                "speed": 1,
                "volume": 0,
            },
            {
                "id": "audio_silence",
                "at": 0,
                "track": "audio",
                "clipType": "media",
                "asset": "silence",
                "from": 0,
                "to": 0.6,
                "speed": 1,
                "volume": 1,
            },
        ],
    }
    timeline_path = media / "timeline.json"
    timeline_path.write_text(json.dumps(timeline))
    return timeline_path, media / "assets.json"


def _prepare_remotion_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path, Path, Path]:
    configured_node = os.environ.get("ASTRID_NODE_EXECUTABLE")
    node = Path(configured_node).expanduser() if configured_node else None
    if node is None:
        discovered_node = shutil.which("node")
        node = Path(discovered_node) if discovered_node else None
    if (
        node is None
        or not node.is_file()
        or not os.access(node, os.X_OK)
        or shutil.which("ffmpeg") is None
    ):
        pytest.skip("node and ffmpeg are required for the Remotion acceptance fixture")
    monkeypatch.setenv(
        "ASTRID_NODE_EXECUTABLE",
        configured_node if configured_node else str(node.resolve()),
    )

    schema_env = "ASTRID_TIMELINE_SCHEMA_PYTHONPATH"
    configured_schema = os.environ.get(schema_env)
    if configured_schema:
        schema_pythonpath = configured_schema
        schema_root = Path(configured_schema).expanduser()
    else:
        try:
            import banodoco_timeline_schema
        except ImportError as exc:
            pytest.fail(
                "the Remotion acceptance fixture needs the installed "
                "banodoco_timeline_schema package or "
                f"{schema_env}: {exc}"
            )
        schema_root = Path(banodoco_timeline_schema.__file__).parent.parent
        schema_pythonpath = str(schema_root)
        monkeypatch.setenv(schema_env, schema_pythonpath)
    if not (schema_root / "banodoco_timeline_schema" / "__init__.py").is_file():
        pytest.fail(
            f"{schema_env} does not contain the installed timeline schema: "
            f"{schema_pythonpath}"
        )

    caller_pythonpath = os.environ.get("PYTHONPATH")
    pythonpath = [str(ROOT), schema_pythonpath]
    if caller_pythonpath:
        pythonpath.append(caller_pythonpath)
    monkeypatch.setenv(
        "PYTHONPATH",
        os.pathsep.join(pythonpath),
    )

    workspace = tmp_path / "workspace"
    shutil.copytree(
        ROOT / "astrid",
        workspace / "astrid",
        symlinks=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    remotion = workspace / "remotion"
    shutil.copytree(
        ROOT / "remotion",
        remotion,
        ignore=shutil.ignore_patterns("node_modules"),
    )
    shutil.copytree(
        DEPENDENCY_ROOT,
        remotion / "node_modules",
        symlinks=True,
        copy_function=shutil.copy2,
    )
    monkeypatch.setenv("ASTRID_REMOTION_PROJECT_DIR", str(remotion.resolve()))
    pack_root = workspace / "astrid" / "packs"
    monkeypatch.setenv("ASTRID_PACKS_PATH", str(pack_root.resolve()))
    # The real host launch owns this validation.  Keep its artifact private to
    # the fixture instead of borrowing readiness from another Remotion root.
    for name in (
        "PYTHONUSERBASE",
        "PYTHONNOUSERSITE",
        "PYTHONSAFEPATH",
        "PYTHONPLATLIBDIR",
        "PYTHONCASEOK",
        "PYTHONUTF8",
        "PYTHONCOERCECLOCALE",
        "PYTHONSTARTUP",
        "PYTHONPYCACHEPREFIX",
        "PYTHONEXECUTABLE",
        "__PYVENV_LAUNCHER__",
        "PYTHONHOME",
        "NODE_OPTIONS",
        "NODE_PATH",
        "NODE_ICU_DATA",
        "OPENSSL_CONF",
    ):
        monkeypatch.delenv(name, raising=False)
    for name in tuple(os.environ):
        if name.startswith(("DYLD_", "LD_")):
            monkeypatch.delenv(name, raising=False)
    interactive_git = {
        "GIT_EDITOR",
        "GIT_SEQUENCE_EDITOR",
        "GIT_PAGER",
        "GIT_TERMINAL_PROMPT",
        "GIT_ASKPASS",
        "GIT_SSH",
        "GIT_SSH_COMMAND",
        "GIT_SSH_VARIANT",
        "GIT_MERGE_AUTOEDIT",
        "GIT_AUTHOR_NAME",
        "GIT_AUTHOR_EMAIL",
        "GIT_COMMITTER_NAME",
        "GIT_COMMITTER_EMAIL",
    }
    for name in tuple(os.environ):
        if name.startswith("GIT_") and name not in interactive_git:
            monkeypatch.delenv(name, raising=False)
    from astrid.sdk.host_bootstrap import _prepare_render_validation

    validation_env = dict(os.environ)
    _prepare_render_validation(
        ROOT,
        validation_env,
        tmp_path / "support",
        sys.executable,
        pack_roots=(pack_root,),
    )
    for name in (
        "ASTRID_REMOTION_VALIDATION_PATH",
        "ASTRID_REMOTION_VALIDATION_SHA256",
        "ASTRID_REMOTION_VALIDATION_LAUNCH",
        "ASTRID_REMOTION_VALIDATION_ROLE",
    ):
        monkeypatch.setenv(name, validation_env[name])
    timeline_path, assets_path = _make_media(workspace)
    return workspace, remotion, timeline_path, assets_path


def test_remotion_fixture_dependency_files_are_private(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The fixture copies dependency bytes without sharing source inodes."""
    _, remotion, _, _ = _prepare_remotion_fixture(tmp_path, monkeypatch)
    source_probe = DEPENDENCY_ROOT / ".package-lock.json"
    private_probe = remotion / "node_modules" / ".package-lock.json"
    source_bytes = source_probe.read_bytes()

    assert private_probe.read_bytes() == source_bytes
    assert private_probe.stat().st_ino != source_probe.stat().st_ino
    assert private_probe.stat().st_nlink == 1
    assert source_probe.read_bytes() == source_bytes


def test_generic_host_remotion_register_claim_execute_settle_and_cas(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, real_runtime
) -> None:
    workspace, remotion, timeline_path, assets_path = _prepare_remotion_fixture(
        tmp_path, monkeypatch
    )
    daemon = real_runtime(production_worker_credentials=True)
    try:
        generated = WorkspaceClient(daemon.endpoint, daemon.token)
        generated.handshake(
            "generic-remotion-acceptance",
            "0.1.0",
            [
                "projects:read",
                "projects:write",
                "objects:read",
                "objects:write",
                "tasks:read",
                "tasks:write",
            ],
        )
        project = generated.create_project(
            "Generic Remotion acceptance",
            slug="generic-remotion-acceptance",
            idempotency_key="generic-remotion-project",
        )
        project_id = str(project["project_id"])
        # The host owns the only path handoff. Import both sources into the
        # runtime, then replace the fixture's stable placeholders with the
        # returned runtime identities/digests before the task is admitted.
        registry = json.loads(assets_path.read_text(encoding="utf-8"))
        input_object_ids: list[str] = []
        for key, filename in (("black", "black.mp4"), ("silence", "silence.m4a")):
            imported = generated.ingest_project_object(
                project_id,
                (workspace / "media" / filename).read_bytes(),
                media_type=registry["assets"][key]["type"],
                idempotency_key=f"generic-remotion-{key}",
                filename=filename,
            )
            object_id = imported.get("object_id") if isinstance(imported, dict) else getattr(imported, "object_id", None)
            digest = imported.get("digest") if isinstance(imported, dict) else getattr(imported, "digest", None)
            assert isinstance(object_id, str) and isinstance(digest, str)
            input_object_ids.append(object_id)
            registry["assets"][key]["media_id"] = object_id
        registry["assets"][key]["content_sha256"] = digest.removeprefix("sha256:")
        assets_path.write_text(json.dumps(registry), encoding="utf-8")
        pack = workspace / "astrid" / "packs" / "rendering" / "executors" / "render"
        host = GenericPackHost(
            pack_roots=[pack],
            client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
            executor_id="astrid-pack-host",
            attempt_root=tmp_path / "attempt",
        )
        record = host.discover()[0]
        host.preflight(record.id)
        assert host.capabilities[record.id].ready is True

        registration = host.register()
        assert registration["registration"].executor_id == "astrid-pack-host"

        spec = {
            "inputs": {
                "timeline": str(timeline_path),
                "timeline_ref": "timeline-generic-remotion",
                "assets_registry": str(assets_path),
                "selector": "rendering.remotion",
                "backend_config": json.dumps(
                    {
                        "rendering.remotion": {
                            "project_dir": str(remotion),
                            "composition_id": "TimelineComposition",
                        }
                    }
                ),
                "output_name": "generic.mp4",
            }
        }
        task = generated.admit_task(
            capability_id=record.id,
            capability_digest=record.capability_digest,
            input_object_ids=input_object_ids,
            idempotency_key="generic-remotion-task",
            project_id=project_id,
            spec=spec,
        )
        claim = generated.claim_task(
            executor_id="astrid-pack-host",
            capability_ids=[record.id],
            idempotency_key="generic-remotion-claim",
            runtime_epoch=generated.health().runtime_epoch,
        )
        assert claim is not None and claim["task_id"] == task.task_id

        settled = host.run_task(
            {
                "task": {
                    "id": task.task_id,
                    "capability": record.id,
                    "spec": claim.spec,
                    "input_object_ids": claim.input_object_ids,
                    "project_id": claim.project_id,
                    "attempt_id": claim["attempt_id"],
                    "fence": claim["fence"],
                }
            },
            lease_token=claim["lease_id"],
            attempt_id=claim["attempt_id"],
            fence=int(claim["fence"]),
        )
        assert settled.state == "succeeded"
        assert generated.get_task(task.task_id).state == "succeeded"

        outputs_dir = tmp_path / "attempt" / "outputs"
        output = outputs_dir / "generic.mp4"
        provenance = outputs_dir / "generic.mp4.provenance.json"
        assert output.is_file() and output.stat().st_size > 0
        assert provenance.is_file() and provenance.stat().st_size > 0
        for path in (output, provenance):
            digest = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            assert generated.get_object(digest).data == path.read_bytes()
    finally:
        daemon.stop()


def test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, real_runtime
) -> None:
    """The documented SDK file-input route carries the imported theme to props."""
    import astrid.sdk as sdk

    workspace, remotion, timeline_path, assets_path = _prepare_remotion_fixture(
        tmp_path, monkeypatch
    )
    # The ordinary file caller cannot authorize assets named inside a registry.
    # Use the media-free title film from test_remotion_backend's real-render
    # fixture, without authored overrides that would mask the theme controls.
    timeline_path.write_text(
        json.dumps(
            {
                "theme": "banodoco-default",
                "tracks": [{"id": "v1", "kind": "visual", "label": "Title"}],
                "clips": [
                    {
                        "id": "title",
                        "at": 0.0,
                        "track": "v1",
                        "clipType": "text",
                        "hold": 0.5,
                        "text": {
                            "content": "Remotion ANGLE",
                            "fontSize": 64,
                            "color": "#ffffff",
                        },
                        "params": {"weight": 700},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    assets_path.write_text(json.dumps({"assets": {}}), encoding="utf-8")
    daemon = real_runtime(production_worker_credentials=True)
    try:
        generated = WorkspaceClient(daemon.endpoint, daemon.token)
        generated.handshake(
            "generic-remotion-theme-proof",
            "0.1.0",
            [
                "projects:read",
                "projects:write",
                "objects:read",
                "objects:write",
                "tasks:read",
                "tasks:write",
            ],
        )
        project = generated.create_project(
            "Generic Remotion theme proof",
            slug="generic-remotion-theme-proof",
            idempotency_key="generic-remotion-theme-project",
        )
        project_id = str(project["project_id"])

        owner = AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.credential_path,
            realm_id=daemon.service.realm["id"],
            actor_id="owner",
            client_name="generic-remotion-theme-proof-owner",
            client_version="test",
            protocol_version="workspace.v1",
        )
        explicit_theme = json.loads(json.dumps(builtin_theme()))
        explicit_theme["id"] = "imported-explicit-theme"
        explicit_theme["visual"]["color"] = {
            "fg": "#e8f1ff",
            "bg": "#26113d",
            "accent": "#ff8a3d",
        }
        theme_source = workspace / "media" / "explicit-theme.json"
        theme_source.write_text(json.dumps(explicit_theme), encoding="utf-8")
        timeline_import = owner.media.import_file(
            project=project_id,
            path=timeline_path,
            idempotency_key="generic-remotion-theme-timeline",
        )
        assert timeline_import.ok
        registry_import = owner.media.import_file(
            project=project_id,
            path=assets_path,
            idempotency_key="generic-remotion-theme-assets",
        )
        assert registry_import.ok
        imported = owner.media.import_file(
            project=project_id,
            path=theme_source,
            idempotency_key="generic-remotion-explicit-theme",
        )
        assert imported.ok
        descriptor = imported.data

        host = GenericPackHost(
            pack_roots=[workspace / "astrid" / "packs"],
            client=RuntimeProtocolClient(daemon.endpoint, daemon.worker_token),
            executor_id="astrid-theme-proof-host",
            attempt_root=tmp_path / "attempt",
        )
        record = next(item for item in host.discover() if item.id == "rendering.render")
        assert "theme" in {port.name for port in record.definition.inputs}
        host.preflight(record.id)
        assert host.capabilities[record.id].ready is True
        registration = host.register()
        assert registration["registration"].executor_id == "astrid-theme-proof-host"

        admissions = []
        create_task = owner.tasks.create

        def capture_admission(**request):
            response = create_task(**request)
            admissions.append((request, response))
            return response

        monkeypatch.setattr(owner.tasks, "create", capture_admission)
        result = sdk.invoke(
            "rendering.render",
            kind="executor",
            project=project_id,
            inputs={
                "timeline": {
                    "object_id": timeline_import.data["object_id"],
                    "digest": timeline_import.data["digest"],
                    "filename": "hype.timeline.json",
                },
                "assets_registry": {
                    "object_id": registry_import.data["object_id"],
                    "digest": registry_import.data["digest"],
                    "filename": "hype.assets.json",
                },
                "theme": {
                    "object_id": descriptor["object_id"],
                    "digest": descriptor["digest"],
                    "filename": "theme.json",
                },
                "selector": "rendering.remotion",
            },
            client=owner,
        )
        assert result.ok, result.to_dict()
        assert len(admissions) == 1
        request, response = admissions[0]
        assert response.ok
        task = generated.get_task(result.kernel_task_id)
        assert task.input_object_ids == request["input_manifest"]
        assert task.spec["inputs"] == request["spec"]["inputs"]
        print(
            json.dumps(
                {
                    "sdk_admission": request,
                    "admission_result": response.data,
                    "sdk_result": result.to_dict(),
                },
                default=str,
            )
        )
        attempt = tmp_path / "materialized-attempt"
        values = host._materialize_inputs(
            {"spec": task.spec, "input_object_ids": task.input_object_ids},
            attempt,
            file_input_names=frozenset(
                port.name for port in record.definition.inputs if port.type == "file"
            ),
        )
        materialized_theme = Path(values["theme"])
        assert materialized_theme == Path(values["materialized_objects"]["theme"])
        assert materialized_theme.name == "theme.json"
        assert materialized_theme.is_relative_to(attempt / "managed-objects")
        assert json.loads(materialized_theme.read_text(encoding="utf-8")) == explicit_theme

        staged_video = tmp_path / "prepared" / "unused.mp4"
        with _prepared_remotion_root(
            Path(values["timeline"]),
            Path(values["assets_registry"]),
            staged_video,
            provenance_out_path=staged_video,
            project_dir=remotion,
            composition_id="TimelineComposition",
            theme_path=materialized_theme,
            min_free_gb=None,
            materialized_root=Path(values["materialized_root"]),
            materialized_objects=values["materialized_objects"],
            staging_parent=tmp_path / "prepared",
            frame_numbers=(0,),
            frame_output_dir=tmp_path / "frames",
        ) as prepared:
            props = prepared[0]
            assert props["theme"]["id"] == explicit_theme["id"]
            assert props["theme"]["visual"]["color"] == explicit_theme["visual"]["color"]

        omitted = _resolved_theme_for_render(Path(values["timeline"]), None)
        builtin = builtin_theme()
        assert omitted == {"id": builtin["id"], "visual": builtin["visual"]}
        assert omitted["id"] != explicit_theme["id"]

        forged = tmp_path / "forged-theme.json"
        forged.write_text(json.dumps(explicit_theme), encoding="utf-8")
        forged_spec = {"spec": {"inputs": {**task.spec["inputs"], "theme": str(forged)}}}
        with pytest.raises(HostError, match="requires a managed Runtime object"):
            host._materialize_inputs(
                {**forged_spec, "input_object_ids": task.input_object_ids},
                tmp_path / "forged-attempt",
                file_input_names=frozenset(
                    port.name for port in record.definition.inputs if port.type == "file"
                ),
            )
    finally:
        daemon.stop()
