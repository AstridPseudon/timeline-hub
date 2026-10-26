#!/usr/bin/env python3
"""Verify the authenticated D141s final packet and its literal-only adoption.

This is deliberately a finite checker for this packet and this candidate.  It
does not install a kit, register a suite, create a checkout, or provide a live
binding mechanism.  The same command can be rerun by the CAS checker against
the candidate tree and the two published owner packets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


BASE_HEAD = "2733c720c555c2853ce73b5b74d7896aa1fe8b38"
BASE_TREE = "eb04b6da47a320f0920ae7dd53d95b0ac85928a9"
DONOR = "56f2d56e7d241d303be85df62166570d51602101"
FINAL_APP_HEAD = "4de54db14bdc9ddc2ce2e5887258b03acbffd30d"
FINAL_APP_TREE = "84c3fb7f73f08c22220f8e808962fe3f24aaa0aa"
OLD_APP_HEAD = "5344c53e3063001bb3255bd0c9cd32cc5e77967f"
OLD_APP_TREE = "dd989783046aeff652486a1ba39db42aea86e201"
FINAL_RUNTIME_HEAD = "95d98f038320d5d46bd679ac000ab3e15825c935"
FINAL_RUNTIME_TREE = "78df31d62c5b9ba4c84dee4ea346e43a767718c1"
FINAL_AGENT_HEAD = "8585ed9c0404d0187b2ce70242d25114a32747c2"
FINAL_AGENT_TREE = "92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c"
FINAL_COMPOSITION_HEAD = "635f4de06fda22a85fc2e4cfc764d0153a4c9f40"
FINAL_COMPOSITION_TREE = "5ab5191a296980a0a6bcd1178ab6902d6478a148"

VALIDATE = "ops-d141-measured-floor/bin/d141-validate-receipt.py"
RUNNER = "ops-d141-measured-floor/bin/test-run"
CONTROLS = "ops-d141-measured-floor/controls/real-controls.py"
MANIFEST = "ops-d141-measured-floor/install-manifest.json"
EXPECTED_FILES = {VALIDATE, RUNNER, "ops-d141-measured-floor/controls/real-controls.py", MANIFEST}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"FAIL: {message}")


def git(candidate: Path, *args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(candidate), *args],
        check=False,
        capture_output=True,
        text=text,
    )
    if result.returncode:
        detail = result.stderr if text else result.stderr.decode(errors="replace")
        fail(f"git {' '.join(args)} failed: {detail.strip()}")
    if text:
        return result.stdout.rstrip("\n")
    return result.stdout


def git_blob(candidate: Path, revision: str, path: str) -> bytes:
    return git(candidate, "show", f"{revision}:{path}", text=False)  # type: ignore[return-value]


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_file(path: Path) -> None:
    require(path.is_file() and not path.is_symlink(), f"required regular file missing or symlinked: {path}")


def source_tuple(value: object, label: str) -> dict[str, str]:
    require(isinstance(value, dict), f"{label} is not an object")
    result = {key: value.get(key) for key in ("head", "tree")}
    require(all(isinstance(item, str) for item in result.values()), f"{label} lacks full source identity")
    require(all(len(item) == 40 for item in result.values()), f"{label} is not full-40 identity")
    return result  # type: ignore[return-value]


def verify_packet(
    binding_path: Path,
    normal_path: Path,
    preflight_path: Path,
    *,
    expected_app: dict[str, str],
    expected_runtime: dict[str, str] | None,
    expected_target: str,
    expected_schema: int,
    expected_binding_digest: str,
) -> tuple[dict[str, object], str, str]:
    for path in (binding_path, normal_path, preflight_path):
        require_file(path)
    raw = binding_path.read_bytes()
    require(digest(raw) == expected_binding_digest, f"binding digest mismatch: {binding_path}")
    binding = read_json(binding_path)
    require(isinstance(binding, dict), f"binding is not an object: {binding_path}")
    require(binding.get("schema_version") == expected_schema, f"unexpected binding schema: {binding_path}")
    require(binding.get("status") == "PROSPECTIVE_PRODUCTION_BUILDER", "binding is not prospective builder data")
    require(binding.get("registration") is False and binding.get("execution") == "none", "packet is not registration=false/execution=none")
    require(binding.get("target") == expected_target and binding.get("repo") == "app", "packet target/repo mismatch")
    require(binding.get("selector") == "p2-automatic-child-placement", "packet first selector mismatch")

    suites = binding.get("suites")
    require(isinstance(suites, dict), "packet suites missing")
    normal_suite = suites.get("normal")
    preflight_suite = suites.get("preflight")
    require(isinstance(normal_suite, str) and isinstance(preflight_suite, str), "packet suite names missing")
    require(normal_suite.endswith("-submit") and preflight_suite.endswith("-submit-preflight"), "packet suite suffix mismatch")

    tuples = binding.get("source_tuple")
    require(isinstance(tuples, dict), "packet source tuple missing")
    app_tuple = source_tuple(tuples.get("app"), "packet App source tuple")
    require(app_tuple == expected_app, "packet App source identity mismatch")
    if expected_runtime is not None:
        runtime_tuple = source_tuple(tuples.get("runtime"), "packet Runtime source tuple")
        require(runtime_tuple == expected_runtime, "packet Runtime source identity mismatch")
        require(source_tuple(tuples.get("agent"), "packet Agent source tuple") == {"head": FINAL_AGENT_HEAD, "tree": FINAL_AGENT_TREE}, "packet Agent source mismatch")
        require(source_tuple(tuples.get("composition"), "packet Composition source tuple") == {"head": FINAL_COMPOSITION_HEAD, "tree": FINAL_COMPOSITION_TREE}, "packet Composition source mismatch")

    commands = binding.get("commands")
    first_pair = binding.get("first_pair")
    require(isinstance(commands, dict) or isinstance(first_pair, dict), "packet command facts missing")
    normal = normal_path.read_bytes()
    preflight = preflight_path.read_bytes()
    require(not normal.endswith(b"\n") and not preflight.endswith(b"\n"), "command file has terminal newline")
    normal_hash = digest(normal)
    preflight_hash = digest(preflight)
    if isinstance(commands, dict):
        normal_fact = commands.get("normal")
        preflight_fact = commands.get("preflight")
        normal_hash_key = "sha256_utf8_without_newline"
        preflight_hash_key = "sha256_utf8_without_newline"
        normal_bytes_key = "bytes_without_newline"
        preflight_bytes_key = "bytes_without_newline"
        normal_row_fact = commands
        preflight_row_fact = commands
        normal_row_hash_key = "normal_row_sha256_utf8_with_one_terminal_lf"
        preflight_row_hash_key = "preflight_row_sha256_utf8_with_one_terminal_lf"
    else:
        normal_fact = first_pair.get("normal_command")
        preflight_fact = first_pair.get("preflight_command")
        normal_hash_key = "sha256_without_terminal_newline"
        preflight_hash_key = "sha256_without_terminal_newline"
        normal_bytes_key = "bytes_without_terminal_newline"
        preflight_bytes_key = "bytes_without_terminal_newline"
        normal_row_fact = first_pair.get("normal_row")
        preflight_row_fact = first_pair.get("preflight_row")
        normal_row_hash_key = "sha256_with_one_terminal_lf"
        preflight_row_hash_key = "sha256_with_one_terminal_lf"
    require(isinstance(normal_fact, dict) and isinstance(preflight_fact, dict), "packet first command facts missing")
    require(normal_fact.get(normal_hash_key) == normal_hash and normal_fact.get(normal_bytes_key) == len(normal), "normal command does not match packet")
    require(preflight_fact.get(preflight_hash_key) == preflight_hash and preflight_fact.get(preflight_bytes_key) == len(preflight), "preflight command does not match packet")

    normal_row = f"app {normal_suite} {normal.decode('utf-8')}\n".encode()
    preflight_row = f"app {preflight_suite} {preflight.decode('utf-8')}\n".encode()
    require(isinstance(normal_row_fact, dict) and isinstance(preflight_row_fact, dict), "packet row facts missing")
    require(normal_row_fact.get(normal_row_hash_key) == digest(normal_row), "normal row does not match packet")
    require(preflight_row_fact.get(preflight_row_hash_key) == digest(preflight_row), "preflight row does not match packet")
    return binding, normal_hash, preflight_hash


def verify_final_manifest(path: Path, binding: dict[str, object], source_home: Path) -> dict[str, object]:
    require_file(path)
    manifest = read_json(path)
    require(isinstance(manifest, dict), "final source manifest is not an object")
    require(manifest.get("status") == "PROSPECTIVE_PRODUCTION_BUILDER" and manifest.get("source_only") is True, "final source manifest status mismatch")
    actual = manifest.get("actual_tuple")
    require(isinstance(actual, dict), "final source manifest actual tuple missing")
    app = actual.get("app")
    require(isinstance(app, dict), "final source manifest App tuple missing")
    require(app.get("repository") == str(source_home) and app.get("commit") == FINAL_APP_HEAD and app.get("tree") == FINAL_APP_TREE, "final source manifest App identity mismatch")
    require(app.get("normal_home_clean") is True and app.get("normal_home_ref_equal") is True, "final source manifest does not authenticate clean HOME")
    delta = manifest.get("app_delta_from_5344")
    require(isinstance(delta, dict), "final source manifest historical App delta missing")
    require(delta.get("final_parent_1") == OLD_APP_HEAD and delta.get("final_tree_equals_reviewed_candidate") is True, "final source manifest old parent/tree authentication failed")
    require(delta.get("only_changed_paths") == ["public/install-manifest.json:runtime.sha", "runtime.lock.json:source_commit"], "final source manifest App delta is not the approved two-field delta")
    builder = manifest.get("builder_source")
    require(isinstance(builder, dict), "final source manifest builder facts missing")
    require(builder.get("final_head") == FINAL_APP_HEAD and builder.get("final_tree") == FINAL_APP_TREE, "final builder source identity mismatch")
    manifest_tuples = manifest.get("actual_tuple")
    binding_tuples = binding.get("source_tuple")
    require(isinstance(manifest_tuples, dict) and isinstance(binding_tuples, dict), "binding/source manifest tuples missing")
    for repo in ("app", "agent", "runtime", "composition"):
        manifest_repo = manifest_tuples.get(repo)
        require(isinstance(manifest_repo, dict), f"manifest {repo} tuple missing")
        manifest_identity = {"head": manifest_repo.get("commit"), "tree": manifest_repo.get("tree")}
        require(source_tuple(manifest_identity, f"manifest {repo} tuple") == source_tuple(binding_tuples.get(repo), f"binding {repo} tuple"), f"binding and source manifest {repo} identities differ")
    return manifest


def verify_home_receipt(path: Path, source_home: Path) -> dict[str, object]:
    require_file(path)
    receipt = read_json(path)
    require(isinstance(receipt, dict), "App HOME receipt is not an object")
    app = receipt.get("app")
    require(isinstance(app, dict), "App HOME receipt lacks app identity")
    require(app.get("head") == FINAL_APP_HEAD and app.get("tree") == FINAL_APP_TREE, "App HOME receipt identity mismatch")
    require(app.get("clean") is True and app.get("normal_ref_equal") is True and app.get("entire_tree_equals_reviewed_candidate") is True, "App HOME receipt is not a clean authenticated HOME")
    require(receipt.get("body_or_REG0_claim") is False, "App HOME receipt makes a forbidden body/REG0 claim")
    require(receipt.get("delta_from5344") == ["public/install-manifest.json:runtime.sha", "runtime.lock.json:source_commit"], "App HOME receipt delta mismatch")
    require(source_home.resolve() == Path("/home/user/work/app"), "source-home must be the actual App HOME")
    return receipt


def verify_diff(candidate: Path, manifest: dict[str, object]) -> dict[str, object]:
    mapping: dict[str, list[tuple[bytes, bytes]]] = {
        VALIDATE: [
            (b"d141g-p2-automatic-child-placement-5344c53e-submit", b"d141g-p2-automatic-child-placement-4de54db1-submit"),
            (b"/home/user/work/wt/app-pin-5344c53e", b"/home/user/work/wt/app-pin-4de54db1"),
            (b"5344c53e3063001bb3255bd0c9cd32cc5e77967f", FINAL_APP_HEAD.encode()),
            (b"dd989783046aeff652486a1ba39db42aea86e201", FINAL_APP_TREE.encode()),
            (b"97277b3a42e033819b830ff4f1e450616073d6ea3f6d8e4bd598e32681541ad7", b"f20ab22c427e46fb06edbc2f91ea11ad27faf7a1b38c11abbc20895e465471a4"),
            (b"98522d5511c5e66fcfeaa68044f84eaf9fb45b22e9a1145613a5262be47f21a6", b"55da9058c938ce4ba362670b1322c49097441007d460677f6f5b2726c7f4c2aa"),
            (b"exact 5344 first placement pair", b"exact 4de54db1 first placement pair"),
            (b"exact 5344 source", b"exact 4de54db1 source"),
            (b"freeze2 5344 first placement caller", b"final 4de54db1 first placement caller"),
        ],
        RUNNER: [
            (b"d141g-p2-automatic-child-placement-5344c53e-submit", b"d141g-p2-automatic-child-placement-4de54db1-submit"),
            (b"app-pin-5344c53e", b"app-pin-4de54db1"),
        ],
        "ops-d141-measured-floor/controls/real-controls.py": [
            (b"prospective freeze2 source binding only", b"prospective final source binding only"),
            (b"design/app-P-D141l-freeze2-suite-binding-0459-binding.json", b"design/app-P-D141s-final-source-binding-0545-binding.json"),
            (b"53a145f29602a9c5925ed4782fb1d4d7d4dfe3025f78171eee253896bc52a539", b"6e9a9a1c611954af6458478ed10c66ae9edb89f6856531b3496dec9e1afa4c28"),
            (b"design/app-P-D141l-freeze2-suite-binding-0459-normal-command.txt", b"design/app-P-D141s-final-source-binding-0545-normal-command.txt"),
            (b"design/app-P-D141l-freeze2-suite-binding-0459-preflight-command.txt", b"design/app-P-D141s-final-source-binding-0545-preflight-command.txt"),
            (b"prospective-freeze2-pair-binding", b"prospective-final-pair-binding"),
        ],
        MANIFEST: [
            (b"16e2592d1307a2567b5e74c6fe018445c428af7c76dbea2b896bfc3fcb06b3df", b"c85a47127c03b670b2fa9596e4a7118252d51f560236d07077b1b6342883493c"),
            (b"a8ede576ef763bae3db4c6acfadc7dcc8f444a9a46f46e69744b0118afda6bc7", b"518b2335516a2cfd1d0a6091d676adc61849b149a6be5d44c823b00d0a9cfcad"),
        ],
    }
    changes: list[dict[str, object]] = []
    for path, replacements in mapping.items():
        before = git_blob(candidate, BASE_HEAD, path)
        after = (candidate / path).read_bytes()
        expected = before
        for old, new in replacements:
            count = expected.count(old)
            require(count > 0, f"approved old literal absent in baseline {path}: {old!r}")
            expected = expected.replace(old, new)
            changes.append({"path": path, "old_sha256": digest(old), "new_sha256": digest(new), "occurrences": count})
        require(after == expected, f"{path} differs outside the finite approved literal mapping")
        require(after.count(b"5344c53e") == 0, f"historical 5344 App literal remains in {path}")

    changed = set(git(candidate, "diff", "--name-only", BASE_HEAD).splitlines())
    require(changed == EXPECTED_FILES, f"changed paths are not exactly the four approved files: {sorted(changed)}")
    status = git(candidate, "status", "--porcelain=v1", "--untracked-files=all")
    require(status == "\n".join(f" M {path}" for path in sorted(EXPECTED_FILES)), f"candidate has unexpected status or staged changes: {status!r}")
    require(git(candidate, "diff", "--cached", "--quiet", BASE_HEAD) == "", "candidate has staged changes")
    require(git(candidate, "diff", "--summary", BASE_HEAD) == "", "candidate has an unexpected mode/type change")

    old_manifest = json.loads(git_blob(candidate, BASE_HEAD, MANIFEST))
    current_manifest = json.loads((candidate / MANIFEST).read_text(encoding="utf-8"))
    require(isinstance(old_manifest, dict) and isinstance(current_manifest, dict), "install manifests are not objects")
    old_entries = {entry["source"]: entry for entry in old_manifest["files"]}
    current_entries = {entry["source"]: entry for entry in current_manifest["files"]}
    require(set(old_entries) == set(current_entries), "install manifest file set changed")
    for name, old_entry in old_entries.items():
        current_entry = current_entries[name]
        require(current_entry.get("mode") == old_entry.get("mode"), f"install mode changed: {name}")
        require(current_entry.get("precondition") == old_entry.get("precondition"), f"install predecessor changed: {name}")
        if name == "bin/d141-validate-receipt.py":
            require(current_entry["sha256"] == "c85a47127c03b670b2fa9596e4a7118252d51f560236d07077b1b6342883493c", "validator manifest output hash mismatch")
        elif name == "bin/test-run":
            require(current_entry["sha256"] == "518b2335516a2cfd1d0a6091d676adc61849b149a6be5d44c823b00d0a9cfcad", "runner manifest output hash mismatch")
        else:
            require(current_entry["sha256"] == old_entry["sha256"], f"unapproved binary output hash changed: {name}")
    donor_manifest = json.loads(git_blob(candidate, DONOR, "privateops-d141-measured-floor/install-manifest.json"))
    donor_entries = {entry["source"]: entry for entry in donor_manifest["files"]}
    for name, entry in current_entries.items():
        donor = donor_entries[name]
        require(entry.get("precondition") == {"sha256": donor["sha256"], "mode": donor["mode"], "type": "regular_nofollow"}, f"donor preimage changed: {name}")

    for path in EXPECTED_FILES:
        expected_mode = 0o755 if path.endswith((".py", "test-run")) else 0o644
        require(stat.S_IMODE((candidate / path).stat().st_mode) == expected_mode, f"unexpected mode: {path}")
    return {"base": {"head": BASE_HEAD, "tree": BASE_TREE}, "changed_files": sorted(changed), "mapping": changes}


def run_controls(candidate: Path, output_dir: Path) -> str:
    private_tmp = Path(os.environ.get("TMPDIR", ""))
    require(private_tmp.is_absolute() and private_tmp.is_dir(), "TMPDIR must be an existing private absolute directory")
    env = dict(os.environ)
    env["TMPDIR"] = str(private_tmp)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = ["python3", "-I", str(candidate / CONTROLS)]
    result = subprocess.run(command, cwd=candidate, env=env, text=True, capture_output=True, check=False)
    payload = result.stdout if result.stdout.strip() else json.dumps({"stdout": result.stdout, "stderr": result.stderr})
    (output_dir / "controls.json").write_text(payload, encoding="utf-8")
    require(result.returncode == 0, f"real-controls.py failed with exit {result.returncode}: {result.stderr.strip()}")
    controls = json.loads(result.stdout)
    require(controls.get("case_count") == 74 and controls.get("verdict", {}).get("SEC001") == "PASS" and controls.get("verdict", {}).get("SEC002") == "PASS", "real-controls did not report all74/SEC001/SEC002 PASS")
    return "TMPDIR=%s PYTHONDONTWRITEBYTECODE=1 python3 -I %s" % (private_tmp, candidate / CONTROLS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--source-home", type=Path, required=True)
    parser.add_argument("--source-receipt", type=Path, required=True)
    parser.add_argument("--old-binding", type=Path, required=True)
    parser.add_argument("--old-normal", type=Path, required=True)
    parser.add_argument("--old-preflight", type=Path, required=True)
    parser.add_argument("--new-binding", type=Path, required=True)
    parser.add_argument("--new-normal", type=Path, required=True)
    parser.add_argument("--new-preflight", type=Path, required=True)
    parser.add_argument("--new-source-manifest", type=Path, required=True)
    parser.add_argument("--new-validation", type=Path, required=True)
    parser.add_argument("--new-handoff", type=Path, required=True)
    args = parser.parse_args()

    candidate = args.candidate.resolve()
    source_home = args.source_home.resolve()
    output_dir = Path(__file__).resolve().parent
    require(candidate.is_dir(), "candidate is not a directory")
    require(git(candidate, "rev-parse", "HEAD") == BASE_HEAD, "candidate HEAD is not authenticated old baseline")
    require(git(candidate, "rev-parse", "HEAD^{tree}") == BASE_TREE, "candidate baseline tree is not authenticated")
    require(git(source_home, "rev-parse", "HEAD") == FINAL_APP_HEAD, "source HOME HEAD is not authenticated final App")
    require(git(source_home, "rev-parse", "HEAD^{tree}") == FINAL_APP_TREE, "source HOME tree is not authenticated final App")

    old_binding, old_normal_hash, old_preflight_hash = verify_packet(
        args.old_binding,
        args.old_normal,
        args.old_preflight,
        expected_app={"head": OLD_APP_HEAD, "tree": OLD_APP_TREE},
        expected_runtime={"head": "6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d", "tree": "ac5b862744bece65b2e30565db1777bacd60da28"},
        expected_target="app-pin-5344c53e",
        expected_schema=2,
        expected_binding_digest="53a145f29602a9c5925ed4782fb1d4d7d4dfe3025f78171eee253896bc52a539",
    )
    new_binding, new_normal_hash, new_preflight_hash = verify_packet(
        args.new_binding,
        args.new_normal,
        args.new_preflight,
        expected_app={"head": FINAL_APP_HEAD, "tree": FINAL_APP_TREE},
        expected_runtime={"head": FINAL_RUNTIME_HEAD, "tree": FINAL_RUNTIME_TREE},
        expected_target="app-pin-4de54db1",
        expected_schema=3,
        expected_binding_digest="6e9a9a1c611954af6458478ed10c66ae9edb89f6856531b3496dec9e1afa4c28",
    )
    require(old_normal_hash == "98522d5511c5e66fcfeaa68044f84eaf9fb45b22e9a1145613a5262be47f21a6" and old_preflight_hash == "97277b3a42e033819b830ff4f1e450616073d6ea3f6d8e4bd598e32681541ad7", "old packet command hashes are not the historical 5344 pair")
    require(new_normal_hash == "55da9058c938ce4ba362670b1322c49097441007d460677f6f5b2726c7f4c2aa" and new_preflight_hash == "f20ab22c427e46fb06edbc2f91ea11ad27faf7a1b38c11abbc20895e465471a4", "final packet command hashes are not the authenticated pair")
    final_manifest = verify_final_manifest(args.new_source_manifest, new_binding, source_home)
    final_receipt = verify_home_receipt(args.source_receipt, source_home)
    for packet_doc in (args.new_validation, args.new_handoff):
        require_file(packet_doc)
    literal_diff = verify_diff(candidate, final_manifest)
    controls_command = run_controls(candidate, output_dir)

    (output_dir / "binding-receipt.json").write_text(json.dumps({"old_binding_sha256": digest(args.old_binding.read_bytes()), "new_binding_sha256": digest(args.new_binding.read_bytes()), "source_home_receipt": final_receipt, "old_packet": old_binding, "new_packet": new_binding}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "literal-diff.json").write_text(json.dumps(literal_diff, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_dir / "source-manifest.json").write_bytes(args.new_source_manifest.read_bytes())
    (output_dir / "validation.md").write_text("""# D141s final literal validation\n\n- Authenticated candidate baseline: `2733c720c555c2853ce73b5b74d7896aa1fe8b38` / `eb04b6da47a320f0920ae7dd53d95b0ac85928a9`.\n- Authenticated App HOME: `4de54db14bdc9ddc2ce2e5887258b03acbffd30d` / `84c3fb7f73f08c22220f8e808962fe3f24aaa0aa`.\n- Authenticated old 5344 packet and final 0545 packet; registration remains false and no body was run.\n- Candidate diff is exactly the finite mapping in `literal-diff.json`; modes and manifest predecessors are unchanged.\n- Existing controls: **74 PASS**, `SEC001 PASS`, `SEC002 PASS`.\n- Existing-control invocation: `%s`.\n""" % controls_command, encoding="utf-8")
    (output_dir / "handoff.md").write_text("""# D141s final literal handoff\n\nThe candidate is ready for the manager's CAS checker. Re-run `check-final-binding.py` unchanged with the same `--candidate`, authenticated App `--source-home`/`--source-receipt`, old 5344 packet paths, and final 0545 packet paths. This evidence claims literal completion and the existing 74-control result only; it claims no install, registration, queue admission, preflight, body, release, or PASS_INSTALL.\n""", encoding="utf-8")
    print("PASS: authenticated final packet, finite literal diff, unchanged predecessors, and 74 controls")
    return 0


if __name__ == "__main__":
    main()
