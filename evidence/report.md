# T2 role-source parity review

Verdict: **PASS**

## Scope

Compared `tl/B-T2-role-source-fix-2` with `tl/shotlayer-integration`.
The diff is limited to:

- `astrid/core/timeline/shot_composition_projection.py`: a clarifying docstring only; no production behavior changed.
- `tests/fixtures/timeline/shot-layering-v1.json`: one canonical source-role visual track and clip, plus the corresponding expected projection.
- `tests/timeline/test_shot_layering_projection.py`: the canonical digest update and one additive source-role regression test.

No assertions were removed, weakened, skipped, or changed to expect missing behavior. The only changed expectations are the required additional source-role group and clip mapping. The fixture has no skip/xfail changes.

## Parity checks

- Canonical fixture SHA-256 is `c779ef38d4f47368967a5afab2704548c70c0f27c646f8ebab6be74ad3cf63a7`; it matches the Runtime fixture at `/home/user/work/wt-int/runtime-tl-shotlayer-integration/conformance/fixtures/shot-layering-v1.json`.
- Source-role visual tracks follow the existing `kind != "audio"` path: `occ-vision~source-plate`, with `track.app.group = {id: "occ-vision", sourceTrack: "source-plate"}`.
- The group is contiguous and retains authored child order, inserted immediately above the occurrence row. The source clip is mapped to the namespaced track.
- Audio remains on its authored id and uses the existing merge-by-id/neighbor placement. No audio fields or settled ordering rules were changed; the source-role addition appears in its canonical authored position before the occurrence row.

## Test evidence

Central targeted lane:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test B-review-T2-role-source-fix-2 targeted --files "tests/timeline/test_shot_layering_projection.py")
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test B-review-T2-role-source-fix-2-targeted-1027000105-29799
```

Result: **pass**, exit 0, `43 passed in 0.35s`.

No full suite or render was run, as required. No blockers or unresolved review findings.
