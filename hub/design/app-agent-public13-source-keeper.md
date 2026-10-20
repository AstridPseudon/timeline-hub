# Agent public13 source keeper

## Selected immutable source

The normal Agent public13 source is already present in the existing Agent
repository and hub refs. No checkout or fetch request was needed, and no fake
archive or synthetic HEAD was used.

- Agent commit: `6f0cdc7df95fe3c9b2d491d6fcb39b754fa212bd`
- Agent tree: `6e3d8589537d581e65e1da21be3e6a7d83022a01`
- Confirmed refs include `hub/tl/agt-m3-public13-kernel-current-port` and
  `hub/tl/vw-m3-d10-source-package-join-deletion`.
- The published source is the merge of `e2c7bdcbe76b225fb075b03d77ded9d95ee626da`
  and `89cdb91da8aa8195955bca55752df018647ef4e4`.

The source is kept as a checkout identity only. This App worktree has no
product-code, Git, shared-dependency, install, build, or public-pin changes.

## Exact source paths and origins

Agent's normal Composition consumer paths are:

- `astrid/core/rendering/remotion_runtime.py`, which requires
  `@banodoco/timeline-composition` `0.0.13` and its normal package exports.
- `remotion/package.json` and `remotion/package-lock.json`, both resolving the
  package from `file:artifacts/banodoco-timeline-composition-0.0.13.tgz`.
- `remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz` and its
  `.sha256` sidecar.
- `remotion/src/` and rendering-pack imports, which import the package and its
  `evaluation`, `theme-api`, registry, effect, animation, and transition
  subpaths rather than a second vendored Composition implementation.

The archive manifest is `@banodoco/timeline-composition` `0.0.13`; its runtime
entry points are the package's `dist` files. The archive has no
`package/typescript/` source tree, so a future installed-host check must not
mistake an optional source-root environment path for the package origin.

The normal Runtime013 source paths are described by Agent's
`runtime.lock.json`. They map to Runtime producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`:

- schema: `astrid/core/timeline/schema/timeline-config.schema.json` from
  `contract/schemas/timeline-config.schema.json`;
- Python client: `astrid_runtime_client/__init__.py`,
  `astrid_runtime_client/contract_metadata.py`,
  `astrid_runtime_client/generated.py`, and
  `astrid_runtime_client/timeline_commit_types.py`;
- response fixtures: `tests/fixtures/runtime-responses/events_page_1_200.json`,
  `events_page_2_200.json`, `invalid_cursor_400.json`,
  `managed_outputs_200.json`, `not_found_404.json`,
  `publish_conflict_409.json`, `task_admission_201.json`,
  `task_read_200.json`, and `validation_error_422.json`; and
- `tests/fixtures/visual-boundary-v1.json`.

The producer-side counterparts are under Runtime's
`conformance/fixtures/`, `conformance/responses/`,
`packages/python/astrid_runtime_client/`, and
`contract/schemas/timeline-config.schema.json` paths, as recorded by each
`from` entry in `runtime.lock.json`.

The Agent client metadata remains contract `0.2.13`, schema digest
`sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`,
and component manifest digest
`sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`.

## Read-only identity checks

- Runtime producer manifest: `contract/artifacts.json`, producer
  `astrid-runtime`, version
  `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`,
  75 artifact entries.
- All 15 Agent Runtime lock files match the producer's corresponding bytes,
  the lock digests, and the producer manifest. The lock's `source_commit` is
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.
- Composition archive SHA-256:
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Composition archive: 58,477 bytes, 77 members, all regular files.
- Composition sidecar equals the archive SHA-256.
- Composition lock entry: version `0.0.13`, resolved path
  `file:artifacts/banodoco-timeline-composition-0.0.13.tgz`, integrity
  `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`.
- Agent `remotion/package.json` SHA-256:
  `4d85289ec9f18d7f0ceb03614f77911b7254b9db62ca65f0a6225b4e641a2682`.
- Agent `remotion/package-lock.json` SHA-256:
  `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.

The Agent manager's existing handoff records the bounded public13 gate as
130 tests passing. That result is retained as prior evidence and was not
relabeled or rerun here. Old Agent8130 proofs remain frozen and are not proof
for this new `6f0cdc7d` source.

## Compatibility boundary

This source is compatible for a future real frame/PCM cohort at the immutable
source and package boundary: Agent points at the public13 dist exports and
its normal Runtime013 client bytes match producer `2c4ac180`. It does not
qualify an installed host, real frame output, PCM output, or frame/audio
parity. The current cap/fixture prerequisite still gates launch. No parity
test or duplicate test was added.
