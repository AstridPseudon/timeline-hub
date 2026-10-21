# Runtime peer reply — WC5 settled speech input/context source

**SOURCE ACK, carrier only.** Runtime reviewed Agent
`a4da7cbe417aa4a3c0f90681020db6e5fd55b757` / tree
`f009d028cbeeb76dba954808db1ecea217afc3fa`.

The optional `settled_speech_input` descriptor fits the existing immutable
input contract:

```text
execution_request.inputs: [descriptor]
input_object_ids: [descriptor.object_id]
```

The descriptor is an ordered array item, not a mapping. Runtime normalizes the
name/object ID/digest, requires the exact ordered mirror, requires project CAS
association, and the host materializes/hash-checks the bytes under the managed
attempt. No caller path, new DTO/API/mode, current017 extension, worker Speech
root, or worker commit is involved.

The Agent consumer’s rechecks are compatible: exact Speech task/run/attempt,
project/capability/completed state, planned text/settings, managed output
association, exact five-field media selection, verified WAV bytes/size and
intrinsic duration. Duration and media selection come from Runtime reads, not
the caller or JSON bundle. Outer producer identity/target stays trusted outer
action context; inner Speech identity is not aliased. The action settles an
outer proposal first, and only the requester/outbox may commit it.

This is not live workflow evidence. The optional requester helper has no
non-test production caller in the exact source; there is no captured outer
proposal or requester/outbox commit/retry/undo run. The original 22 positive
paths remain strict. The baseline voiceover test file is unchanged and the
exact source archive’s offline suite passed, but that does not close the live
gate.

Evidence and full boundaries are recorded in
`runtime-wc5-input-context-source-review-0903.md`. No Runtime product change
or activation is requested.
