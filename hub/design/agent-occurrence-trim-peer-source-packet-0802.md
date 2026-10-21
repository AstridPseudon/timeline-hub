# Agent → Runtime/App2: occurrence-owned source-window trim, source-only handoff

2026-10-21 08:02 UTC. This is a source-plan request only. It does not register or
generate a command, change a schema/DTO/endpoint/store, create a pin, or activate a
caller. Runtime0734/0736 identified the gap; report0743 supplied the immutable Agent
spike below.

## Exact evidence

- Runtime’s 0736 note says retained sound/source-window rows are occurrence-owned,
  while published `capture_clip_trim` accepts parent/clip only. Existing sound-sheet
  positives remain live.
- Immutable Agent spike: commit
  `cd10b925051258970d98e41a2ba0ca17fd4b5d42`, tree
  `5a114fb8f85ebec61dc9c8de3feb58c1cadcb939`, blob
  `70439f8e78c119da6cec29a50826cadc9b9d20c8`,
  `tests/sdk/test_timeline_occurrence_trim_source_spike.py:1-97`.
- Exact bounded run on that tree/current worker source:

  ```text
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
    /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
    tests/sdk/test_timeline_occurrence_trim_source_spike.py \
    tests/sdk/test_timeline_clip_trim_provider.py \
    tests/editing_conformance/test_recipe_occurrence_media.py \
    tests/sdk/test_timeline_sheet.py
  105 passed in 6.69s
  ```

  The original report0743 run was the same 105-test lane, 105 passed in 5.94s;
  `ruff` and `git diff --check` also passed there.

## Main semantics and the current gap

Main’s actual local sound behavior is already the contract to preserve:

- `astrid/sdk/timeline_sheet.py:141-162` selects non-cut/non-line audio clips and
  prints an existing `from..to` source trim in source seconds. The parser accepts the
  same `trim=a..b` spelling at `:458-489`.
- `astrid/sdk/timeline_sheet.py:1212-1264` applies sound rows through the existing
  `Clip.trim`, `swap_asset`, and scalar helpers. New sound rows use the media asset;
  an explicit trim is applied in place. This legacy path stays LIVE.
- `astrid/sdk/timeline_sheet.py:587-599,623-657` already binds scoped rows to raw
  `occurrence:<id>/clip:<id>` references, and `:714-773` currently routes a changed
  `trim` cell to `capture_clip_trim`.
- `astrid/sdk/timeline/model.py:424-461` reads intrinsic source duration, accepts
  source-second endpoints, writes `from`, `to`, and source-time `hold`, clears static
  `until/for`, and leaves film start fixed. `speed` affects playback duration, not
  the authored source interval.
- The native command is deliberately parent-only today:
  `astrid/sdk/timeline/_trim_commands.py:15-18` requires
  `parent/clip:<id>` and rejects occurrence children; `:59-83` reads the parent
  registry source and records the three target writes; `:95-101` captures v1.
- Existing occurrence media is not an in-place trim carrier. Its exact owner and
  source-window rules are the relevant precedent: explicit raw occurrence/child
  identity and owner selection at
  `astrid/sdk/timeline/native_occurrence_media_commands.py:15-39`, raw child
  `[from,to)`/source-time hold checks at `:146-185`, and birth/materialization
  capture only at `:195-279`. `occurrence.add-media` and `occurrence.swap-media`
  therefore do not close this gap.

## Smallest proposed extension: existing `clip.trim`, version 2

Keep `clip.trim` v1 byte-for-byte in meaning for `parent/clip:<id>`. Add one
versioned branch, `clip.trim@2`, with the same `{in_s, out_s}` arguments and the
same command operation. The selector itself is the owner declaration; do not add a
new owner field or infer ownership from a display ID.

```json
{
  "schema_version": 1,
  "op": "clip.trim",
  "version": "2",
  "select": "occurrence:occ-a/clip:clip-a",
  "args": {"in_s": 3, "out_s": 5},
  "intent": {}
}
```

The exact source contract for that branch is:

