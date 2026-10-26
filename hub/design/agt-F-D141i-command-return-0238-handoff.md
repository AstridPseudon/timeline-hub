# F/D141i corrected handoff

The four 0232 command blockers are corrected in one bounded wrapper/manifests
return. The positive and poison manifests are fresh serialized files; the
positive profile lock digest is read from the existing protected profile and
the poison differs only in `agent_sha`.

Fresh normal launcher controls passed against the final serialized files:
positive preflight 0, retained stub exit 17, one call; poison exit 1 before
the stub, zero calls. The materialized positive manifest and launcher
runmanifest retain the exact durable JUnit path. The wrapper uses
`shutil.disk_usage(...).free` and propagates terminal after-body disk failures
to nonzero finish status.

Do not submit or run the one Agent-core-full body from this packet. Independent
final command review is the next gate. If it passes, the normal controller may
use the one native row in `service-row.txt`, preserve the queued/unstarted
population, and make its own admission decision. This packet claims no body,
REG, behavior, or ship credit.
