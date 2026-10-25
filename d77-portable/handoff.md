# D124.6 / D77 Farm stage/render handoff

## D77 corrected source provenance

The temporary `cd3f5480350d1ca68c9d8ec16aeae2863501c2a4` and
`62040eeab98747dfb65abb6366236bf213109d6c` labels are historical and are not
present in the product repositories. The exact source trees are preserved by
the truthful live heads published at
`timeline/agent/tl/rt-D77-Agent-applied-source-1620`
(`91398e9de4500ce16c8e55741209ba3609cb1694`) and
`timeline/runtime/tl/rt-D77-Runtime-applied-source-1620`
(`1daca2a33f6d7b10053e07c539a54843e3984e19`). This handoff uses the normal
`tl` branch/hub route: the lead performs normal fetch/code publication, with
no integration merge; a worker does not write a remote helper or the hub.
Rendering-child qualification remains **UNKNOWN**.

Sol1243 is the author of the guard; independent Luna1257 recorded PASS for 18
flat controls in `design/handoff-rt-D77-guard-review-1257.md` (SHA-256
`cdbb9fd919edf832e2da6f09e591f9aa9366cefd51d3f87ab44c8acf0211e57e`), and
Custody1300 independently recorded PASS A in
`design/rt-D124-handoff-custody-review-1300.md` (SHA-256
`8b29293a95628463bf567b82b852e23d679685af9b7a11d527b554ee58b8f588`). D131's
`123bb93c` change is reserve-only, not an ownership fix. The recorded a4e016
retained-source refusal remains unresolved and dropped; there is no bypass,
retry, or Farm-core cycle. Any new D77 source request requires the lead's
actual disposition through the ordinary guarded path; this handoff invents no
seven-key, profile, or manifest values.

Status: source-only preparation from Composition `tl/integration`; no phase ran on Main, and this worker did not fetch, duplicate an archive, materialize a checkout, install, stage, render, or create a collector. The copyable shell recipe is [farm-stage-render-recipe.sh](../workers/rt-D124-Farm-render-handoff-1253/evidence/farm-stage-render-recipe.sh). It is deliberately gated on an independently recorded Sol1243 PASS and Farm's own storage admission.

## Farm lead brief

```text
Run this on Farm only, after independently recording Sol1243 guard PASS and
strict fresh-heavy admission free > 5,200,000,000 bytes. Run stage, then
preflight, then genuine render, and retain durable private results. Do not run
any phase on Main. Do not use profile819acf, old f4ed/0013 carriers, or the
D123 b742893 candidate. Do not use ZIPs or ad-hoc copies.

ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch

"$ORCH/bin/request-checkout" agent \
  91398e9de4500ce16c8e55741209ba3609cb1694 \
  'D124.6 exact applied Agent source'
"$ORCH/bin/request-checkout" runtime \
  1daca2a33f6d7b10053e07c539a54843e3984e19 \
  'D124.6 exact applied Runtime source'

env -u RUNTIME_AGENT_CHECKOUT -u RUNTIME_RUNTIME_CHECKOUT \
  -u RUNTIME_RUNTIME_SHA -u RUNTIME_TEMPLATE_SUITE -u RUNTIME_NODE_BIN \
  "$ORCH/bin/request-runtime" agent-remotion-d124-applied \
  91398e9de4500ce16c8e55741209ba3609cb1694 \
  f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d \
  /home/user/work/wt/agt-pin-91398e9 \
  /home/user/work/wt/rt-pin-1daca2a \
  1daca2a33f6d7b10053e07c539a54843e3984e19 remotion-env-nodes \
  /home/user/work/toolchain/node-v20.19.4-linux-x64/bin

"$ORCH/bin/request-child-venv" venv-agent-child-d124-applied \
  91398e9de4500ce16c8e55741209ba3609cb1694 \
  --source-carrier /home/user/work/wt/agt-pin-91398e9 \
  /home/user/work/wt/rt-pin-1daca2a \
  1daca2a33f6d7b10053e07c539a54843e3984e19

# After exact receipts and an authenticated manifest are present, use the
# normal installed astrid/run-astrid launcher.  This is not a direct CLI file
# or Backend call.  Then use the recipe's actual profile/custody values.
./evidence/farm-stage-render-recipe.sh
```

The recipe is the authoritative argv/env shape. Farm must set its required
variables from normal requester and installer receipts, including
`ASTRID_RUN`, `INSTALL_MANIFEST`, `PROGRAM_ROOT`, `DATA_ROOT`, `UV`, actual
post-stage `PROFILE`, the seven-key `BINDINGS`, pack-host `PY`/`SITE`, exact
Runtime, Remotion project, Node, browser, ffmpeg, ffprobe, `ASTRID_PACKS_PATH`,
private `RUN_ROOT`, and private `RESULT_ROOT`. The recipe verifies the exact
Agent/Runtime commit and tree and requires clean checkouts. The manifest must
carry the exact VibeComfy pin `31f90bb03d330283b76e7dbdda51197be787090d`, tree
`101744f0d87eebe5ddf6752c10f01f52dc94e3e9`.

Transport only the small public source identity/hash records and ordinary
requester receipts. Keep profile, bindings, source digests, installed origins,
logs, and rendered media private under Farm's result root. The recipe writes
durable `source-identities.txt`, `status.txt`, stage/preflight/render stdout and
stderr there. It does not create or send a ZIP.

## Immutable source custody

The applied source tuple is:

