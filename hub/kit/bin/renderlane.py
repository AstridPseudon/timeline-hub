#!/usr/bin/env python3
"""Central-service browser lanes; dependencies and product sources stay read-only."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

NODE = Path("/home/user/work/toolchain/node-v20.19.4-linux-x64/bin")
ORCH = Path(__file__).resolve().parent.parent
REMOTION_BROWSER = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
STAGING_REF = "refs/remotes/origin/staging/timeline-v2.1"


def matching_checkout(repo, base):
    project = Path("/home/user/work") / repo
    ref = ""
    if base.startswith("origin/"):
        ref = f"refs/remotes/{base}"
    elif base.startswith("tl/"):
        ref = f"refs/heads/{base}"
    resolved = subprocess.run(
        ["git", "-C", str(project), "rev-parse", "--verify", f"{ref}^{{commit}}"],
        capture_output=True,
        text=True,
    ) if ref else None
    if resolved is None or resolved.returncode:
        ref = STAGING_REF
    sha = subprocess.check_output(
        ["git", "-C", str(project), "rev-parse", "--verify", f"{ref}^{{commit}}"],
        text=True,
    ).strip()
    checkout = Path("/home/user/work/wt-int") / f"{repo}-{sha[:12]}"
    if checkout.is_symlink():
        raise RuntimeError(f"refusing symlinked {repo} checkout: {checkout}")
    if checkout.exists():
        head = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
        status = subprocess.check_output(["git", "-C", str(checkout), "status", "--porcelain"], text=True)
        branch = subprocess.run(
            ["git", "-C", str(checkout), "symbolic-ref", "-q", "--short", "HEAD"],
            capture_output=True,
            text=True,
        ).stdout.strip()
        if head != sha or status or branch:
            raise RuntimeError(f"{repo} checkout is not a clean detached worktree at {sha}: {checkout}")
    else:
        subprocess.check_call(["git", "-C", str(project), "worktree", "add", "--detach", str(checkout), sha])
    return str(checkout)


def matching_sources():
    base = os.environ.get("ASTRID_TEST_BASE", "")
    return matching_checkout("agent", base), matching_checkout("runtime", base)


def main():
    lane, *selectors = sys.argv[1:]
    root = Path.cwd()
    result = Path(os.environ["D66_OUTPUT_DIR"]).parent
    env = dict(os.environ)
    runtime_source = env.get("ASTRID_RUNTIME_SOURCE")
    if lane == "render-proof":
        # Render validation deliberately rejects dispatcher Git/loader overrides.
        env = {key: env[key] for key in ("HOME", "LANG", "PATH") if key in env}
    env.update(
        PATH=f"{NODE}:{env['PATH']}",
        NODE_OPTIONS="--max-old-space-size=6144",
        PLAYWRIGHT_CHROMIUM_EXECUTABLE="/opt/pw-browsers/chromium",
        ASTRID_REMOTION_BROWSER_EXECUTABLE=REMOTION_BROWSER,
        ASTRID_NODE_EXECUTABLE=str(NODE / "node"),
        PYTHONDONTWRITEBYTECODE="1",
    )
    # Chromium creates Unix-domain sockets below TMPDIR; the full ORCH run path
    # exceeds their 108-byte limit. Keep the directory private and short.
    with tempfile.TemporaryDirectory(prefix="tl-browser-", dir="/tmp") as short:
        env.update(TMPDIR=short, TMP=short, TEMP=short)
        print(f"renderlane: {lane}; node={NODE / 'node'}; browser=/opt/pw-browsers/chromium; remotion-browser={REMOTION_BROWSER}; tmp={short}", flush=True)
        if lane == "browser-toolchain":
            command = [str(NODE / "node"), "-e", """
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE});
const p=await b.newPage(); await p.setContent('<title>central browser proof</title>');
if(await p.title()!=='central browser proof') throw Error('page failed');
console.log('browser launched: '+b.version()+'; 1 passed'); await b.close()})().catch(e=>{console.error(e);process.exitCode=1});
"""]
        elif lane == "browser-journey":
            agent, runtime = matching_sources()
            env.update(
                ASTRID_RUNTIME_CHECKOUT=runtime,
                ASTRID_RUNTIME_PYTHON="/home/user/work/venv-runtime/bin/python",
                ASTRID_CHECKOUT=agent,
                ASTRID_PYTHON="/home/user/work/venv-agent/bin/python",
                PYTHONPATH=f"{agent}:{runtime}",
                PLAYWRIGHT_OUTPUT_DIR=str(result / "browser-results"),
            )
            command = [str(NODE / "node"), str(root / "node_modules/@playwright/test/cli.js"),
                       "test", "--config", "playwright.three-products.config.ts",
                       *(selectors or ["tests/e2e/local/three-products.p2-shot-gallery.spec.ts"])]
        elif lane == "render-proof":
            runtime = runtime_source
            assert runtime, "test-run did not select the pinned Runtime source"
            env.update(
                PYTHONPATH=f"{root}:{runtime}",
                ASTRID_RUNTIME_CHECKOUT=runtime,
                ASTRID_REMOTION_PROJECT_DIR=str(root / "remotion"),
                ASTRID_TEST_NODE_MODULES=str(root / "remotion/node_modules"),
                ASTRID_TIMELINE_SCHEMA_PYTHONPATH=str(root / "astrid/core/timeline/schema/timeline-config.schema.json"),
            )
            # Registry generator probes intentionally drop PYTHONPATH. A tiny
            # private venv gives those children the same Runtime/source imports
            # without writing into the shared dependency environment.
            overlay = Path(short) / "python"
            shared_python = "/home/user/work/venv-agent/bin/python"
            subprocess.check_call([shared_python, "-m", "venv", "--without-pip", str(overlay)], env=env)
            shared_site = Path(subprocess.check_output([
                shared_python, "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"], env=env, text=True).strip())
            private_site = overlay / "lib" / shared_site.parent.name / "site-packages"
            private_site.mkdir(parents=True, exist_ok=True)
            (private_site / "renderlane.pth").write_text(
                f"import site; site.addsitedir({str(shared_site)!r})\n"
                f"import sys; sys.path[:0] = {[str(root), runtime]!r}\n")
            python = str(overlay / "bin/python")
            generated = subprocess.call([
                python, "scripts/gen_remotion_types.py",
                "--include-element-registries"], env=env)
            if generated:
                return generated
            smoke = root / "remotion/.renderlane.mjs"
            shutil.copyfile(ORCH / "bin/renderlane-agent.mjs", smoke)
            env["RENDERLANE_OUTPUT"] = str(result / "agent-render-smoke")
            smoke_code = subprocess.call([str(NODE / "node"), str(smoke)], env=env)
            if smoke_code:
                return smoke_code
            # The old real-pack-host path was removed; this is its current real
            # host/claim/execute/settle/CAS acceptance test, not a mocked render.
            command = [python, "-m", "pytest",
                       "-q", "-s", "-o", "addopts=", "-p", "no:cacheprovider",
                       "-m", "integration", *(selectors or [
                           "tests/integrations/test_generic_host_remotion_render.py"])]
        elif lane == "preview-vs-export":
            agent, _runtime = matching_sources()
            harness = root / ".renderlane"
            harness.mkdir()
            shutil.copyfile(ORCH / "bin/renderlane-capture.mjs", harness / "capture.mjs")
            env.update(ASTRID_CHECKOUT=agent, RENDERLANE_OUTPUT=str(result / "captures"))
            command = [str(NODE / "node"), str(harness / "capture.mjs")]
        else:
            raise ValueError(f"unknown lane {lane}")
        print("command: " + " ".join(command), flush=True)
        code = subprocess.call(command, env=env)
        if code and lane == "render-proof":
            probes = Path(short) / "astrid-probe-logs"
            for log in probes.glob("*.log"):
                destination = result / "probe-logs" / log.name
                destination.parent.mkdir(exist_ok=True)
                destination.write_bytes(log.read_bytes()[-1_000_000:])
        return code


if __name__ == "__main__":
    sys.exit(main())
