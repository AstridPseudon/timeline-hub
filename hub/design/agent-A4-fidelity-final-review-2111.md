## Result

**FAIL — A4 source/oracle closure only.**

- Exact four App packets, bytes, SHA-256 hashes, base closures, source pins, and caller binding preserved.
- Omitted `reads` remains distinct from `reads: []`.
- New v2 assertions match existing provider/schema structures.
- Inherited latent oracle defect: subminimum case expects the anchor unchanged and reads `changes[1]` as the later clip’s `at`; actual patch uses `changes[1]` for anchor hold and `changes[2]` for later `at`. This is pre-existing in `ff810d8a1`, not introduced by `03d6ec851`.
- App authority remains blocked separately: synthetic `dependency_manifest.media=[]`; provider correctly refuses all four with `dependency_changed`. No acceptance or P1 qualification claimed.
- Prior result retained: **4 failures / 16 passes**; known provider bodies were not rerun.

Checks passed:

- Offline packet reconstruction: 4/4 exact.
- Collection: 4 tests collected.
- Ruff and mypy: passed.
- Vendor lock `34eac004`: passed.
- Artifact manifest: current.
- Diff check and outside-file identity: passed; only the allowed test differs.
- Runtime `8ea0766f` tree `6047ac30`, matching integrated `abd47e68` source context.

No product edits were made. Commit message and `DONE` marker were created.