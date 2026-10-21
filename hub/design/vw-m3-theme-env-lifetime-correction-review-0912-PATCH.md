# APPROVED minimal fixture patch

```diff
diff --git a/tests/integrations/test_generic_host_remotion_render.py b/tests/integrations/test_generic_host_remotion_render.py
--- a/tests/integrations/test_generic_host_remotion_render.py
+++ b/tests/integrations/test_generic_host_remotion_render.py
@@ -569,31 +569,32 @@ def test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_sour
         # The private pack tree is a host-launch fixture input.  Leaving it in
         # the caller environment makes SDK discovery combine it with the
         # checkout's implicit source tree, duplicating h3_av.transform.
-        monkeypatch.delenv("ASTRID_PACKS_PATH", raising=False)
-        result = sdk.invoke(
-            "rendering.render",
-            kind="executor",
-            project=project_id,
-            inputs={
-                "timeline": {
-                    "object_id": timeline_import.data["object_id"],
-                    "digest": timeline_import.data["digest"],
-                    "filename": "hype.timeline.json",
-                },
-                "assets_registry": {
-                    "object_id": registry_import.data["object_id"],
-                    "digest": registry_import.data["digest"],
-                    "filename": "hype.assets.json",
-                },
-                "theme": {
-                    "object_id": descriptor["object_id"],
-                    "digest": descriptor["digest"],
-                    "filename": "theme.json",
-                },
-                "selector": "rendering.remotion",
-            },
-            client=owner,
-        )
+        with monkeypatch.context() as invoke_env:
+            invoke_env.delenv("ASTRID_PACKS_PATH", raising=False)
+            result = sdk.invoke(
+                "rendering.render",
+                kind="executor",
+                project=project_id,
+                inputs={
+                    "timeline": {
+                        "object_id": timeline_import.data["object_id"],
+                        "digest": timeline_import.data["digest"],
+                        "filename": "hype.timeline.json",
+                    },
+                    "assets_registry": {
+                        "object_id": registry_import.data["object_id"],
+                        "digest": registry_import.data["digest"],
+                        "filename": "hype.assets.json",
+                    },
+                    "theme": {
+                        "object_id": descriptor["object_id"],
+                        "digest": descriptor["digest"],
+                        "filename": "theme.json",
+                    },
+                    "selector": "rendering.remotion",
+                },
+                client=owner,
+            )
         assert result.ok, result.to_dict()
         assert len(admissions) == 1
         request, response = admissions[0]
```

This is an unapplied review artifact; it changes only fixture environment
lifetime and leaves the SDK call arguments and all existing assertions intact.
