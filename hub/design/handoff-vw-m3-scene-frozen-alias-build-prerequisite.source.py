#!/usr/bin/env python3
"""Run the bounded live Scene-only managed-carrier proof in a private graph."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
from pathlib import Path

RUNTIME_PIN = Path("/home/user/work/wt/rt-pin-2c4ac180")
RUNTIME_SHA = "2c4ac180c2220bdad966bc01e95ad230e99ce26a"
NODE_PIN = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node"
)
PEERS = Path("/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules")
NODE_SHA256 = "43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490"
PUBLIC13_NAME = "banodoco-timeline-composition-0.0.13.tgz"
PUBLIC13_SHA256 = "9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738"
PUBLIC13_FILES = 77
WORKER_ARTIFACT = Path(
    "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/"
    "scratchpad/orch/workers/vw-m3-scene-posthandoff-real-binding-cause/proof/scene-only-public13-bundle.zip"
)


def _sha256(path: Path) -> str:
    import hashlib
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require(path: Path, *, directory=False) -> Path:
    resolved = path.resolve(strict=False)
    if not (resolved.is_dir() if directory else resolved.is_file()):
        raise RuntimeError(f"required {'directory' if directory else 'file'} is unavailable: {path}")
    return resolved


def _private(path: Path, *shared: Path) -> None:
    if path.is_symlink():
        raise RuntimeError(f"private path is a symlink: {path}")
    resolved = path.resolve(strict=False)
    for candidate in shared:
        root = candidate.resolve(strict=True)
        if resolved == root or root in resolved.parents:
            raise RuntimeError(f"private path resolves into shared input: {resolved}")


def _apply_private_sdk_scene_patch(payload: bytes) -> bytes:
    """Apply the qualified owner SDK patch only to the private proof graph."""
    source = payload.decode("utf-8")

    def replace(old: str, new: str) -> None:
        nonlocal source
        if source.count(old) != 1:
            raise RuntimeError("qualified SDK owner patch no longer matches SDK9b")
        source = source.replace(old, new, 1)

    replace(
        '''    if not all(isinstance(context.get(key), str) and context[key] for key in (\n'''
        '''        "video_digest", "video_object_id", "managed_object_reference", "capture_identity",\n'''
        '''    )):\n'''
        '''        return None\n''',
        '''    if snapshot.get("video_digest") != capture_identity:\n'''
        '''        return None\n''',
    )
    replace(
        '''        "video_digest": context["video_digest"],\n'''
        '''        "video_object_id": context["video_object_id"],\n'''
        '''        "managed_object_reference": context["managed_object_reference"],\n''',
        "",
    )
    replace(
        '''    candidates = [\n'''
        '''        getattr(result, "outputs", None),\n'''
        '''        getattr(result, "raw_result", None),\n'''
        '''        result if isinstance(result, Mapping) else None,\n'''
        '''    ]\n''',
        '''    outputs = getattr(result, "outputs", None)\n'''
        '''    candidates = [outputs] if isinstance(outputs, Mapping) and outputs else [\n'''
        '''        getattr(result, "raw_result", None),\n'''
        '''        result if isinstance(result, Mapping) else None,\n'''
        '''    ]\n''',
    )
    replace(
        '            scene_name = entrypoints.get("scene_answers") if isinstance(entrypoints, Mapping) else None',
        '            scene_name = entrypoints.get("scene") if isinstance(entrypoints, Mapping) else None',
    )
    replace(
        '''    invoke_result = getattr(client, "invoke_result", None)\n'''
        '''    if not callable(invoke_result):\n'''
        '''        return _scene_only_unavailable(context, reason="managed visualization invocation unavailable"), context\n'''
        '''    result = invoke_result(\n'''
        '''        "rendering.timeline_visualize", kind="executor", project=project,\n'''
        '''        inputs=request, wait=True, read_managed_outputs=True,\n'''
        '''    )\n''',
        '''    from astrid.sdk.invocation import _invoke_internal_result\n'''
        '''\n'''
        '''    result = _invoke_internal_result(\n'''
        '''        "rendering.timeline_visualize", kind="executor", project=project,\n'''
        '''        inputs=request, client=client, wait=True, read_managed_outputs=True,\n'''
        '''    )\n''',
    )
    replace('        "include_media": True,', '        "include_media": False,')
    return source.encode("utf-8")


def _apply_private_executor_source_patch(payload: bytes) -> bytes:
    """Carry the already-minted source into private executor children.

    The current owner correction belongs in the core host.  This wrapper keeps
    the central proof graph private until that correction lands there.
    """
    source = payload.decode("utf-8")
    marker = '''                        allow_runtime_connection=not private_runtime_context)\n                    try:\n'''
    replacement = '''                        allow_runtime_connection=not private_runtime_context)\n                    from astrid.core.rendering.verified_source import PreparedTimelineInputs\n                    PreparedTimelineInputs.handoff_source(inputs, worker_env)\n                    try:\n'''
    if source.count(marker) != 1:
        raise RuntimeError("executor source handoff patch target is ambiguous")
    return source.replace(marker, replacement, 1).encode("utf-8")


def _apply_private_registry_digest_patch(payload: bytes) -> bytes:
    """Retain the verified CAS digest in the derived, attempt-local registry."""
    source = payload.decode("utf-8")
    old = '                entry = dict(raw)\n                entry["file"] = str(destination)\n'
    new = '                entry = dict(raw)\n                entry.setdefault("digest", digest_hex)\n                entry["file"] = str(destination)\n'
    if source.count(old) != 1:
        raise RuntimeError("derived registry digest patch target is ambiguous")
    return source.replace(old, new, 1).encode("utf-8")


def _source_binding_regression(repo: Path) -> None:
    """Reproduce the missing derived digest and retain the strict child checks."""
    import yaml

    declaration = yaml.safe_load((repo / "astrid/packs/rendering/pack.yaml").read_text())
    action = declaration["actions"]["timeline_visualize"]
    if action["invocation"]["kind"] != "command":
        raise RuntimeError("visualization no longer uses the command dispatch branch")
    WORKER_ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        sys.executable, "-B", "-m", "pytest", "-q", "-o", "addopts=",
        "-p", "no:cacheprovider", "--basetemp=" + str(WORKER_ARTIFACT.parent / "regression"),
        "tests/packs/rendering/test_scene_private_registry_handoff.py",
    ], cwd=repo, env={**os.environ, "ASTRID_RUNTIME_CHECKOUT": str(RUNTIME_PIN)}, check=True)


def _overlay(repo: Path, stage: Path) -> Path:
    overlay = stage / "agent-overlay"
    shutil.copytree(
        repo, overlay,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "node_modules"),
        symlinks=False,
    )
    for reference, relative in (
        ("9b887e232", "astrid/sdk/timeline_filmstrip.py"),
        ("23db420c1", "astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py"),
    ):
        payload = subprocess.check_output(["git", "-C", str(repo), "show", f"{reference}:{relative}"])
        if relative == "astrid/sdk/timeline_filmstrip.py":
            payload = _apply_private_sdk_scene_patch(payload)
        target = overlay / relative
        target.write_bytes(payload)
    executor = overlay / "astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py"
    executor_source = executor.read_text(encoding="utf-8")
    old = "    except (SceneQueryUnavailable, OSError, TypeError, ValueError, KeyError):\n"
    new = "    except (SceneQueryUnavailable, OSError, TypeError, ValueError, KeyError) as exc:\n"
    new += f"        Path({str(WORKER_ARTIFACT.parent / 'executor-failure.json')!r}).write_text(json.dumps({{'type': type(exc).__name__, 'reason': str(exc)}}))\n"
    if executor_source.count(old) != 1:
        raise RuntimeError("private exception probe no longer matches executor23db")
    executor_source = executor_source.replace(old, new, 1)
    old = "        source.validate_snapshot(snapshot)\n        bound = source.read()\n"
    new = "        source.validate_snapshot(snapshot)\n        bound = source.read()\n"
    new += "        from astrid.core.rendering.verified_source import VerifiedTimelineSource, SOURCE_ENV\n"
    new += f"        Path({str(WORKER_ARTIFACT.parent / 'child-source')!r} + '-' + bound['ref']['source_kind'] + '.json').write_text(json.dumps({{'type_exact': type(source) is VerifiedTimelineSource, 'source_module': __import__('inspect').getfile(type(source)), 'source_sha256': hashlib.sha256(Path(__import__('inspect').getfile(type(source))).read_bytes()).hexdigest(), 'executor_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'executor_file': __file__, 'source_env': os.environ.get(SOURCE_ENV), 'binding': bound, 'snapshot': snapshot}}, sort_keys=True))\n"
    if executor_source.count(old) != 1:
        raise RuntimeError("private source probe no longer matches executor23db")
    executor_source = executor_source.replace(old, new, 1)
    old = "        label = snapshot_label(bound_snapshot, source=source)\n"
    new = old + "        source.validate(timeline_path, assets_path)\n"
    new += f"        Path({str(WORKER_ARTIFACT.parent / 'child-postquery')!r} + '-' + bound['ref']['source_kind'] + '.json').write_text(json.dumps({{'source_still_valid': True, 'ref': bound['ref'], 'provenance': {{'video_digest': capture_identity, 'timeline_id': source_timeline_id}}, 'frames': len(answers)}}))\n"
    if executor_source.count(old) != 1:
        raise RuntimeError("private lifetime probe no longer matches executor23db")
    executor.write_text(executor_source.replace(old, new, 1), encoding="utf-8")
    generic_host = overlay / "astrid/core/execution/generic_host.py"
    generic_host.write_bytes(_apply_private_registry_digest_patch(
        _apply_private_executor_source_patch(generic_host.read_bytes())))
    return overlay


def _project(repo: Path, stage: Path) -> Path:
    # Keep the normal checkout layout: native aliases discover built-in pack
    # resources beside remotion, just as the Python registry generator does.
    project = repo / "remotion"
    modules = project / "node_modules"
    _private(modules, PEERS)
    # The source graph is read-only. Materialize it inside the owned project so
    # the production Remotion validator never follows a directory link back to
    # the shared checkout (leaf links inside the copied graph remain inert).
    shutil.copytree(PEERS, modules, symlinks=False)
    scope = modules / "@banodoco"
    _private(scope, PEERS)
    if scope.exists():
        shutil.rmtree(scope)
    scope.mkdir()
    artifact = _require(repo / "remotion" / "artifacts" / PUBLIC13_NAME)
    if _sha256(artifact) != PUBLIC13_SHA256:
        raise RuntimeError("public13 archive hash mismatch")
    extracted = stage / "public13"
    _private(extracted, PEERS)
    extracted.mkdir()
    with tarfile.open(artifact) as archive:
        archive.extractall(extracted, filter="data")
    package = extracted / "package"
    destination = scope / "timeline-composition"
    _private(destination, PEERS)
    package.rename(destination)
    files = [path for path in destination.rglob("*") if path.is_file()]
    if len(files) != PUBLIC13_FILES:
        raise RuntimeError(f"public13 file count mismatch: {len(files)}")
    if modules.resolve() != modules:
        raise RuntimeError("private node_modules root is not real")
    return project


def _environment(overlay: Path, runtime: Path, project: Path) -> dict[str, str]:
    env = {
        key: value for key, value in os.environ.items()
        if key not in {"NODE_OPTIONS", "NODE_PATH", "PYTHONPATH", "PYTHONPYCACHEPREFIX"}
        and not key.startswith("GIT_")
    }
    env.update({
        "PYTHONPATH": os.pathsep.join((str(overlay), str(runtime))),
        "ASTRID_RUNTIME_CHECKOUT": str(runtime),
        "ASTRID_NODE_EXECUTABLE": str(NODE_PIN),
        "ASTRID_REMOTION_PROJECT_DIR": str(project),
        "ASTRID_TIMELINE_SCHEMA_PYTHONPATH": sysconfig.get_paths()["purelib"],
        "ASTRID_SCENE_PROOF_ARTIFACT": str(WORKER_ARTIFACT),
        "PATH": os.pathsep.join((str(NODE_PIN.parent), env.get("PATH", ""))),
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    return env


def _bundle_preflight(overlay: Path, project: Path, env: dict[str, str], stage: Path) -> dict[str, object]:
    """Qualify the private generated registry/source graph before managed work."""
    generator = overlay / "scripts" / "gen_effect_registry.py"
    subprocess.run(
        [sys.executable, "-B", str(generator)],
        cwd=overlay,
        env=env,
        capture_output=True,
        check=True,
        text=True,
    )

    # Resolve every normal generator import through the exact native alias
    # implementation.  This catches a detached remotion/ root before the
    # renderer can turn all generated animation imports into UNAVAILABLE.
    alias_probe = r"""
