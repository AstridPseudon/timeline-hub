# U4p D141p validation

## Identity and custody

- Candidate App commit `dc1a86cf4797b6ca3799d9ad1dee7e7d949caf04`, tree `dd989783046aeff652486a1ba39db42aea86e201`, sole parent `8f278b91accec5852e39bb84822e99124fccb81d`.
- App base tree is `99d79cb47496c0ca682b0cd42aa911177761bb31`.
- Exact Agent checkout is clean at commit `8585ed9c0404d0187b2ce70242d25114a32747c2`, tree `92a3ffdb5a8bf476e10bfa1bbda3e2856fb9938c`, parents `28e56cacb42d3da85b02e5b3543895b44f3d0f70` and `5d202569f3af3852476d182ff49683787bb1e881`.
- Exact Runtime checkout is clean at commit `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, tree `ac5b862744bece65b2e30565db1777bacd60da28`, parents `0ca306dfd3cf4e21976271cc4b2e779b10e025b0` and `24107e83b096264e59f64ed5bd65e00650567f22`.
- `e1c751def40f8fde59277226b6c190354d22744c` is an ancestor of the Agent head. `astrid/installer/tools.py` directly imports `ASTRID_VERSION` and passes `headers={"User-Agent": f"astrid-installer/{ASTRID_VERSION}"}` to `urllib.request.Request` before `urlopen`.

## Generation and idempotence

The exact normal command was run read-only in plan mode twice:

```text
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/wt/rt-pin-6a011d58 --agent-checkout /home/user/work/wt/agt-pin-8585ed9c --plan
```

Both outputs were byte-identical and reported the qualified Agent, qualified Runtime, and schema digest exactly as present in the candidate manifest. The author receipt records the required `--plan` then `--write` generation path; no manual pin or hash was introduced.

The author receipt also records a private vendor refresh comparison followed by the normal default refresh on the exact Agent checkout. The final provenance and payloads independently verify against the exact source.

## Conservation

- `git diff` from base to candidate contains only `public/install-manifest.json` and `vendor/astrid-browser/provenance.json`.
- Every other tree entry is exact.
- All 160 `vendor/astrid-browser` payload blobs are exact; only `provenance.json` differs.
- The candidate manifest retains the exact Runtime SHA `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` and schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.
- The vendor verifier passed: 65 pinned source files, 160 vendor files, and 11 public imports.

## Tests

```text
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --test scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs
```

Result: 4 passed, 0 failed, 0 skipped under Node `v20.19.4`.

`git diff --check 8f278b91accec5852e39bb84822e99124fccb81d dc1a86cf4797b6ca3799d9ad1dee7e7d949caf04` passed. No full/browser/provider/journey/unchanged broad suite was run.
