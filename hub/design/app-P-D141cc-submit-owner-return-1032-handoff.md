# D141cc handoff

Status: **READY_FOR_INDEPENDENT_REVIEW**.

Use `evidence/candidate/check.sh` as the same-author/reviewer control. The
candidate is private operational source only; it does not invoke the genuine
builder or service. The exact seven-row recipe/binding packet is in
`evidence/candidate/cases.json`, with a concise dispatch policy in
`evidence/dispatch-recipes.json`.

The manager may dispatch one selector at a time in this order:

1. `p2-popup-add@popup-retry-1` (the one explicitly authorized corrected attempt)
2. `p2-parent-move@original`
3. `p2-transition-none-single@original`
4. `p2-transition-none-bulk@original`
5. `p2-register-asset@original`
6. `p1@original`
7. `p3@original`

For each future real dispatch, use the unchanged supported production builder
with the exact 12 environment bindings and the unique suite/output/plan paths.
The submit invocation remains the sole owner of checkout, preflight, normal
request, artifact persistence, and its direct wait/reap. Never repeat printed
request lines. Before any create or relaunch, inspect same target/suite/source,
exact command/row bytes, normal/preflight IDs, and immutable artifact state.
Adopt exact existing IDs; a missing normal ID does not authorize another call.
If custody is ambiguous or permission/safety refuses, retain the first error,
stop that selector, and continue only independent selectors after the shared
safety check.

## Next independent review command

From the worker evidence directory, run:

```bash
sha256sum candidate/controller.py candidate/check.sh candidate/cases.json
candidate/check.sh
```

Expected candidate hashes are recorded in `source-manifest.json` and the exact
check script hash is `36df5df5cc83c0574a29c0215926748a2897a2f17e37115212baa879912be435`.
The review purpose is to verify: source/tuple conservation; unique retry
scope; exact request adoption; no duplicate normal/body calls; honest terminal
status; custody stop behavior; selector isolation; 4-GB exact-ID attribution;
and absence of service/process/network operations. Do not broaden it into a
real dispatch or product qualification.
