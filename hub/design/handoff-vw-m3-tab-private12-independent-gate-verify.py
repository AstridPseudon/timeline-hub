#!/usr/bin/env python3
"""Read-only physical graph snapshot and exact copy comparator."""
import argparse
import hashlib
import json
import os
import stat
from pathlib import Path


def digest_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def snapshot(root):
    root = Path(root)
    assert root.is_absolute() and not root.is_symlink(), root
    entries = {}
    def walk(parent):
        for item in sorted(parent.iterdir()):
            relative = item.relative_to(root).as_posix()
            st = item.lstat()
            mode = st.st_mode
            if stat.S_ISLNK(mode):
                entries[relative] = {"kind": "symlink", "target": os.readlink(item)}
            elif stat.S_ISDIR(mode):
                entries[relative] = {"kind": "directory"}
                walk(item)
            elif stat.S_ISREG(mode):
                entries[relative] = {"kind": "file", "sha256": digest_file(item), "size": st.st_size, "executable": bool(mode & 0o111)}
            else:
                raise AssertionError(f"Unsupported graph entry: {item}")
    walk(root)
    payload = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return {"root": str(root), "sha256": hashlib.sha256(payload).hexdigest(), "entries": entries}


def compare_copy(baseline, root):
    current = snapshot(root)
    before = baseline["entries"]
    after = current["entries"]
    return {"beforeSha256": baseline["sha256"], "afterSha256": current["sha256"], "added": sorted(after.keys() - before.keys()), "removed": sorted(before.keys() - after.keys()), "changed": sorted(k for k in before.keys() & after.keys() if before[k] != after[k])}


def audit_evidence(baseline):
    import base64
    import io
    import subprocess
    import tarfile
    root = Path(baseline["root"])
    design = Path(__file__).parent
    audit = json.loads((design / "handoff-vw-m3-tab-package-additions-audit-REPORT.json").read_text())
    old = json.loads((design.parent / "workers/vw-m3-tab-discovery-fix/owned-source-fingerprint.json").read_text())
    excluded = {x["package"] + "/" + x["relativeEntry"]: x for x in audit["addedEntries"]}
    entries = baseline["entries"]
    for rel, expected in excluded.items():
        assert entries[rel] == {"kind": "symlink", "target": expected["target"]}
    links = []
    for rel, entry in entries.items():
        if entry["kind"] != "symlink":
            continue
        path = root / rel
        physical = (path.parent / entry["target"]).resolve(strict=False)
        links.append(dict(path=rel, target=entry["target"], resolved=str(physical), selfTargeting=physical == path.parent.resolve(), authorizedExclusion=rel in excluded))
    remaining = [x for x in links if x["selfTargeting"] and not x["authorizedExclusion"]]
    assert len(links) == 193 and sum(x["selfTargeting"] for x in links) == 152 and len(remaining) == 147
    def encoded(x):
        return json.dumps(x, separators=(",", ":"), ensure_ascii=False).encode()
    def sha(x):
        return hashlib.sha256(x).hexdigest()
    selected = {}
    for package in old["packages"]:
        rows = []
        prefix = package + "/"
        for rel in sorted(entries, key=lambda k: tuple(k.split("/"))):
            entry = entries[rel]
            if not rel.startswith(prefix) or rel in excluded or entry["kind"] == "directory":
                continue
            kind = "symlink" if entry["kind"] == "symlink" else "executable" if entry["executable"] else "file"
            digest = sha(entry["target"].encode()) if kind == "symlink" else entry["sha256"]
            rows.append([rel[len(prefix):], kind, digest])
        version = json.loads((root / package / "package.json").read_text())["version"]
        selected[package] = dict(version=version, tree=dict(sha256=sha(encoded(rows)), fileCount=len(rows)))
    selected_hash = sha(encoded(selected))
    assert selected_hash == audit["grantComparison"]["oldPackageGraphHash"]
    frozen = "5117b9da2e17828ec0b3cfbcdf3ff4987dc77ab3"
    def git_bytes(path):
        return subprocess.check_output(["git", "show", frozen + ":" + path], cwd="/home/user/work/app")
    manifest = git_bytes("package.json")
    lock_bytes = git_bytes("package-lock.json")
    artifact_path = "vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz"
    artifact = git_bytes(artifact_path)
    lock = json.loads(lock_bytes)["packages"]["node_modules/@banodoco/timeline-composition"]
    assert lock["version"] == "0.0.12" and lock["resolved"] == "file:" + artifact_path
    assert lock["integrity"] == "sha512-" + base64.b64encode(hashlib.sha512(artifact).digest()).decode()
    assert sha(artifact) == "0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3"
    members = []
    with tarfile.open(fileobj=io.BytesIO(artifact)) as archive:
        for member in archive.getmembers():
            assert member.isfile() and member.name.startswith("package/") and ".." not in Path(member.name).parts
            members.append(dict(path=member.name.removeprefix("package/"), bytes=member.size, sha256=sha(archive.extractfile(member).read())))
    assert len(members) == 77
    supplied = json.loads((design / "handoff-vw-m3-app-private-clean12-graph-frozen12-members.json").read_text())
    assert members == supplied
    peer_reference = json.loads((design / "handoff-vw-m3-app-current-viewer-cut-source.json").read_text())["peer_manifests"]
    peers = {}
    for name, expected in peer_reference.items():
        data = (root / name / "package.json").read_bytes()
        assert sha(data) == expected["manifest_sha256"]
        assert json.loads(data)["version"] == expected["version"]
        peers[name] = dict(manifestSha256=sha(data), **selected[name])
    return dict(status="REJECT", frozenSource=frozen, frozenManifestSha256=sha(manifest), frozenLockSha256=sha(lock_bytes), artifactSha256=sha(artifact), artifactMemberCount=len(members), artifactMembers=members, selected11FilteredHash=selected_hash, selected11IsWholeGraph=False, sixPeerChecks=peers, remainingSelfTargetingLinkCount=len(remaining), remainingSelfTargetingLinks=remaining, privateGraphVerified=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["snapshot", "compare", "evidence"])
    parser.add_argument("root")
    parser.add_argument("output")
    parser.add_argument("--baseline")
    args = parser.parse_args()
    free = os.statvfs(args.root).f_bavail * os.statvfs(args.root).f_frsize
    assert free >= 10 * 1024**3, f"Below 10 GiB floor: {free}"
    if args.command == "snapshot":
        result = snapshot(args.root)
        count = len(result["entries"])
    elif args.command == "evidence":
        result = audit_evidence(json.loads(Path(args.baseline).read_text()))
        count = result["remainingSelfTargetingLinkCount"]
    else:
        result = compare_copy(json.loads(Path(args.baseline).read_text()), args.root)
        count = {k: len(result[k]) for k in ["added", "removed", "changed"]}
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"output": args.output, "freeBytes": free, "count": count, "sha256": result.get("sha256"), "beforeSha256": result.get("beforeSha256"), "afterSha256": result.get("afterSha256")}))

if __name__ == "__main__":
    main()
