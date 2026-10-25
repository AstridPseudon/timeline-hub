# U2/D139 merged-head targeted acceptance

## PASS

- Actual HEAD: `4c4ee35d5687c4cd40a0e5395efda53aa56f939d`; tree `d50fd98f7d1bc6860de810f38e8a0b3a55ca224e`.
- Parents: `708ba3fbc1b802d45e766d9c3e6899835a15ca78` and `32dde0c035f59029064fe782d5147d4e68e75835`.
- Ancestry, zero unmerged index entries, exact marker scan, and `git diff --check` passed.
- The prior candidate’s 56 upstream-only paths remain blob-identical to upstream `886a3183bd4…`; all 14 later parent-1-only paths remain blob-identical to `708ba3fbc1…`.
- The exact two FPS paths, three historical-source paths, and latest CLI-ingress source path remain byte-identical to parent 1. The generated chat bundle is byte-identical to the prior review.
- Runtime source was read before testing from clean checkout commit `cf0b82dd47452a7a34fc63eb233e9b1dc0532806`, tree `8d5683702f36034f27ee7f49737665d66dbc2b75`.

## Targeted commands

- `PYTHONPATH=/home/user/work/wt/agt-U2-D139-integrated-acceptance-2146:/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_host_bootstrap_source_identity.py tests/test_installer_omp_source.py tests/core/generation/test_gpu_environment.py tests/test_installer_platforms.py --junitxml=/tmp/agt-U2-D139-integrated-acceptance-2146/targeted.xml` — exit 0, 244 passed in 3.16s; run once. Private XML/log retained at `/tmp/agt-U2-D139-integrated-acceptance-2146/`.
- Temporary verified symlink to `/home/user/work/runtimes/agent-remotion-current/node_modules` + `bun run check:chat-bundle` — exit 0; run once; named symlink removed.
- Temporary verified symlink to the same immutable dependency tree + `bun test ./astrid/chat` — exit 0, 195 passed, 0 failed, 428 expectations, 23 files, 108.03s; run once; named symlink removed.
- `bash -n tools/p4-d73-pinned-launch.sh` — exit 0.

## Static and inherited checks

AST checks passed for the 14 composed Python files and production caller/provider wiring. The C0 request/reply field checks passed, including accepted/merged canonical data, receipts, records, bindings/derived effects/dependencies, history/undo, conflict head/reason, invalid code/path/hint/command, and preview `receipt: null`.

The prior review’s Ruff 76-findings and mypy 74-error inventories were reused because every corresponding diagnostic blob is unchanged; no ignore, fix, or weakened test was used.

Full/core/P1–P5/gate suites, browser/live integration, acquisition/install/build/render, and ZIP/delivery verification were not run.
