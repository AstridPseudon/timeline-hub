# Agent Timeline core size census

Read-only census captured 2026-10-21 UTC. The comparison is the frozen
upstream Main497 source `497714c73531f164082555ec81b61ca5bc8b6554` (`origin/main`)
against the actual Agent integration source
`cc37291af12ac6504eb48dd71ea39b9dfdb56d71` (`tl/integration` at census time).
The latter source SHA is fixed in the reproducer below so later documentation
commits cannot silently move the measurement.

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
| Read/Edit core, compiler, text views | 33,836 / 29,647 | 42,304 / 37,263 | +8,468 / +7,616 |
| See adapters and filmstrip Scene handoff | 3,362 / 3,079 | 4,013 / 3,670 | +651 / +591 |
| Provider/adapters | 1,088 / 995 | 1,292 / 1,188 | +204 / +193 |
| Selected SDK transport slices | 1,463 / 1,412 | 1,449 / 1,398 | −14 / −14 |
| **Scoped Agent total** | **39,749 / 35,133** | **49,058 / 43,519** | **+9,309 / +8,386** |

The current total is larger than the historical preliminary figure because it
is measured at the later integration SHA and includes the current authored
filmstrip Scene handoff and authoring-media provider. It is not a deletion
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
  `astrid/core/timeline/scene_answers.py`,
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
6 See paths, 5 provider/adapter paths, and 2 mixed files; Main497 has 101,
4, 4, and 2 respectively. The command below is the authoritative complete
list, including paths absent from Main497.

## Changed main infrastructure (separate, not counted)

`astrid/core/execution/generic_host.py` remains excluded as generic host
infrastructure; it is not counted as a whole merely because Timeline source
preparation now passes through it. From Main497 to the current source its raw
diff is **30 insertions / 18 deletions**. The adjacent
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
    "current": "cc37291af12ac6504eb48dd71ea39b9dfdb56d71",
}

SEE = {
    "astrid/sdk/timeline_filmstrip.py",
    "astrid/sdk/_timeline_filmstrip_scene.py",
    "astrid/packs/timeline/cli_visualize.py",
    "astrid/core/timeline/scene_answers.py",
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
PY
```

Expected totals are Main497 `39,749 / 35,133` and current
`49,058 / 43,519`, as shown above. No product tests, full suite, build,
package, profile, fixture cleanup, or deletion was run for this census.