import fs from 'node:fs';
import path from 'node:path';
import {remotionPrimitiveAliasesFor} from './webpack-alias.mjs';

const project = process.cwd();
const aliases = remotionPrimitiveAliasesFor(project)({}).resolve.alias;
const imports = [];
for (const name of ['effects', 'animations', 'transitions']) {
  const source = fs.readFileSync(path.join(project, 'src', `${name}.generated.ts`), 'utf8');
  for (const match of source.matchAll(/from '([^']+)'/g)) {
    if (match[1].startsWith('@pack-')) imports.push({name, specifier: match[1]});
  }
}
const resolved = imports.map(({name, specifier}) => {
  const alias = Object.keys(aliases).find(key => specifier === key || specifier.startsWith(`${key}/`));
  if (!alias) throw new Error(`${name}: no alias for ${specifier}`);
  const suffix = specifier.slice(alias.length).split('?')[0];
  const target = path.join(aliases[alias], suffix);
  const resolvedTarget = [target, ...['.ts', '.tsx', '.js', '.jsx'].map(extension => `${target}${extension}`)]
    .find(candidate => fs.existsSync(candidate) && fs.statSync(candidate).isFile());
  if (!resolvedTarget) throw new Error(`${name}: missing ${target}`);
  return {name, specifier, alias, target: resolvedTarget};
});
process.stdout.write(JSON.stringify({aliases, imports: resolved}));
"""
    aliases = subprocess.run(
        [str(NODE_PIN), "--input-type=module", "-e", alias_probe],
        cwd=project,
        env=env,
        capture_output=True,
        check=True,
        text=True,
    )
    alias_result = json.loads(aliases.stdout)

    # The private copy intentionally dereferences shared install symlinks;
    # invoke TypeScript from its real package path, not the copied .bin shim.
    tsc = project / "node_modules" / "typescript" / "bin" / "tsc"
    subprocess.run(
        [str(NODE_PIN), str(tsc), "--noEmit"],
        cwd=project,
        env=env,
        capture_output=True,
        check=True,
        text=True,
    )
    bundle = stage / "bundle-preflight"
    cli = project / "node_modules" / "@remotion" / "cli" / "remotion-cli.js"
    subprocess.run(
        [str(NODE_PIN), str(cli), "bundle", "src/index.ts", "--out-dir", str(bundle), "--bundle-cache=false"],
        cwd=project,
        env=env,
        capture_output=True,
        check=True,
        text=True,
    )
    return {
        "generated_imports": len(alias_result["imports"]),
        "resolved_aliases": sorted(alias_result["aliases"]),
        "typecheck": "passed",
        "bundle_files": sum(path.is_file() for path in bundle.rglob("*")),
    }


def main() -> int:
    repo = Path.cwd().resolve()
    if "--source-regression" in sys.argv[1:]:
        _source_binding_regression(repo)
        return 0
    _require(RUNTIME_PIN, directory=True)
    _require(PEERS, directory=True)
    if subprocess.check_output(["git", "-C", str(RUNTIME_PIN), "rev-parse", "HEAD"], text=True).strip() != RUNTIME_SHA:
        raise RuntimeError("Runtime2c4 source pin changed")
    node = _require(NODE_PIN)
    if node.is_symlink() or _sha256(node) != NODE_SHA256 or subprocess.check_output([str(node), "--version"], text=True).strip() != "v20.19.4":
        raise RuntimeError("pinned Node43d6 is not the qualified executable")
    WORKER_ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="scene-only-public13-", dir=WORKER_ARTIFACT.parent))
    _private(stage, RUNTIME_PIN, PEERS)
    try:
        overlay = _overlay(repo, stage)
        runtime = stage / "runtime-source"
        shutil.copytree(RUNTIME_PIN, runtime, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"), symlinks=False)
        project = _project(overlay, stage)
        env = _environment(overlay, runtime, project)
        WORKER_ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        measured = ["astrid/sdk/timeline_filmstrip.py", "astrid/core/execution/generic_host.py",
                    "astrid/core/rendering/verified_source.py",
                    "astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py"]
        for name in measured:
            destination = WORKER_ARTIFACT.parent / "source" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(overlay / name, destination)
        (WORKER_ARTIFACT.parent / "overlay-source.json").write_text(json.dumps({
            "files": {name: _sha256(overlay / name) for name in measured},
            "pythonpath": env["PYTHONPATH"], "agent": str(overlay), "runtime": str(runtime),
            "project": str(project), "node": str(node),
        }, sort_keys=True))
        bundle_preflight = _bundle_preflight(overlay, project, env, stage)
        preflight = {
            "phase": "preflight", "runtime": RUNTIME_SHA, "node": str(node),
            "node_sha256": NODE_SHA256, "composition": PUBLIC13_NAME,
            "composition_sha256": PUBLIC13_SHA256, "composition_files": PUBLIC13_FILES,
            "source_tuple": {"sdk": "9b887e232", "executor": "23db420c1", "runtime": RUNTIME_SHA},
            "bundle_preflight": bundle_preflight,
        }
        print(json.dumps(preflight, sort_keys=True), flush=True)
        if "--preflight" in sys.argv[1:]:
            return 0
        command = [sys.executable, "-B", "-m", "pytest", "-q", "-o", "addopts=",
                   "-p", "no:cacheprovider", "--tb=short", "--basetemp=" + str(stage / "pytest"),
                   "tests/packs/rendering/test_live_scene_only_managed_carrier.py"]
        result = subprocess.run(command, cwd=overlay, env=env, check=False)
        if result.returncode:
            for log in stage.rglob("generic-host.log"):
                lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
                print(json.dumps({"phase": "host-log-tail", "path": str(log),
                                  "lines": lines[-80:]}, sort_keys=True), flush=True)
        print(json.dumps({"phase": "postflight", "pytest_returncode": result.returncode,
                          "artifact": str(WORKER_ARTIFACT), "source_tuple": preflight["source_tuple"]}, sort_keys=True), flush=True)
        return result.returncode
    finally:
        if stage.is_symlink():
            raise RuntimeError("refusing to remove symlink stage")
        shutil.rmtree(stage)
        print(json.dumps({"phase": "cleanup", "stage_removed": not stage.exists()}), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
