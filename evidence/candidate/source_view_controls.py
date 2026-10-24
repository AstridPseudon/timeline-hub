"""Exercise the private App source-view input boundary without running delivery-build."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

CALLER = Path(__file__).with_name("run-final-delivery.py")


def load_caller():
    spec = importlib.util.spec_from_file_location("final_delivery_candidate", CALLER)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load private delivery caller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
        env={
            "PATH": "/usr/bin:/bin",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null",
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )
    return process.stdout.strip()


def commit(root: Path, message: str) -> str:
    run_git(root, "add", "note.txt")
    run_git(root, "commit", "-q", "-m", message)
    return run_git(root, "rev-parse", "HEAD")


def main() -> None:
    caller = load_caller()
    with tempfile.TemporaryDirectory(prefix="timeline-source-view-controls-") as raw_tmp:
        tmp = Path(raw_tmp)
        full = tmp / "full"
        run_git(tmp, "init", "-q", "--initial-branch=main", str(full))
        run_git(full, "config", "user.name", "source-view-controls")
        run_git(full, "config", "user.email", "source-view-controls@localhost")
        (full / "note.txt").write_text("base\n")
        upstream_base = commit(full, "base")
        (full / "note.txt").write_text("tip\n")
        gated_tip = commit(full, "tip")
        run_git(full, "update-ref", "refs/remotes/origin/main", upstream_base)
        run_git(full, "update-ref", "refs/heads/tl/integration", gated_tip)

        source = tmp / "shallow-source"
        subprocess.run(
            ["git", "clone", "--depth=2", "--no-local", str(full), str(source)],
            check=True,
            capture_output=True,
            text=True,
            env={
                "PATH": "/usr/bin:/bin",
                "GIT_CONFIG_GLOBAL": "/dev/null",
                "GIT_CONFIG_SYSTEM": "/dev/null",
                "GIT_OPTIONAL_LOCKS": "0",
            },
        )
        run_git(source, "config", "user.name", "source-view-controls")
        run_git(source, "config", "user.email", "source-view-controls@localhost")
        run_git(source, "update-ref", "refs/remotes/origin/main", upstream_base)
        run_git(source, "update-ref", "refs/heads/tl/integration", gated_tip)
        tree = run_git(source, "rev-parse", f"{gated_tip}^{{tree}}")
        upstream_tree = run_git(source, "rev-parse", f"{upstream_base}^{{tree}}")
        source_item = {"root": str(source), "sha": gated_tip, "tree": tree}
        gate_item = {
            "root": str(source),
            "base_ref": "origin/main",
            "gate_ref": "tl/integration",
            "upstream_base": upstream_base,
            "upstream_base_tree": upstream_tree,
            "gated_tip": gated_tip,
            "gated_tree": tree,
        }
        assert run_git(source, "rev-parse", "--is-shallow-repository") == "true"

        holder, view, facts = caller.prepare_private_app_source_view(
            source_item, gate_item, tmp, min_free_bytes=0
        )
        try:
            assert facts["tip"] == gated_tip
            assert facts["tree"] == tree
            assert facts["origin_main"] == upstream_base
            assert facts["origin_main_tree"] == upstream_tree
            assert facts["missing_objects"] == 0
            assert run_git(view, "rev-parse", "--is-shallow-repository") == "false"
            assert run_git(view, "rev-parse", "origin/main") == upstream_base
            assert run_git(view, "rev-parse", "tl/integration") == gated_tip
            assert run_git(source, "rev-parse", "--is-shallow-repository") == "true"
        finally:
            shutil.rmtree(holder)

        for poisoned in (
            {**source_item, "sha": "0" * 40},
            {**source_item, "tree": "0" * 40},
            {**source_item, "root": str(tmp / "missing")},
        ):
            try:
                caller.prepare_private_app_source_view(poisoned, gate_item, tmp, min_free_bytes=0)
            except ValueError:
                pass
            else:
                raise AssertionError("poisoned source input was accepted")

        try:
            caller.prepare_private_app_source_view(
                source_item,
                gate_item,
                tmp,
                min_free_bytes=10**18,
            )
        except ValueError as exc:
            assert "8.5 GB heavy-work floor" in str(exc)
        else:
            raise AssertionError("low-space source input was not refused")

        source_payload = {
            name: {"root": str(source), "sha": gated_tip, "tree": tree}
            for name in ("agent", "runtime", "app", "composition")
        }
        gate_payload = {
            "version": 1,
            "repos": {
                name: dict(gate_item)
                for name in ("agent", "runtime", "app", "composition")
            },
        }
        source_path = tmp / "source-input.json"
        gate_path = tmp / "gate-input.json"
        source_path.write_text(json.dumps(source_payload, indent=2, sort_keys=True) + "\n")
        gate_path.write_text(json.dumps(gate_payload, indent=2, sort_keys=True) + "\n")
        core = tmp / "core.py"
        wrapper = tmp / "wrapper.py"
        builder = tmp / "builder.py"
        core.write_text("core\n")
        wrapper.write_text("wrapper\n")
        builder.write_text("builder\n")
        seen: dict[str, object] = {}

        def stub_wrapper(command: list[str], _service_tmp: Path) -> tuple[int, str]:
            seen["command"] = command
            derived_gate = Path(command[command.index("--gate-tuple") + 1])
            seen["gate_payload"] = json.loads(derived_gate.read_text())
            receipt = Path(command[command.index("--receipt") + 1])
            receipt.write_text("{}\n")
            return 0, "stub builder not run\n"

        original_prepare = caller.prepare_private_app_source_view
        caller.CORE_RUNNER = core
        caller.CORE_RUNNER_SHA256 = caller.digest(core.read_bytes())
        caller.REVIEWED_WRAPPER_SHA256 = caller.digest(wrapper.read_bytes())
        caller.REVIEWED_BUILDER_SHA256 = caller.digest(builder.read_bytes())
        caller.prepare_private_app_source_view = lambda source_entry, gate_entry, parent: original_prepare(
            source_entry, gate_entry, parent, min_free_bytes=0
        )
        caller.run_wrapper = stub_wrapper
        receipt = tmp / "stub-receipt.json"
        assert caller.main(
            [
                "--source-tuple",
                str(source_path),
                "--tuple-sha",
                caller.digest(source_path.read_bytes()),
                "--gate-tuple",
                str(gate_path),
                "--gate-tuple-sha",
                caller.digest(gate_path.read_bytes()),
                "--wrapper",
                str(wrapper),
                "--wrapper-sha",
                caller.REVIEWED_WRAPPER_SHA256,
                "--builder",
                str(builder),
                "--builder-sha",
                caller.REVIEWED_BUILDER_SHA256,
                "--receipt",
                str(receipt),
                "--",
                "--dry-run",
            ]
        ) == 0
        command = seen["command"]
        assert isinstance(command, list)
        assert Path(command[command.index("--gate-tuple") + 1]) != gate_path
        gate_payload_seen = seen["gate_payload"]
        assert isinstance(gate_payload_seen, dict)
        assert gate_payload_seen["repos"]["app"]["root"].endswith("/app")

        try:
            caller.main(
                [
                    "--source-tuple",
                    str(tmp / "missing-source.json"),
                    "--tuple-sha",
                    "0" * 64,
                    "--gate-tuple",
                    str(tmp / "missing-gate.json"),
                    "--gate-tuple-sha",
                    "0" * 64,
                    "--builder",
                    str(tmp / "missing-builder"),
                    "--builder-sha",
                    "0" * 64,
                    "--receipt",
                    str(tmp / "receipt.json"),
                    "--",
                    "--dry-run",
                ]
            )
        except ValueError as exc:
            assert "reviewed f25d builder" in str(exc)
        else:
            raise AssertionError("poisoned builder hash was accepted")

    print("source-view controls: PASS (positive, poisoned, and low-space inputs; no builder)")


if __name__ == "__main__":
    main()
