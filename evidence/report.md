# A-T3-proof-r4 qualification report

Date: 2026-10-27
Branch: `tl/A-T3-proof-r4` at `b9b60c6eb3` (`tl/zoom-integration`)

## Owner sandbox and pack input

The approved sandbox copy and custom project pack were not available in this
worker's accessible inputs. The exact missing inputs are:

- sandbox project `almost-ready`, timeline
  `almost-ready-no-first-second-v2`, including shot clip
  `c02-02-am-discord`;
- the admitted smooth-zoom project-pack snapshot whose abbreviated revision is
  `sha256:1b1e3523...`; the full digest, `elementRef`, and Runtime pin are not
  available.

Read-only searches under the assigned worktree, worker scratch, orchestration
worker/reports, and accessible `/home/user/{work,peteromallet,banodoco}` roots
found no matching sandbox, pack, snapshot, MP4, or still artifacts. A direct
read-only inspect attempt was:

```text
PYTHONPATH=$PWD:/home/user/work/runtime \
ASTRID_PROJECT_PACKS_ROOT=/tmp/w-b5512899cf/no-owner-pack \
/home/user/work/venv-agent/bin/python -m astrid.core.element.cli \
  project-pack inspect --realm owner --project almost-ready
```

Result: exit 1, `ServiceUnavailableError: neutral runtime bootstrap was not
ready: No workspace is configured; run astrid-runtime workspace create or
workspace attach.` No workspace was created or attached because that would not
identify an owner-approved sandbox and could risk touching the owner's data.

Therefore placement on the real shot, the resulting `elementRef`/pin, the
real child/browser/MP4 export, and local Vite preview capture could not be
performed. No substitute source was used.

## Existing merged proof tests

Direct local command (using Node 20.19.4 and a private `/tmp` overlay whose
package symlinks point read-only at the shared Remotion install):

```text
PYTHONPATH=$PWD:/home/user/work/runtime \
PYTHONDONTWRITEBYTECODE=1 \
ASTRID_REMOTION_PROJECT_DIR=/tmp/w-b5512899cf/pinned-export-host \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
/home/user/work/venv-agent/bin/python -m pytest -q \
  tests/core/test_timeline_element_placement.py \
  tests/packs/rendering/test_pinned_project_elements.py \
  -o cache_dir=/tmp/w-b5512899cf/pinned-export-host/pytest-cache-2 \
  --basetemp=/tmp/w-b5512899cf/pinned-export-host/pytest-basetemp-2
```

Result: **27 passed in 40.19s**. This covers initial placement on an
occurrence/shot clip with only built-in `clipType: am-discord`, two distinct
revisions in one render-local registry/assets selection, and missing/corrupt
snapshot fail-closed cases without catalog fallback.

The first local invocation was 26 passed, 1 failed because its temporary host
lacked Node package resolution for `remotion/package.json`. The private
overlay corrected that setup; no shared dependency or cache path was changed.

Central service request:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  A-T3-proof-r4 targeted --files \
  "tests/core/test_timeline_element_placement.py tests/packs/rendering/test_pinned_project_elements.py"
```

Result: `A-T3-proof-r4-targeted-1027000123-31765`, **26 passed, 1 failed in
37.27s**. The failure is
`test_two_revisions_keep_source_dispatch_aliases_and_assets`; the service
checkout used Node 22.22.0 and failed before the assertion with
`Cannot find module ... remotion/package.json`. The full log is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/A-T3-proof-r4-targeted-1027000123-31765/log.txt`

## Real-render/parity result

Not run. The required owner sandbox and full custom-pack digest/source were
missing, so there are no export or local-Vite stills, clip-relative sample
times, pixel measurements, or tolerance result to report. No MP4/browser/mock
render was substituted.

No product code or assertions were changed. `git diff --check` passed and the
worktree was clean before this evidence report was added.

