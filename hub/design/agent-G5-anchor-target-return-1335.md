# G5 anchored helper target return — blocked causal handoff

## Result

No worktree change was made. The requested connection cannot be made in the
scoped fixture without changing the retained child topology or adding an Agent
production binding path, both of which the brief forbids.

The retained positive is still the same child target:

```text
occurrence:occ-film/clip:inside
owner = ("occ-film", "film", "inside")
app.astrid.cut = "c2"
app.astrid.on = '"second"'
at = 4.6
```

The genuine public Runtime transcript capture resolves the exact source
`occurrence:occ-film/clip:vo2`, the exact `media.transcript/v1` pin and the
stable word ID below. The existing registered `clip.anchor` operation records
that source, but its target contract is parent-only. It cannot record a
binding for the retained child target. The Agent timing validator then refuses
the newly introduced child legacy word declaration before the cut setup reaches
Runtime acceptance.

## Full source/capture/binding map

This is the exact map from the one corrected probe (Runtime
`rt-pin-8592822f`):

```json
{
  "runtime_scope": {
    "project": "907b00659b7d4c86a054ba494ca0c360",
    "timeline": "t"
  },
  "base_pair": {
    "revision_id": "authoring-parent-revision-69ccc29a78a6c972128d90f48ef441f9dd0fc51ec846f5d4f69983a81065accc",
    "content_digest": "sha256:874d7d52aad150c13886dbcf9dadef44a3f7162b83309c219a3a72e846d72205"
  },
  "transcript": {
    "kind": "media.transcript",
    "document_id": "transcript:475e6c4d4b4be4f229434174c64532c074dcc6851ad6ffeaced06790fd14bcc6",
    "version": 1,
    "content_digest": "sha256:f01e8e5776c7bda992a54db9022576facda56b1e0e73528b06b96dbcf23c11f2",
    "content": {
      "schema": "media.transcript/v1",
      "media_id": "sha256:a25513c7e0f6eaa80a3337ee18081b9e2ed09e00af8531c8f7bb2542764027e7",
      "source_id": "astrid.narration",
      "segments": [{
        "id": "s2",
        "start": 0.1,
        "end": 0.4,
        "text": "second",
        "words": [{
          "id": "word:0759e1ca31a50b4c2b49f59e406ca8ae4b6be00f6e864255875ed7c00bf33934",
          "start": 0.1,
          "end": 0.4,
          "text": "second"
        }]
      }]
    }
  },
  "choice": {
    "source": "occurrence:occ-film/clip:vo2",
    "document": {
      "document_id": "transcript:475e6c4d4b4be4f229434174c64532c074dcc6851ad6ffeaced06790fd14bcc6",
      "version": 1,
      "content_digest": "sha256:f01e8e5776c7bda992a54db9022576facda56b1e0e73528b06b96dbcf23c11f2"
    },
    "word_ids": ["word:0759e1ca31a50b4c2b49f59e406ca8ae4b6be00f6e864255875ed7c00bf33934"],
    "edge": "start",
    "offset_s": 0,
    "offset_frames": 0
  },
  "native_capture": {
    "operation": "clip.anchor",
    "captured_target": "parent/clip:anchor-carrier",
    "bindings": [{
      "key": "anchor.source",
      "ref": "occurrence:occ-film/clip:vo2",
      "policy": "follow",
      "dependencies": ["anchor.transcript"]
    }],
    "dependencies": [{
      "key": "anchor.transcript",
      "kind": "transcript",
      "pin": {
        "document_id": "transcript:475e6c4d4b4be4f229434174c64532c074dcc6851ad6ffeaced06790fd14bcc6",
        "version": 1,
        "content_digest": "sha256:f01e8e5776c7bda992a54db9022576facda56b1e0e73528b06b96dbcf23c11f2"
      },
      "policy": "exact"
    }],
    "authored": {
      "parent/clip:anchor-carrier::app.astrid.on": "\"second\"",
      "parent/clip:anchor-carrier::app.astrid.word_anchors.on": {
        "source": "occurrence:occ-film/clip:vo2",
        "word_ids": ["word:0759e1ca31a50b4c2b49f59e406ca8ae4b6be00f6e864255875ed7c00bf33934"]
      }
    }
  },
  "retained_target": {
    "select": "occurrence:occ-film/clip:inside",
    "owner": ["occ-film", "film", "inside"],
    "cut": "c2",
    "declaration": "\"second\"",
    "at": 4.6
  },
  "target_mapping": {
    "source_owner": ["occ-film", "film", "vo2"],
    "desired_target_owner": ["occ-film", "film", "inside"],
    "recorded_native_target_owner": ["parent", "", "anchor-carrier"],
    "same_target_capture_error": {
      "type": "CommandError",
      "message": "'occurrence:occ-film/clip:inside' does not match '^parent/clip:(?!.*::)[^/]+$'"
    },
    "classification": "The exact source authority is genuine and stable, but the recorded binding is for a different physical/ownership representation. No safe typed-binding lookup or alias handoff exists in this scoped test; inventing one would change causality."
  }
}
```

