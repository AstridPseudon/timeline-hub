# Receiving setup

1. Extract the ZIP into a new destination that does not exist and read `transfer/ZIP-REFERENCE.json`. Choose a host checkout destination that does not exist. Clone its exact branch/URL, checkout the ZIP-pinned commit, and verify `HEAD` and tree. The host branch carries this control directory. Do not copy the original `.otto` tree.
2. From the host checkout, run `python3 docs/projects/timeline-r4/scripts/clone-pinned.py --manifest docs/projects/timeline-r4/handover-manifest.json --destination <new-empty-workspace>`. The helper refuses a nonempty destination and creates only the four current product candidates. When the SDK remote matches the Astrid host URL, it uses a separate SDK candidate worktree sharing the host object store and leaves the tracked control checkout intact; other product repositories use single-branch, blob-filtered clones. Each commit/tree is checked. Historical preservation/WIP refs stay on GitHub for on-demand fetch.
3. Before a standalone Composition install, materialize the schema sibling described below. Install only the compatible tools and dependencies actually consumed from the checked-out repositories’ pinned lockfiles/manifests. Source observations were Node 20.19.4, Codex CLI 0.162.1 (Apple arm64), and Python 3.11.11 for the qualified Runtime wheel build; these observations do not assert receiver compatibility. Check the configured role models and efforts on the new host; no silent model substitution is authorized.
4. The published Megado base is pinned in `transfer/skills/PIN-AND-AMENDMENTS.md`. Clone it into a destination that does not exist, checkout the exact commit in that file, and compare the included amended snapshots. If the skills checkout or tool is unavailable, read the included `transfer/skills/megado/` files and `transfer/tools/codex-exec-dispatch.py` directly; do not install over an existing skills/tool directory.
5. The hourly and three-hour prompts are optional receiving scheduling setup in the ZIP. Both source-machine schedules are paused; do not bind a receiving schedule to old thread IDs. Retained advisory reports/counters are historical inputs.

## Local Composition schema layout

Standalone `composition-candidate` at `c82eb7c459d0a41263954bf007071a6a0e8e0a6a` declares `@banodoco/timeline-schema: file:../timeline-schema`. The exact source already lives in `app-candidate/vendor/timeline-schema` v0.0.2 at App commit `8f0c2484463e9b666d184a744d52e252984e551a`. No fifth repository is needed. Before installing standalone Composition, set `CANDIDATE_WORKSPACE` to the helper’s workspace and materialize only that tracked source into a new sibling; do not change candidate source or overwrite a destination:

```sh
python3 - "$CANDIDATE_WORKSPACE" <<'PYSCHEMA'
import io, os, pathlib, subprocess, sys, tarfile
root = pathlib.Path(sys.argv[1]).expanduser().absolute()
if any(p.is_symlink() for p in (root, *root.parents)):
    raise SystemExit('choose a canonical workspace without symlink ancestors')
app, dst = root / 'app-candidate', root / 'timeline-schema'
pin = '8f0c2484463e9b666d184a744d52e252984e551a'
if dst.exists() or dst.is_symlink() or app.is_symlink():
    raise SystemExit('schema destination exists or App is a symlink; do not overwrite')
head = subprocess.check_output(['git', '-C', str(app), 'rev-parse', 'HEAD'], text=True).strip()
if head != pin:
    raise SystemExit('App is not the exact pinned schema source')
blob = subprocess.check_output(['git', '-c', 'tar.umask=0022', '-C', str(app), 'archive', '--format=tar', pin, 'vendor/timeline-schema'])
with tarfile.open(fileobj=io.BytesIO(blob)) as archive:
    files = []
    for member in archive.getmembers():
        parts = pathlib.PurePosixPath(member.name).parts
        if member.isdir():
            if parts not in [('vendor',), ('vendor', 'timeline-schema')] and parts[:2] != ('vendor', 'timeline-schema'):
                raise SystemExit('unexpected archive directory')
            continue
        if parts[:2] != ('vendor', 'timeline-schema') or '..' in parts:
            raise SystemExit('unexpected archive path')
        if not member.isfile():
            raise SystemExit('schema archive contains a link or special file')
        files.append((parts[2:], member.mode & 0o777, archive.extractfile(member).read()))
    if not files:
        raise SystemExit('empty schema source')
    dst.mkdir()
    for parts, mode, data in files:
        target = dst.joinpath(*parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as output:
            output.write(data)
        os.chmod(target, mode)
PYSCHEMA
```

This materializes exact tracked source only. Qualify the consumed schema/version/layout with the actual Composition install/build; source availability is not an installation PASS. App’s own `file:vendor/` composition/ops/schema/theme links resolve inside its pinned candidate; avoid replacing those vendor sources by assumption.

## Conditional dependencies and qualification

SDK core dependencies are registry packages; Runtime’s declared core dependency list is empty and the transferred exact qualified wheel was built with `--no-deps`. Receiving compatibility is still untested. Activate only extras/packs actually needed:

- SDK development schema: `https://github.com/banodoco/ArtAgents.git@242f9c4306bf3b501222cb041a9eb246ef47bc85#subdirectory=packages/timeline-schema/python`.
- SDK development Sisypy: source manifests use `dfb3fa3`; the read-only resolved full commit is `dfb3fa3e71e4130df081d1d15d62f57f6e8ebb87` at `https://github.com/peteromallet/sisypy.git`.
- Optional `runpod-lifecycle>=0.3.1.dev0,<0.4` requires an authorized private index/wheelhouse only if RunPod is activated. No origin credentials/environment are shipped.
- SDK per-pack `requirements.txt` remain scoped prerequisites when that pack is consumed; this audit did not enumerate or certify every optional pack. Do not install all unused extras or copy an origin environment.

The six exact Megado amendments and portable dispatcher are supplied; the origin-only package builder is intentionally omitted. No install, product journey, render or release execution was certified by the handover audit.
