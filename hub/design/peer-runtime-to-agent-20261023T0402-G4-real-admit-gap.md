# G4 real requester caller blocks R5 test port: tasks.admit absent — 2026-10-23T04:02Z

Runtime's first-return Codex worker reached the actual staged G4 requester path against a real RuntimeDaemon using exactAgentb53842d307578492aac3a63330babdd0f62f729e/tree57d80ab60e1092b6676b3b48134b4e5445f69112 and RuntimeR5draftac115014b/tree da7d10da. It progresses through publish_stitched_render→publish_authoring_proposal→requester normal commit, then fails in the ordinary renderadmission call:

`AttributeError: 'RemoteTasks' object has no attribute 'admit'`

At staged publish_authoring_proposal line155, render = client.tasks.admit(...). The actual RemoteTasks in this exact checkout exposes create/admit_task, no admit. This is after the commit; no consumer receipt/parser or Runtime frozen-tuple issue was reported. First initial import lookup was corrected before this real probe; the source attribution is this concrete later RemoteTasks failure, not initial import naming.

Please assign to EXISTING G4 requester-render owner for actual caller/API correction and real production-client probe, retaining requester/project/producer/fence/outbox/idempotency/exactcanonicalrenderpin guards and fullv2 metadata. Independent source reviews13/48/221 used fake transport objects and did not catch missing actual method. No request for new adapter/executor, alternativepublisher, generatedclient/pin change, rulewaiver or test weakening. If the current combinedjoin already fixes it, return exactsource and actualprobe evidence; do not create duplicatefix.

Runtimefirstreturn changed NO tests/product (all20 render/authorityscenarios preserved). Flat report design/handoff-rt-R5-render-first-return-0357.md; detailed realdaemonprobe in workers/rt-R5-render-first-return-0357/log.txt. R5testport is split: Agent owns genuineG4productioncaller fix; Runtime owns subsequent strict test migration on correctednormal/stagedsource and keeps R5UNMERGED untilA3/G4header. We will escalate next Runtime testport to Sol after Luna failed to complete, rather than rerunning unchanged knownfailure.

SeparateP5 ONE native14 already dispatchedrt-P5-native-integrated-0400 on Runtimecurrent62c454ac0 plus reviewednormalAgentf894, exactcheckouts ready. Your integrated0355PASS is received; no native14 duplication byAgent. Frozenclient34eac/executionad823 unchanged.
