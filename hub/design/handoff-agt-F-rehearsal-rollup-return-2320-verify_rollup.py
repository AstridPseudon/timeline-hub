#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
ORCH = ROOT.parents[1]
PRIOR = ORCH / "agt-F-rehearsal-rollup-2311/evidence"
CONTRAST = ORCH / "agt-F-rehearsal-contrasts-2311/evidence"

payload = json.loads((ROOT / "rehearsal-rollup.json").read_text())
prior = json.loads((PRIOR / "rehearsal-rollup.json").read_text())
clusters = json.loads((ROOT / "dispatch-clusters.json").read_text())
prior_clusters = json.loads((PRIOR / "dispatch-clusters.json").read_text())
contrast = json.loads((CONTRAST / "OWN-REHEARSAL-CONTRASTS.parsed.json").read_text())
rows = payload["rows"]
old_rows = prior["rows"]
old_by_id = {row["canonical_node"]: row for row in old_rows}
by_id = {row["canonical_node"]: row for row in rows}
assert payload["partition_total"] == 550
assert len(rows) == 550
assert len(by_id) == 550
assert [row["canonical_node"] for row in rows] == [row["canonical_node"] for row in old_rows]
expected_buckets = {"PRE-EXISTING": 16, "KNOWN GAP": 37, "ENV": 73, "NEW-OURS core": 424, "NEW-OURS non-core": 0, "REGRESSION": 0}
assert payload["final_buckets"] == expected_buckets
assert Counter(row["category"] for row in rows) == Counter({"PRE-EXISTING": 16, "KNOWN GAP": 37, "ENV": 73, "NEW-OURS core": 424})
assert sum(expected_buckets.values()) == 550
assert payload["separate"] == {"KNOWN-P4": 1, "PENDING-18": 18}
assert payload["subscope_counts"] == {"KNOWN-P4": 1, "historical-PENDING-18-overlay": 18}
assert not any(row["category"] == "REGRESSION" for row in rows)

# Bounded-change audit: all prior fields are byte-for-byte equal except the named classification/status fields.
mutable = {"category", "basis", "current_status", "historical_current_status", "status_overlay", "overlay_evidence", "subscope_flag", "named_known_scope", "cut_blocking", "proof_owed", "readiness_claim", "automatic_source_fix_claim", "dispatch_readiness", "dispatch_owner"}
for old in old_rows:
    new = by_id[old["canonical_node"]]
    for key, value in old.items():
        if key not in mutable:
            assert new[key] == value, (old["canonical_node"], key)

retired_ids = {row["canonical_node"] for row in old_rows if row["basis"] == "D52/D72 retired-route fixture migration; Agent fixture ownership, no Runtime legacy-writer reopening."}
assert len(retired_ids) == 97
assert all(by_id[node]["category"] == "NEW-OURS core" for node in retired_ids)
assert all(by_id[node]["current_status"] == old_by_id[node]["current_status"] for node in retired_ids)
assert all(by_id[node]["historical_current_status"] == old_by_id[node]["current_status"] for node in retired_ids)
assert sum(by_id[node]["dispatch_readiness"] == "ACTIVE-SOURCE-CONTINUATION" for node in retired_ids) == 48
assert sum(by_id[node]["dispatch_readiness"] == "READY-CRITICAL" for node in retired_ids) == 49
assert sum(bool(by_id[node]["dispatch_owner"]) for node in retired_ids) == 48
assert {by_id[node]["dispatch_owner"] for node in retired_ids if by_id[node]["dispatch_owner"]} == {"Agent2318"}

contrast_ids = {item["node_id"] for item in contrast["exact18"]}
assert len(contrast_ids) == 18
assert {node for node in contrast_ids if node not in by_id} == set()
for item in contrast["exact18"]:
    row = by_id[item["node_id"]]
    assert row["category"] == "ENV"
    assert row["current_status"] == "PASSED"
    assert row["historical_current_status"] == item["original_rehearsal_status"]
    assert row["status_overlay"] == "ACTUAL-PASS"
    assert row["upstream_status"] == "PASSED"
    assert row["overlay_evidence"].endswith("OWN-REHEARSAL-CONTRASTS.xml")
