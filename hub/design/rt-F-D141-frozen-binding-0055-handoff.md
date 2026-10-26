# D141 frozen Farm source-binding handoff

The D140 ordinary D139a installed-schema route is preserved and now binds the
approved D141 tuple in `ops-d140-farm/receive-farm.sh`. The `FARM_REQUIRED=1`
special branch and its requester/maker refusal guard are unchanged. C0 v2
request/reply fields remain the existing Runtime contract; the D141 schema
bytes equal the historical f103 schema.

## Ready-to-send sequence

Use the complete command sequence in `ops-d140-farm/commands.md`:

1. Bind the actual four clean normal checkout paths and their `queue/done`
   receipts for the D141 tuple, plus the normal D139a installed schema and
   all other declared venue inputs.
2. Run `D140_PHASE=pre-child ops-d140-farm/receive-farm.sh --check-only`.
   Stop on `NOT_READY`; this census is harmless and read-only.
3. Only after `READY`, issue the ordinary installed-schema
   `venv-agent-child-d140` request from `commands.md`, exactly once.
4. Bind the returned registered child and run the post-child check-only census.
5. Run the registered-child import check; a nonzero result is a hard stop.
6. Run the fresh D134 positive control (exactly one call, exit 17), then the
   poison control (zero calls, nonzero exit), and retain the request-scoped
   manifest/evidence.
7. Only after those gates pass, use the existing D124 unfiltered 22-root
   `CORE_ROUTE` command with its real XML, raw log, runner, start/stop, disk,
   and KEEP outputs; then run the post-launch census.

The current handoff is source-bound but venue `NOT_READY`: exact Runtime/App
normal checkout receipts, schema carrier, child, current import census,
controls, service/profile, and retained outputs remain Farm-owned inputs. No
venue input is represented as `READY` here. Do not use the stale shared homes,
historical child/census, oldvenv, alternate schema, synthetic receipts, or the
conditional pristine rerun body.
