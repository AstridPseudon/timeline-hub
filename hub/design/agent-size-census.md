# Agent Timeline core size census

Read-only census captured 2026-10-21 UTC. The comparison is the frozen
upstream Main497 source `497714c73531f164082555ec81b61ca5bc8b6554` (`origin/main`,
tree `daaeb1149898dd327947e21c554b484094f960b2`) against the actual Agent
integration source `18a89a0d29766bd3cec31391042836ba7c951fa1` (`tl/integration`,
tree `6802b125647c6b836749e661b6c534e1f2e9d811`). The source SHAs are fixed in
the reproducer below so later documentation commits cannot silently move the
measurement.

This follows the PLAN3 owner 08:00/10:34 boundary: authored Agent product
code implementing Timeline Read, See, or Edit, including the compiler,
provider/adapters, and text views. Untouched generic main infrastructure,
generated clients/registries and contract data, tests/fixtures, vendored
Composition, build output, and lockfiles are excluded. Physical lines include
blank and comment lines; nonblank is reported for context. These are footprint
counts, not claims that every line is newly authored Timeline meaning or
removable.

## Result

| disjoint bucket | Main497 physical / nonblank | current physical / nonblank | delta physical / nonblank |
|---|---:|---:|---:|
| Read/Edit core, compiler, text views | 33,836 / 29,647 | 42,484 / 37,422 | +8,648 / +7,775 |
| See adapters and filmstrip Scene handoff | 3,362 / 3,079 | 4,013 / 3,670 | +651 / +591 |
| Provider/adapters | 1,088 / 995 | 1,295 / 1,191 | +207 / +196 |
| Selected SDK transport slices | 1,463 / 1,412 | 1,449 / 1,398 | −14 / −14 |
| **Scoped Agent product total** | **39,749 / 35,133** | **49,241 / 43,681** | **+9,492 / +8,548** |

The current total is larger than the historical preliminary `49,058 / 43,519`
figure because this source is later than `cc37291a` and retains the authored
filmstrip/Scene handoff while counting its pure rename into the Rendering-owned
`astrid/core/rendering/scene_answers.py` exactly once. It is not a deletion
target.

Historical preliminary numbers remain preserved: **39,109 physical lines on
Main497 and 46,573 physical lines on the earlier integration snapshot** (the
earlier report also recorded 34,541 and 41,282 nonblank lines). Those numbers
were valid for their then-selected surface and are not silently rewritten by
this current-source census.

The PLAN's approximately 20–26k figure is a rough guide, not a hard limit or
gate. No behavior is removed or simplified to reach it.

## Exact path boundary

The reproducer's `selected_paths()` output is the exact path list for each
source SHA; it prints every selected path before counting. The disjoint groups
are:

- Read/Edit core: Python under `astrid/sdk/timeline/`, Python matching
  `astrid/sdk/timeline_*.py`, Python under `astrid/packs/timeline/`, and Python
  under `astrid/core/timeline/`, excluding the six See files and the five
  explicit provider/adapters below. The `cli_visualize.py` file is excluded
  from the core family and counted in See.
- See: `astrid/sdk/timeline_filmstrip.py`,
  `astrid/sdk/_timeline_filmstrip_scene.py`,
  `astrid/packs/timeline/cli_visualize.py`,
  `astrid/core/timeline/scene_answers.py` when present in the baseline, or its
  pure-rename successor `astrid/core/rendering/scene_answers.py` in current,
  `astrid/core/timeline/onscreen.py`, and
  `astrid/core/timeline/shot_composition_projection.py`.
- Provider/adapters: `astrid/sdk/_remote_timeline.py`,
  `astrid/sdk/authoring_bundle.py`, `astrid/sdk/authoring_remote.py`,
  `astrid/sdk/authoring_revision_diff.py`, and
  `astrid/sdk/authoring_media.py`.
- Selected transport slices: `RemoteTimelines` and `RemoteShots` in
  `astrid/sdk/remote.py`, plus the named hand-authored timeline/shot/text
  methods in `astrid/sdk/workspace_client.py`. The rest of both mixed files
  is excluded; generated operation maps and generic client plumbing are not
  charged.

Non-Python schema files under `astrid/core/timeline/schema/` and other
JSON/YAML/generated data are excluded. The current source has 140 core paths,
6 See paths, 5 provider/adapter paths, and 2 mixed files (153 selected paths);
Main497 has 101, 4, 4, and 2 respectively (111 selected paths). The command
below is the authoritative complete list, including paths absent from Main497.

The Scene query file is renderer-owned operationally, but it is authored
Timeline See code. Main497 has no Scene query file in this boundary. Current
`astrid/core/rendering/scene_answers.py` is a byte-for-byte rename of Main497's
post-baseline Timeline Scene surface (the move landed in `5c0a1ab5d`); it is
counted in the See bucket once, not also in a generic Rendering bucket. Any
aggregate across the separate Rendering census must subtract this explicit
row rather than treating the ownership move as a deletion.

### Recorded path-set differences

The exact authored path list is the output of `selected_paths()` in the
reproducer. For auditability, the baseline/current differences from that list
are recorded here; all other paths are the intersection of the four explicit
families above:

