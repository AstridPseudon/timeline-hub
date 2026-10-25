#!/usr/bin/env python3
"""Build the Timeline delivery ZIP.

For each repo: one squashed patch that turns origin/main into the pinned source-tuple tree, and a
git bundle of that same pinned tip. The patch is a single commit on origin/main whose message
lists the first-parent commits of the range. Verification re-applies the patch with git am to a
fresh repository holding only origin/main, checks the bundle, and compares both resulting trees
with the pinned tuple tree. Work repos are only read; delivery writes go to staging and the ZIP,
while verifier roots are private children of the configured work root.

  delivery-build [--dry-run] [--repos "agent runtime"]

The ZIP is not written if any repo fails verification.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import time
import zipfile
from pathlib import PurePosixPath

ORCH = "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch"
DELIVERY = os.path.join(ORCH, "delivery")
TEMPLATE = os.path.join(DELIVERY, "README.template.md")
GATE_RESULTS = os.path.join(DELIVERY, "gate-results.md")
WORK = "/home/user/work"
ALL_REPOS = ["agent", "runtime", "app", "composition"]
BRANCH = "tl/integration"
BASE = "origin/main"
TEST_DIRS = {"tests", "test", "__tests__", "e2e", "spec"}
# Work repos are only read (no index locks). Commits are made only in temp clones.
GIT_ENV = {
    **os.environ,
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_AUTHOR_NAME": "delivery-build",
    "GIT_AUTHOR_EMAIL": "delivery-build@localhost",
    "GIT_COMMITTER_NAME": "delivery-build",
    "GIT_COMMITTER_EMAIL": "delivery-build@localhost",
}


class Refused(RuntimeError):
    """A delivery input failed closed before package writes began."""


def absolute_path(value, label):
    try:
        raw = os.fspath(value)
    except TypeError as exc:
        raise Refused(f"{label} must be an absolute non-symlink path: {value!r}") from exc
    if not isinstance(raw, str) or not os.path.isabs(raw):
        raise Refused(f"{label} must be an absolute non-symlink path: {value!r}")
    path = os.path.normpath(raw)
    if os.path.islink(path):
        raise Refused(f"{label} must be an absolute non-symlink path: {path}")
    return path


def configured(value, *env_names, default):
    if value is not None:
        return value
    for name in env_names:
        if os.environ.get(name):
            return os.environ[name]
    return default


def regular_file(path, label):
    path = absolute_path(path, label)
    if not os.path.isfile(path):
        raise Refused(f"{label} must be an existing regular file: {path}")
    return path


def private_root(path, label):
    path = absolute_path(path, label)
    if os.path.lexists(path) and not os.path.isdir(path):
        raise Refused(f"{label} must be a directory when it exists: {path}")
    return path


def source_tuple(path, expected_sha=None):
    path = regular_file(path, "source tuple")
    with open(path, "rb") as stream:
        raw = stream.read()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if expected_sha is not None and actual_sha != expected_sha:
        raise Refused(f"source tuple SHA mismatch: {actual_sha} != {expected_sha}")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise Refused(f"source tuple is not valid JSON: {path}") from exc
    if not isinstance(value, dict) or set(value) != set(ALL_REPOS):
        raise Refused("source tuple must name exactly agent, runtime, app, composition")
    result = {}
    for name in ALL_REPOS:
        item = value[name]
        if not isinstance(item, dict) or set(item) != {"root", "sha", "tree"}:
            raise Refused(f"source tuple entry {name} must contain exactly root, sha, tree")
        root = absolute_path(item["root"], f"source tuple {name}.root")
        if not os.path.isdir(root):
            raise Refused(f"source tuple {name}.root is not a directory: {root}")
        for field in ("sha", "tree"):
            value_id = item[field]
            if (not isinstance(value_id, str) or len(value_id) != 40
                    or any(char not in "0123456789abcdef" for char in value_id)):
                raise Refused(f"source tuple {name}.{field} must be a lowercase Git object ID")
        result[name] = {"root": root, "sha": item["sha"], "tree": item["tree"]}
    return raw, actual_sha, result


def ancestry(repo, base, tip, name):
    proc = subprocess.run(
        ["git", "-C", repo, "merge-base", "--is-ancestor", base, tip],
        capture_output=True, text=True, env=GIT_ENV, check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        suffix = f": {detail}" if detail else ""
        raise Refused(f"ancestry refused for {name}: repo={repo} base={base} tip={tip}{suffix}")


def preflight_source(name, item):
    repo = item["root"]
    if git(repo, "rev-parse", "--is-inside-work-tree") != "true":
        raise Refused(f"source tuple {name}.root is not a Git worktree: {repo}")
    if git(repo, "status", "--porcelain", "--untracked-files=all"):
        raise Refused(f"source tuple source is dirty: {name} repo={repo}")
    tip = git(repo, "rev-parse", f"{item['sha']}^{{commit}}")
    if tip != item["sha"]:
        raise Refused(f"source tuple tip mismatch for {name}: repo={repo} tip={item['sha']}")
    tree = git(repo, "rev-parse", f"{item['sha']}^{{tree}}")
    if tree != item["tree"]:
        raise Refused(f"source tuple tree mismatch for {name}: repo={repo} tip={item['sha']} tree={item['tree']}")
    base = git(repo, "rev-parse", f"{BASE}^{{commit}}")
    ancestry(repo, base, item["sha"], name)
    return {"name": name, "repo": repo, "base": base, "tip": item["sha"], "tree": item["tree"]}


def preflight_all(source, names):
    resolved = []
    failures = []
    for name in names:
        try:
            resolved.append(preflight_source(name, source[name]))
        except (Refused, RuntimeError) as exc:
            failures.append(str(exc))
    if failures:
        raise Refused("all-repository preflight refused:\n" + "\n".join(failures))
    return resolved


def git(repo, *args):
    proc = subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True, env=GIT_ENV, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:2])}: {(proc.stderr or proc.stdout).strip()[-600:]}")
    return proc.stdout.strip()


def attempt(problems, label, fn, *args):
    """Run fn. A git failure becomes a problem for the README rather than an abort."""
    try:
        return fn(*args)
    except RuntimeError as e:
        problems.append(f"{label}: {e}")
        return None


def fresh_repo(path):
    os.makedirs(path)
    git(path, "init", "-q")
    return path


def private_source_view(name, repo, base, tip, tmp):
    """Return a private read-only object view for the pinned source tuple.

    Bundle creation needs a ref endpoint, but the source checkout is never allowed
    to receive a temporary ref.  Use an alternates-backed private repository with
    refs bound to the already-preflighted base and tip.  All writes are under tmp.
    """
    view = os.path.join(tmp, name, "source-view")
    fresh_repo(view)
    objects = git(repo, "rev-parse", "--git-path", "objects")
    if not os.path.isabs(objects):
        objects = os.path.join(repo, objects)
    objects = os.path.realpath(objects)
    if not os.path.isdir(objects):
        raise RuntimeError(f"source object store is not a directory: {objects}")
    alternates = os.path.join(view, ".git", "objects", "info", "alternates")
    with open(alternates, "w") as f:
        f.write(objects + "\n")
    git(view, "update-ref", "refs/heads/main", base)
    git(view, "update-ref", f"refs/heads/{BRANCH}", tip)
    git(view, "update-ref", "refs/delivery/tip", tip)

    if git(view, "rev-parse", "--is-shallow-repository") != "false":
        raise RuntimeError("private App source view unexpectedly has shallow metadata")
    shallow = git(view, "rev-parse", "--git-path", "shallow")
    if not os.path.isabs(shallow):
        shallow = os.path.join(view, shallow)
    if os.path.exists(shallow):
        raise RuntimeError(f"private App source view has shallow file: {shallow}")
    missing = git(view, "rev-list", "--objects", "--missing=print", base, tip)
    missing = [line for line in missing.splitlines() if line.startswith("?")]
    if missing:
        raise RuntimeError(f"private App source view has {len(missing)} missing reachable object(s)")
    if git(view, "rev-parse", "refs/delivery/tip^{commit}") != tip:
        raise RuntimeError("private App source view changed the pinned tip")
    if git(view, "rev-parse", "refs/delivery/tip^{tree}") != git(repo, "rev-parse", f"{tip}^{{tree}}"):
        raise RuntimeError("private App source view changed the pinned tip tree")
    return view


def is_test(path):
    parts = path.split("/")
    name = parts[-1]
    return (any(p in TEST_DIRS for p in parts[:-1])
            or name.startswith("test_") or name.endswith("_test.py")
            or ".test." in name or ".spec." in name)


def line_split(repo, base, tip):
    """{'product': [files, added, deleted], 'tests': [...]} for origin/main -> tl/integration."""
    totals = {"product": [0, 0, 0], "tests": [0, 0, 0]}
    for line in git(repo, "diff", "--numstat", "--no-renames", base, tip).splitlines():
        added, deleted, path = line.split("\t", 2)
        total = totals["tests" if is_test(path) else "product"]
        total[0] += 1
        total[1] += 0 if added == "-" else int(added)
        total[2] += 0 if deleted == "-" else int(deleted)
    return totals


def squash(name, repo, base, tip, patches, tmp):
    """Write one patch: a commit on origin/main with tl/integration's tree.

    Works whether or not the two share history, because it compares trees. Returns the
    first-parent subjects of the range, which the commit message lists.
    """
    build = fresh_repo(os.path.join(tmp, name, "build"))
    # Fetch immutable object IDs into real local refs.  Ref names from a linked
    # worktree are not guaranteed to be advertised by every local transport.
    fetch = ["fetch", "-q", "--no-tags"]
    fetch += [repo, f"{base}:refs/heads/main", f"{tip}:refs/delivery/tip"]
    git(build, *fetch)
    subjects = git(build, "log", "--first-parent", "--reverse", "--format=%s",
                   "main..refs/delivery/tip").splitlines()
    message = os.path.join(tmp, name, "MESSAGE")
    with open(message, "w") as f:
        f.write(f"Squash {BRANCH} of {name} onto {BASE}\n\n" + "".join(f"- {s}\n" for s in subjects))
    tree = git(build, "rev-parse", "refs/delivery/tip^{tree}")
    commit = git(build, "commit-tree", tree, "-p", "refs/heads/main", "-F", message)
    git(build, "format-patch", "-q", "--binary", "-o", patches, f"main..{commit}")
    return subjects


def verify(name, repo, base, tip, bundle, patches, ranged, tmp, problems):
    """Re-apply the patch to a fresh repo holding origin/main, and check the bundle.

    Both resulting trees must equal tl/integration's tree. Problems are appended to `problems`,
    so the README can say what failed.
    """
    want = git(repo, "rev-parse", f"{tip}^{{tree}}")

    main = fresh_repo(os.path.join(tmp, name, "main"))
    # Keep the prerequisite as a local branch, just as a fresh checkout does.
    # The immutable base ID also makes this independent of source ref layout.
    # Keep the source's real base ancestry: merged side branches can make an
    # older ancestor another bundle prerequisite.  Accept existing shallow
    # boundaries from the source without inventing a new depth-1 boundary.
    fetch = ["fetch", "-q", "--no-tags", "--update-shallow"]
    fetch += [repo, f"{base}:refs/heads/main"]
    attempt(problems, "fetch origin/main", git, main, *fetch)
    attempt(problems, "checkout main", git, main, "checkout", "-q", "main")

    # A ranged bundle needs origin/main as a prerequisite, so it is checked in the main clone.
    # A full bundle is checked in an empty repo, which proves it stands alone.
    bundle_dir = main if ranged else fresh_repo(os.path.join(tmp, name, "bundle-only"))
    attempt(problems, "bundle verify", git, bundle_dir, "bundle", "verify", bundle)
    attempt(problems, "bundle fetch", git, bundle_dir,
            "fetch", "-q", "--no-tags", bundle, f"refs/heads/{BRANCH}:refs/delivery/tip")
    bundle_tip = attempt(problems, "bundle tip", git, bundle_dir, "rev-parse", "refs/delivery/tip^{commit}")
    if bundle_tip is not None and bundle_tip != tip:
        problems.append(f"bundle tip {bundle_tip} != pinned {BRANCH} {tip}")
    bundle_tree = attempt(problems, "bundle tree", git, bundle_dir, "rev-parse", "refs/delivery/tip^{tree}")

    series = sorted(glob.glob(os.path.join(patches, "*.patch")))
    if series:
        attempt(problems, "git am", git, main, "am", "-q", *series)
    else:
        problems.append("no patch to apply")
    applied_tree = attempt(problems, "applied tree", git, main, "rev-parse", "HEAD^{tree}")

    if applied_tree is not None and applied_tree != want:
        problems.append(f"applied tree {applied_tree} != pinned tuple tree {want}")
    if bundle_tree is not None and bundle_tree != want:
        problems.append(f"bundle tree {bundle_tree} != pinned tuple tree {want}")
    return {
        "status": "PASS" if not problems else "FAIL",
        "want_tree": want,
        "applied_tree": applied_tree,
        "bundle_tree": bundle_tree,
        "bundle_tip": bundle_tip,
        "applied": len(series),
    }


def build_repo(resolved, staging, tmp):
    name, repo, base, tip = (resolved[key] for key in ("name", "repo", "base", "tip"))
    source = private_source_view(name, repo, base, tip, tmp)
    result = {
        "name": name,
        "tip": tip,
        "base": base,
        "ahead": int(git(source, "rev-list", "--count", f"{base}..{tip}")),
        "ranged": True,
        "shortstat": git(source, "diff", "--shortstat", base, tip),
        "split": line_split(source, base, tip),
    }
    problems = []

    patches = os.path.join(staging, "patches", name)
    os.makedirs(patches)
    attempt(problems, "squash", squash, name, source, base, tip, patches, tmp)

    bundle = os.path.join(staging, "bundles", f"{name}.bundle")
    os.makedirs(os.path.dirname(bundle), exist_ok=True)
    # Keep the advertised integration ref as the bundle endpoint; git bundle
    # requires a ref endpoint for this ranged form.  The exclusion is pinned.
    # The endpoint is a temporary ref created from the already-validated tuple tip;
    # the source checkout never receives a ref and a moving integration branch is
    # never consulted.
    bundle_args = ["bundle", "create", bundle, BRANCH, f"^{base}"]
    attempt(problems, "bundle create", git, source, *bundle_args)

    result.update(verify(name, repo, base, tip, bundle, patches, True, tmp, problems))
    for ref, pinned in ((BASE, base),):
        current = attempt(problems, f"recheck {ref}", git, repo, "rev-parse", f"{ref}^{{commit}}")
        if current is not None and current != pinned:
            problems.append(f"{ref} moved from pinned {pinned} to {current}")
    result["status"] = "PASS" if not problems else "FAIL"
    result["problems"] = problems
    return result


def short(sha):
    return sha[:12] if sha else "(missing)"


def summary_row(r):
    p, t = r["split"]["product"], r["split"]["tests"]
    kind = "ranged" if r["ranged"] else "full"
    return (f"| {r['name']} | {r['ahead']} | {kind} | {r['applied']} "
            f"| {p[0]} files, +{p[1]} / -{p[2]} | {t[0]} files, +{t[1]} / -{t[2]} "
            f"| **{r['status']}** | {r['seconds']:.0f} |")


def repo_section(r):
    name = r["name"]
    lines = [
        f"### {name}",
        "",
        f"- Pinned tuple tip: `{r['tip']}`",
        f"- `{BASE}`: `{r['base']}`",
        f"- Diff (`git diff --shortstat {BASE}..pinned-tip`): {r['shortstat'] or 'no changes'}",
        (f"- Product: {r['split']['product'][0]} files, +{r['split']['product'][1]} / "
         f"-{r['split']['product'][2]}. Tests: {r['split']['tests'][0]} files, "
         f"+{r['split']['tests'][1]} / -{r['split']['tests'][2]}."),
    ]
    if r["ranged"]:
        lines.append(f"- Bundle: `bundles/{name}.bundle`, ranged: {r['ahead']} commits after `{BASE}`. "
                     f"It needs `{BASE}` present.")
    else:
        lines.append(f"- **Invalid state:** pinned tuple tip is not descended from `{BASE}`.")
    lines.append(f"- Patches: {r['applied']} in `patches/{name}/`.")
    lines.append(f"- Verify: **{r['status']}** ({r['seconds']:.0f}s)")
    lines.append(f"  - tree from `git am` on `{BASE}`: `{short(r['applied_tree'])}`")
    lines.append(f"  - tree from the bundle: `{short(r['bundle_tree'])}`")
    lines.append(f"  - pinned tuple tree: `{short(r['want_tree'])}`")
    for problem in r["problems"]:
        lines.append(f"  - problem: {problem}")
    if r["ranged"]:
        lines.append(f"- Apply: `git switch -c {BRANCH} origin/main` then "
                     f"`git am patches/{name}/*.patch`, or fetch the bundle as described under Applying.")
    else:
        lines.append(f"- Apply: fetch the pinned bundle endpoint into a local `{BRANCH}` ref.")
    lines.append("")
    return "\n".join(lines)


def render_readme(results, template_path, gate_results_path):
    with open(template_path) as f:
        template = f.read()
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    summary = "\n".join([
        "| Repo | Commits | Bundle | Patches | Product | Tests | Verify | Seconds |",
        "|---|---|---|---|---|---|---|---|",
        *[summary_row(r) for r in results],
    ])
    if os.path.exists(gate_results_path):
        with open(gate_results_path) as f:
            gates = f.read().strip()
    else:
        gates = (f"_Not recorded yet. Paste the gate results here before handing over, or put them in "
                 f"`{gate_results_path}` and rebuild._")
    return (template
            .replace("{{UTC}}", now)
            .replace("{{REPO_SUMMARY}}", summary)
            .replace("{{REPO_SECTIONS}}", "\n".join(repo_section(r) for r in results))
            .replace("{{GATE_RESULTS}}", gates))


def write_checksums(staging):
    lines = []
    for root, _, files in os.walk(staging):
        for name in files:
            path = os.path.join(root, name)
            rel = os.path.relpath(path, staging)
            if rel == "SHA256SUMS":
                continue
            with open(path, "rb") as f:
                lines.append(f"{hashlib.sha256(f.read()).hexdigest()}  {rel}")
    with open(os.path.join(staging, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sorted(lines)) + "\n")


def staged_files(staging):
    return sorted(os.path.relpath(os.path.join(root, name), staging)
                  for root, _, files in os.walk(staging) for name in files)


class ExtraError(ValueError):
    """A requested extra cannot be safely added to the delivery staging tree."""


def parse_extra(value):
    """Parse one destination=source input for an existing delivery staging tree."""
    destination, separator, source = value.partition("=")
    if not separator or not destination or not source:
        raise ExtraError("--extra must be DESTINATION=SOURCE")
    if "\\" in destination or "\x00" in destination:
        raise ExtraError("--extra destination must use POSIX separators")
    parts = destination.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ExtraError("--extra destination must stay below the delivery root")
    path = PurePosixPath(destination)
    if path.is_absolute():
        raise ExtraError("--extra destination must stay below the delivery root")
    source_path = os.path.expanduser(source)
    if "\x00" in source_path or os.path.islink(source_path) or not os.path.isfile(source_path):
        raise ExtraError(f"--extra source must be a regular non-symlink file: {source}")
    return path.as_posix(), source_path


def _open_extra_source(source):
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    parent_fd = None
    source_fd = None
    try:
        parent, leaf = os.path.split(source)
        parent_fd = os.open(os.sep if os.path.isabs(parent) else ".", directory_flags)
        for component in parent.split(os.sep):
            if component in ("", "."):
                continue
            child_fd = os.open(component, directory_flags, dir_fd=parent_fd)
            try:
                os.close(parent_fd)
            except BaseException:
                os.close(child_fd)
                raise
            parent_fd = child_fd
        source_fd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        if not stat.S_ISREG(os.fstat(source_fd).st_mode):
            raise ExtraError(f"--extra source must be a regular non-symlink file: {source}")
        os.close(parent_fd)
        parent_fd = None
        fd = source_fd
        source_fd = None
        return fd
    except OSError as e:
        try:
            if source_fd is not None:
                os.close(source_fd)
        finally:
            raise ExtraError(f"--extra source must be a regular non-symlink file: {source}") from e
    except BaseException:
        if source_fd is not None:
            os.close(source_fd)
        raise
    finally:
        if parent_fd is not None:
            os.close(parent_fd)


def _preflight_extra_destinations(staging, extras):
    destinations = [destination for destination, _ in extras]
    if len(destinations) != len(set(destinations)):
        raise ExtraError("--extra destinations must be unique")
    if {"README.md", "SHA256SUMS"}.intersection(destinations):
        raise ExtraError("--extra destination is reserved by the delivery packer")

    destination_set = set(destinations)
    for destination in destinations:
        parts = destination.split("/")
        for index in range(1, len(parts)):
            parent = "/".join(parts[:index])
            if parent in destination_set:
                raise ExtraError(f"--extra destination parent collides with another extra: {parent}")

        for index in range(1, len(parts)):
            parent = os.path.join(staging, *parts[:index])
            try:
                mode = os.lstat(parent).st_mode
            except FileNotFoundError:
                continue
            if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                raise ExtraError(f"--extra destination parent is not a directory: {destination}")

        target = os.path.join(staging, *parts)
        if os.path.lexists(target):
            raise ExtraError(f"--extra destination already exists: {destination}")


def _open_extra_parent(staging, parts):
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open(staging, flags)
    try:
        for part in parts[:-1]:
            try:
                child = os.open(part, flags, dir_fd=fd)
            except FileNotFoundError:
                try:
                    os.mkdir(part, 0o755, dir_fd=fd)
                except FileExistsError:
                    pass
                child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def _copy_extra(source_fd, staging, destination):
    parts = destination.split("/")
    parent_fd = _open_extra_parent(staging, parts)
    destination_fd = None
    try:
        destination_fd = os.open(
            parts[-1],
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o644,
            dir_fd=parent_fd,
        )
        os.lseek(source_fd, 0, os.SEEK_SET)
        while True:
            block = os.read(source_fd, 1024 * 1024)
            if not block:
                break
            view = memoryview(block)
            while view:
                written = os.write(destination_fd, view)
                view = view[written:]
    finally:
        if destination_fd is not None:
            os.close(destination_fd)
        os.close(parent_fd)


def add_extras(staging, values):
    """Copy explicitly named, regular files into the normal delivery staging tree."""
    extras = [parse_extra(value) for value in values]
    _preflight_extra_destinations(staging, extras)
    source_fds = []
    try:
        for _, source in extras:
            source_fds.append(_open_extra_source(source))
        for (destination, source), source_fd in zip(extras, source_fds):
            try:
                _copy_extra(source_fd, staging, destination)
            except OSError as e:
                detail = e.strerror or str(e)
                raise ExtraError(f"--extra copy failed for {destination}: {detail}") from e
    finally:
        for source_fd in source_fds:
            os.close(source_fd)


def mib(n):
    return f"{n / 1048576:.1f} MiB"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="build and verify everything, print sizes, do not write the ZIP")
    parser.add_argument("--repos", default=" ".join(ALL_REPOS),
                        help='space-separated subset of: %(default)s')
    parser.add_argument("--source-tuple", default=(os.environ.get("TIMELINE_DELIVERY_SOURCE_TUPLE")
                                                     or os.environ.get("TIMELINE_SOURCE_TUPLE")),
                        help="required D59 source tuple JSON (root, sha, tree for all repos)")
    parser.add_argument("--source-tuple-sha", default=os.environ.get("TIMELINE_DELIVERY_SOURCE_TUPLE_SHA"),
                        help="optional SHA256 for the source tuple JSON")
    parser.add_argument("--delivery-root", default=None,
                        help="private delivery root (TIMELINE_DELIVERY_ROOT also accepted)")
    parser.add_argument("--work-root", default=None,
                        help="private verifier work root (TIMELINE_WORK_ROOT also accepted)")
    parser.add_argument("--template", "--template-root", dest="template", default=None,
                        help="README template file (TIMELINE_TEMPLATE also accepted)")
    parser.add_argument("--gate-results", default=None,
                        help="gate-results file (TIMELINE_GATE_RESULTS also accepted)")
    parser.add_argument("--extra", action="append", default=[], metavar="DESTINATION=SOURCE",
                        help="copy an existing regular file into the delivery ZIP (repeatable)")
    args = parser.parse_args()
    expected_sha = os.environ.get("TIMELINE_DELIVERY_SCRIPT_SHA")
    if expected_sha:
        with open(__file__, "rb") as f:
            actual_sha = hashlib.sha256(f.read()).hexdigest()
        if actual_sha != expected_sha:
            parser.error(f"delivery script SHA {actual_sha} != expected {expected_sha}")
    names = args.repos.split()
    unknown = [n for n in names if n not in ALL_REPOS]
    if unknown:
        parser.error(f"unknown repo(s): {', '.join(unknown)}")

    if not names:
        parser.error("at least one repository is required")
    if not args.source_tuple:
        parser.error("source tuple is required; no Agent fallback is permitted")
    if len(set(names)) != len(names):
        parser.error("repositories must be unique")
    try:
        delivery_root = private_root(
            configured(args.delivery_root, "TIMELINE_DELIVERY_ROOT", "DELIVERY_ROOT", "DELIVERY", default=DELIVERY),
            "delivery root")
        work_root = private_root(
            configured(args.work_root, "TIMELINE_WORK_ROOT", "WORK_ROOT", "WORK", default=WORK), "work root")
        template_default = (os.path.join(delivery_root, "README.template.md")
                            if args.delivery_root or os.environ.get("TIMELINE_DELIVERY_ROOT")
                            else TEMPLATE)
        template_path = regular_file(
            configured(args.template, "TIMELINE_TEMPLATE", "TEMPLATE", default=template_default), "README template")
        gate_results_path = absolute_path(
            configured(args.gate_results, "TIMELINE_GATE_RESULTS", "GATE_RESULTS",
                       default=(os.path.join(delivery_root, "gate-results.md")
                                if args.delivery_root or os.environ.get("TIMELINE_DELIVERY_ROOT")
                                else GATE_RESULTS)), "gate-results path")
        _, _tuple_sha, source = source_tuple(args.source_tuple, args.source_tuple_sha)
        resolved_all = preflight_all(source, names)
    except (Refused, RuntimeError, OSError) as exc:
        parser.error(str(exc))
    resolved_by_name = {item["name"]: item for item in resolved_all}

    # No delivery or verifier directory is created until every selected source has
    # passed identity and ancestry.  This is the D135 no-partial-package boundary.
    os.makedirs(delivery_root, exist_ok=True)
    os.makedirs(work_root, exist_ok=True)

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    staging = os.path.join(delivery_root, f"build-{stamp}")
    tmp_root = tempfile.mkdtemp(prefix="timeline-delivery-", dir=work_root)
    os.makedirs(staging)

    results = []
    try:
        for name in names:
            started = time.monotonic()
            try:
                result = build_repo(resolved_by_name[name], staging, tmp_root)
            finally:
                shutil.rmtree(os.path.join(tmp_root, name), ignore_errors=True)
            result["seconds"] = time.monotonic() - started
            results.append(result)
            print(f"{name}: {result['status']} in {result['seconds']:.0f}s; "
                  f"{result['applied']} patch(es); trees "
                  f"{short(result['applied_tree'])} / {short(result['bundle_tree'])} / "
                  f"{short(result['want_tree'])}", flush=True)
            for problem in result["problems"]:
                print(f"  problem: {problem}", flush=True)
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    with open(os.path.join(staging, "README.md"), "w") as f:
        f.write(render_readme(results, template_path, gate_results_path))
    try:
        add_extras(staging, args.extra)
    except (ExtraError, OSError) as e:
        shutil.rmtree(staging)
        parser.error(str(e))
    write_checksums(staging)

    failed = [r["name"] for r in results if r["status"] != "PASS"]
    files = staged_files(staging)
    total = sum(os.path.getsize(os.path.join(staging, f)) for f in files)
    print(f"staging: {staging} ({len(files)} files, {mib(total)} uncompressed)")
    for f in files:
        if f.startswith("bundles/"):
            print(f"  {f}: {mib(os.path.getsize(os.path.join(staging, f)))}")

    if args.dry_run:
        print("dry run: ZIP not written")
        return 1 if failed else 0
    if failed:
        print(f"not writing ZIP: verification failed for {', '.join(failed)}; staging kept at {staging}")
        return 1

    zip_path = os.path.join(delivery_root, f"timeline-delivery-{stamp}.zip")
    zip_fd, zip_tmp = tempfile.mkstemp(dir=delivery_root, prefix=".timeline-delivery-", suffix=".tmp")
    os.close(zip_fd)
    try:
        with zipfile.ZipFile(zip_tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(os.path.join(staging, f), arcname=f)
        os.replace(zip_tmp, zip_path)
    except BaseException:
        try:
            os.unlink(zip_tmp)
        except FileNotFoundError:
            pass
        raise
    shutil.rmtree(staging)
    print(f"wrote {zip_path} ({mib(os.path.getsize(zip_path))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
