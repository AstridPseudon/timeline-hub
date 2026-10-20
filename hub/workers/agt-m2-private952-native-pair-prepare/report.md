Prepared the real private Agent `a53703ce…` / Runtime `95202c2b…` pair after pin ACK.

Changed only [test_commit_runtime_occurrence_media.py](/home/user/work/wt/agt-m2-private952-native-pair-prepare/tests/editing_conformance/test_commit_runtime_occurrence_media.py), adapting setup to current authoritative Runtime bindings and v2 capture.

Guards passed:

- Vendor lock matches Runtime manifest.
- Runtime artifact and generator checks passed.
- Schema: `613123…`; bundle: `4a0779…`; manifest: `35aa9d…`.

Tests:

- Occurrence + identity: **51 passed**
- Native lost-ACK/restart subset: **17 passed**
- Materialization/version/map: **66 passed**
- Schema/client controls: **59 passed**

Full native batch remains **34 passed, 6 failed** on existing reload `_source_closure` shape assertions; assertions were preserved.

Wrote `commit-msg`, `commit-msg.txt`, report, and `DONE`.