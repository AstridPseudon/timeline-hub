# F/D141i validation

## Commands run

```text
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-cut-measurement-prep-0227/evidence/measurement-command.sh
=> PASS
bash -n /home/user/work/wt/agt-pin-28e56cac/tools/p4-d73-pinned-launch.sh
=> PASS
prep=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141i-cut-measurement-prep-0227/evidence; python3 -P - "$prep" <<'PY'  # stdlib JSON/hash/argv/selector checks
=> PASS for JSON parsing, candidate/manifest hashes, poison one-field delta,
   exact 22-root selector order, JUnit join check reported FAIL, die check
   reported FAIL
for spec in the four exact pinned source tuples; do git -C PATH rev-parse HEAD HEAD^{tree}; git -C PATH remote get-url origin; git -C PATH status --porcelain --untracked-files=all; done
=> PASS exact requested commits/trees, clean status, official origins
realpath /home/user/work/venv-agent/bin/python; /home/user/work/venv-agent/bin/python --version; /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --version; sha256sum profile/archive/registry/schema/runtime-lock paths
=> PASS except profile package-lock receipt: manifest/source ...be18e,
   actual package-lock ...be18d
python3 -P - "$prep" <<'PY'  # git cat-file membership check for all 22 roots
=> PASS, no missing roots
```

The first inline static-check invocation had a syntax typo in the checker
itself; it was immediately corrected and rerun. No task or product file was
changed by that checker.

## Not run

No pytest, collection, provider/product import, full body, request-test,
launcher control, repeated control, package acquisition, installation,
profile/kit/launcher replacement, or source/pin/service/queue write was run.
