# Bounded whole-path first-seam assessment

```text
exact D136a source delta + held D100
        |
        v
registered Runtime commit caller
  publish_authoring_candidate -> writer.commit_timeline
  -> _RuntimeAuthoringWriter -> RuntimeService.commit_timeline
        |
        v
immutable Runtime command-output projection
  command_output -> missing authenticated physical observation
  guard refusal at timeline_commit_auth.py:2209
        |
        v
original9: 9 setup errors, no test body reached
```

The D100 comparator's meaningful registered node is the existing first
physical-item `doc.patch` path in
`tests/sdk/test_d100_item_birth_boundary.py:205-246`: its recorded evidence
shows accepted first-item custody and a later wrong-previous no-write refusal
through the same Runtime commit route. The original9 caller is the authoring
publication path described above, and its actual XML fails earlier than any
projection assertion at the intermediate-observation guard seam. This is a
bounded ordering comparison only; it does not establish a shared cause or
authorize a guard change.

The earliest actual mismatch that is authenticated by safe evidence is the
Runtime `command_output` lookup refusing because its intermediate result lacks
an authenticated physical observation. The exact missing record/ref/ordinal
is withheld because the only available sources are private request/payload
and raw-stack material. Causal owner remains UNKNOWN.

## Authority and privacy boundary

The request route is the existing full v2 shape: API/project/timeline/base
identity, commands, label/steps, merge mode, reads, idempotency, dry-run,
source/rationale/group fields; replies remain accepted/merged/conflict/invalid
or preview forms. No credentials, Git writes, hub writes, merge request,
upstream action, acquisition, retry, or auth widening was performed. Runtime
remains the sole writer and the D130 SWAP/WAL/recovery/tour hold is unchanged.
