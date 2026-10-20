# D10 App vendor provenance seam

## Owner proposal

Use the existing `config/astrid-vendor-files.json` selection manifest as the
single exclusion seam. Add nine exact Astrid-relative `component.tsx` paths to
`exclude`; make `refresh-vendor.mjs` filter only directory enumeration by that
set, reject unsafe paths and explicit-file collisions, and write the sorted set
to generated `vendor/astrid-browser/provenance.json`.

This is a normal refresh selection, not a second catalog or a source rewrite.
The public catalog remains the data-only identity/schema/diagnostic surface.
The nine descriptors and their `element.yaml` files remain selected; local and
custom packs, assets, tool bindings, and explicit `--files` / `--destination`
overrides remain available. No hash is hand-edited: the owner refresh produces
the resulting file map and hashes from the selected source commit.

## Exact proposal

Apply:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d10-vendor-provenance-retirement-seam/UNAPPLIED.patch`

Then apply the already-qualified `27ee90ac1` registry bridge and flat Home
migration packet, run one normal vendor refresh from the owner-selected Astrid
commit, and run the verifier plus focused host tests. This worker intentionally
left the App product worktree untouched.

## Nine excluded implementation paths

```text
astrid/packs/rendering/rendering/elements/animations/fade/component.tsx
astrid/packs/rendering/rendering/elements/animations/fade-up/component.tsx
astrid/packs/rendering/rendering/elements/animations/scale-in/component.tsx
astrid/packs/rendering/rendering/elements/animations/slide-left/component.tsx
astrid/packs/rendering/rendering/elements/animations/slide-up/component.tsx
astrid/packs/rendering/rendering/elements/animations/type-on/component.tsx
astrid/packs/rendering/rendering/elements/effects/text-card/component.tsx
astrid/packs/rendering/rendering/elements/transitions/cross-fade/component.tsx
astrid/packs/rendering/rendering/elements/transitions/fade/component.tsx
```

The frozen Agent candidate contains all nine source files and all nine catalog
descriptors. The source files are therefore not blindly deleted from Agent;
the App vendor selection omits only their package-owned runtime payloads. If
the settled packet requires the source commit to omit them, the owner still
must provide that exact source commit; this proposal remains valid for either
source state and does not invent a source commit.

## Qualification status

Current App baseline: host/alias focused tests PASS (18 tests), vendor source
verifier PASS (65 pinned source files, 155 vendor files, 20 imports), and public
boundary test PASS. Patch applicability, script syntax, manifest JSON, exact
nine-path selection, Agent source existence, and catalog descriptor checks PASS.

The private normal-refresh execution was not qualified in this sandbox because
Node `spawnSync('git', ...)` is denied with EPERM when the refresh script reads
the allowed Agent checkout. No generated provenance claim is made here. The
owner's refresh and post-refresh verifier are required evidence.
