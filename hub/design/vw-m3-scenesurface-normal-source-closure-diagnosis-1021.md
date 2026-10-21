# SceneSurface source-closure diagnosis

The exact cause of physical15923 is an incomplete external Remotion staging
closure. The frozen d0a importer at `remotion/src/LiveSceneClip.tsx:3-4`
resolves `../../astrid/packs/rendering/editor/live-scenes/SceneSurface` from
`/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/src` to
`/home/user/work/runtimes/astrid/packs/rendering/editor/live-scenes/`, where
`SceneSurface.tsx`, `runtime.ts`, and `diagnostics.ts` are all absent. The same
three files exist in Agent d0a (commit
`d0a5072bbe7b7ce9489f43aa0a81027ec400343b`, tree
`6adb4a1190dfb2874e101565f37eccd392b1ae2f`) and origin/main. Therefore this is
"immutable runtime copied without sibling source / product staging closure
incomplete". It is not an absent product source or a resolver rename.

Source hashes: d0a/main `SceneSurface` `830b7966ed736431ef688242c0917273d563e9716f3f58a633b5402879e7c2f9`,
`runtime` `3bdfa73290d935699d3937798df950376cfd25209a442fc9b294fc12c98a14f2`,
`diagnostics` `012c8d739dfddf33742e0479a19a59d0a1f1b7e618e1e3948a049b962080a022`.
Current integration `e211a3288` has renamed source under
`ui/threejs-live-editor`; it is not the source pinned by the failed tuple.

Live callers are the frozen/main Remotion importer at
`remotion/src/LiveSceneClip.tsx:3-4` and the frozen/main editor lazy import at
`editor/live-scenes/extension.tsx:53-54`; current integration has the same two
call sites under `ui/threejs-live-editor`. Origin/main's `pack.yaml:1337-1353`
declares the UI support resources, but that is not a declaration of the old
Remotion importer's editor sibling closure.

Minimal correction for a new d0a tuple: materialize those exact three existing
files at the importer’s sibling path beside the external Remotion project.
Do not mutate the consumed packet, change the frozen importer, add aliases, or
substitute a second component. Add a pre-admission static closure witness at
the staging boundary; the negative case must fail before webpack/browser when
the sibling source is omitted. Full details, caller list, evidence command,
and test status are in the worker report.
