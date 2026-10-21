# Gate 6 single-lock execution — 2026-10-21

## Result

The approved 0845 packet was executed with exactly one internal fd9 lock. The
central preflight passed. The one conditional physical run was then started,
issued its fresh tuple/grant/marker once, and stopped immediately after its
first physical case failed. No retry, alternate, full suite, or second
physical request was made.

The 0851 independent custody verdict was **APPROVE**. Request 29098 remains
preserved as cancelled evidence; it used the invalid outer `flock` wrapper and
issued no tuple, grant, marker, browser, Runtime, export, or cases.

## Exact registered commands

```text
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-short-temp-device-inode-source-fix-0845/run.sh --preflight
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-short-temp-device-inode-source-fix-0845/run.sh
```

Unique suite names were added without editing the old suite lines:
`e2e-viewing-gate6-short-temp-preflight-0856` and
`e2e-viewing-gate6-short-temp-physical-0856`.

## Central results

- Preflight: `vw-m3-gate6-single-lock-exact-command-executor-0856-e2e-viewing-gate6-short-temp-preflight-0856-1021085527-6388` — PASS, exit 0, 42s. It discovered exactly five cases, verified GET 200, all source/graph/toolchain/negative guards, cleanup, and `token-issued:false`.
- Physical: `vw-m3-gate6-single-lock-exact-command-executor-0856-e2e-viewing-gate6-short-temp-physical-0856-1021085644-18439` — cancelled after first failure, central exit 143 / result exit 130, 195s. Its `CANCELLED` record documents stop-on-failure and no retry.

The physical run’s first case failed because the App render download assertion
expected filename `frame-parity.mp4` but received
`timeline-6c0e5aa0-99af-408a-af71-11a9e2e337de.mp4`. The second case began
only as cancellation propagated and reported closed-browser errors; it is not
an independent result. Cases 3–5 did not run. Therefore there are no valid
frame/PCM positives, same-export parity results, picture-only or half-gain
negative results, or raw MP4/VP8/Opus/WAV media from this run; zero bodies is
not parity.

## Frozen tuple and hashes

- App: `d00a66134f330672ea7471dc69db38c1566d94cf` / tree `a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba`; source `sha256:76694aa3da39f17ef0945fb50a22f64a86908e2ad94dc46b79c362db22220fa0`; graph `8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b`.
- Agent: `d0a5072bbe7b7ce9489f43aa0a81027ec400343b` / tree `6adb4a1190dfb2874e101565f37eccd392b1ae2f`.
- Runtime: `8f105c26e3b62f9c2683f717a9773a12bc775a8e` / tree `b7f456d5135cba6049980ebc43a91c7a72ab8f7e`; graph `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`.
- Composition: `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` / tree `13e375534fffd704305eced5686699d2c8c9c948`.
- Node: `20.19.4`, executable SHA `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Chrome: `155.0.8059.84`, executable SHA `cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76`, tree `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`.
- Dist: 339 files; index `aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b`; tree SHA `43e2cd02d757f6f63833b7c4b89fc9241fd1ba41fa6b2dd8723ac398af070ed4`.
- Packet manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-short-temp-device-inode-source-fix-0845/SHA256SUMS`; `sha256sum -c` passed before both requests.

## Evidence and cleanup

Physical evidence is retained at:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-short-temp-device-inode-source-fix-0845/gate6-20261021T0845/`.
It contains the source tuple, issued manager grant and one-shot marker, two
Playwright error contexts, traces, screenshots, and page diagnostics.

The runner cleaned `/tmp/vw-6MSE0w` with the helper. Cancellation left
`/tmp/vw-D2eHyS`; after checking owner `uid=0`, mode `0700`, and identity
`dev=65024, ino=926725`, the same helper returned
`cleanup=PASS ... symlinks=unlinked-without-following` and removed it. The
browser lock was then verified free. The Composition worktree is clean; no
product, harness, packet, dependency, or source files were edited.

## Next step

Stop at the failed physical result. Triage the App render filename contract
against the frozen five-case expectation before any future execution is
considered.