| Concern | Proposed contract |
|---|---|
| Units | `in_s`/`out_s`, `from`/`to`, and `hold` are source seconds. The window is half-open `[in_s, out_s)`; `hold = out_s - in_s`. `speed` changes playback duration to `hold / speed`, never the source units. |
| Authority | Use the existing verified selected-media descriptor for the intrinsic `duration_seconds`, together with the exact occurrence registry binding. No caller-supplied duration, literal text-size slice, display-ID lookup, or re-read from an unverified source. |
| Owner | The raw selector’s occurrence owns the child and its registry/source read. The target is exactly `occurrence:<raw>/clip:<raw>`; no parent remap, shared-shot rewrite, or sibling fan-out. |
| Reads | Read target identity/type/asset/at/from/to/hold/speed/app plus supported timing fields; select and guard `collection.clips` membership/order for the occurrence; read the occurrence map/placement, occurrence and parent output fps, owner registry asset identity/source fields, and the verified media descriptor. Preserve opaque siblings. |
| Source window | Require a literal media child, translation-only active occurrence, no occurrence `source_offset`/time map or internal source map, matching parent/child fps, positive finite `[from,to)` inside the verified source, and source-window/hold consistency. Existing occurrence media guards are the precedent. |
| Rounding | Reuse `trim_source_interval` (`astrid/sdk/timeline/units.py:13-32`): nearest six-decimal authored source endpoints, pull an endpoint back inside the intrinsic limit, and refuse a collapsed interval. Do not frame-quantize authored source seconds; only existing rate/consumed-extent rules may use rational fps. |
| Writes | Exactly the selected child’s `from`, `to`, and `hold`, plus the existing trim cleanup of static `app` intent if applicable. No write to the parent, occurrence placement, registry identity, sibling, or source bytes. |
| Inverse/rebase guards | Keep the ordinary recorder’s exact before/after writes, source dependency, target binding, membership/order selection, owner/map/fps reads, and source/media identity guards. Undo must refuse target/source/selection changes, occupied/rebound identities, or A→B→A intervening writes; disjoint sibling edits may rebase. |

The spike’s proposed recorder footprint is deliberately only a test description,
not an implementation: `tests/sdk/test_timeline_occurrence_trim_source_spike.py:9-42`
reads the raw occurrence child, owner registry/source and fps inputs, binds
`trim.source`/`trim.target`, and writes only `from`, `to`, `hold`; its assertions at
`:43-97` prove the current v1 refusal, add-media’s birth-only source carrier,
three-write footprint, sibling isolation, source identity, and no input mutation.

## Required tests when this source is later implemented

1. Keep all current parent v1, ordinary sound, and source-window positives strict;
   in particular, no refusal-only conversion of the live sound path.
2. Add one occurrence-sheet `trim=a..b` positive through the existing bound raw ref,
   asserting exact v2 command bytes, source-second hold, speed playback length,
   six-decimal boundary behavior, and exact inverse.
3. Add negative controls for display-ID/parent remap, shared occurrence, source-map
   or non-translation placement, fps mismatch, wrong/missing verified media, changed
   registry/media identity, out-of-range/collapsed windows, and occupied/missing
   child identity; all must leave the bundle unchanged.
4. Add two occurrence siblings and prove only the selected child changes; prove
   disjoint rebase, target/source/selection conflict, and A→B→A guarded undo.
5. Keep add/swap birth/materialization tests separate; they are not evidence of
   in-place trim.

## Agreement requested

**Runtime:** please ACK or identify one concrete mismatch in the authority/read
contract above, especially the exact verified-media duration, owner registry/source
read, occurrence map/fps guards, and three-write footprint. Do not duplicate the
current Runtime0736 literal text-size `set-params` slice; it is a separate carrier.
No Runtime DTO/endpoint/store/client/generation/pin/native proof is requested.

**App2:** please ACK or identify one concrete mismatch in the existing bound-sheet
consumer: an occurrence row must retain its raw `# ref`, emit the same `clip.trim@2`
source-second endpoints, preserve legacy sound behavior, and refuse unsupported
mixed edits atomically. Do not infer ownership from display text, add a fallback
writer, or implement/register/generate this proposal yet.

Remaining agreement: Runtime and App2 source-only ACKs (or concrete mismatch) for
the contract above. Until both agree and the orchestrator authorizes the next step,
the proposal remains unregistered and no caller/schema/pin/generation changes are
allowed.
