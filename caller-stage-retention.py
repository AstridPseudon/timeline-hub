#!/usr/bin/env python3
"""D21 offline control for retaining Playwright diagnostics by caller stage.

This is a prepared caller artifact, not a replacement for either live suite
row.  It reads the two existing rows, locks their selected source/body
identities, syntax-checks the decoded shell, and runs a tiny installed
Playwright test with no page, browser, server, Runtime, Agent, or App import.
The fixture intentionally uses the real Playwright runner so the old same-root
loss and the child-directory correction are measured rather than mocked.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile


ORCH_ROOT = Path(
    os.environ.get(
        "TIMELINE_ORCH_ROOT",
        "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch",
    )
).resolve()
SUITES = ORCH_ROOT / "tests" / "suites.conf"
P2_SUITE = "full-e2e-three-products"
P3_SUITE = "ap2-P3-gate5-h6-0348"
APP_SOURCE = "c0fe88994405fd517b58473c14678a0d1b73056d"
AGENT_SOURCE = "079580ca46af77e0292d49dc34386b25c8391f99"
RUNTIME_SOURCE = "37eb6c7bdb79dcae2523883e66b5cea5be721ffd"

# These are the hashes asserted by the actual selected caller rows.  The
# selected source commit is authoritative; the current integration branch may
# contain later unrelated changes to a body.
BODY_LOCKS = {
    "tests/e2e/local/three-products.p2-tour.spec.ts": (
        "45a8088fafd72a462409e444c0294e8a35682a0f",
        "533461d30e94fd2b2eae8877b77f3909ab578eb71429f47a6b7b217ca517ce76",
    ),
    "tests/e2e/local/three-products.p2-elements-assets.spec.ts": (
        "836d144bc0e3bbd8f1677d23e96385bcd8127daa",
        "e98bb092a37a449da7efd76981d32f24d79d00702b46f192527edc64ffd3b5b0",
    ),
    "tests/e2e/local/three-products.p2-popup.spec.ts": (
        "8072fcee4da01fc5dc39852c645af959251ae153",
        "722b7e9f938cefe0dfe625fabc89b4486b6968a56e6bc727e28c73b3883f8b8e",
    ),
    "tests/e2e/local/three-products.spec.ts": (
        "37caf28577d42fbe98afd2320dffa3c72e6e74b1",
        "0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14",
    ),
}

P2_BODY_ARGS = [
    "npm",
    "run",
    "test:e2e:three-products",
    "--",
    "tests/e2e/local/three-products.p2-tour.spec.ts",
    "tests/e2e/local/three-products.p2-elements-assets.spec.ts",
    "tests/e2e/local/three-products.p2-popup.spec.ts",
]
P3_MOUNTED_ARGS = [
    "npm",
    "run",
    "test:e2e:three-products",
    "--",
    "tests/e2e/local/three-products.mounted-readiness.spec.ts",
]
P3_GATE5_ARGS = [
    "npm",
    "run",
    "test:e2e:three-products",
    "--",
    "--grep",
    r"M2 real gate 5 \(M1 real mounted path\): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent$",
]


class ControlError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ControlError(message)


def selected_rows() -> tuple[list[str], dict[str, tuple[int, str]]]:
    require(SUITES.is_file() and not SUITES.is_symlink(), f"missing suites file: {SUITES}")
    lines = SUITES.read_text(encoding="utf-8").splitlines(keepends=True)
    found: dict[str, tuple[int, str]] = {}
    for index, line in enumerate(lines, 1):
        fields = line.split(maxsplit=2)
        if len(fields) >= 2 and fields[0] == "app" and fields[1] in {P2_SUITE, P3_SUITE}:
            require(fields[1] not in found, f"duplicate selected row: {fields[1]}")
            found[fields[1]] = (index, line)
    require(set(found) == {P2_SUITE, P3_SUITE}, "the two selected app rows were not found exactly once")
    return lines, found


def row_command(row: str) -> str:
    fields = row.rstrip("\n").split(maxsplit=2)
    require(len(fields) == 3, "selected row has no command")
    command = fields[2]
    if command.startswith("unset "):
        require(";" in command, "unset row has no command separator")
        command = command.split(";", 1)[1].lstrip()
    return command


def source_body_checks(repo: Path, rows: dict[str, tuple[int, str]]) -> dict[str, str]:
    require(repo.is_dir(), f"App checkout is missing: {repo}")
    for name, (blob, sha) in BODY_LOCKS.items():
        selected_blob = run(["git", "rev-parse", f"{APP_SOURCE}:{name}"], cwd=repo)
        require(selected_blob.returncode == 0, f"cannot read selected body: {name}")
        require(selected_blob.stdout.strip() == blob, f"selected body blob changed: {name}")
        selected_bytes = run(["git", "show", f"{APP_SOURCE}:{name}"], cwd=repo)
        require(selected_bytes.returncode == 0, f"cannot hash selected body: {name}")
        require(digest(selected_bytes.stdout.encode()) == sha, f"selected body SHA changed: {name}")

    p2 = rows[P2_SUITE][1]
    p3 = rows[P3_SUITE][1]
    for marker in (
        f"P2A={AGENT_SOURCE}", f"P2R={RUNTIME_SOURCE}", f"P2APP={APP_SOURCE}",
        'P2FAIL=', "p2stop()", "original-body-NOTRUN", "PLAYWRIGHT_OUTPUT_DIR=",
        "missing-receipt:", "ASTRID_APP_DIRECT_DOOR_PORT", "P2-tour-body-blob",
    ):
        require(marker in p2, f"P2 guard missing from live row: {marker}")
    for marker in (
        f"P3A={AGENT_SOURCE}", f"P3R={RUNTIME_SOURCE}", f"P3APP={APP_SOURCE}",
        'P3FAIL=', "original-body-NOTRUN", "PLAYWRIGHT_OUTPUT_DIR=",
        "ASTRID_APP_DIRECT_DOOR_PORT", "Gate5-body-git-hash", "p3fail",
    ):
        require(marker in p3, f"P3 guard missing from live row: {marker}")
    require("$ACTUAL_RUN_DIR/playwright-output" in p2, "P2 real output root not found")
    require("$P3O/tests/$RUN_ID/playwright-output" in p3, "P3 real output root not found")
    return {
        "p2_line": str(rows[P2_SUITE][0]),
        "p3_line": str(rows[P3_SUITE][0]),
    }


def argv_checks(rows: dict[str, tuple[int, str]]) -> dict[str, object]:
    p2 = rows[P2_SUITE][1]
    p3 = rows[P3_SUITE][1]
    p2_command = row_command(p2)
    p3_command = row_command(p3)
    for label, command in ((P2_SUITE, p2_command), (P3_SUITE, p3_command)):
        checked = run(["bash", "-n", "-c", command])
        require(checked.returncode == 0, f"bash -n failed for {label}: {checked.stderr.strip()}")

    p2_literal = " ".join(P2_BODY_ARGS)
    require(p2_literal in p2, "P2 body argv changed")
    require(" ".join(P3_MOUNTED_ARGS) in p3, "P3 mounted argv changed")
    require(P3_GATE5_ARGS[0:5] == ["npm", "run", "test:e2e:three-products", "--", "--grep"], "P3 argv control malformed")
    require("--grep '" + P3_GATE5_ARGS[-1] + "'" in p3, "P3 Gate5 grep argv changed")
    return {
        "p2_body_argv": P2_BODY_ARGS,
        "p2_body_outer_argc": len(P2_BODY_ARGS) - 1,
        "p3_mounted_argv": P3_MOUNTED_ARGS,
        "p3_mounted_outer_argc": len(P3_MOUNTED_ARGS) - 1,
        "p3_gate5_argv": P3_GATE5_ARGS,
        "p3_gate5_outer_argc": len(P3_GATE5_ARGS) - 1,
        "bash_n": "PASS",
    }


def inventory(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ControlError(f"unexpected symlink in output root: {path}")
        if path.is_file():
            result[str(path.relative_to(root))] = digest(path.read_bytes())
    return result


def contained(child: Path, parent: Path) -> None:
    require(not child.is_symlink(), f"stage child is a symlink: {child}")
    require(child.resolve().is_relative_to(parent.resolve()), f"stage child escaped root: {child}")


def fixture_source() -> tuple[str, str]:
    config = """const { defineConfig } = require(process.env.PLAYWRIGHT_TEST_PACKAGE);\nmodule.exports = defineConfig({\n  testDir: __dirname,\n  testMatch: 'retention.spec.cjs',\n  outputDir: process.env.PLAYWRIGHT_OUTPUT_DIR,\n  workers: 1,\n  retries: 0,\n  reporter: [['line']],\n});\n"""
    test = """const { test } = require(process.env.PLAYWRIGHT_TEST_PACKAGE);\nconst fs = require('node:fs');\nconst path = require('node:path');\n\ntest('D21 real output fixture', async ({}, info) => {\n  const stage = process.env.RETENTION_STAGE;\n  const output = path.resolve(info.project.outputDir);\n  const write = (relative, bytes) => {\n    const target = info.outputPath(relative);\n    fs.mkdirSync(path.dirname(target), { recursive: true, mode: 0o700 });\n    fs.writeFileSync(target, bytes, { mode: 0o600 });\n    return target;\n  };\n  const readiness = write(`${stage}/readiness.json`, Buffer.from(`readiness:${stage}`));\n  const lifecycle = write(`${stage}/lifecycle.json`, Buffer.from(`lifecycle:${stage}`));\n  const body = write(`${stage}/body/original-body.bin`, Buffer.from(`original-body:${stage}`));\n  const worker = path.join(output, `worker-${info.workerIndex}`);\n  fs.mkdirSync(worker, { recursive: true, mode: 0o700 });\n  fs.writeFileSync(path.join(worker, `${stage}-worker.json`), JSON.stringify({ stage, worker: info.workerIndex }), { mode: 0o600 });\n  await info.attach(`${stage}-readiness`, { path: readiness, contentType: 'application/json' });\n  await info.attach(`${stage}-lifecycle`, { path: lifecycle, contentType: 'application/json' });\n  if (!fs.existsSync(body)) throw new Error('original body artifact was not written');\n});\n"""
    return config, test


def run_fixture(node: str, cli: Path, fixture: Path, output: Path, stage: str) -> None:
    require(not output.exists() or not output.is_symlink(), f"output path is a symlink: {output}")
    output.mkdir(parents=True, mode=0o700, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "PLAYWRIGHT_OUTPUT_DIR": str(output),
            "RETENTION_STAGE": stage,
            "PLAYWRIGHT_TEST_PACKAGE": str(cli.parent / "index.js"),
        }
    )
    result = run([node, str(cli), "test", "--config", str(fixture / "playwright.config.cjs")], cwd=fixture, env=env)
    require(result.returncode == 0, f"Playwright fixture failed for {stage}: {result.stdout[-1000:]}{result.stderr[-1000:]}")


def retention_control(repo: Path) -> dict[str, object]:
    node = shutil.which("node")
    require(node is not None, "node is required for the installed Playwright control")
    node_version = run([node, "--version"])
    require(node_version.returncode == 0, "node --version failed")
    package_root = (repo / "node_modules" / "@playwright" / "test").resolve()
    cli = package_root / "cli.js"
    package_json = json.loads((package_root / "package.json").read_text(encoding="utf-8"))
    require(cli.is_file(), f"installed Playwright CLI missing: {cli}")
    require(package_json.get("version") == "1.60.0", f"unexpected Playwright version: {package_json.get('version')}")

    temp_root = Path(tempfile.mkdtemp(prefix="timeline-d21-stage-retention-"))
    try:
        fixture = temp_root / "fixture"
        fixture.mkdir(mode=0o700)
        config, test = fixture_source()
        (fixture / "playwright.config.cjs").write_text(config, encoding="utf-8")
        (fixture / "retention.spec.cjs").write_text(test, encoding="utf-8")

        same_root = temp_root / "same-output-root"
        run_fixture(node, cli, fixture, same_root, "first-readiness")
        first = inventory(same_root)
        require(first, "same-root first invocation produced no files")
        run_fixture(node, cli, fixture, same_root, "second-later-stage")
        second = inventory(same_root)
        lost = sorted(set(first) - set(second))
        require(lost, "same-root RED was not observed: prior files survived")

        p2_root = temp_root / "actual-request" / "p2"
        p3_root = temp_root / "actual-request" / "p3"
        require(p2_root != p3_root, "P2/P3 roots are not separate")
        p2_stages = ("mounted-readiness", "original-body")
        p3_stages = ("mounted-readiness", "gate5")
        snapshots: dict[str, dict[str, str]] = {}
        for stage in p2_stages:
            child = p2_root / stage
            contained(child, p2_root)
            run_fixture(node, cli, fixture, child, f"p2-{stage}")
            if stage == "mounted-readiness":
                snapshots["p2-mounted-readiness"] = inventory(child)
        require(snapshots["p2-mounted-readiness"] == inventory(p2_root / "mounted-readiness"), "P2 readiness changed")
        require(snapshots["p2-mounted-readiness"], "P2 readiness produced no files")
        p2_body_files = inventory(p2_root / "original-body")
        require(any("original-body.bin" in name for name in p2_body_files), "P2 original body is not in its stage subtree")
        require(snapshots["p2-mounted-readiness"] == inventory(p2_root / "mounted-readiness"), "P2 later stage cleared readiness")

        for stage in p3_stages:
            child = p3_root / stage
            contained(child, p3_root)
            run_fixture(node, cli, fixture, child, f"p3-{stage}")
            if stage == "mounted-readiness":
                snapshots["p3-mounted-readiness"] = inventory(child)
        require(snapshots["p3-mounted-readiness"] == inventory(p3_root / "mounted-readiness"), "P3 readiness changed")
        require(snapshots["p3-mounted-readiness"], "P3 readiness produced no files")
        p3_body_files = inventory(p3_root / "gate5")
        require(any("original-body.bin" in name for name in p3_body_files), "P3 original body is not in its stage subtree")
        require(snapshots["p3-mounted-readiness"] == inventory(p3_root / "mounted-readiness"), "P3 later stage cleared readiness")

        return {
            "node": node_version.stdout.strip(),
            "playwright": package_json["version"],
            "old_same_root": {
                "verdict": "RED (expected)",
                "first_file_count": len(first),
                "second_file_count": len(second),
                "lost_file_count": len(lost),
                "lost_files": lost,
                "first_hashes": first,
                "second_hashes": second,
            },
            "new_child_roots": {
                "verdict": "GREEN",
                "p2_root": str(p2_root),
                "p3_root": str(p3_root),
                "p2_readiness_hashes": snapshots["p2-mounted-readiness"],
                "p2_body_hashes": p2_body_files,
                "p3_readiness_hashes": snapshots["p3-mounted-readiness"],
                "p3_body_hashes": p3_body_files,
            },
        }
    finally:
        shutil.rmtree(temp_root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--static-only", action="store_true", help="skip the real installed Playwright fixture")
    args = parser.parse_args()
    before = SUITES.read_bytes()
    lines, rows = selected_rows()
    source = source_body_checks(args.repo.resolve(), rows)
    argv = argv_checks(rows)
    unrelated_before = digest("".join(line for i, line in enumerate(lines, 1) if i not in {rows[P2_SUITE][0], rows[P3_SUITE][0]}).encode())
    control = {} if args.static_only else retention_control(args.repo.resolve())
    after = SUITES.read_bytes()
    require(before == after, "suites.conf changed during control")
    _, after_rows = selected_rows()
    unrelated_after = digest(b"".join(line for i, line in enumerate(after.splitlines(keepends=True), 1) if i not in {after_rows[P2_SUITE][0], after_rows[P3_SUITE][0]}))
    require(unrelated_before == unrelated_after, "unrelated suites rows changed during control")
    print(json.dumps({
        "status": "PASS",
        "suites": str(SUITES),
        "selected_rows": source,
        "selected_row_sha256": {name: digest(rows[name][1].encode()) for name in rows},
        "unrelated_row_count": len(lines) - 2,
        "unrelated_rows_sha256": unrelated_before,
        "body_locks": BODY_LOCKS,
        "argv": argv,
        "retention": control,
        "adoption": {
            "P2": 'Set PLAYWRIGHT_OUTPUT_DIR to "$ACTUAL_RUN_DIR/playwright-output/p2/<stage>" for mounted-readiness and original-body invocations.',
            "P3": 'Set PLAYWRIGHT_OUTPUT_DIR to "$P3O/tests/$RUN_ID/playwright-output/p3/<stage>" for mounted-readiness and gate5 invocations.',
            "guards": "Keep the existing source/body/port/receipt/export/failfast guards and original-body-NOTRUN branches byte-for-byte; only the output-root assignment changes.",
        },
    }, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ControlError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
