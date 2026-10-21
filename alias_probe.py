"""Pure copy-boundary probe for the ordered inverse diagnosis."""
import copy
import json

from astrid.sdk.timeline._collections import AcceptedRecords
from astrid.sdk.timeline._command_state import State, present
from astrid.sdk.timeline.inverse import coalesce


before = {"state": "present", "value": {}}
raw = {
    "ordinal": 0,
    "command": {"op": "project-data.write"},
    "writes": [
        {
            "ref": "parent",
            "path": ["config", "app", "com.example.compiler-canary", "gone"],
            "before": {"state": "present", "value": None},
            "after": {"state": "absent"},
        },
        {
            "ref": "parent",
            "path": ["config", "app", "com.example.compiler-canary"],
            "before": before,
            "after": {"state": "absent"},
            "insertion_order": ["a-before", "com.example.compiler-canary", "z-after"],
        },
    ],
    "reads": [],
    "selections": [],
    "bindings": [],
    "created": [],
    "dependencies": [],
    "derived_writes": [],
}
entry = {"records": {"commands": [raw], "undo_of": []}}
accepted = AcceptedRecords([entry], copy.deepcopy([raw]), lambda _: ({}, {}))
raw_before = copy.deepcopy(accepted[0])
print("entry_vs_flattened_identity=", entry["records"]["commands"][0] is accepted[0])
print("before_value_identity=", entry["records"]["commands"][0]["writes"][1]["before"]["value"] is accepted[0]["writes"][1]["before"]["value"])
coalesced = coalesce(accepted)
print("coalesced_before=", json.dumps(coalesced[0]["before"], sort_keys=True))
print("flattened_unchanged=", accepted[0] == raw_before)
state = State({
    "parent": {"config": {"app": {"com.example.compiler-canary": {"gone": None}}}},
    "placements": [],
    "shots": {},
    "source_mapping": {},
})
source = present({"gone": None})
state.set("parent", ["config", "app", "com.example.compiler-canary"], {"state": "absent"})
print("setter_source_retains_gone=", "gone" in source["value"])
