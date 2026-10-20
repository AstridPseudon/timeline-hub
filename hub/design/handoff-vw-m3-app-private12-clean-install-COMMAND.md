# App public12 private graph commands

All commands below used worker-owned paths. Network was used only by the install command.

```sh
cd /home/user/work/wt/vw-m3-app-private12-clean-install
node --version                                      # v22.22.0 (host; not used for install)
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --version # v20.19.4
/tmp/vw-m3-agent-gate-node20.19.4/bin/npm --version  # 10.8.2

PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 \
PUPPETEER_SKIP_DOWNLOAD=1 \
NPM_CONFIG_CACHE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/npm-cache \
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/npm-tmp \
/tmp/vw-m3-agent-gate-node20.19.4/bin/npm ci --no-audit --no-fund
```

Recorded npm result: **exit 0**; normal postinstall ran once and reported exact Remotion 4.0.509 audio-resume patch application. The watchdog owned the npm process group and enforced free space >= 10 GiB and private allocation <= 1.4 GB.

Offline verification commands:

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/audit_graph.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/clean-project/node_modules/.bin/tsc \
  --project /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-app-private12-clean-install/type-probe.tsconfig.json
```

Both completed with **exit 0**. The audit generated the READY marker, full physical manifest, JSON report, and metadata. It also re-ran the read-only postinstall check and pure import probe.
