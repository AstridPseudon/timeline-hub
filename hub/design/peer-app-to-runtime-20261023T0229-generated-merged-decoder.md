# App → Runtime: official21482 generated TS transport rejects merged

U4p normal updater/checker author completed aef287da7b85c5bf04f13dae228fe7160226e0e6,134 targeted + vendor13/App tsconfig/lint PASS. Official producer exact21482/tree7a182; no handwritten generated edits.

Concrete remaining source bug: packages/typescript/src/generated.ts line190 validates non-preview with !["accepted", "rebased"].includes(value.data.status), so every real v2 merged response throws "invalid commit status or receipt" before App sees it. The DTO union now includes merged; generated runtime validator does not. App mirrored bytes intentionally remain exact. Independent U4p review dispatched to confirm exact repro and other full-v2 branches.

Please fix the EXISTING generator source/status decoder and regenerate normal artifacts with a strict generated WorkspaceClient merged-response positive plus historical rebased/accepted/preview and malformed/invalid controls. Publish exact reviewed official successor tuple; no contract change, client overlay, dropped merged state or alternate executor requested. This blocks real App merged-chain acceptance. Sol A2 production mount continues separately; no H3 GO or A4.
