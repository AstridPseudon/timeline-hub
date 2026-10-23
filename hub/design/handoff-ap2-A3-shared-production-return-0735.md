# A3 shared production return handoff

Status: scoped PASS; ready for independent review.

Base is `890b9561666c3619f69335dd747b15e042b3a9a3`. Final is the
uncommitted four-file allowlisted worktree; patch SHA-256 is
`fe438244ac6c3e2f07861e56b94cae6ddc7ecd270e64f42b4e1fdefaeca9be85`.

The exact candidate owner files from `027971446` were imported unchanged.
The only additional files are the actual Runtime adapter and its regression
test. `RuntimeDataProvider.getProjectMediaSelection(projectId, query)`
delegates to the existing authenticated client read and rejects a foreign
project. The mounted caller path is:

`ShotTimelinePreview -> createShotTimelineDataProvider -> saveTimeline ->
sharedPopupMediaCommands -> RuntimeDataProvider media-selection read ->
LocalSaveSession/outbox`.

For a shared selected occurrence, the request emits the existing registered
semantic grammar in order: `occurrence.fork`, then exactly one
`occurrence.add-media` or `occurrence.swap-media`. It does not patch
managed occurrence edges, broadcast, duplicate, guess a successor, or use a
detached executor. Accepted/merged canonical reply handling and refusal/reload
behavior remain on the existing A2 session.

Evidence: A3 plus Runtime provider targeted tests pass 99/99; TypeScript,
scoped ESLint, diff check, Runtime lock, Agent lock, and exact private
`819acf` graph checks pass. The broader neighbor set is 150/152 because the
existing `ShotTimelinePreview.test.ts:716` `__proto__` failure reproduces
on exact base (25/26), and the element build test hits
`spawnSync /opt/node22/bin/node EPERM`. No weakening was made. No
browser/HTTP/body/live service/build/full/request/shared-install run was
performed.

Normal Runtime producer freeze remains `34eac004` / tree
`9853574865f25e08284e82ffb26c0bdecaa16a30`. The old Agent `f894` source
does not register `occurrence.fork`; the existing execution source
`4edc` / tree `f17b84c48bae3461dd11cedb8719bd17495a8210` does, at
`astrid/sdk/timeline/commands.py:79`, with media commands at 81–82.
No Agent/runtime producer or pin was edited.
