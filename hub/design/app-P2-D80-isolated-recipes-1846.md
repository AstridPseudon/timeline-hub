## Done

Added five D66 focused descriptors and one unit assertion in:

- [d66-plain-stack.mjs](/home/user/work/wt/app-P2-D80-isolated-recipes-1846/scripts/testing/d66-plain-stack.mjs)
- [d66-plain-stack.test.mjs](/home/user/work/wt/app-P2-D80-isolated-recipes-1846/scripts/testing/d66-plain-stack.test.mjs)

Each selects exactly one unchanged original test and retains Runtime logs.

Checks passed:

- Node 20 syntax checks
- 20 Node unit tests
- `npm run lint`
- Five `--collect` runs, each reporting `Total: 1 test in 1 file`
- `git diff --check`
- Protected spec files unchanged

Strict TypeScript was blocked by pre-existing missing Astrid vendor/generated modules in unrelated files.

Manager commands:

```sh
D66_SUBMIT_SUITE=d80-p2-register-asset-1846 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-register-asset --submit
D66_SUBMIT_SUITE=d80-p2-automatic-child-placement-1846 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-automatic-child-placement --submit
D66_SUBMIT_SUITE=d80-p2-popup-swap-1846 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-popup-swap --submit
D66_SUBMIT_SUITE=d80-p2-transition-none-single-1846 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-transition-none-single --submit
D66_SUBMIT_SUITE=d80-p2-transition-none-bulk-1846 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-transition-none-bulk --submit
```

Commit message and DONE marker created.