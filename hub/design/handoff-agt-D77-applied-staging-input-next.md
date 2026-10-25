# D77 applied-source staging input inventory

Date: 2026-10-25 UTC  
Disposition: **SOURCE-ONLY / UNPROVIDED APPLIED DEPLOYMENT**

This is a read-only inventory for the D108 source rehearsal. It does not
execute staging, build or install anything, acquire archives, start a Runtime,
open a socket, run a renderer, or run the D13 test.

## Exact applied graph

The authoritative source rehearsal manifest is
`handoff-rt-D108-0645-d108-source-rehearsal-manifest.json`, SHA-256
`37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`.
Its applied tuple is:

| component | applied commit | applied tree |
| --- | --- | --- |
| Agent | `cd3f5480350d1ca68c9d8ec16aeae2863501c2a4` | `523893dcf54dbe756db8fe2915d14055b1da660b` |
| Runtime | `62040eeab98747dfb65abb6366236bf213109d6c` | `a522511414947e48e317a5e5c2103483b121a750` |
| App | `5391d71d871c73458ef27710fc132694d57983dd` | `204a9216697953f765b5bd550aefa5822503a44c` |
| Composition | `ccd3a1084a9a4adc8f391befe01828ca7f9612e8` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` |

The Agent applied patch SHA-256 is
`348350d78ee5cea1f4736e5962990128a579e88836e0c84a9cfb8788b809da3e`.
The manifest records source-stage `SOURCEONLY/PASS`, with build, render and
ZIP still `PENDING`; that status is not installed-deployment qualification.

## Carrier result

**No authentic deployment receipt or matching seven-key carrier was found for
Agent `523893dc...` / tree `523893dc...`.** The following required values are
therefore `UNPROVIDED` for the applied graph:

| required D13 value | applied-graph result |
| --- | --- |
| `agent_commit` | `UNPROVIDED` as an installed-carrier field; source-manifest value is the exact commit above |
| `agent_tree` | `UNPROVIDED` as an installed-carrier field; source-manifest value is the exact tree above |
| `agent_wheel` | `UNPROVIDED` |
| `agent_wheel_sha256` | `UNPROVIDED` |
| `source_checkout` | `UNPROVIDED` for an installed applied checkout |
| `source_digest` | `UNPROVIDED` for an installed applied checkout |
| `runtime_environment` | `UNPROVIDED` |
| installed schema package/path and hash | `UNPROVIDED` for the applied graph |
| Remotion project/package-lock and hash | `UNPROVIDED` for the applied graph |
| normal transfer/staging receipt | `UNPROVIDED` |

The existing durable carriers are not matches and remain rejected inputs:

* `workers/agt-F-D13-inputs-1017/d13-bindings.json` is Agent
  `ef851b22c506245441b9a630c093b3460e39cbdc` / tree
  `b11eee891208d11e23c55950f8954ddd3377d5a8`, wheel SHA-256
  `fcccab4dc881faa4eead1f971fc655dc96ebfac9efac199015794d7b644007e3`,
  source digest `302834da6581954c2cb070e99fb4021bea6775cdde2ba351057ca832279f2326`,
  and Runtime `1365e4b17b31c4a7093d5943674637067fd2bab4` / tree
  `6c69c3dc47822fffbaf27cd63815d2895155ffaa`. It is explicitly not the
  applied graph.
* The older `f4edcb4b...` / tree `1cbd1801...` carrier has wheel SHA-256
  `7455220aa1d3f8c67c7c9cee0f7a6571fb4f51882eca2543ead25943eebd185a` and
  source digest `f6cdf8c2daada3f4877802baf839cdbecede7943fc3c0312d2aa4d4933abe09a`.
  It is the historical `f4ed`/0013 family and is not an applied-523893 input.
* The current local Composition artifact SHA-256
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` is
  current integration material only. It is not relabeled as an applied-Agent
  artifact and supplies no installed schema Python package.

The 2026-10-25 Runtime peer confirms this disposition: the installed-render
preparation was **NOT RUN** because a genuine source profile, seven-key
carrier, installed schema, and Remotion inputs were missing. No old profile,
fake carrier, or near-match was used.

## Exact ordinary production route

The source-traced caller and materialization route are the existing installer
implementation, not a new handoff framework:

1. `astrid/installer/cli.py:41-111` selects `install`/`update`, constructs
   `Backend(root, log, uv)`, reads and validates the hosted manifest through
   `tools.validate_manifest`, then calls
   `Installer(root, data, backend).run(mode, manifest, ...)`.
2. `astrid/installer/core.py:245-246` calls `self.backend.stage(manifest,
   self.root, self.data)` after the normal update stop/backup path. The normal
   continuation at `core.py:247-274` performs upgrade or create/attach,
   switches `root/current`, registers and starts the selected version, verifies
   the Runtime realm, and finishes retention. No alternative staging caller is
   selected here.
