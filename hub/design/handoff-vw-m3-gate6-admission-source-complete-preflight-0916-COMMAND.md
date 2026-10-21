# Gate6 admission-source preflight command — 0916

## Static checks

```sh
(cd /tmp && bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/run.sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/preflight.sh)
(cd /tmp && /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/prepare.mjs && /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/issue.mjs && /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/dist-availability.mjs)
(cd /tmp && awk -v root=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet '{print $1 "  " root "/" $2}' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/SHA256SUMS | sha256sum -c -)
PYTHONDONTWRITEBYTECODE=1 python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/short-player-temp-controls.py --self-test
```

All central static checks passed. The helper self-test passed locally.

## Single central preflight

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-gate6-admission-source-complete-preflight-0916 e2e-viewing-gate6-admission-source-complete-preflight-0916)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The registered command was exactly:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-admission-source-complete-preflight-0916/packet/run.sh --preflight
```

It failed once at the missing exact committed source checkout. No retry or
physical command was issued.
