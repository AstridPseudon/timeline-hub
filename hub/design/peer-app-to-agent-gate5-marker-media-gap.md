# App Gate5 marker migration — exact Agent 8130 gap

App ported the intervening Agent edit in `three-products.spec.ts` to the
normal frozen-8130 CLI command path (`timelines edit commands-file`) using two
native `clip.set` commands. The first marker case remains intentionally
unmigrated because the frozen 8130 pair cannot express its old-media input.

## Reproduction against frozen Agent 8130

Source checkout:

```text
/home/user/work/wt/app-m3-agent8130-safety-source-keeper
HEAD 8130a401bf44a518d5a40ae274d398b8c560be55
```

The installed CLI help lists native timeline edit adapters only for `move`,
`track-label`, and `commands-file` (plus ordinary parent trim). The command
file adapter validates registered native commands and captures them through
`TimelineSession.commit_many`; it does not provide a media alias shortcut.

The registered `occurrence.swap-media` operation is present in
`astrid/sdk/timeline/native_occurrence_media_commands.py`, but its exact
arguments require both `old_media` and `media` as five-field
`MediaSelection` values (`asset`, `generation_id`, `variant_id`, `object_id`,
`catalog_digest`). Runtime `RequestCommitPort.selected_media()` also refuses
any selection not declared by the command request.

The seeded `f2-placeholder` registry entry is only the imported/raw fixture
shape (`media_id`, `content_sha256`, `type`, filename). It has no generation,
variant, or catalog pin. The current `clip.set` recipe explicitly allows
`clear: ['asset']` but rejects exposing another media selector; it cannot
replace the asset. Therefore the original marker write
(`--swap-asset f2-marker=task:<task>/marker#0`) cannot be translated into an
accepted 8130 native command without inventing an old selection or bypassing
the provider.

## Executable source check

```sh
AGENT=/home/user/work/wt/app-m3-agent8130-safety-source-keeper \
PYTHONPATH="$AGENT" PYTHONDONTWRITEBYTECODE=1 \
/home/user/work/venv-agent/bin/python -m astrid timelines edit --help
```

The exact source points are:

- `astrid/packs/timeline/cli_native.py`: only `configure_track_label()` and
  `configure_commands_file()` are native timeline adapters;
- `astrid/sdk/timeline/native_occurrence_media_commands.py`: swap requires
  exact verified old/new selections;
- `astrid/sdk/timeline/_clip_scalar_commands.py`: asset assignment is not a
  scalar write; only explicit asset clearing is supported;
- `astrid/sdk/timeline/commit.py`: media operations call
  `port.selected_media()` for each supplied selection.

## Requested Agent-side resolution

Provide a frozen-8130-compatible, public way to obtain and verify the exact
five-field selection for the seeded old media, or otherwise qualify the
fixture as a native media selection. Do not ask App to guess a generation or
catalog pin, manufacture a command receipt, or use a private document/store
writer. Once that source is frozen, App can send one `occurrence.swap-media`
command through the existing `commands-file` adapter while preserving the
marker adoption/opaque/no-reload assertions.
