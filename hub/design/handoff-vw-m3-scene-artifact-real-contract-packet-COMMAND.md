# Regeneration command

The bounded examples and manifest were generated from the assigned worktree by:

```sh
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-artifact-real-contract-packet-generate.sh
```

The script uses the pinned Node 20.19.4 path and the read-only peer graph, creates
its own temporary pytest stage, and removes that stage on exit. It writes only the
four result variants plus their managed/nested manifests, ZIPs, and one manifest
under the `...-examples/` directory. It does not export a timeline snapshot,
credentials, or source-binding file.

The existing managed artifact entrypoint is:

```text
filmstrip_bundle -> filmstrip-view/scene-answers.json
```

The SDK checks `snapshot_label.status` before passing `answers` to the existing
`scene_problems` formatter; `unavailable` is advisory and has empty answers/map.