## Evidence

Using the requested Runtime 859 checkout:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8592822f \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8592822f \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_helper_capture.py::test_genuine_anchor_capture_has_exact_source_scope_and_base_pair \
  tests/sdk/test_timeline_helper_capture.py::test_missing_or_forged_anchor_binding_never_writes \
  --basetemp=/tmp/agt-g5-anchor-controls-859
```

Result: **3 passed in 18.50s**. This covers the public Runtime document read,
exact project/timeline scope and authenticated base pair, exact transcript pin
and stable word binding, plus same-word/missing-pin/forged-word refusal with
SQLite no-write assertions.

The one corrected retained node was run once after the genuine capture was
available:

```text
... pytest tests/sdk/test_timeline_helper_capture.py \
  -k 'test_cut_nudge_restart_merges_other_cut and second' \
  --basetemp=/tmp/agt-g5-anchor-second-859
```

Result: **1 failed** at the `Cut setup` commit with:
`candidate.timing: missing exact word binding for ('occ-film', 'film', 'inside').on`.
The failure is before nudge/save/restart/peer-other-cut publication, so no
anchored helper behavior is claimed.

The complete scoped helper file on Runtime 859 was also run once:

```text
... pytest tests/sdk/test_timeline_helper_capture.py \
  --basetemp=/tmp/agt-g5-anchor-helper-859
```

Result: **23 passed, 2 failed in 154.09s**. The second failure is the existing
`test_contiguous_helpers_keep_sequential_steps[True]` moved-head
`root is outside the verified closure` blocker; it is outside this fixture-only
return.

Static and integrity checks:

- `ruff check --no-cache tests/sdk/test_timeline_helper_capture.py`: **pass**.
- `scripts.reshape.compare_ruff_baseline`: **current=2149, baseline=2149**.
- `scripts.reshape.compare_mypy_baseline`: **current=1912, baseline=1912**.
- `git diff --check`: **pass**.
- AST body mapping against `HEAD`: **13/13 function bodies equal; no changes**.
- `git status --short`: clean; no production, Runtime, schema, pin,
  generated, shared dependency, or test file change.

## Blocker and handoff

The blocker is an Agent ownership/representation gap, not Runtime source
authority: `clip.anchor` and its compiler binding are parent-owned, while the
promised positive introduces a word declaration on a child clip. Retargeting
the child to a parent-only carrier, flattening/replacing the original topology,
stripping the declaration, or manually attaching a guessed `WordBinding` would
violate the settled brief. The next owner must add/qualify the existing
child-target typed-binding/physical-alias handoff in the appropriate Agent
production slice, then rerun this unchanged retained positive and its strict
negative controls. G5 remains DRAFT-only / P1 NO-GO.