3. `astrid/installer/backend.py:386-430` is the concrete `Backend.stage`
   route. It:
   * defaults the omitted VibeComfy source to
     `VIBECOMFY_ENGINE_REVISION`;
   * checks the selected `uv --version` against `manifest["tools"]["uv"]`;
   * creates `root/versions/<agent8>-<runtime8>-<random8>/`;
   * materializes Agent to `a`, Runtime to `r`, and VibeComfy to `v` with
     `tools.source(name, sha, destination[, repo=...])`;
   * runs `_verify_local_timeline_schema` at `backend.py:172-187`, requiring
     `a/astrid/core/timeline/schema/timeline-config.schema.json` and its
     `runtime.lock.json` pin to `contract/schemas/timeline-config.schema.json`;
   * creates `py` with the manifest Python version, installs the Agent
     `requirements/runtime.lock` with `uv pip --require-hashes`, then installs
     Runtime, `r/packages/python`, Agent, and VibeComfy with the normal
     `uv pip --no-deps` call at `backend.py:404-407`;
   * materializes the pinned tool set via `install_tools` (Node/Bun/media/OMP),
     installs the locked Remotion dependencies, and calls `_declare_services`;
   * computes `source_digest` using the installed interpreter's
     `astrid.core.execution.generic_host.source_checkout_digest` and writes the
     normal `profile.json` fields `profile`, `runtime_checkout`,
     `source_checkout`, `runtime_environment`, `source_digest`, and
     `service_declaration`, followed by `version.json` and `manifest.json`.
4. `astrid/installer/tools.py:214-237` is the source transfer primitive. A
   full 40-hex commit is required. With `repo`, it uses `git cat-file`/`git
   archive` from that local repository; without `repo`, it fetches the normal
   GitHub `<repo>/archive/<sha>.tar.gz`, verifies the expected one-directory
   archive shape, and moves the extracted tree into `a`, `r`, or `v`.
   This task did not invoke either branch.
5. `astrid/services.py:14-54` writes the normal service declaration. The
   `pack-host` row launches the selected installed `python -m
   astrid.core.execution.generic_host --service --source-checkout <a>
   --support-root <runtime support>` and uses the selected Python in
   `ASTRID_PACK_HOST_PYTHON`.

## Concrete required materialization

The smallest real applied deployment needed before any D13 installed preflight
is a private, noneditable result of the route above, bound to the exact four
applied commits/trees—not a copied current checkout and not a renamed old
carrier. It must contain:

* an exact Agent source archive/tree for commit `cd3f...` and tree `523893...`,
  plus the normal Agent `runtime.lock.json` and local schema pin;
* exact Runtime `62040...`/`a522...`, its `packages/python`, and exact
  VibeComfy source selected by the effective manifest;
* the `py` runtime environment with the hash-locked Agent runtime dependency
  set and the selected product distributions installed noneditably;
* the normal `tools/` and Remotion `node_modules` closure, with their actual
  lock/tool hashes; and
* the normal profile/service/version/manifest outputs from `Backend.stage`.

For the existing D13 test graph, an additional exact test-input carrier is
needed after that materialization: the seven keys
`agent_commit`, `agent_tree`, `agent_wheel`, `agent_wheel_sha256`,
`source_checkout`, `source_digest`, and `runtime_environment`, plus the
existing external input hashes read by `_d13_inputs` in
`tests/packs/video_editing/test_runtime_publication_chain.py:44-124`.
The test's required installed origins are exactly `host`, `child`, `action`,
`client`, `sdk`, `runtime_protocol`, `runtime_protocol.platform`, and
`astrid_runtime` (`:47-51`); its profile carrier is the existing four-key
SourceProfile shape (`:44-47`), and its wheel/RECORD/source parity checks are
at `:170-341` and `:357-443`.

`Backend.stage` does not itself emit an `agent_wheel` or seven-key JSON
carrier; those are manager/test inputs that must truthfully identify the
resulting exact installed bytes. Since no applied-523893 wheel, installed
profile, schema/Remotion closure, or normal transfer receipt exists, the
smallest honest result this pass is the source route and the `UNPROVIDED`
inventory above. No profile, wheel, receipt, owner marker, bench-store state,
or retry was constructed.

## D13 graph and limits

The current D13 node is
`tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight`
at `:673-678` in the read-only current Agent graph. It only checks the exact
installed tuple/profile/resource contract; it does not create the applied
deployment. The normal downstream D13 environment gap remains a Runtime peer
input dependency, not an Agent or orchestrator authority decision.

The original D77 source trace remains UNKNOWN for a genuine staged host:
`handoff-rt-D77-upstream-source-trace-1749.md` proves only source controls and
mocked staging controls. The strict D72 review also records the concrete
schema/runtime distinction: local JSON verification in `Backend.stage` is not
equivalent to an installed Python schema package when the strict host reader
requires the package. That unresolved runtime input is preserved here rather
than inferred from a current Composition artifact.

No production caller, Runtime writer, render controller, authority, schema,
pin, test, or generated file was changed.
