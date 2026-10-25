"""Read normal producer artifacts using Farm's separately authenticated bindings.

No producer is executed. Digests are supplied by the receiving owner, never
learned from the file being checked. These are custody checks, not signatures.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


def bound(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise ValueError(f"missing trusted binding {name}")
    return value


def physical(path: str | Path, directory: bool = False) -> Path:
    path = Path(path)
    if not path.is_absolute() or path.resolve(strict=True) != path:
        raise ValueError("path is not physical and absolute")
    info = path.stat()
    if info.st_uid != os.getuid() or info.st_mode & 0o022:
        raise ValueError("foreign owner or broadly writable artifact")
    if directory:
        if not stat.S_ISDIR(info.st_mode):
            raise ValueError("not a directory")
    elif not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError("not a single-link regular file")
    return path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def authenticated(name: str) -> tuple[Path, bytes]:
    path = physical(bound(name))
    expected = bound(name + "_SHA256")
    data = path.read_bytes()
    if not re.fullmatch(r"[0-9a-f]{64}", expected) or digest(data) != expected:
        raise ValueError(f"{name} digest mismatch")
    return path, data


def producer(root: Path, name: str, expected: str) -> Path:
    path = physical(root / "bin" / name)
    if path.stat().st_mode & 0o777 != 0o755 or digest(path.read_bytes()) != expected:
        raise ValueError(f"wrong producer {name}")
    return path


def git(repo: str | Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.DEVNULL)


def checkout(repo: str | Path, commit: str, tree: str) -> None:
    physical(repo, directory=True)
    if (git(repo, "rev-parse", "HEAD").decode().strip() != commit
            or git(repo, "rev-parse", "HEAD^{tree}").decode().strip() != tree
            or git(repo, "status", "--porcelain", "--untracked-files=all")):
        raise ValueError("checkout does not close the receipt source")


def pairs(text: str) -> dict[str, str]:
    result = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        if not key or key in result:
            raise ValueError("duplicate/empty field")
        result[key] = value
    return result


def source(root: Path, name: str, repo: str, commit: str, tree: str) -> None:
    path, raw = authenticated(name)
    kind = name.removeprefix("FARM_CURRENT_").removesuffix("_RECEIPT").lower()
    prefix = {"agent": "agt", "runtime": "rt", "app": "app", "composition": "vw"}[kind]
    worker = f"{prefix}-pin-{commit[:8]}"
    if path != root / "queue" / "done" / f"checkout-{kind}-{commit}":
        raise ValueError("not the normal checkout queue result")
    if raw.decode() not in (
        f"created {repo} (detached at {commit}, KEEP)\n",
        f"exists: {repo} at {commit}\n",
    ):
        raise ValueError("not make-checkout output")
    meta = pairs(physical(root / "workers" / worker / "meta").read_text())
    expected = {"name": worker, "repo": kind, "base": commit[:8], "base_sha": commit[:8],
                "model": "none", "effort": "none", "heavy": "0", "worktree": repo}
    if set(meta) != {*expected, "started"} or any(meta[key] != value for key, value in expected.items()):
        raise ValueError("checkout worker metadata mismatch")
    physical(root / "workers" / worker / "KEEP")
    checkout(repo, commit, tree)


def kit(root: Path, name: str) -> None:
    _, raw = authenticated(name)
    value = json.loads(raw)
    # This is the existing lead's installed-kit summary, not a child or a
    # farm-distribution-inputs component receipt. Its digest is external trust.
    if value["schema"] != "timeline.ops.d137.installed-kit/v1" or value["status"] != "qualified_for_one_request":
        raise ValueError("unsupported installed-kit format")
    installer = value["installer"]
    maker = producer(root, "make-child-venv", bound("MAKER_SHA"))
    if installer != {"path": str(maker), "sha256": bound("MAKER_SHA"), "bytes": 111171,
                     "mode": "0755", "regular_nonsymlink": True}:
        raise ValueError("installed maker mismatch")
    if bound("RECEIVED_MAKER") != str(maker):
        raise ValueError("detached received maker")
    source = value["source"]
    if source["review"] != "PASS_SOURCE_SECURITY" or source["reviewed_installer"] != "installer1826":
        raise ValueError("kit was not qualified by the reviewed installation route")
    repo = bound("KIT_SOURCE_CHECKOUT")
    checkout(repo, source["commit"], source["tree"])
    # Kit source is the reviewed Composition OPS join, not Agent film source.
    for rel, sha in (("make-child-venv", "MAKER_SHA"), ("request-child-venv", "WRAPPER_SHA"),
                     ("check-child-imports", "CHECKER_SHA")):
        if digest(git(repo, "show", f"{source['commit']}:ops-child-custody/{rel}")) != bound(sha):
            raise ValueError("kit source bytes mismatch")
    expected_helpers = {
        "bench_store.py": "123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2",
        "verify_dependency_seed.py": "116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2",
    }
    if value["protected_helpers"] != expected_helpers:
        raise ValueError("wrong helper identities")
    for helper, sha in expected_helpers.items():
        producer(root, helper, sha)
    installation, data = authenticated("FARM_KIT_INSTALLATION")
    if value["receipts"]["installation"] != str(installation):
        raise ValueError("detached installation receipt")
    installed = json.loads(data)
    if (installed["result"] != "PASS_INSTALL"
            or installed["installer"] != "ops-child-custody/install-prep/apply-reviewed-maker.sh"
            or installed["installer_review"] != "installer1826"
            or installed["source_commit"] != source["commit"]
            or installed["source_tree"] != source["tree"]
            or installed["candidate"] != {key: installer[key] for key in ("sha256", "bytes", "mode")}
            or installed["target"] != {"path": str(maker), "sha256": installer["sha256"],
                                       "bytes": 111171, "mode": "0755", "regular_single_link": True,
                                       "matches_candidate": True}
            or installed["protected_helpers"] != expected_helpers):
        raise ValueError("installation/source closure mismatch")


def child(root: Path, name: str) -> None:
    path, raw = authenticated(name)
    request = "venv-agent-child-d140"
    if path != root / "queue" / "done" / f"childvenv-{request}":
        raise ValueError("not a normal child queue result")
    producer(root, "make-child-venv", bound("MAKER_SHA"))
    producer(root, "request-child-venv", bound("WRAPPER_SHA"))
    # The dispatcher retains producer progress before this final success line.
    line = raw.decode().splitlines()[-1]
    match = re.fullmatch(r"(?:created |reused child venv path=)(/\S+) (.+)", line)
    if match is None:
        raise ValueError("not a registered maker success receipt")
    child_path = physical(match[1], directory=True)
    fields = pairs(match[2].replace(" ", "\n"))
    agent, runtime = bound("AGENT_SHA"), bound("RUNTIME_SHA")
    expected = {"agent": agent, "runtime": runtime, "actual_agent": agent, "actual_runtime": runtime,
                "registration": "existing", "requested_name": request, "status": "passed", "remotion": "none"}
    if (set(fields) != {*expected, "key", "provision_report", "provision_report_sha256", "schema_source_identity_sha256"}
            or any(fields[key] != value for key, value in expected.items())
            or not re.fullmatch(r"[0-9a-f]{64}", fields["key"])
            or child_path.name != "child-" + fields["key"]
            or bound("CHILD_PYTHON") != str(child_path / "bin/python")
            or bound("P4_PYTHON") != bound("CHILD_PYTHON")):
        raise ValueError("child receipt binding mismatch")
    report = physical(root / "tests" / "provision" / f"{request}.txt")
    data = report.read_bytes()
    if (fields["provision_report"] != str(report) or digest(data) != fields["provision_report_sha256"]
            or physical(child_path / ".provision-report").read_bytes() != data):
        raise ValueError("provision report digest/path mismatch")
    header, sections = data.decode().split("installed_import_origins:\n", 1)
    imports, sections = sections.split("installed_distribution_metadata:\n", 1)
    metadata, freeze = sections.split("pip_freeze:\n", 1)
    client = git(bound("RUNTIME_CHECKOUT"), "ls-tree", "-r", "--name-only", runtime,
                 "packages/python/astrid_runtime_client/").decode().splitlines()
    if not client:
        raise ValueError("missing generated client source")
    identity = "\n".join(f"{rel}={digest(git(bound('RUNTIME_CHECKOUT'), 'show', runtime + ':' + rel))}" for rel in client)
    schema = physical(child_path / ".schema-source-identity").read_text().strip()
    if fields["schema_source_identity_sha256"] != digest(schema.encode()):
        raise ValueError("schema identity digest mismatch")
    schema_value = json.loads(schema)
    expected_schema = {"origin": "https://github.com/banodoco/ArtAgents.git",
                       "commit": "242f9c4306bf3b501222cb041a9eb246ef47bc85",
                       "subdirectory": "packages/timeline-schema/python",
                       "source_tree": "75a5a697f630affee40632e500b3f5b704a9b834",
                       "input_kind": "installed_distribution", "package": "banodoco-timeline-schema",
                       "version": "0.0.2", "record_rows": 18, "record_hashed_rows": 12,
                       "tree_tie": "UNAVAILABLE"}
    if (any(schema_value.get(key) != value for key, value in expected_schema.items())
            or schema_value["record_sha256"] != digest(physical(bound("SCHEMA_RECORD_CLOSURE")).read_bytes())
            or schema_value["manifest_sha256"] != digest(physical(bound("SCHEMA_SOURCE_MANIFEST")).read_bytes())
            or schema_value["direct_url_sha256"] != digest(physical(bound("SCHEMA_DIRECT_URL")).read_bytes())):
        raise ValueError("schema input closure mismatch")
    if pairs(header) != {"status": "passed", "agent_sha": agent, "runtime_sha": runtime,
                         "runtime_client_identity_sha256": digest(identity.encode()),
                         "schema_source_identity_sha256": digest(schema.encode()),
                         "requirements_path": "requirements/proof.lock", "requirements_lock_sha256": bound("PROOF_LOCK_SHA")}:
        raise ValueError("provision source header mismatch")
    for section, marker in ((imports, ".astrid-import-origins"), (metadata, ".astrid-distribution-metadata")):
        if not section or physical(child_path / marker).read_text() != section:
            raise ValueError("provision section does not close to child")
    if pairs(metadata).get("schema_source_identity") != schema:
        raise ValueError("provision metadata schema identity mismatch")
    if not freeze or pairs(imports).keys() != {"astrid", "astrid_runtime", "runtime_protocol", "astrid_runtime_client"}:
        raise ValueError("incomplete provision inventory")
    for origin in pairs(imports).values():
        if not physical(origin).is_relative_to(child_path / "lib"):
            raise ValueError("import origin escapes child")
    for marker, expected in ((".astrid-source-commit", agent), (".astrid-runtime-source-commit", runtime),
                             (".astrid-runtime-client-identity", identity)):
        if physical(child_path / marker).read_text().strip() != expected:
            raise ValueError("child source marker mismatch")
    for kind in ("AGENT", "RUNTIME"):
        checkout(bound(kind + "_CHECKOUT"), bound(kind + "_SHA"), bound(kind + "_TREE"))


def d73(root: Path, name: str) -> None:
    _, raw = authenticated(name)
    _, positive = authenticated("P4_D73_MANIFEST")
    if raw != positive:
        raise ValueError("D73 receipt differs from manager's authenticated manifest")
    launcher = physical(Path(bound("AGENT_CHECKOUT")) / "tools/p4-d73-pinned-launch.sh")
    if (str(launcher) != bound("D73_LAUNCHER") or launcher.stat().st_mode & 0o777 != 0o755
            or digest(launcher.read_bytes()) != bound("LAUNCHER_SHA")):
        raise ValueError("detached D73 producer")
    values = pairs(raw.decode())
    required = "format agent_sha agent_tree agent_parents agent_path runtime_sha runtime_tree runtime_path app_sha app_tree app_path composition_sha composition_tree composition_path python node profile schema node_version profile_lock_sha profile_archive_sha profile_registry_sha composition_version original_p4_test_hash service_versions junit_paths".split()
    if not set(required) <= values.keys() or not all(values[key] for key in required) or values["format"] != "p4-d73-v1":
        raise ValueError("not a complete D73 manifest")
    for kind in ("agent", "runtime", "app", "composition"):
        for suffix, binding in (("sha", "SHA"), ("tree", "TREE"), ("path", "CHECKOUT")):
            if values[kind + "_" + suffix] != bound(kind.upper() + "_" + binding):
                raise ValueError("D73 source mismatch")
        checkout(values[kind + "_path"], values[kind + "_sha"], values[kind + "_tree"])
        if kind + "_parents" in values and git(values[kind + "_path"], "rev-list", "--parents", "-n", "1", "HEAD").decode().strip() != values[kind + "_parents"]:
            raise ValueError("D73 parent mismatch")
    for field, binding in (("python", "P4_PYTHON"), ("node", "NODE_BIN"), ("profile", "PROFILE")):
        if values[field] != bound(binding):
            raise ValueError("D73 input binding mismatch")


def main() -> int:
    try:
        kind, name, *args = sys.argv[1:]
        root = physical(bound("FARM_ORCH_ROOT"), directory=True)
        producer(root, "dispatcher-daemon", "d5c6753312e485f2368ab61d34161f0853b27aa6c5e2b5c22036d3bd628da8ed")
        if kind == "source":
            producer(root, "make-checkout", "8430f253367b308ba69b93e084e57351891bce42235a018d061d2b07c5dc6ffc")
            source(root, name, *args)
        else:
            {"child": child, "kit": kit, "d73": d73}[kind](root, name)
    except (OSError, ValueError, KeyError, TypeError, IndexError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
