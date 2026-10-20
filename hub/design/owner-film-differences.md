# Owner-film differences to review at the hard stop
Single viewing list shared by Agent and Viewing, per orchestrator04:24. These are intended semantic changes, not qualified owner-film results. No production films will be supplied here (orchestrator04:33). Ship the readonly credential-free scanner in the delivery ZIP; the owner runs it locally before the hard-stop viewing and keeps film data locally. Film-specific references will be generated there. Viewing owns scan evidence/physical comparisons; Agent adds compiler/source facts without overwriting Viewing rows.

| Change | MAIN behavior | Unified behavior / decision | Films and exact references | Evidence and remaining proof |
| --- | --- | --- | --- | --- |
| Explicit fade curve= | Parsed curve name discarded; linear fades | Honour public fadeInCurve/fadeOutCurve, author intent; PLAN04:24 | OWNER RUN at hard stop; no local clean claim | Agent shared compile contract/vector publication pending locally; Viewing scanner extension queued. Actual audible/visible affected-film comparison at hard stop. |
| Element/custom-effect clip look | MAIN locked Composition0.0.6 mounts element clips bare | Owner v0.0.7 clip-look wrapper: opacity/crop/fades/entrance/exit; independent overlapping fades DIP16–30, PLAN03:59 supersedes preserveopaque | OWNER RUN at hard stop; bounded local search found none, not no affected films | ActualMAIN6 ownRoot/generator vsunified10 source/body/archive proof prepared. Central1020043344-8195 PASS1/79.79s after minimal fixture root-route repair:90actualPNGs, exactoutside16–29, exactpublicopacitysourceoverinside; allsource/peer/browserguardsunchanged. Actualincoming-COVERED positive retained. Earlier404run unqualified. |
| Continuous audio fade sampling | Frame-held gain, historical comparison remains5/6RED | Public applyAudioEnvelope continuous source-time gain in BOTH preview/export; constantbasegain/readiness/retry/mute/amplify kept, PLAN03:20 | OWNER RUN at hard stop; no local clean claim | Golden/source evidence up to~0.7dB midfade change; inactivePCM15+7PASS, notnormalroute/physicalparity. Canonicalcompiler/trustedjoin/decoderorigin and measuredglobalcaptureorigin pending. |

Read-only scanner **1.0.8** is ready for delivery selection after Viewing's independent gate and Agent's assigned canonical-policy review: `artifacts/owner-film-viewing-tools-v1.0.8.tgz`, 18,116 bytes, SHA256 `e87e88705679e320bc83b6c72dff31fe23bbd0122981f314b5890411d6449cfb`. The exact extracted suite passed124 tests; Agent reran84 malformed-value regressions and102 codec tests. Independent130-case checks retained clears/extensions and refused malformed fields. It reuses ONE Agent projector and strict declared-field codecs; output stays bounded and unknown/incomplete is explicit. Earlier1.0.6 and1.0.7 remain rejected, never relabelled. See `design/agent-review-scanner-1.0.8.md` and `design/viewing-scanner108-delivery-selection.json`. The immutable archive's build-time held wording is superseded by these external approval records; its bytes are unchanged. No owner-film, renderer, macOS or full-suite result is claimed. At delivery selection ship this exact archive and approval record; the owner runs it with the qualified Agent environment:

    PYTHONPATH="$AGENT_ROOT" "$OWNER_AGENT_PYTHON" -B owner_film_cliplook_scan.py --agent-root "$AGENT_ROOT" --input "$OWNER_FILM_INPUT" --json-out "$OWNER_SCAN_OUTPUT"

Keep owner data local. The scanner reports unknown/incomplete and never claims a film is clean. It inventories incoming transition declarations without pretending to compute converted boundaries, and explicitly lists unmeasured areas.

## Shared implicit theme — final decision, 2026-10-20 06:18 UTC