| source | exact commit | exact tree |
| --- | --- | --- |
| Agent | `91398e9de4500ce16c8e55741209ba3609cb1694` | `523893dcf54dbe756db8fe2915d14055b1da660b` |
| Runtime | `1daca2a33f6d7b10053e07c539a54843e3984e19` | `a522511414947e48e317a5e5c2103483b121a750` |
| VibeComfy | `31f90bb03d330283b76e7dbdda51197be787090d` | `101744f0d87eebe5ddf6752c10f01f52dc94e3e9` |
| public OMP | `9e282751c0059e37d2f6fbc14ffa0b450710bd23` | `2074d7a2e26cc954b5cf3d77e91f3efbb25ad34f` |

OMP's retained supported-local-input controls are archive SHA-256
`a7673f9f9b77d24989a5a84b70380f77af3dd869a7be2b94c8d56de404065ecb`, source
tree SHA-256
`3a84ac8be7d11434de8b22f4f0f1d643582ecc01c644e347bb0e056401da7b2e`, Bun lock
SHA-256 `f08eab1fd7e0519e8b131697d6a35815fd71d9b0a61a8d70cc57b499bcba53ee`,
package `17.4.0`, Bun `1.3.14`. The permitted source input was public Git with
`GIT_LFS_SKIP_SMUDGE=1`; fsck passed and retained LFS pointer count was zero.
The exact Remotion lock SHA-256 is
`f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d`.

Retained source/rehearsal hashes are recorded in
[source-hashes.txt](../workers/rt-D124-Farm-render-handoff-1253/evidence/source-hashes.txt).
The D108 source manifest SHA-256 is
`37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`; its
phase is `SOURCEONLY` and `build_render_zip` remains `PENDING`.

## Normal route and custody

The production route is `astrid` gateway → `Installer.run` → `Backend.stage` →
service declaration → `generic_host --service` →
`run_pack_host_foreground` → `ensure_pack_host`. Use the normal installed
launcher shape:

```text
ASTRID_RUN install --root PROGRAM_ROOT --data-root DATA_ROOT \
  --manifest INSTALL_MANIFEST --uv UV
```

The authenticated manifest and normal installer own source materialization,
locked dependencies, tools, Remotion dependencies, service declaration,
profile, version, and manifest. A direct `python -m astrid.installer.cli`,
direct `Backend` call, ad-hoc source copy, shared venv, shared
`node_modules`, shared runtime, cache, or archive duplication is not an
equivalent route.

The seven-key carrier must be authentic and retained privately:

```text
agent_commit
agent_tree
agent_wheel
agent_wheel_sha256
source_checkout
source_digest
runtime_environment
```

Do not report a profile, service argv, schema, installed origin, or seven-key
carrier until the ordinary stage receipt supplies it. In particular,
`agent_wheel`, `agent_wheel_sha256`, `source_checkout`, `source_digest`, and
`runtime_environment` are not present in the retained D77 pre-stage artifacts.

## Genuine render selectors

After normal stage has produced the actual profile and custody values, run the
two retained selectors in this order:

```text
tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
```

The second selector is the genuine daemon-backed authoring/final-render
selector. The recipe preserves the exact isolated environment shape from the
retained rehearsal: `ASTRID_HOST_EXECUTION_PROFILE=installed`, installed pack
host and rendering pack paths, actual Remotion project, browser, Node,
ffmpeg/ffprobe, schema path, profile, seven-key bindings, exact Runtime
checkout, and the retained public tool hashes. The profile and all private
paths must come from the Farm stage receipt; none are guessed here.

## Storage and phase gates

Farm owns admission. The fresh heavy start gate is strictly greater than
`5,200,000,000` free bytes; a phase cancels at or below `4,500,000,000`; the
overall stop is `4,000,000,000`. The retained `1,623,728,128` allocated-byte
observation is only a lower bound, not a complete peak. OMP/native and
Remotion/npm peak behavior was not fully measured, so no stage-fit claim is
made. No reserve reduction, shared dependency credit, or reserve hack is
permitted.

Sol1243's retained report records its private guard helper and 18 passing
finite controls, but Farm must independently verify the PASS and retain the
receipt before any new phase. The current D77 stage artifacts stopped before
the ordinary installer and provide no installed profile, service argv, schema,
origins, or seven-key carrier. This handoff does not turn those unknowns into
claims.

## V2 request contract

The production caller remains unchanged. A request carries
`api_version`, `project_id`, `timeline_id`, `base_revision_id`,
`base_publication_id`, `commands`, `label`, `steps`, `merge`, `reads`,
`dry_run`, and HTTP `Idempotency-Key`; each step carries `id`, `label`,
`intent`, `tags`, `command_ordinals`, `patch`, and `reads`. Accepted/merged
replies carry `canonical_document`, `receipt`, `head`, `effects`, `bindings`,
and `dependencies` alongside `accepted`/`merged`; conflicts return `head` and
`reason`; invalid requests return `code`, `path`, and `hint`; dry runs write
nothing. No contract or production-behavior change is proposed.

## EXACTMISSING

The following are deliberately unresolved and must be supplied by Farm's
normal control plane before stage/render:

- independent Sol1243 PASS receipt/path;
- Farm free-space admission and a complete finite peak bound;
- exact request-checkout, request-runtime, and request-child-venv receipts;
- authenticated installer manifest and ordinary installer receipt;
- actual installed profile, service declaration/argv, schema, and origins;
- authentic seven-key carrier values and private source digest custody;
- actual installed Python/site/Remotion/Node/browser/ffmpeg/ffprobe paths and verified hashes;
- preflight result, genuine render result, and durable result paths;
- all private payload bytes and rendered media.

