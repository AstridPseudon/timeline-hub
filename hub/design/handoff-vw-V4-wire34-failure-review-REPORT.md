# FAIL — V4 integrated54 command-identity review

## Classification

V4 is **FAIL54**, not PASS. The authoritative integrated run reached fixture
setup and all 54 original nodes errored before any word-anchor test body ran.
The common refusal was Runtime `invalid_records` / `provider executed a
different command` at `timeline_commit_auth.validate_claims`.

This is a native command-envelope mismatch at the fixture's initial
`track.create`, not a classifier or safety denial, and not evidence that the
V4 source deletion caused the failure.

## Integrated evidence

- Agent commit: `f894c3c9dda25ab03527eeb7f52da5da31d627c1`.
- Agent tree: `d24f25a65be282a56b3fcd814a8718a3c0587b9b`; required `cf31566e8`
  ancestor present.
- Runtime execution checkout: `/home/user/work/wt/rt-pin-ad823e0a`.
- Runtime commit: `ad823e0a0f5be4a7acf1d3006df6f794709da63d`.
- Runtime tree: `33904550800ee3e2fa34fe0b13c26754b46c7fdc`.
- Official client producer in `runtime.lock.json`:
  `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- The compatible execution checkout preserves the official artifact bytes:
  `contract/artifacts.json` SHA-256
  `7c541b705a9dbc0827ed2e81a847455402b1d475491de702cde7ef85f4a8235d`;
  all 15 lock mappings matched in the completed proof.

## Exact submitted-versus-recorded mismatch

The fixture submits this command at
`tests/editing_conformance/native_word_anchor_fixture.py:194-195`:

```json
{
  "schema_version": 1,
  "op": "track.create",
  "version": "1",
  "select": "parent",
  "args": {"row": {"id": "initial", "kind": "audio"}}
}
```

The submitted `created` field is omitted, so Runtime evaluates
`submitted.get("created", [])` as `[]`.

Agent’s normal provider path is `commit.py:1050` → `commands.execute` and
calls `track_create` in `astrid/sdk/timeline/capture.py:235-237`. The normal
`Recording.create` path in `_recording.py:149-172` allocates the canonical
entity and records:

```json
{
  "schema_version": 1,
  "op": "track.create",
  "version": "1",
  "select": "parent",
  "args": {"row": {"id": "initial", "kind": "audio"}},
  "created": ["parent/track:initial"]
}
```

`Recording.finish(capture=True)` sets that `created` list at
`astrid/sdk/timeline/_recording.py:240-264`. The existing capture helper at
`astrid/sdk/timeline/capture.py:258-261` demonstrates the caller-side
authoritative form, but the fixture's initial seed uses the literal command
above rather than that helper.

Runtime then compares the command envelope at
`runtime_protocol/timeline_commit_auth.py:241-248`: the five fields
`schema_version`, `op`, `version`, `select`, and `args` match, but

```text
submitted created: []
recorded  created: ["parent/track:initial"]
```

The comparison is invoked from
`runtime_protocol/timeline_commit_store.py:732-737`, after Agent reaches
`commit.py:1141` → `port.accept` → Runtime store validation. This precisely
explains the recorded `invalid_records: provider executed a different command`
message.

The contract’s creation rule (§2, lines 569-576) says native `created` claims
list canonical entity refs. Therefore the narrow existing owner seam is the
Agent G234 combined join / caller-provider lane: align this native caller with
the existing capture form (or otherwise make the request’s native creation
claim explicit), then let the existing Runtime native14 owner requalify its
strict validation. This review does not change either owner’s source. Do not
start a competing source worker or weaken Runtime’s command-identity check.

## V4 deletion and production-caller evidence

The V4 source deletion is **not causal** on this trace:

- The active production catalog still imports and registers
  `astrid/packs/rendering/editor/catalog.ts:7,17` →
  `ui/threejs-live-editor/extension.tsx`.
- The completed source assertions found six stale `live-scenes` paths absent
  and zero tracked `live-scenes/` paths.
- The failure occurs during initial Runtime command authentication, before the
  anchor test body and without a renderer/scene import. The active caller is
  therefore retained and is not the failing path.
- `tests/editing_conformance/word_binding_recipe.py` and its test companion,
  plus the `clip.anchor` assertions in
  `tests/editing_conformance/test_native_word_anchor.py`, remain present and
  unchanged.

Imported origins recorded by the completed proof:

```text
astrid                     /home/user/work/wt/vw-V4-wire34-integrated
astrid.sdk.timeline.commit /home/user/work/wt/vw-V4-wire34-integrated
astrid_runtime_client      /home/user/work/wt/vw-V4-wire34-integrated
runtime_protocol           /home/user/work/wt/rt-pin-ad823e0a
```

## Required command and result

Exact command already run by the integrated worker (not repeated by this
review):

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ad823e0a PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-ad823e0a /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_native_word_anchor.py
```

Result: **54 errors in 62.44s**. All failures were fixture setup failures at
the mismatch above; no anchor body qualified.

Other evidence:

- `git diff --check`: PASS.
- No product, test, generated, pin, package, or assertion changes were made
  by this review.
- New lint/typecheck: N/A because this review made no source changes. Prior
  normal Agent Ruff `2151` and private mypy `1915` evidence is retained, not
  re-run.
- No full54, native14, browser, full, or heavy suite was repeated.

## Handoff

Consume this classification in the already-owned Agent G234 / Runtime native14
work. After a reviewed source correction, rerun the original54 once on the
resulting integrated head. Until then V4 remains FAIL; this report makes no
V1, H3, full-suite, or physical-parity claim.

