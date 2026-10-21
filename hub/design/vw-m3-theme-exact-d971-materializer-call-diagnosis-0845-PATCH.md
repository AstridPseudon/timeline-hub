# UNAPPLIED PATCH — exact d971 fixture plumbing

This is a proposal only. It was not applied to the Agent worktree. It changes
no product contract and adds no Theme DTO/store/resolver/authority. Apply it
only in the fixture owner’s worktree before the next authorized central run.

```diff
diff --git a/tests/integrations/test_generic_host_remotion_render.py b/tests/integrations/test_generic_host_remotion_render.py
--- a/tests/integrations/test_generic_host_remotion_render.py
+++ b/tests/integrations/test_generic_host_remotion_render.py
@@ -600,8 +600,9 @@
         assert response.ok
         task = generated.get_task(result.kernel_task_id)
         assert task.input_object_ids == request["input_manifest"]
-        assert task.spec["inputs"] == request["spec"]["inputs"]
+        admitted_inputs = task.spec["spec"]["inputs"]
+        assert admitted_inputs == request["spec"]["inputs"]
         print(
@@ -613,9 +614,10 @@
         )
         attempt = tmp_path / "materialized-attempt"
         values = host._materialize_inputs(
-            {"spec": task.spec, "input_object_ids": task.input_object_ids},
+            task.spec,
             attempt,
+            authorized_input_object_ids=task.input_object_ids,
             file_input_names=frozenset(
                 port.name for port in record.definition.inputs if port.type == "file"
@@ -654,7 +656,7 @@
         forged = tmp_path / "forged-theme.json"
         forged.write_text(json.dumps(explicit_theme), encoding="utf-8")
-        forged_spec = {"spec": {"inputs": {**task.spec["inputs"], "theme": str(forged)}}}
+        forged_spec = {"spec": {"inputs": {**admitted_inputs, "theme": str(forged)}}}
         with pytest.raises(HostError, match="requires a managed Runtime object"):
```

The first and third hunks are the prior approved nested-descriptor correction
needed because this selected d971 source predates the 0839 private snapshot.
The middle hunk is the new diagnosis result: it removes the extra envelope
layer and supplies the explicit authorized ID carrier used by the normal host
caller.