Main497-only:

```text
astrid/core/timeline/inverses.py
```

Current-only:

```text
astrid/core/rendering/scene_answers.py
astrid/core/timeline/scene_roles.py
astrid/packs/timeline/cli_native.py
astrid/sdk/_remote_timeline.py
astrid/sdk/_timeline_filmstrip_scene.py
astrid/sdk/timeline/_clip_commands.py
astrid/sdk/timeline/_clip_scalar_commands.py
astrid/sdk/timeline/_collections.py
astrid/sdk/timeline/_command_state.py
astrid/sdk/timeline/_delete_commands.py
astrid/sdk/timeline/_media_inputs.py
astrid/sdk/timeline/_recording.py
astrid/sdk/timeline/_root_inverse.py
astrid/sdk/timeline/_scalar_commands.py
astrid/sdk/timeline/_selected_param_authority.py
astrid/sdk/timeline/_shot_commands.py
astrid/sdk/timeline/_split_commands.py
astrid/sdk/timeline/_timing_evaluators.py
astrid/sdk/timeline/_track_commands.py
astrid/sdk/timeline/_trim_commands.py
astrid/sdk/timeline/capture.py
astrid/sdk/timeline/commands.py
astrid/sdk/timeline/commit.py
astrid/sdk/timeline/compiler.py
astrid/sdk/timeline/document_diff.py
astrid/sdk/timeline/inverse.py
astrid/sdk/timeline/native_auto_placement.py
astrid/sdk/timeline/native_checkout.py
astrid/sdk/timeline/native_initialize.py
astrid/sdk/timeline/native_occurrence_create.py
astrid/sdk/timeline/native_occurrence_delete.py
astrid/sdk/timeline/native_occurrence_duplicate.py
astrid/sdk/timeline/native_occurrence_media_commands.py
astrid/sdk/timeline/native_parent_media_commands.py
astrid/sdk/timeline/native_placement_commands.py
astrid/sdk/timeline/native_shot_pool_commands.py
astrid/sdk/timeline/native_text_binding.py
astrid/sdk/timeline/native_word_anchor.py
astrid/sdk/timeline/outbox.py
astrid/sdk/timeline/producer.py
astrid/sdk/timeline/rebase.py
astrid/sdk/timeline/sync.py
astrid/sdk/timeline_media_replacement.py
```

The explicit See, provider/adapter, and mixed-file lists above plus these
differences make the 111-path Main497 and 153-path current manifests
reconstructible without checking out either revision.

## Changed main infrastructure (separate, not counted)

`astrid/core/execution/generic_host.py` remains excluded as generic host
infrastructure; it is not counted as a whole merely because Timeline source
preparation now passes through it. From Main497 to the current source its raw
diff is **30 insertions / 11 deletions**. The adjacent
`astrid/core/rendering/verified_source.py` source-authority helper is also
outside this product footprint (current file: 206 physical / 176 nonblank).
These are disclosed infrastructure context, not added to the scoped total.
The renderer-owned `astrid/packs/rendering/**` and generic SDK invocation/
process-host plumbing remain outside this Agent census as well.

## Existing ledger frontiers only

This census does not perform a new duplicate-writer audit or change ledger
status. The already-owned Agent frontiers still relevant to the counted code
are:

- in progress: `D13`, `D01a`, `D01b`, `AG01`, `AG02`, `AG03`, and `WC7`;
- held: `AG-M2-TB01`, `AG-M3-CAP-01..04`, `AG05`, `WC1`, `WC3`, `WC5`, `WC8`,
  and `WC10`.

The ledger's deleted rows remain deleted, including `D05`, `D06`, `D07`,
`WC2`, `WC4`, `WC6`, `WC9`, `AG-RECOVER`, and `AG-M2-DEAD-LEAF-01`. Open
frontiers are not treated as deletions and no new frontier is proposed here.

## Deterministic reproduction

Run from this Agent worktree. It reads only committed Git blobs; it does not
import the product, install packages, create caches, or run tests.

