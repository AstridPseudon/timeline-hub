# CPU backend cleanup replay preparation

**READY for manager review and one physical central replay. No replay submitted.**

Read PLAN.md, the cleanup audit's FIRST_DRAFT and full report, and the original
`vw-m3-cpu-profile-proof-e2e-viewing-cpu-profile-1019223448-19007`
request/snap/summary/log. That result remains uncertain: its recorded eight
passes are backend plumbing evidence, with three black/silent exports. They
do not establish frame or audio parity.

## Exact source

The assigned HEAD is `d0130b44c8ac8fba44568030d155ea9e11c9cbb7`, whose tree is
already **`d3508cb5158c80b34e90e6de8b5430423e3a692f`**, the actual central-tested
tree. No reconstruction delta was necessary. In particular, using the old
reported `a1238c627` alone would lose 41 added lines and restore one changed
line in the CPU test: retained color metadata and the existing
`yuv420p`/`yuvj420p` codec spelling assertion. These remain exactly as tested.

`test_viewing_cpu_export.py` is byte-identical to retained blob
`70f6dc9c021f0b2888e9281f83bdc7b4ab35c576`. There are four test functions,
instantiating eight cases:

| Original function | Cases |
| --- | --- |
| `test_parity_environment_absent_install_is_optional` | 1 |
| `test_parity_environment_accepts_public_built_package` | 1 |
| `test_parity_environment_broken_install_fails` | `package.json`, `dist/index.js`, `cli` |
| `test_canonical_cpu_export_publishes_real_video` | `media-only`, `text-card`, `transition-windows` |

All assertions, exception expectations, codec fixtures, normal `RenderService`
construction, managed asset binding, routing/provenance checks, H.264/AAC
requirements, frame counts and duration tolerances are unchanged. The static
checker verified all **2,890 original files**, including their executable modes,
against retained Git blob identities; this covers fixtures, helpers and product
source, not merely the test file. No product/test file was edited.

## Prepared runner and dependencies

All setup artifacts are in the assigned orchestration directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-cpu-backend-clean-replay-prep/`

- `setup-run.sh`, `replay.py`, unchanged original `browser-preflight.cjs`.
- `expected.json`: retained 77 package hashes, six known Agent graph hashes,
  versions and selected tool hashes; `READY.json`: test inventory/setup freeze.
- `READY`: preparation status; `ORCHREPORT.md`: this report; `commit-msg`.

Added only the unique `agent e2e-viewing-cpu-backend-clean-replay` entry to
`tests/suites.conf`; no existing suite/script was edited. It wraps the entire
foreground controller in `/tmp/timeline-viewing-browser.lock`.

The selected read-only runtime is the explicitly permitted protected
`/home/user/work/wt/vw-m1-ssr-snapshot/remotion`, HEAD
`f8164bef73215272562c4d6974acadbd82c2898a`. All **60 tracked Remotion files**
match the original tested tree. Its actual install and artifact match all 77
retained Composition 0.0.8 hashes. Tarball SHA256 remains
`93bc66b5c63d2d20597c66a2458dcab1c9cd65838b2ff493486c1e84dbec6caa`.
React/ReactDOM remain 18.3.1; Remotion/CLI/renderer/Player remain 4.0.509;
Node/npm remain 20.19.4/10.8.2. The selected browser remains
`/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.

The six hashes match the retained **Agent** graph in
`vw-m3-viewer-host-live-proof/host-live-result.json`; they are deliberately not
the patched App audio graph. The old CPU runner retained the 77 package hashes,
not a separate six-file record. No stronger historical six-file claim is made.
No dependency install, graph copy, browser replacement, shared pin change or
runtime source edit was performed.

Central execution requires its own snapshot and exact `PYTHONPATH=$PWD`.
Before/after guards check original source bytes and modes, root/file device and
inode identities, donor HEAD/source, package bytes, six hashes, installed lock,
versions, tools and setup hashes. The original transport/nested-child browser
selector checks and browser preflight are retained. Successful pytest execution
must also have exactly the eight original JUnit case names, no skip/failure/error,
and three retained MP4/provenance/probe sets. A single-use `RUN_STARTED` marker
prevents another launch; failures return to the manager without retry.

## Validation performed

These checks launched no browser or test body:

```sh
python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-cpu-backend-clean-replay-prep/replay.py --check-only
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-cpu-backend-clean-replay-prep/setup-run.sh
git diff --check
```

Results: **PASS** source/dependency check (2,890 source / 60 runtime / 77
Composition / six hashes); **PASS** shell syntax; **PASS** diff whitespace.
An inline `python3 -` stdlib AST/control check also passed Python syntax,
four-function/eight-case inventory, missing-fresh-grant refusal, unchanged
browser preflight and exactly three historical export directories after excluding
pytest's `current` symlink. No `RUN_STARTED` or new export directory exists.

During final checks the real absolute `orch/QUIET.md` became active for P4.
The grant check refused at that marker and wrote an actual `PAUSED_ACK`; further
validation paused until removal. After release, the missing-grant refusal and
static checks passed. The first control-check attempt did not pass its intended
missing-grant assertion because the earlier live-QUIET refusal fired instead.

**No pytest suite or collection, central request, full suite, browser, export,
RenderService invocation, socket work, git mutation, integration edit or push
was performed. The prepared central path remains unexecuted.**

## Manager handoff

After the harness commits, freeze/protect this branch, its orchestration setup,
the f816 runtime lease and the eventual live `.test-*` snapshot through postflight.
Review `READY.json`. While the absolute QUIET marker exists, remain paused.
After release and fresh peer pause acknowledgements, author
`READY_GRANTED.json` in this worker's orchestration directory with:

```json
{
  "worker": "vw-m3-cpu-backend-clean-replay-prep",
  "suite": "e2e-viewing-cpu-backend-clean-replay",
  "readySha256": "<SHA256 of READY.json>",
  "sourceTree": "<final harness-committed worker tree>",
  "peerPauseAcknowledged": true,
  "runtimeLeaseProtected": true,
  "issuedAtUnix": 0,
  "expiresAtUnix": 0
}
```

Use actual Unix timestamps, issued after READY and the latest PAUSED_ACK, with
at most a 30-minute grant window. These placeholders are not a grant. The runner
checks QUIET/grant again immediately before browser preflight and pytest.
Only the manager then requests **once**:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$("$O/bin/request-test" vw-m3-cpu-backend-clean-replay-prep e2e-viewing-cpu-backend-clean-replay --no-cache)
"$O/bin/wait-test" "$R"
```

Wait the same ID on timeout; never resubmit or remove `RUN_STARTED`. Compare
original **8/8/0/0 and three exports** against actual replay results and both
postflight guards. Keep backend status uncertain until that review; escalate a
nonreproduction as instructed by the audit. No retained source/object was missing;
the remaining dependency is the manager's review, fresh grant and physical replay.
