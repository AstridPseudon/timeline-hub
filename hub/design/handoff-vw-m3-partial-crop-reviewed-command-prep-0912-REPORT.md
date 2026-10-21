# VW-D09b/c partial-crop reviewed command preparation

## Result

Prepared one manager-only, future central command for the reviewed explicit
799 px plus partial 697 px fixture. The 0901 custody verdict is **APPROVE**;
therefore no REQUEST CHANGES correction was applied and no changed-hunk review
is claimed. The Agent worktree remains clean at source revision
`883833ad4c91e7764950f26b9a07a7c46a6beea4`, tree
`1da635d2e819a2c6ab9f0b4c420034a489dca792`.

The command collects both helper nodes (2 total), then selects exactly one
physical node: `test_actual_registered_presenter_partial_crop_pixels`. The
original explicit 799 px assertions and its natural-pair, strict boundary,
padding16, planted 8/15/16/20 mismatch, source-byte, PNG-format/size, and
unchanged strict `> .02` controls remain untouched. The preserved 32349
source is `ac4e004a664b96d58a00b66c7a2fa702a191f5bd`; its explicit test was
read directly and its 799/387, natural, strict boundary, padding16, planted
8/15/16/20, and PNG-byte-preservation assertions are still present in the
current helper. Existing 32349 evidence continues to be evidence for
explicit 799 only; it is not relabelled as partial. The partial physical
result remains **NOT RUN**.

## Offline checks

- Pure geometry/control lane: `10 passed in 4.07s`.
- Physical helper collection: `2 tests collected in 0.18s`; no physical test
  executed.
- Private staging safety: `3 passed in 0.08s`.
- Node20.19.4 `--check`: geometry, entry, and capture passed.
- Ruff: all checks passed.
- `git diff --check`: passed; worktree clean.
- Public13 archive: SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77
  regular members, no symlink/hardlink members.
- Node binary: v20.19.4, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Chromium1194 launcher: exact realpath
  `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`,
  SHA-256 `63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4`.

## Preflight contract

The companion command refuses a dirty or wrong Agent source/tree, wrong
four-file bytes, wrong public13 archive, wrong Node, wrong browser path/hash,
linked artifact/peer scope, archive links, less than 10 GiB available storage,
or an unheld shared browser lock. It uses the existing `presenter_query`
fixture's temporary project and private staging only; no shared install,
borrowed graph, or worktree output is a write target. The original registered
`am-presenter`/`astrid_motion` path, component-frame-zero query, browser
cleanup, process cleanup, archive checks, and source/peer postconditions remain
owned by the existing helper. No second geometry oracle is introduced.

The prep worker did not request a central grant, create a marker, acquire the
shared lock, invoke a browser/helper/socket/render, clone a graph/stage,
install dependencies, mutate Git, or run a full suite. A manager must perform
the sole later capture under the normal central grant and lock protocol.

## Handoff files

- Command: `handoff-vw-m3-partial-crop-reviewed-command-prep-0912-COMMAND`
- No-op patch record: `handoff-vw-m3-partial-crop-reviewed-command-prep-0912-PATCH`
- This report and hash manifest: matching files in `ORCH/design`.
