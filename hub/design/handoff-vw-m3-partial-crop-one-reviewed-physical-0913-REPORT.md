# VW-D09b/c reviewed partial-crop physical proof 0913

## Result

**HELD.** No central named-suite request was submitted; no grant, marker,
browser, helper, socket, renderer, or physical capture was started. The
0912 preparation is source-qualified and its offline checks are clean, but its
exact command cannot preserve the raw PNG/comparator evidence required by the
0913 authority.

The approved command creates `scratch` with `mktemp`, runs pytest with
`--tmp_path_retention_policy=all`, then unconditionally removes that entire
tree in its EXIT trap:

```sh
trap 'find "$scratch" -depth -delete 2>/dev/null || true' EXIT
```

Both physical tests write their PNGs and `inspection.json` below pytest's
temporary directory. The partial test asserts comparator values and PNG
identity but does not print or serialize those values; therefore the exact
prepared argv would destroy the only raw PNG/comparator outputs on exit.
Changing the command or assertions to add retention would no longer be the
approved exact prepared fixture, so no physical run was attempted.

The exact 0912 command also has no entry in the central `suites.conf`; the
existing similarly named mouth697 suite targets a different older source and
was not reused. No suite was registered or changed here.

## Prerequisite evidence

- 0901 custody verdict: **APPROVE**.
- 0912 preparation verdict: **READY**, reviewed Agent revision
  `883833ad4c91e7764950f26b9a07a7c46a6beea4`, tree
  `1da635d2e819a2c6ab9f0b4c420034a489dca792`.
- Current worktree is clean and exactly that revision/tree.
- `bash -n` on the exact 0912 command: **PASS**.
- Exact collect-only argv: **PASS**, `2 tests collected in 0.18s`, listing
  the explicit 799-pixel node and partial 697-pixel node.
- Static source/tuple/realpath/storage/archive checks: **PASS**.
- Current free bytes: `11534008320`; standing floor: `10737418240`.
- Shared browser lock probe: free; no competing Gate6 physical/preflight
  queue entry was active.

## Frozen hashes

```text
presenter_crop_capture.mjs  38abb1a8854a97473f01dd2886bf805945200f9cc45bd6c61d2e17233c2be49f
presenter_crop_capture.py   68291e26500154b0ac2531a0b69558c5ef64d02aac10b8261f8329e036b87016
presenter_crop_entry.mjs    5223ef4ecf007124920773bef10a9f543749cd07c943e5143720837f18e29947
test_presenter_crop_equivalence.py 2419620a92c9972c1a7e4bd5a3b79790631ced2661227cc9420b6977946957b1
public13                    9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
node20.19.4                 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
chromium1194                63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4
```

## Required next step

Manager/orchestrator must provide a revised, reviewed command that retains
the raw PNGs and comparator JSON outside the cleanup scratch tree, then
register that exact command as one named central suite. Preserve the existing
guards and do not retry this held request with the current command.
