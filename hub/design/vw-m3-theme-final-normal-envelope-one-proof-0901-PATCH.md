# Patch: corrected normal Theme materializer envelope

Worktree: `/home/user/work/wt/vw-m3-theme-final-normal-envelope-one-proof-0901`
Base: `tl/vw-m3-theme-envelope-corrected-space-cleared-0839`
Base SHA: `d6176de7d38cda56591ffe313ed40c2326374935`

Applied only the reviewed double-envelope correction in
`tests/integrations/test_generic_host_remotion_render.py`:

```diff
@@
         values = host._materialize_inputs(
-            {"spec": task.spec, "input_object_ids": task.input_object_ids},
+            task.spec,
             attempt,
+            authorized_input_object_ids=task.input_object_ids,
             file_input_names=frozenset(
```

The earlier approved `admitted_inputs = task.spec["spec"]["inputs"]`
descriptor assertion and its use in the forged-source path were already in the
base and were preserved. No production, Runtime, DTO, store, resolver,
authority, or source edit was made.
