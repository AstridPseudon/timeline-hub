# R2r redo native-input ownership review

## Independent verdict

**FAIL for the current redo positive: Agent-owned source-capture defect. Runtime’s refusal is correct.**

This is a source-owner classification, not a behavioral PASS. The retained
accepted native history does not authenticate the working `shot-placement-…`
alias as equivalent to the canonical `document-diff-…-shot` edge required by
the redo stage. No Runtime alias normalization or equal-payload exception is
justified.

## Packet and accepted-history facts

Reviewed the exact packet
`design/agent-R2-redo-media-1404-a29df82beb548306.json`:

- size: `1,481,631` bytes;
- SHA-256: `a29df82beb548306683ab64d738eb776a519587fdb30cad3e997e91468621ef8`;
- embedded source-packet SHA: `9603ca432b1c9d1c1b16908f00547d26da6d04df3ad681308cbae5f3e57635d1`;
- Runtime pin: `cfa0af0d476e6954df041c08d7ef378fd6782932`.

The accepted forward publication is
`txn-7d039d147e1b4c5ba6cc7ca912b95cba`, with ordered steps:

| step | command ordinals | native/effect consequence |
| --- | ---: | --- |
| `fork-edit-0` | `[0]` | `occurrence.fork`; native writes `[0,1]` in the inverse source partition; effects `[5,9]` |
| `fork-edit-1` | `[1]` | `doc.patch`; native writes `[0,1]`; effects `[0,5]` |

The accepted whole undo is
`txn-75285c95600949c8b1267a71f8e71a9d`, with `undo_of` exactly the forward
publication and step `undo-0`. Its authenticated `inverse.stage` order is the
reverse source order, not a final-output reconstruction:

- `fork-edit-1`, source ordinals `[1]`, native range `[0,1]`, effect range `[0,5]`;
- `fork-edit-0`, source ordinals `[0]`, native range `[1,3]`, effect range `[5,9]`.

The redo request targets only that accepted undo and has base publication
`txn-75285c95600949c8b1267a71f8e71a9d` plus the canonical parent revision
`document-diff-e0c6162a4844471b99fd8d1076df92e9-parent-revision`. The retained
redo auth input and source document are byte-equal.

## The decisive counterexample

The forward `occurrence.fork` native capture records this occurrence edge:

```text
occurrence:f2-occurrence / [shot_id]
before = shot-placement-90b9827beed9a42dfba309ec7e05837ada743a57e18dd5f26704de552870c382
after  = selected-shot
```

The accepted undo therefore records the reverse native write in its
`fork-edit-0` stage:

```text
occurrence:f2-occurrence / [shot_id]
before = selected-shot
after  = shot-placement-90b9827beed9a42dfba309ec7e05837ada743a57e18dd5f26704de552870c382
```

But the redo stage begins from the canonical accepted undo input. Its actual
parent occurrence edge is:

```text
f2-occurrence.shot_id = document-diff-e0c6162a4844471b99fd8d1076df92e9-shot
```

Thus Runtime’s sequential check compares `document-diff-…-shot` with the
native write’s claimed `shot-placement-…` before-image and correctly rejects
with `invalid_records: inverse stage write differs from its sequential input`.
This is a direct mismatch at the stage boundary, not a final-byte mismatch.

The canonical accepted source binding is instead:

```text
key          = fork.source
ref          = occurrence:f2-occurrence/source
physical_ref = internal-revision:document-diff-e0c6162a4844471b99fd8d1076df92e9-internal-revision
digest       = sha256:0fd72e6d7c0c4ba0b477d39e9d1624e5ae3712ad596f0a6dd136bb30032f367d
owners       = occurrence:f2-occurrence/shot,
               occurrence:shared-sibling/shot
```