```sh
python3 - <<'PY'
import ast
import subprocess

SHAS = {
    "main497": "497714c73531f164082555ec81b61ca5bc8b6554",
    "current": "18a89a0d29766bd3cec31391042836ba7c951fa1",
}

SEE = {
    "astrid/sdk/timeline_filmstrip.py",
    "astrid/sdk/_timeline_filmstrip_scene.py",
    "astrid/packs/timeline/cli_visualize.py",
    "astrid/core/timeline/scene_answers.py",
    "astrid/core/rendering/scene_answers.py",
    "astrid/core/timeline/onscreen.py",
    "astrid/core/timeline/shot_composition_projection.py",
}
ADAPTERS = {
    "astrid/sdk/_remote_timeline.py",
    "astrid/sdk/authoring_bundle.py",
    "astrid/sdk/authoring_remote.py",
    "astrid/sdk/authoring_revision_diff.py",
    "astrid/sdk/authoring_media.py",
}
MIXED = {"astrid/sdk/remote.py", "astrid/sdk/workspace_client.py"}
WORKSPACE_METHODS = {
    "get_project_shot_revision", "get_project_timeline_revision",
    "get_project_parent_composition_revision", "publish_parent_composition",
    "replace_parent_composition_media", "create_timeline", "rename_timeline",
    "create_timeline_document", "update_timeline_document", "list_timelines",
    "commit_timeline", "list_timeline_commits", "get_project_verified_document",
    "get_project_verified_document_object", "get_timeline", "inspect_timeline",
    "create_timeline_view", "list_timeline_history", "replace_timeline_clip",
    "diff_timeline", "archive_timeline", "recover_timeline", "list_project_shots",
    "create_project_shot", "get_project_shot", "update_project_shot",
    "archive_project_shot", "recover_project_shot", "add_shot_item",
    "promote_project_shot_candidate", "remove_shot_item", "reorder_shot_items",
    "list_project_shot_text_bindings", "set_project_shot_text_binding",
    "get_project_shot_text_binding", "set_project_shot_text_binding_by_id",
    "rebind_project_shot_text_binding",
}

def run(*args):
    return subprocess.check_output(args)

def blob(sha, path):
    return run("git", "show", f"{sha}:{path}").decode("utf-8")

def selected_paths(sha):
    names = run("git", "ls-tree", "-r", "--name-only", sha).decode().splitlines()
    names = set(names)
    paths = (SEE | ADAPTERS | MIXED) & names
    paths |= {
        p for p in names
        if p.endswith(".py") and (
            p.startswith("astrid/sdk/timeline/")
            or p.startswith("astrid/packs/timeline/")
            or p.startswith("astrid/core/timeline/")
            or p.startswith("astrid/sdk/timeline_")
        )
    }
    return sorted(paths)

def selected_lines(sha, path):
    lines = blob(sha, path).splitlines()
    if path not in MIXED:
        return set(range(1, len(lines) + 1)), lines
    tree = ast.parse("\n".join(lines))
    if path.endswith("/remote.py"):
        nodes = [
            node for node in tree.body
            if isinstance(node, ast.ClassDef)
            and node.name in {"RemoteTimelines", "RemoteShots"}
        ]
    else:
        nodes = [
            node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name in WORKSPACE_METHODS
        ]
    selected = {
        line
        for node in nodes
        for line in range(node.lineno, node.end_lineno + 1)
    }
    return selected, lines

def bucket(path):
    if path in SEE:
        return "see"
    if path in ADAPTERS:
        return "adapters"
    if path in MIXED:
        return "mixed"
    return "core"

for label, sha in SHAS.items():
    paths = selected_paths(sha)
    totals = {name: [0, 0, 0] for name in ("core", "see", "adapters", "mixed")}
    for path in paths:
        selected, lines = selected_lines(sha, path)
        kind = bucket(path)
        totals[kind][0] += 1
        totals[kind][1] += len(selected)
        totals[kind][2] += sum(bool(lines[line - 1].strip()) for line in selected)
    print(f"{label} {sha} paths={len(paths)}")
    for path in paths:
        print(f"  {path}")
    for kind, (files, physical, nonblank) in totals.items():
        print(f"  {kind}: files={files} physical={physical} nonblank={nonblank}")
    total = [sum(values[index] for values in totals.values()) for index in range(1, 3)]
    print(f"  total: physical={total[0]} nonblank={total[1]}")

def test_fixture_counts(sha):
    totals = {"test_code": [0, 0, 0], "fixtures": [0, 0, 0]}
    names = run("git", "ls-tree", "-r", "--name-only", sha).decode().splitlines()
    for path in names:
        if not path.startswith("tests/"):
            continue
        raw = run("git", "show", f"{sha}:{path}")
        try:
            lines = raw.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        kind = "fixtures" if path.startswith("tests/fixtures/") or "/fixtures/" in f"/{path}/" else "test_code"
        totals[kind][0] += 1
        totals[kind][1] += len(lines)
        totals[kind][2] += sum(bool(line.strip()) for line in lines)
    print(f"{sha} test_code files={totals['test_code'][0]} physical={totals['test_code'][1]} nonblank={totals['test_code'][2]}")
    print(f"{sha} fixtures files={totals['fixtures'][0]} physical={totals['fixtures'][1]} nonblank={totals['fixtures'][2]}")

for sha in SHAS.values():
    test_fixture_counts(sha)
PY
```

Expected product totals are Main497 `39,749 / 35,133` and current
`49,241 / 43,681`, as shown above. The separately excluded repository test and
fixture corpus is:

| excluded corpus | Main497 physical / nonblank | current physical / nonblank | delta physical / nonblank |
|---|---:|---:|---:|
| test code (`tests/**` excluding any `fixtures/` component) | 244,289 / 209,272 | 290,741 / 249,809 | +46,452 / +40,537 |
| fixtures (`tests/fixtures/**` and nested `tests/**/fixtures/**`) | 37,230 / 36,684 | 92,910 / 92,343 | +55,680 / +55,659 |

The command counts committed UTF-8 text under `tests/` only; undecodable binary
files contribute zero. These excluded counts are context, not product size and
not a test result. No product tests, full suite, build, package, profile,
fixture cleanup, or deletion was run for this census.
