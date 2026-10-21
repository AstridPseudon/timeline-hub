# Agent private15 trusted Python host context

Implementation in progress; coordination seam for the parallel shared worker:

- Use `astrid.core.execution.executor._action_context._require_action_context()`.
- It returns an ephemeral private object with `.producer` (a read-only exact
  five-field mapping), `.admitted_target` (a read-only exact four-field mapping),
  and `.out` (the live ExecutorRunRequest output directory).
- It refuses outside a verified managed Python invocation; no client attribute,
  caller mapping, environment variable, or inner speech identity is consulted.
- Shared `draft_voiceover._trusted_outer_producer` must call this accessor,
  never `getattr(client, "trusted_execution_context", ...)`. The latter currently
  visible in the parallel draft is caller mutable and cannot establish custody.
- The action checks the returned proposal's producer and admitted target against
  this context, then writes only the standard proposal and result manifest.

The existing private host-worker admission envelope is the carrier; no public
request/DTO/schema/action input is added. Context objects themselves are created
only after admission/source verification and are never serialized or attached to
clients. Exact minimal transport and lifetime justification follows with tests.
