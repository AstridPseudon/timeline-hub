#!/usr/bin/env python3
import csv, json
from collections import Counter
from pathlib import Path

root = Path(__file__).parent
payload = json.loads((root / "rehearsal-rollup.json").read_text())
rows = payload["rows"]
clusters = json.loads((root / "dispatch-clusters.json").read_text())["clusters"]
assert payload["partition_total"] == 550
assert len(rows) == 550
assert len({row["canonical_node"] for row in rows}) == 550
assert payload["final_buckets"] == {"PRE-EXISTING": 16, "KNOWN GAP": 135, "ENV": 54, "NEW-OURS core": 326, "NEW-OURS non-core": 0, "REGRESSION": 0}
assert payload["separate"] == {"KNOWN-P4": 1, "PENDING-18": 18}
assert Counter(row["category"] for row in rows) == Counter({"NEW-OURS core": 326, "KNOWN GAP": 135, "ENV": 54, "PENDING-18": 18, "PRE-EXISTING": 16, "KNOWN-P4": 1})
assert Counter((row["current_status"], row["upstream_status"]) for row in rows) == Counter({("FAILED", "FAILED"): 16, ("FAILED", "PASSED"): 7, ("ERROR", "PASSED"): 11, ("FAILED", "MISSING"): 285, ("ERROR", "MISSING"): 231})
with (root / "rehearsal-rollup.tsv").open() as stream:
    tsv_rows = list(csv.DictReader(stream, delimiter="\t"))
assert len(tsv_rows) == 550
assert [row["canonical_node"] for row in tsv_rows] == [row["canonical_node"] for row in rows]
assert sum(c["count"] for c in clusters if c["family"] == "commitTimeline provider / occurrence-media") == 48
assert sum(c["count"] for c in clusters if c["family"] == "timeline commit provider ABI / contract validation") == 20
assert not any(row["category"] == "REGRESSION" for row in rows)
print("PASS rollup-json-tsv assertions: rows=550 categories=16/135/54/326/0/0 separate=1/18")
