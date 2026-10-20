# vw-m4-root-build-realpath-write-guard

Agent worktree: `/home/user/work/wt/vw-m4-root-build-realpath-write-guard`
on `tl/vw-m4-root-build-realpath-write-guard`, based on `tl/integration`
`ab4e6f6a6`.

The persisted Viewing-owned staging call in the Agent integration tree was the
inline peer loop in
`tests/packs/rendering/test_presenter_scene_capability.py`. It now uses
`_stage_private_node_modules` from `tests/packs/rendering/_helpers.py`.
The helper visits the peer graph once, creates real scope directories, uses
leaf-only `ln -sfnT`, rejects linked/borrowed destination ancestors before
directory or link writes, and guards tar extraction destinations with the same
realpath containment check. The focused regression is
`tests/packs/rendering/test_private_node_modules_staging.py`.

The original f816 root-build command was historical worker shell text rather
than a repo-native helper. The corrected reusable script is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-root-build-realpath-write-guard/f816-root-build-safe.sh`

It iterates `"$OLD"/@*` and `"$OLD"/[!@]*` once, keeps scopes real, uses
`ln -sfnT`, and checks realpath/linked ancestors immediately before every
staging directory operation and the tar extraction. It does not install or
modify the borrowed graph.

Evidence:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -B -m pytest -q --basetemp=/tmp/vw-m4-root-build-realpath-write-guard-pytest tests/packs/rendering/test_private_node_modules_staging.py` — `3 passed`.
- `ruff check tests/packs/rendering/_helpers.py tests/packs/rendering/test_presenter_scene_capability.py tests/packs/rendering/test_private_node_modules_staging.py` — passed.
- `bash -n .../f816-root-build-safe.sh` — passed.
- Private synthetic shell fixture — passed: clean staging twice, linked-scope/self-link refusal, tar-through-scope refusal, and unchanged borrowed-file SHA-256 snapshot.
- `git diff --check` — passed.

No full suite, browser/render suite, install, network, or shared dependency
write was run.
