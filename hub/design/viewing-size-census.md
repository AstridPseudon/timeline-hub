# Viewing Timeline Core — current M4 size census

Captured 2026-10-21 UTC from committed Git blobs. This is one source snapshot
for the approved Viewing-owned boundary, not a final hard-stop census,
qualification claim, deletion forecast, or size-limit gate. Physical lines use
the existing UTF-8 committed-blob line method; nonblank lines count lines whose
`strip()` is non-empty.

## Exact source tuple

The Main baselines are the same `origin/main` commits used by the preceding
census. The current tuple is the actual current `tl/integration` tip observed
at capture time; local and hub integration refs matched for all three included
repositories.

| repository | Main commit | Main tree | current commit | current tree |
| --- | --- | --- | --- | --- |
| Composition | `67b8aa3d0d6831d3e3504a340ff583c3da253707` | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` | `7bb54bbd64107e5090643ecca1e4d33164173e85` | `20467712e66dbadff4d562c0d5baae22b8c077a7` |
| Agent (Astrid/sdk) | `a411628f8fd6129f9c58c332019b56769d997384` | `e0ca791bb8adbf11e25e0e97843aaf246a04f965` | `931ebb3da20eba1851b5bcd3a75ffdca4c10fefd` | `b55c1697512896905cb0415ac7e6434b8eaf0dff` |
| App (Reigh) | `580508eed1bf6ed95caaf476c9d69a4672472a2f` | `ab3a5e296b01cc5458c88049c9eb5be402a05ccf` | `e1e153091b23aeafd09a15c500616384fba4330a` | `aa20a99731b91c2fa5e36b258c131147f3d7d651` |

Runtime is outside this approved Viewing boundary and is not counted.

The current Agent tip contains the published Main014 adoption and the current
App tip contains its current Main014/published014 adoption work. Those adoption
changes are not silently credited as Viewing size: the App counted roots have
no source-path change from the preceding tuple, and Agent’s counted delta is
the scoped extraction listed below.

## Canonical authored source

Values are files / bytes / physical lines / nonblank lines. Delta is current
minus the exact Main baseline.

| approved owned slice | Main | current tuple | delta |
| --- | ---: | ---: | ---: |
| Composition `typescript/src/**`, excluding generated registries/curves and timer declaration | 16 / 45,621 / 1,550 / 1,398 | 79 / 195,770 / 4,525 / 4,174 | +63 / +150,149 / +2,975 / +2,776 |
| Agent `timeline_visualize/**`, excluding schemas, stage/docs, fonts, inspector assets | 54 / 1,253,951 / 27,700 / 24,911 | 57 / 1,304,866 / 28,775 / 25,922 | +3 / +50,915 / +1,075 / +1,011 |
| Agent explicit render/evaluator adapters and `rendering/elements/**` text | 29 / 375,489 / 11,381 / 10,993 | 20 / 363,710 / 11,067 / 10,700 | −9 / −11,779 / −314 / −293 |
| Agent `onscreen.py`, `scene_answers.py` | 1 / 18,156 / 452 / 375 | 2 / 25,278 / 598 / 503 | +1 / +7,122 / +146 / +128 |
| Agent Remotion host, excluding adjacent paths and generated/declaration/test files | 11 / 24,264 / 631 / 573 | 10 / 28,084 / 690 / 630 | −1 / +3,820 / +59 / +57 |
| App non-test source in `PreviewPanel/**`, `compositions/**`, `render/**`, excluding fallback | 29 / 282,934 / 7,533 / 6,932 | 30 / 307,481 / 7,945 / 7,335 | +1 / +24,547 / +412 / +403 |
| **Viewing-owned canonical total** | **140 / 2,000,415 / 49,247 / 45,182** | **198 / 2,225,189 / 53,600 / 49,264** | **+58 / +224,774 / +4,353 / +4,082** |

Tests, fixtures, generated data, vendor copies, archives, fallback paths, and
untouched infrastructure are excluded by the existing method; no separate test
product-size count is introduced here.

## Material change since the previous tuple

The immediate prior current tuple was Composition `7bb54bbd…`, Agent
`4467c1c1…`, and App `69276584…`, measuring 197 / 2,225,238 bytes / 53,601
physical / 49,267 nonblank. Against that tuple, the current total is **+1 file,
−49 bytes, −1 physical line, −3 nonblank lines**.

- Agent D08 source extraction added the committed leaf
  `astrid/packs/rendering/actions/timeline_visualize/_audio_cache.py` and moved
  the cache helpers out of `filmstrip_execution.py`. The durable-replace and
  current-runtime source adjustments are included in the same scoped row.
- Agent D10’s nine duplicate Composition source adapters were already physically
  deleted in the preceding tuple; no new D10 deletion is credited here.
- The Composition source and all App counted paths are unchanged from the
  preceding tuple. Main014 adoption is present in the captured Agent/App heads,
  but adoption/pin work outside these owned paths does not alter the census.

## Still-open duplication boundaries

- D08’s broad App `VisualClip`/`TimelineRenderer` host replacement remains
  uncredited until a complete public-host parity proof exists.
- D09’s private Agent `onscreen.py` and motion/ROI/evaluator callers remain
  open pending the named public-caller and parity gates.
- AUDIO duplication remains open: App `lib/audioFade.ts`/`AudioTrack` policy
  and the Agent export/audio path still require the shared public policy and
  cross-consumer parity proof. The `_audio_cache.py` extraction is only a leaf
  extraction, not AUDIO closure.

## Boundary and reproduction

The approved read-only scanner was reused unchanged:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-size-census-gate-review-script.mjs`

It reads `git ls-tree` and `git show` only. The boundary includes authored
Composition `typescript/src/**`, Agent visualize plus the explicit
render/evaluator/elements/Remotion paths, and App non-test source under the
three named preview/composition/render roots. Generated data, tests/fixtures,
vendor copies, archives, fallback paths, stale `dist`, untouched
infrastructure, and Runtime remain excluded.

The exact current reproduction command is recorded in the worker `COMMAND`
artifact for this refresh. No tests, build, install, browser, renderer, graph
copy, or qualification run was performed for this documentation-only census.

## Historical comparison

The older actual-current census remains historical evidence: Composition
`4788e107…`, Agent `57d66356…`, and App `813a8510…`, measuring 197 / 2,227,916
bytes / 53,657 physical / 49,316 nonblank. It is not part of the current
tuple and receives no current credit.
