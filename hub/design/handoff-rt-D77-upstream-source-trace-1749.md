# D77 upstream render-path evidence

## Scope and verdict

Verdict: **UNKNOWN** for the requested genuine staged-host result.

The upstream source path is internally complete and its finite mocked staging
controls pass, but no authenticated upstream npm archive was available for a
read-only artifact inspection, and the task forbids installation, acquisition,
or an installed-host/render-body run. Therefore this evidence does not prove
that the real v0.0.6 archive extracts the Python subtree and that a real staged
host reaches readiness.

This is not evidence that upstream fails. The unresolved limit is actual
archive extraction plus the real staged Python environment/host validation.

## Exact source identities

- Agent HEAD: `92443771676ef2bbb547d0a103d708fa8bec4c63`;
  tree `a81a8c7f262e4416dcdefc0720fd760e026d766b`.
- Composition source: `67b8aa3d0d6831d3e3504a340ff583c3da253707` (`v0.0.6`);
  tree `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120`.
- Upstream source blobs: `remotion/package.json`
  `992262dd204a39564d0adff5a59d47bca33e2e11`, `remotion/package-lock.json`
  `526705c1b8e31bff9ae8c9001043e7b7ca046951`, installer backend
  `e28357d09172bce9c09540ae3bf777f6cf280f5a`, host bootstrap
  `0c04a4444a36dba2eeb416b4fd0937badc591b96`, strict reader
  `f66e28b20c1bcba13b5de78897eeca380c5e3105`.

## Upstream declared and executed path

1. `remotion/package.json` declares Composition archive
   `...timeline-composition.../v0.0.6.tar.gz`.
2. Composition `67b8aa3d0` declares the transitive schema archive
   `...timeline-schema.../v0.0.1.tar.gz`.
3. Agent `remotion/package-lock.json` records both archives and integrity:
   Composition `sha512-QV17ysuq...OMgtsZg==`; schema
   `sha512-m7oUjUV+...WCgUS8lQ==`.
4. `astrid/installer/backend.py:397-404` runs the locked Remotion install,
   then invokes `uv pip install --no-deps` on
   `a/remotion/node_modules/@banodoco/timeline-schema/python` before
   `_declare_services`.
5. `astrid/services.py:43-47,81-90` launches the generic `pack-host` with the
   staged Agent source checkout. `host_bootstrap.py:745-759,865-888` calls
   `_provision_render_runtime_env`; its lines 485-496 derive
   `ASTRID_TIMELINE_SCHEMA_PYTHONPATH` from that installed schema subtree.
6. The strict reader requires the three Banodoco packages plus six Python
   schema files (`remotion_runtime.py:46-89,324-350`) and `_SCHEMA_PROBE`
   imports `AssetEntry`, `Theme`, `ThemeOverrides`, `TimelineClip`,
   `TimelineConfig`, `TimelineOutput`, `materialize_output`, and `resolve_theme`.
7. Actual host consumers are `generic_host.py:6270-6282` (full preflight),
   `generic_host.py:7840-7845` (worker validation), and the Remotion renderer
   `packs/rendering/rendering/renderers/remotion/run.py:441-443`.

## Finite controls run against upstream HEAD

- `PYTHONPATH="$PWD:/home/user/work/runtime:/home/user/work/runtime/packages/python" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest tests/test_installer_schema.py -q -o addopts= -p no:cacheprovider --junitxml=.../installer-schema.xml`
  -> **2 passed**. This is a mocked stage control: it creates the schema
  subtree after a mocked `npm ci`; it does not authenticate or extract the
  upstream archive.
- Same environment, `pytest tests/stage1/test_cold_launch_autobootstrap.py tests/core/rendering/test_node_pin.py -q -o addopts= -p no:cacheprovider --junitxml=.../bootstrap-node.xml`
  -> **41 passed**. These controls exercise source-level bootstrap/Node-path
  behavior with temporary fixtures, not a genuine installed host.

## Corrected b4/current integration comparison

- b4: `b4f79d12e0037f283ccc929f364f38d21dc50d4a` uses the local canonical
  `astrid/core/timeline/schema/timeline-config.schema.json` digest
  `sha256:4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd`
  and removes the external npm schema install. Its lock has only the local
  Composition artifact.
- Current integration `f4d6c72ce336da66813fc39828187bccbaf80a5b` declares local
  Composition artifact `remotion/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz`, package version `0.0.14`,
  lock integrity `sha512-Ajl7ly...Dt65oQ==`, and no `timeline-schema` lock entry.
  Read-only tar listing showed only `package/package.json` for schema-related
  names; no Python/schema payload. The artifact bytes hash is
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Current integration’s backend has a later stale external-schema install at
  lines 398-404; b4 itself has the local verification at lines 400-407 and no
  such install. In both corrected/local routes, the unchanged strict reader
  still requires the external Python models and host bootstrap still derives
  the external package path. The local JSON artifact is therefore not model
  package evidence and was not treated as equivalent.

## Existing installed model control

Prior independently authenticated evidence records
`/home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema`
version `0.0.2`, direct URL Git source `ArtAgents.git` at commit
`242f9c4306bf3b501222cb041a9eb246ef47bc85`, with RECORD entries verified.
Its strict probe passed; a checked-in JSON-schema directory failed the trusted
origin/model probe. This control is only for the package’s true installed
origin/scope; it is not evidence that the upstream v0.0.1 npm archive was
staged or installed.

No product, test, generated, pin, or Git files were changed.
