# Validation

Source-only checks completed:

- `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node private-rebuild-route.mjs`: exit 0. The unchanged App builder emitted the prospective checkout plan and both recipes; preflight is 1,184 bytes with SHA-256 `f00719b9e0f95e31ef66038796c49723dc408fdce85f530607a3a59b0d112365`; normal is 1,172 bytes with SHA-256 `5cdd8db6eb6b1eac72eae8b37af7cc7efdf8542c425a1f54427eb1066df979e9`.
- `git -C /home/user/banodoco/reigh-app show 3bb09fc656c6b8a81243f8f796115013b56d621f:src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx | nl -ba | sed -n '248,375p'`: exit 0. Actual first and repeated-read controls are lines 254-294 and 296-371.
- `git -C /home/user/banodoco/reigh-app diff --name-status 82e9e13ddf1d7ec6c736521b2eb091dca9877598..3bb09fc656c6b8a81243f8f796115013b56d621f -- ...`: exit 0. The candidate source files are the four paths listed in `source-manifest.json`; popup spec, builder, and manifests are unchanged.
- `git -C /home/user/banodoco/reigh-app rev-parse 3bb09fc656c6b8a81243f8f796115013b56d621f^{tree}`: exit 0; tree is `3d286bf4dd68c3c791b0351bb6257d302fbdca73`.
- Initial required foreground five-second sampler: exit 0 and reaped; `disk-trace.txt` retained. The filesystem showed 4.3G available, below the future one-time 5.2GB admission threshold.

Independent evidence incorporated, not rerun here:

- 1245: `PASS_SOURCE_VISIBILITY` for the 3bb production chain and exact checker semantics.
- 1305: `FAIL_FINITE_MOUNTED_WIRING` for the ad651 helper candidate; no native run occurred.

No product or full/localhost/browser test suite was run. No service request or registration was attempted.
