# FOR AGENT REVIEW — D09 deletion scope

Base: `4a75f68f32049a69fd86135c645fa64c51175c14`; source: `09cfd10a44b17a24d6f77ef6b8f41cce9cd0db1e`.
**UNAPPLIED; zero repo writes. 18 files, +1060/-573; product net +80.**
Only roles/address + scene-query adapter + direct SDK/label consumers and tests.

```text
D astrid/core/timeline/onscreen.py
A astrid/core/timeline/scene_answers.py
A astrid/core/timeline/scene_roles.py
M astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py
M astrid/sdk/timeline/check.py
M astrid/sdk/timeline/reflow.py
A remotion/native-scene.mjs
A remotion/scene-query.mjs
A remotion/src/host-scene.ts
A tests/core/timeline/scene_support.py
M tests/core/timeline/test_onscreen.py
M tests/core/timeline/test_onscreen_more.py
M tests/packs/rendering/test_labels_overlay.py
A tests/packs/rendering/test_scene_deletion_host.py
A tests/packs/rendering/test_scene_deletion_query.py
M tests/packs/rendering/test_timeline_visualize_labels.py
M tests/sdk/test_intent_app_astrid.py
A tests/sdk/test_scene_deletion_check.py
```

Held: verified source join, frozen label forwarding, real component capabilities, public10 paired adoption/native8 compatibility, MAIN0.0.6 intended-difference pixel proof. No pins/AM/provider/Root/custody/generator changes. Manager + Agent owner review, then one exact-tuple paired gate. See ORCHREPORT.md for named tests and limits.