The accepted effect pins separately identify the canonical parent image
(`document-diff-…-parent-revision`, digest
`sha256:d27b4d12889d6e8d76d6ac7f47668cff6c0e25b901a14ece5f4da6061853b74e`)
and the occurrence-local selected roots (`authoring-shot-revision-e568…`,
`authoring-timeline-revision-7a35…`, owner only
`occurrence:f2-occurrence/shot`). The accepted undo’s final canonical parent
effect remains the same `document-diff-…-parent-revision` and digest. None of
these authenticated physical bindings names `shot-placement-…`.

## C0 classification

C0 §2 requires closure resolution to physical images, persistence of the
submitted ref plus physical ref, revision, digest, boundary and managed edge,
and says identity IDs, matching bytes and newest-revision searches are not
provenance. It also requires occurrence edges to follow their exact shot
revision pins. C0 §5 requires undo/redo to load authenticated closures and
native facts, then inherit authenticated provenance; it does not permit a
caller or Runtime to infer provenance from an inverse write.

There is no accepted-history mapping for the alias. A packet scan found
`shot-placement-…` only in authored/native values (`expect`, read/dependency
state, and write before/after values), never in an authenticated `physical_ref`,
`successor`, `edge_before`/`edge_after`, revision, digest, owner, or managed-edge
binding. The `fork.source` binding maps the canonical internal source image and
both owners; it does not map the working alias. The materialization bindings map
the physical `c3c… → e568…` shot and `8be… → 7a35…` internal successors; they
also do not map the alias.

Therefore the native before-image is **not** authoritative C0 equivalence. A
concrete counterexample is the same retained payload bytes under a different
shot identity or revision pin: payload equality would select the wrong image or
owner, while C0 requires a unique authenticated physical lineage. The sibling
remaining on the canonical `document-diff-…` closure makes owner/edge identity
material, not cosmetic.

Runtime’s current check at `runtime_protocol/timeline_commit_auth.py:971-972`
must reject this before-image. The later occurrence-fork repair branch at
`:984-1007` is reached only after that check passes; it can restore an exact
source edge, but cannot manufacture one. The aggregate exception at
`:1137-1140` is limited to a `shot:` root comparison (dropping the internal
timeline pin after authenticated turnover); this failing write is the
non-root occurrence `shot_id` path, so that exception does not apply.

## Owner and bounded next seam

The Agent seam is `inverse.py`’s `_restore_write`/`apply_inverse` stage capture
and `inverse_stages` recording (`8c355a48…`: lines 585-735 and
`_step_undo.py:129-140`). It replays the retained native before value and
records stage ranges, but the retained alias has no source-bound mapping. The
next Agent repair must capture the canonical source-bound occurrence edge and
its exact revision/digest/owner/managed-edge provenance, or export a complete
authenticated alias mapping with source publication, step, command ordinal,
input head, physical roots, pins, owners and edges. Alias-name or equal-payload
normalization is insufficient.

The `80523b472…` candidate only adds the historical restored-shot baseline
carrier in `_commit_patch.py`; it leaves `inverse.py`, `_root_inverse.py` and
`_step_undo.py` byte-identical. That carrier cannot repair this occurrence-edge
capture. Sol 1416’s parent/config orientation issue is a distinct concern, and
the Agent 1404 historical-baseline compiler fix is also distinct; neither is a
common-cause explanation for this exact alias mismatch.

The lossless accepted packet is already public and contains the retained SQL,
document, head and history snapshots; the failed redo leaves all four snapshots
byte-equal. There is no artifact-transport gap.

## Verification and limits

Source-only assertions passed for packet size/hash, Runtime pin, accepted
forward/undo publication and step order, inverse stage ranges, native capture
and canonical stage input, accepted source/effect pins and owners, absence of
an authenticated alias mapping, and exact database/document/head/history
equality across the refusal. `git diff --check` passed on the assigned Runtime
worktree; it remained unchanged.

No product files, tests, schemas, clients, pins, contracts, config, env or Git
refs were changed. No public redo rerun, full suite, browser/native/matrix
suite, or typecheck was run. This handoff is report-only and **NEVERMERGE**.
