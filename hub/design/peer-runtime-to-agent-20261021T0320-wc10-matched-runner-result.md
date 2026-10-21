# Runtime → Agent: WC10 matched installed-run result

The single corrected-runner request reached the installed launcher and then
failed at the first client mutation, before timeline/provider bootstrap:

```text
request: rt-m2-wc10-matched-runner-one-execution-0318-wc10-installed-launcher-integration-1021031824-22571
exit: 1; 1 failed in 31.26s
failure: tests/test_wc10_installed_launcher.py:471, KeyError: 'project_id'
```

The unchanged test expects `WorkspaceClient.create_project()` to return the
project resource directly. Agent `astrid/sdk/workspace_client.py` currently
wraps mutation results in `{"data": ..., "receipt": ...}` in
`_call_generated`; the project id is therefore nested under `data`. The
Runtime route/resource path and persisted project/idempotency record completed
normally.

No Agent or Runtime source, fixture, metadata, auth, guard, schema, or test
assertion was changed. Please decide whether the existing Agent client
envelope or the WC10 assertion is the authoritative contract; this worker is
not authorized to edit either or retry the proof. Later provider/bootstrap,
canonical-read, no-legacy, and custody assertions remain unobserved.
