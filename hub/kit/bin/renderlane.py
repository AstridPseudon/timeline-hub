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


def main():
    lane, *selectors = sys.argv[1:]
    root = Path.cwd()
    result = Path(os.environ["D66_OUTPUT_DIR"]).parent
    env = dict(os.environ)
    env.update(
        PATH=f"{NODE}:{env['PATH']}",
        NODE_OPTIONS="--max-old-space-size=6144",
        PLAYWRIGHT_CHROMIUM_EXECUTABLE="/opt/pw-browsers/chromium",
        ASTRID_REMOTION_BROWSER_EXECUTABLE="/opt/pw-browsers/chromium",
        ASTRID_NODE_EXECUTABLE=str(NODE / "node"),
        PYTHONDONTWRITEBYTECODE="1",
    )
    # Chromium creates Unix-domain sockets below TMPDIR; the full ORCH run path
    # exceeds their 108-byte limit. Keep the directory private and short.
    with tempfile.TemporaryDirectory(prefix="tl-browser-", dir="/tmp") as short:
        env.update(TMPDIR=short, TMP=short, TEMP=short)
        print(f"renderlane: {lane}; node={NODE / 'node'}; browser=/opt/pw-browsers/chromium; tmp={short}", flush=True)
        if lane == "browser-toolchain":
            command = [str(NODE / "node"), "-e", """
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE});
const p=await b.newPage(); await p.setContent('<title>central browser proof</title>');
if(await p.title()!=='central browser proof') throw Error('page failed');
console.log('browser launched: '+b.version()+'; 1 passed'); await b.close()})().catch(e=>{console.error(e);process.exitCode=1});
"""]
        elif lane == "browser-journey":
            env.update(
                ASTRID_RUNTIME_CHECKOUT="/home/user/work/runtime",
                ASTRID_RUNTIME_PYTHON="/home/user/work/venv-runtime/bin/python",
                ASTRID_CHECKOUT="/home/user/work/agent",
                ASTRID_PYTHON="/home/user/work/venv-agent/bin/python",
                PYTHONPATH="/home/user/work/agent:/home/user/work/runtime",
                PLAYWRIGHT_OUTPUT_DIR=str(result / "browser-results"),
            )
            command = [str(NODE / "node"), str(root / "node_modules/@playwright/test/cli.js"),
                       "test", "--config", "playwright.three-products.config.ts",
                       *(selectors or ["tests/e2e/local/three-products.p2-shot-gallery.spec.ts"])]
        elif lane == "render-proof":
            runtime = env["ASTRID_RUNTIME_SOURCE"]
            env.update(
                PYTHONPATH=f"{root}:{runtime}",
                ASTRID_RUNTIME_CHECKOUT=runtime,
                ASTRID_REMOTION_PROJECT_DIR=str(root / "remotion"),
                ASTRID_TEST_NODE_MODULES=str(root / "remotion/node_modules"),
                ASTRID_TIMELINE_SCHEMA_PYTHONPATH=str(root / "astrid/core/timeline/schema/timeline-config.schema.json"),
            )
            # The old real-pack-host path was removed; this is its current real
            # host/claim/execute/settle/CAS acceptance test, not a mocked render.
            command = ["/home/user/work/venv-agent/bin/python", "-m", "pytest",
                       "-q", "-s", "-o", "addopts=", "-p", "no:cacheprovider",
                       "-m", "integration", *(selectors or [
                           "tests/integrations/test_generic_host_remotion_render.py"])]
        elif lane == "preview-vs-export":
            harness = root / ".renderlane"
            harness.mkdir()
            shutil.copyfile(ORCH / "bin/renderlane-capture.mjs", harness / "capture.mjs")
            env.update(ASTRID_CHECKOUT="/home/user/work/agent", RENDERLANE_OUTPUT=str(result / "captures"))
            command = [str(NODE / "node"), str(harness / "capture.mjs")]
        else:
            raise ValueError(f"unknown lane {lane}")
        print("command: " + " ".join(command), flush=True)
        return subprocess.call(command, env=env)


if __name__ == "__main__":
    sys.exit(main())
