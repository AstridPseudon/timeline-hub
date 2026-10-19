#!/usr/bin/env python3
"""Materialize four current candidates; historical refs stay on GitHub."""
import argparse, json, pathlib, subprocess, sys

def git(*args):
    return subprocess.run(["git", *map(str, args)], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", required=True, help="handover-manifest.json in the receiving Astrid control checkout")
    p.add_argument("--destination", required=True, help="explicit new or empty workspace directory")
    a = p.parse_args()
    manifest = json.loads(pathlib.Path(a.manifest).read_text())
    refs = manifest.get("receiving_clones") or []
    host_url = (manifest.get("host_repository") or {}).get("url")
    host_checkout = pathlib.Path(a.manifest).resolve().parents[3]
    root = pathlib.Path(a.destination).expanduser().absolute()
    def reject_symlinks(path):
        for component in (path, *path.parents):
            if component.is_symlink():
                p.error(f"refusing symlink in destination path: {component}; choose a canonical real path")
    reject_symlinks(root)
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        p.error("destination exists and is not an empty directory; choose a new empty directory")
    if len(refs) != 4 or {r.get("role") for r in refs} != {"sdk", "runtime", "app", "composition"}:
        p.error("manifest must select exactly the four current product candidates")
    targets = set()
    for ref in refs:
        relative = pathlib.Path(ref.get("directory", ""))
        if (ref.get("kind") != "candidate" or not relative.parts
                or relative.is_absolute() or ".." in relative.parts):
            p.error("manifest must contain safe relative directories for current candidates only")
        target = root / relative
        reject_symlinks(target)
        if target in targets or target.exists():
            p.error(f"refusing existing or duplicate clone path: {target}")
        targets.add(target)
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    for ref in refs:
        if ref.get("role") == "host":
            continue
        if ref.get("kind") != "candidate":
            p.error("preservation refs are not cloned by default; fetch them from GitHub on demand")
        target = root / ref["directory"]
        if target.exists():
            p.error(f"refusing to overwrite existing clone path: {target}")
        branch_ref = ref["ref"] if ref["ref"].startswith("refs/heads/") else f"refs/heads/{ref['ref']}"
        if ref["url"] == host_url:
            top = git("-C", host_checkout, "rev-parse", "--show-toplevel")
            if pathlib.Path(top).resolve() != host_checkout:
                p.error("handover manifest is not inside the expected Astrid host checkout")
            origin = git("-C", host_checkout, "remote", "get-url", "origin")
            if origin != host_url:
                p.error(f"host checkout origin differs from the pinned publication URL: {origin}")
            tracking_ref = "refs/remotes/origin/" + branch_ref.removeprefix("refs/heads/")
            subprocess.run(["git", "-C", str(host_checkout), "fetch", "--filter=blob:none",
                            "--no-tags", "origin", f"+{branch_ref}:{tracking_ref}"], check=True)
            fetched = git("-C", host_checkout, "rev-parse", tracking_ref)
            fetched_tree = git("-C", host_checkout, "rev-parse", f"{fetched}^{{tree}}")
            if fetched != ref["commit"] or fetched_tree != ref["tree"]:
                p.error(f"shared-repository candidate pin mismatch for {ref['role']}: {fetched}/{fetched_tree}")
            subprocess.run(["git", "-C", str(host_checkout), "worktree", "add", "--detach",
                            str(target), ref["commit"]], check=True)
            head = git("-C", target, "rev-parse", "HEAD")
            tree = git("-C", target, "rev-parse", "HEAD^{tree}")
            if head != ref["commit"] or tree != ref["tree"]:
                p.error(f"pinned worktree identity mismatch for {ref['directory']}: {head}/{tree}")
            print(f"verified {ref['role']} {ref['kind']} worktree sharing Astrid host object store: {head} tree {tree}")
            continue
        subprocess.run(["git", "clone", "--filter=blob:none", "--single-branch", "--no-tags",
                        "--no-checkout", "--branch", ref["ref"], ref["url"], str(target)], check=True)
        fetched = git("-C", target, "rev-parse", f"refs/remotes/origin/{ref['ref']}")
        if fetched != ref["commit"]:
            p.error(f"candidate branch moved since the manifest was sealed: {ref['role']} {fetched} != {ref['commit']}")
        subprocess.run(["git", "-C", str(target), "checkout", "--detach", ref["commit"]], check=True)
        head = git("-C", target, "rev-parse", "HEAD")
        tree = git("-C", target, "rev-parse", "HEAD^{tree}")
        if head != ref["commit"] or tree != ref["tree"]:
            p.error(f"pinned identity mismatch for {ref['directory']}: {head}/{tree}")
        print(f"verified {ref['role']} {ref['kind']}: {head} tree {tree}")
    print("Materialized only four current candidates; the same-repository SDK candidate uses a separate worktree sharing the Astrid control checkout object store, and other candidates use filtered single-branch clones. Preservation refs remain on GitHub for on-demand fetch; no dependencies were installed.")

if __name__ == "__main__":
    main()
