# G4 current integrated held-image qualification

## Scope and boundary

This is a read-only qualification of the current integrated Agent source
against the genuine Runtime `8592822fd11275540f596562f43c715676f2bc0f`.
It runs exactly the four cases in
`tests/editing_conformance/test_occurrence_hold_current_runtime.py`: image
ADD, image SWAP, and the two parameterized video-hold refusal controls. No
product, test, schema, generated, pin, contract, or dependency files are
changed by this qualification. The prior Runtime `9345cb58...` evidence is
not used.

## Preflight provenance (recorded before test body execution)

- Agent checkout: `/home/user/work/wt/agt-G4-held-image-qualified-1320`
- Agent commit/base: `f6116e1b658514021cbbf08d5a6f16a240523f1a`
- Agent tree: `26f260e0674161f9f786bf93b15a1477a5e63a86`
- Runtime checkout: `/home/user/work/wt/rt-pin-8592822f`
- Runtime commit/base: `8592822fd11275540f596562f43c715676f2bc0f`
- Runtime tree: `ed9856f43a4e44a058bf2230badea2c4c7080050`
- Agent and Runtime worktrees were clean at preflight; Runtime is detached
  at the pinned commit.
- Runtime selection inputs: `PYTHONDONTWRITEBYTECODE=1`,
  `PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f`,
  `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f`, and
  `/home/user/work/venv-agent/bin/python`.
- Provision inputs: `RealmStore.initialize(tmp_path / "realm")`, public
  `RuntimeService.create_project`, provider registration via
  `load_timeline_commit_provider('astrid')`, and public
  `create_timeline(..., idempotency_key='timeline')`.
- Real media seed: the fixture's 68-byte PNG seed has SHA-256
  `431ced6916a2a21a156e38701afe55bbd7f88969fbbfc56d7fe099d47f265460`;
  it is imported twice through `import_media` as `old.png` and `new.png`
  with media type `image/png`. The refusal control creates real `video/mp4`
  bytes through ffmpeg.
- Fixture selector and target: `params=['add', 'swap']`, owner
  `occurrence:occ-a`, target `occurrence:occ-a/clip:clip-a`.

Preflight module origins and SHA-256 hashes:

| Module | Origin | SHA-256 |
| --- | --- | --- |
| `astrid.sdk.timeline.commit` | Agent `astrid/sdk/timeline/commit.py` | `741e8afcca27577e3a620b60351880a8df60aa2f4b48f15e0961fb63695edabc` |
| `astrid.sdk.timeline.commands` | Agent `astrid/sdk/timeline/commands.py` | `d1439159267154f36bda603c030b6b5299058411628b18edcbeea0779743bebf` |
| `astrid.sdk.timeline.native_occurrence_create` | Agent `astrid/sdk/timeline/native_occurrence_create.py` | `962016ffdba404dfd88ed4fbf62bd4882e96e42038a0548549a0cf727ef25d22` |
| `astrid.sdk.timeline.native_occurrence_media_commands` | Agent `astrid/sdk/timeline/native_occurrence_media_commands.py` | `849339bbe7ab62e5a09604c834c08c195a2fec6e0c9757baed226ca9b3a79212` |
| `runtime_protocol.service` | Runtime `runtime_protocol/service.py` | `267bec1aee551e7ea1f92f987adb24268be11c6dd165ee56f24aa68ff2b6a692` |
| `runtime_protocol.store` | Runtime `runtime_protocol/store.py` | `578dd8f075a9d0ab05554e30b48434444c9777ede09379b9e2814a5fbd61c30c` |
| `runtime_protocol.timeline_commit_port` | Runtime `runtime_protocol/timeline_commit_port.py` | `d78dd313220634baaf37c9a6cb7a578b4453c3c94060eb13c02778834eeac867` |
| `runtime_protocol.timeline_commit_provider` | Runtime `runtime_protocol/timeline_commit_provider.py` | `2dff389a11475420395a812d036888ad91c01e16df1170bb77917cc3cf128faf` |

## Qualification result

**Pending execution.**

The exact command and its output will be recorded below. The result boundary
is limited to the four cases above; it is not a whole G4/P2/P3, inverse, or
full-suite claim.

## Durable evidence

The fixture writes accepted ADD/SWAP evidence containing the complete v2
request, prepared reply records, canonical before/after documents, history,
bindings, effects, and module origins. The per-case evidence and final
classification will be linked here after the run.