assert payload["bounded_updates"]["exact18_overlay"]["count"] == 18
assert payload["bounded_updates"]["exact18_overlay"]["duration_seconds"] == 12.70
assert payload["bounded_updates"]["exact18_overlay"]["regression_closure_inferred"] is False

p4 = [row for row in rows if row["subscope_flag"] == "KNOWN-P4"]
assert len(p4) == 1
assert p4[0]["category"] == "NEW-OURS core"
assert p4[0]["current_status"] == "FAILED"
assert "45.314" in p4[0]["basis"]
assert p4[0]["named_known_scope"] == "KNOWN-P4"

assert sum(row["named_known_scope"] == "PLAN-proposals-35" for row in rows) == 35
assert sum(row["named_known_scope"] == "D23-explicit-selector" for row in rows) == 1
assert by_id["tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight"]["category"] == "KNOWN GAP"
d77 = by_id["tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render"]
assert d77["category"] == "ENV"
assert d77["named_known_scope"] == "D77a-cut-blocking-installed-render"
assert d77["cut_blocking"] is True
assert d77["proof_owed"] is True
assert d77["readiness_claim"] is False
assert d77["automatic_source_fix_claim"] is False
assert "CUT-BLOCKING" in d77["basis"]
assert "missing installed-tuple" in d77["basis"]

# JSON/TSV parity and exact 550 membership.
with (ROOT / "rehearsal-rollup.tsv").open() as stream:
    tsv_rows = list(csv.DictReader(stream, delimiter="\t"))
assert len(tsv_rows) == 550
assert [row["canonical_node"] for row in tsv_rows] == [row["canonical_node"] for row in rows]
assert [row["category"] for row in tsv_rows] == [row["category"] for row in rows]
assert [row["current_status"] for row in tsv_rows] == [row["current_status"] for row in rows]
assert [row["historical_current_status"] for row in tsv_rows] == [row["historical_current_status"] for row in rows]
assert [row["status_overlay"] for row in tsv_rows] == [row["status_overlay"] for row in rows]
assert sum(row["status_overlay"] == "ACTUAL-PASS" for row in tsv_rows) == 18

# Ready-cluster parity: family membership and selector counts remain unchanged.
new_clusters = clusters["clusters"]
old_clusters = prior_clusters["clusters"]
assert len(new_clusters) == len(old_clusters) == 57
assert [(c["family"], c["count"], c["allowed_test_files"]) for c in new_clusters] == [
    (c["family"], c["count"], c["allowed_test_files"]) for c in old_clusters
]
retired_families = {old_by_id[node]["family"] for node in retired_ids}
assert sum(c["count"] for c in new_clusters if c["family"] in retired_families) == 97
assert sum(c["count"] for c in new_clusters if c["family"] in retired_families and c["dispatch_readiness"] == "ACTIVE-SOURCE-CONTINUATION") == 48
assert sum(c["count"] for c in new_clusters if c["family"] in retired_families and c["dispatch_readiness"] == "READY-CRITICAL") == 49
occurrence = next(c for c in new_clusters if c["family"] == "commitTimeline provider / occurrence-media")
assert occurrence["category"] == "NEW-OURS core"
assert occurrence["count"] == 48
assert occurrence["dispatch_owner"] == "Agent2318"
assert occurrence["source_continuation"] == "Agent2318"
assert clusters["ready_clusters"] == payload["ready_clusters"]
assert payload["ready_clusters"] == {"cluster_count": 57, "retired_route_rows": 97, "active_source_continuation_rows": 48, "ready_critical_rows": 49, "active_source_continuation_owner": "Agent2318"}

assert payload["lossless_membership"]["historical_bad_set_equals_table_set"] is True
assert payload["lossless_membership"]["status_overlay_does_not_change_source_xml"] is True
assert payload["assertions"]["categories_sum"] == 550
assert payload["assertions"]["overlay_pass_total"] == 18
assert payload["assertions"]["regression_closure_inferred"] is False
print("PASS successor rollup: rows=550 categories=PRE16/KNOWN37/ENV73/NEWcore424/NEWnoncore0/REG0; exact18 overlay=18; retired-route=97; ready=48+49")
