# Commands and exits (tf-zip-dryrun-1905, 2026-10-25)

Paths: `W` = `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/tf-zip-dryrun-1905`.
Every command below was a single simple command, or a script run as a file. Exits are shown as seen.

## 1. Read-only identity (before)

| Command | Exit |
|---|---|
| `git -C <pin or integration checkout> rev-parse HEAD` / `HEAD^{tree}` / `status --porcelain` (8 checkouts) | 0 (status empty = clean) |
| `git -C <checkout> symbolic-ref -q HEAD` (agent pin) | 1 (detached) |
| `git -C <repo> rev-parse tl/integration` (agent, runtime, app, composition) | 0; agent = `a30e74e9`, others equal pins |
| `git -C <repo> rev-parse origin/main` | 0 (agent `886a3183`, runtime `dbcdb97c`, app `213318f1`, composition `67b8aa3d`) |
| `git -C <repo> cat-file -t <upstream>` (agent, runtime, app) | 0, `commit` |
| `git -C <repo> rev-parse --git-common-dir`, `--is-shallow-repository` | 0 (App pin not shallow) |

## 2. Ancestry and erasure exposure

| Command | Exit | Result |
|---|---|---|
| `merge-base --is-ancestor 547e1045 a30e74e9` (agent) | 1 | pinned agent is not an ancestor of the integration tip |
| `merge-base --is-ancestor a30e74e9 547e1045` | 1 | not reverse either |
| `merge-base 547e1045 a30e74e9` | 0 | `070dfc5e` |
| `rev-list --count <tip>..<upstream>` agent / runtime / app / composition | 0 | 22 / 16 / 68 / 0 |
| `merge-base --is-ancestor <upstream> <tip>` runtime / app / composition | 1 / 1 / 0 | runtime and app upstream not ancestors; composition linear |
| `merge-base <upstream> <tip>` agent / runtime / app | 0 | `92443771` / `d4f496ec` / `3881e944` |
| `diff --shortstat <merge-base> <upstream>` agent / runtime / app | 0 | 98 files +2724/-668; 29 files +1048/-21; 154 files +6890/-1089 |

## 3. Private roots (no live write)

| Command | Exit | Note |
|---|---|---|
| `mkdir -p <W>/tmpdir/...` | 1 | `W/tmpdir` is an existing file (a pointer to `/tmp/w-195a7c12e9`), not a directory; nothing created |
| `mkdir -p /tmp/w-195a7c12e9/dryrun/...` | refused | needs approval (outside allowed dirs); not run |
| `mkdir -p <W>/dryrun/{work,delivery,agent-view} <W>/evidence` | 0 | private roots under the worker folder |
| `git init -q <W>/dryrun/agent-view` | 0 | left as an empty repo (could not delete it, see report) |
| Write `<W>/dryrun/agent-view/.git/objects/info/alternates` | refused | "sensitive file"; not written |
| `git -C <W>/dryrun/agent-view update-ref refs/remotes/origin/main 886a3183...` | 128 | no alternates yet (expected); superseded |
| `git clone -q --bare --shared /home/user/peteromallet/astrid-agent/.git <W>/dryrun/agent-view.git` | 0 | shares farm objects; source not written |
| `git -C <W>/dryrun/agent-view.git update-ref refs/remotes/origin/main 886a3183...` | 0 | private ref |
| `git -C <W>/dryrun/agent-view.git update-ref refs/heads/tl/integration 547e1045...` | 0 | private ref; farm `tl/integration` untouched |
| `ln -s` x5 into `<W>/dryrun/work/` (agent view, runtime/app/composition pins) | 0 | read-only use of pins |
| `sha256sum <installed>/bin/delivery-build` | 0 | `f25dfab13bbfb090bf26cf97a85e59bd4818859f5b974dac94aae7e6f2272708` |

## 4. Dry run (installed script, loaded read-only, private roots)

| Command | Exit |
|---|---|
| `python3 -B <W>/dryrun/run-dryrun.py` (first try) | 1: `AttributeError` (`spec_from_file_location` returns None for an extension-less file); nothing written |
| `python3 -B <W>/dryrun/run-dryrun.py` (after switching to `SourceFileLoader`) | 0 (no error; the script ends with `dry run: ZIP not written`) |

The runner (`dryrun/run-dryrun.py`) loads `ORCH/bin/delivery-build` with `SourceFileLoader`, sets
`DELIVERY`, `TEMPLATE`, `GATE_RESULTS` and `WORK` to private paths in memory, and sets
`TIMELINE_DELIVERY_SCRIPT_SHA` to the hash above. Bytecode writing is disabled. The installed file is not edited.

Output summary: agent PASS (67s), runtime PASS (8s), app PASS (149s), composition PASS (1s). Each applied tree equals the bundle tree equals the pinned `tl/integration` tree.

## 5. Apply check against fresh upstream clones

| Command | Exit |
|---|---|
| `python3 -B <W>/dryrun/applycheck.py` | 0: agent, runtime, app, composition each `applies=True rc=0` |

Inside the script, per repo: `git clone -q --no-checkout --shared <farm .git> <W>/dryrun/clones/<name>`, then `read-tree <upstream>`, `write-tree`, `apply --cached --check <patch>`, and `diff --name-only --no-renames <merge-base> <upstream>`. All clones are rc 0; index tree equals the upstream tree for all four.

## 6. After identity and disk

| Command | Exit |
|---|---|
| `python3 -B <W>/dryrun/identity.py after` | 0; all 8 checkouts match before; all refs unchanged; free 9.66 GiB |

## 7. Hashes

`sha256sum` run on the patches, the staging `SHA256SUMS`, and the evidence files (values in `manifest.json` and the final report).

## Not run

- No push, fetch into a farm repo, checkout, commit, merge or reset in any farm repo.
- No ZIP, no delivery claim, no wheel/build/render/gate, no tests (no code changed), no D77/D130/D134 action.
- No write to live `ORCH/delivery` (the path does not exist; not created; confirmed by Glob after the run).
