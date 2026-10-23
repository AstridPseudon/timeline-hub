# A3 shared popup return review — FAIL

Reviewed `95367498b311a5b45981aa143aa9576746039afe` against protected
`890b9561666c3619f69335dd747b15e042b3a9a3`.

The four-file allowlist, current-890 protection, Runtime adapter capability,
current Agent fork/media registrations, A2 outbox carrier, physical-closure
guards, command ordering, and unchanged v2 request/reply contract all inspect
correctly. The review nevertheless fails the production seam:

`projectMediaSelection` extracts `provider.getProjectMediaSelection` into
`reader` and invokes it without its receiver (`shotTimelineDataProvider.ts`
lines 692–697). The real `RuntimeDataProvider` method uses `this.projectId`
and `this.client` and is not constructor-bound (`dataProvider.ts` lines
849–858, constructor 394–400). The actual shared ADD/SWAP production path
therefore throws before `LocalSaveSession.append`, while the focused test's
arrow mock passes. Preserve the existing authenticated API and command grammar;
Sol must correct receiver preservation, then obtain a fresh current commit and
repeat review.

Direct `node --import tsx` source reproduction returned
`Cannot read properties of undefined (reading 'projectId')` from the extracted
real class method.

Evidence: A3/provider targeted tests 99/99; broader neighbors 150/152 with
the exact `890b95616` baseline reproducing the existing opaque `__proto__`
failure (25/26), plus the known `/opt/node22/bin/node EPERM` environment
failure; typecheck, scoped lint, diff check, normal producer checks, and private
Composition `819acf…`/public exports pass. No product edits were made here.
No browser, HTTP/body, service, build, full, central request, or actual Runtime
admission proof was run.
