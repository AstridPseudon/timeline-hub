#!/usr/bin/env python3
"""Refresh the reviewed fork recipe; users run neither this script nor Git.

python scripts/refresh_omp_recipe.py --producer-repo /path/to/oh-my-pi \
    --candidate 9e282751c0059e37d2f6fbc14ffa0b450710bd23 --cache /tmp/omp-archives

Review the resulting JSON and unified diff together. The source tree pin is
independent of gzip/tar container bytes; every native tarball has SHA256 and SRI.
"""

from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from astrid.installer.tools import (  # noqa: E402
    _apply_omp_patch,
    extract,
    local_source,
    source_tree_sha256,
)

BASE = "9962a46db1e8340320a0f2fb276964f957985505"
FILES = ("packages/coding-agent/src/main.ts", "packages/coding-agent/src/modes/acp/acp-agent.ts",
         "packages/coding-agent/src/modes/acp/acp-mode.ts")
TARGETS = {"linux-x64": "linux-x64", "linux-arm64": "linux-arm64", "macos-x64": "darwin-x64",
           "macos-arm64": "darwin-arm64", "windows-x64": "win32-x64"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer-repo", required=True, type=Path)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1] / "astrid/installer/omp")
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    args.output.mkdir(parents=True, exist_ok=True)

    def git(*argv):
        return subprocess.check_output(["git", "-C", str(args.producer_repo), *argv])

    candidate = git("rev-parse", "--verify", args.candidate + "^{commit}").decode().strip()
    changed = set(git("diff", "--name-only", BASE, candidate, "--", "packages/coding-agent/src").decode().splitlines())
    if changed != set(FILES):
        raise ValueError(f"Expected exactly the three reviewed production files, got {changed}")
    patch = git("-c", "color.ui=false", "diff", "--no-ext-diff", "--no-textconv", "--full-index",
                BASE, candidate, "--", *FILES)
    rows = []
    for name in FILES:
        before, after = git("show", BASE + ":" + name), git("show", candidate + ":" + name)
        old, new = before.decode("utf-8").splitlines(keepends=True), after.decode("utf-8").splitlines(keepends=True)
        edits = [{"start": i, "old": old[i:j], "new": new[k:end]}
                 for tag, i, j, k, end in difflib.SequenceMatcher(a=old, b=new, autojunk=False).get_opcodes()
                 if tag != "equal"]
        rows.append({"path": name, "before_sha256": sha(before), "after_sha256": sha(after), "edits": edits})
    with tempfile.TemporaryDirectory(prefix="omp-recipe-") as temporary:
        folder = Path(temporary)
        local_source(str(args.producer_repo.resolve()), BASE, folder / "source.tar")
        extract(folder / "source.tar", folder / "source")
        tree = source_tree_sha256(folder / "source")
        _apply_omp_patch(folder / "source", {"files": rows})
    recipe = {"schema_version": 1, "version": "17.4.0", "bun_version": "1.3.14",
              "repository": "https://github.com/peteromallet/oh-my-pi", "base_commit": BASE,
              "reviewed_candidate_commit": candidate,
              "source": {"url": f"https://codeload.github.com/peteromallet/oh-my-pi/tar.gz/{BASE}",
                         "directory": "oh-my-pi-" + BASE, "tree_sha256": tree},
              "bun_lock_sha256": sha(git("show", BASE + ":bun.lock")),
              "patch": {"sha256": sha(patch), "files": rows}, "native": {}}
    for target, tag in TARGETS.items():
        package = "@oh-my-pi/pi-natives-" + tag
        with urllib.request.urlopen(f"https://registry.npmjs.org/{package}/17.4.0", timeout=120) as response:
            metadata = json.load(response)
        dist = metadata["dist"]
        if metadata["name"] != package or metadata["version"] != "17.4.0" or not dist["tarball"].startswith("https://"):
            raise ValueError("Unexpected native package identity or transport.")
        archive = args.cache / (package.rsplit("/", 1)[1] + "-17.4.0.tgz")
        if not archive.exists():
            with urllib.request.urlopen(dist["tarball"], timeout=120) as response, archive.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
        content = archive.read_bytes()
        integrity = "sha512-" + base64.b64encode(hashlib.sha512(content).digest()).decode()
        if integrity != dist["integrity"]:
            raise ValueError(f"Native SRI mismatch: {package}")
        with tarfile.open(archive) as bundle:
            files = sorted(member.name.removeprefix("package/") for member in bundle
                           if member.isfile() and member.name.endswith(".node"))
        baseline = f"pi_natives.{tag}-baseline.node"
        modern = f"pi_natives.{tag}-modern.node"
        valid = (files in ([baseline], sorted([baseline, modern])) if tag.endswith("-x64")
                 else files == [f"pi_natives.{tag}.node"])
        if not valid:
            raise ValueError(f"Unexpected native variants: {package}: {files}")
        recipe["native"][target] = {"url": dist["tarball"], "sha256": sha(content),
                                    "integrity": integrity, "files": files}
    (args.output / "source.patch").write_bytes(patch)
    (args.output / "recipe.json").write_text(json.dumps(recipe, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_tree_sha256": tree, "patch_sha256": sha(patch),
                      "candidate": candidate, "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
