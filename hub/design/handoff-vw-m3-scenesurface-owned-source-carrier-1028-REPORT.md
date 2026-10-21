# SceneSurface owned source carrier — process-custody handoff

Status: **READY for independent pre-admission review; physical rerun HELD**.

The failed physical task was a source staging defect. Frozen d0a's
`remotion/src/LiveSceneClip.tsx` imports
`../../astrid/packs/rendering/editor/live-scenes/SceneSurface`; the failed
immutable Remotion project carried `src/` and dependencies but no sibling
`astrid/packs/rendering/editor/live-scenes/` source. The exact d0a source is
present in the owned capsule, and the current renamed UI source is explicitly
not substituted.

Owned packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scenesurface-owned-source-carrier-1028/packet.pnylvl`

Authority: Agent d0a commit
`d0a5072bbe7b7ce9489f43aa0a81027ec400343b`, tree
`6adb4a1190dfb2874e101565f37eccd392b1ae2f`. Positive capsule: 26 regular
files, 176,719 bytes, `st_nlink=1`, no symlinks. Dependency graph copy: 0
bytes. Shared runtime target `/home/user/work/runtimes/astrid`: untouched.

The pure witness is `validate-source-closure.mjs`. It uses the existing Node
esbuild resolution seam with bare package imports externalized. Negative omits
the three sibling closure files and reports four missing local edges before
bundle. Positive resolves all `index -> Root -> Three -> LiveSceneClip` local
edges plus `SceneSurface -> runtime/diagnostics`, verifies exact d0a hashes,
and emits a 75,274-byte bundle.

Exact execution:

```sh
BASE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scenesurface-owned-source-carrier-1028
PACKET=$(find "$BASE" -maxdepth 1 -type d -name 'packet.*' | sort | tail -1)
node "$BASE/validate-source-closure.mjs" "$PACKET/negative" negative
node "$BASE/validate-source-closure.mjs" "$PACKET/positive" positive
```

Both commands passed. No launch or render was attempted. The future selected
knob is existing `ASTRID_REMOTION_PROJECT_DIR="$PACKET/positive/remotion"`
only after normal project/dependency validation accepts the complete carrier;
the source-only packet does not claim that validation or render readiness.

Guard trace, unchanged and read-only:

- `remotion_host_session.py:116-125`: absolute project, real project path,
  frame worker, executable Node, and in-project CLI.
- `remotion_runtime.py:294-348`: project/package/lock/schema/source/package
  roots and file identity binding.
- `remotion_runtime.py:996-1050`: validation artifact owner/mode/digest,
  launch context, registry inputs, runtime inputs, and custody checks.
- `source_identity.py:37-64`: real source closure and no symlink descendants.

Frozen graph reference remains `sha256:4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`
(21,455 entries), read-only. Node for the pure witness was `v22.22.0`; no
claim is made about the frozen launch Node. Live caller count is **none**;
the report lists static source edges only.

Recommended next step: independent process-custody review should attach this
owned source capsule to the complete d0a Remotion project with normal
read-only dependencies, run the existing pre-admission validation, and hold
if that would require a real graph copy. Do not make `/home/user/work/runtimes/astrid`,
rewrite the importer, add a resolver alias, or infer final render success from
the bundle witness.