The public Composition DEFAULT_THEME is the one authority. Its complete value becomes the existing Agent export style: banodoco-default, navy #050814, Arial, cyan, and its existing sizes, weights, line heights and fadeMs. Agent's constant must equal that object. Existing final exports therefore keep their style; implicit App preview changes from black/Georgia/white to match. The Player ground paints the same resolved background.

Explicit film themes are preserved; no film rewrite or hidden fixture override. Review preview sidebands and theme-aware text/effects in the duplicate film, especially films relying on implicit styling or partial overrides. Custom runtime-pinned theme transport and nested-merge behavior remain unqualified until actual positives. The read-only scanner does not prove theme appearance or classify every implicit-style dependency.


## App automatic placement — temporarily missing on integration (2026-10-20 06:49 UTC)

D03 removed the Supabase canonical writers as directed. Generated media is retained, but complete_task now records automatic_timeline_placement_retired and does not automatically place the asset on the timeline. This user-visible behavior remains temporarily missing on integration until D01-app-placement restores automatic placement through native EditCommands and the requesting App durable session. It is the top M2 App writer priority. No edge writer will be restored. Manual placement and every old image/video/auto/pool/shift variant require individual native coverage before their existing writers can be retired. The native-gap worker is tracing the precise trigger and unsupported contracts; no automatic-placement qualification is claimed.


## Known pre-existing App clear bug — 2026-10-20 07:10 UTC

Clearing a transition does not stick on main/integration until the native clear lands. The current legacy None callback removes the local field, but legacy publication restores the prior raw transition. This is a known pre-existing bug, not an intended semantic change. Native single and atomic bulk clear are staged; D01-app-transition-none-serialization remains OPEN until actual current-tuple accepted reload, inverse, retry and zero-legacy proof. The transition revision/opaque-field safety repair does not fix publication removal. Owner decision07:00.


## Old anonymous automatic-placement requests — owner decision 07:05 UTC

Old task intents submitted before the upgrade without explicit canonical owner/basis/approval bindings are not retroactively auto-placed by inference. The asset stays in the gallery and must show a visible recoverable “Not placed: place manually” state. New automatic placement requires durable explicit requester bindings before task submission and the native capture/commit path; it is not yet qualified on integration. Manual placement remains subject to its existing honest refusal and later native migration.

## Agent compiler/source evidence — 2026-10-20 09:23 UTC

Agent integration has published the compile contracts and fixtures (38e427e3 audio, 6b108a8e visual; contracts now under docs/design after 21f062ed). The shared handoff fixtures remain available as handoff-agent-audio_compile_contract.fixture.json and handoff-agent-visual_compile_contract.fixture.json.

- Audio source reference is origin/main e51595c6, core/timeline/shot_composition_projection.py and main's Composition 0.0.6 AudioTrack.tsx. Gain is multiplicative; boost and mute are kept. Occurrence source_offset is metadata-only on that reference path; its canonical value/unit is milliseconds (the source vector is 350, never silently converted to .35). Occurrence speed is not inherited by that main audio path. Contract test: tests/editing_conformance/test_compile_contracts.py.
- Fade curve= honours the selected public curve instead of main's discarded/linear form. Continuous PCM sampling remains a deliberate improvement, subject to normal real WAV route qualification; source-phase carry must preserve the unsliced clip's original fade. Agent's 470e4001 slice-origin stamp alone does not prove this route.
- The native popup golden uses App 309cb7a4 add.output verbatim: occurrence A 8–18 s, B 10–20 s, with source windows, rational clock and opaque data intact. The explicitly separate overhang vector exercises the one compiler's clamp rule. The obsolete clamp-off tests were removed in ef6eec55 under the 06:18 instruction; this is no per-caller render policy.
- The v0.0.7 element clip-look change and the implicit preview navy/Arial/cyan theme remain the approved viewing-list changes above. No owner film data is present here, so affected-film identities must come from the shipped scanner run locally. These source facts do not qualify owner-film pixels, normal-route PCM or macOS.
