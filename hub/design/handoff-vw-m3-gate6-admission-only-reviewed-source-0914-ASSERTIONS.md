# Retained assertion map: admission-only correction

| Location | Final assertion | Source authority |
| --- | --- | --- |
| `tests/e2e/timeline/viewing-parity/cases.ts:91` | `output_policy.filename` is ``timeline-${fixture.timelineId}.mp4`` | Managed admission default from `renderRouter.ts` |
| `tests/e2e/timeline/viewing-parity/cases.ts:159` | `download.suggestedFilename()` is `authoredOutput.file` | Normal UI result/config filename; fixture value is `frame-parity.mp4` |

The two names intentionally remain distinct: the Runtime-managed admission name is timeline-ID-derived, while the normal UI download name remains the authored config name. All other 0911-retained assertion groups remain unchanged one-for-one.
