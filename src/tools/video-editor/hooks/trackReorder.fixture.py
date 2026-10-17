"""W48 caller wires through the selected immutable SDK and synthetic acceptance port."""
# ruff: noqa: E402 -- bind the immutable SDK before importing it.
import copy
import json
import os
from pathlib import Path
import sys

sdk = Path(os.environ["ASTRID_CHECKOUT"])
sys.path[:0] = [str(sdk), str(sdk / "tests/sdk")]
from test_timeline_commit import Port
from astrid.core.timeline import scene_answers
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.identity import retain_cut_reservations


class Answers:
    def query_scene(self, *, revision_digest, scene, frames):
        return [dict(frame=frame, coverage="COVERED", content="CONTENT", findings=[], layers=[]) for frame in frames]


scene_answers._client = lambda: Answers()
Checkout._native_outline_integrity = lambda *args: None
value = json.load(sys.stdin)
config = copy.deepcopy(value["config"])
fixture = json.loads((sdk / "tests/fixtures/timeline_editing/tiny_publishable.json").read_text())
clips = config.pop("clips")
fixture["parent"] = dict(config=config, clips=clips, registry=value["registry"])
retain_cut_reservations(fixture)
mode = value.get("mode", "positive")
if mode == "stale":
    fixture["parent"]["config"]["tracks"].reverse()
tl = Checkout(fixture)
tl.resolve()
before = copy.deepcopy(tl.document())
document = before
results = []
accept_counts = []
replays = []


class CallerService(RuntimeCommitService):
    @staticmethod
    def _load_revision(port, request, revision):
        return copy.deepcopy(document)


class CallerPort(Port):
    def accept(self, prepared):
        response = super().accept(prepared)
        result = response["stored_result"]
        if result["status"] == "accepted":
            result.update(accepted_revision_id="parent-r" + str(len(results) + 2),
                          accepted_publication_id="pub-parent-r" + str(len(results) + 2))
        self.saved["result"] = copy.deepcopy(result)
        return response


service = CallerService()
for request in value["requests"]:
    port = CallerPort(request)
    port.current = request["base_revision_id"]
    result = service.commit(request, port)
    if mode == "stale":
        assert result["status"] in {"refused", "conflict"}, result
        assert not port.accepts and not result["change"]["direct_writes"]
        assert result["accepted_publication_id"] is None
    elif mode == "no_change":
        assert result["status"] == "no_change", result
        assert not result["change"]["direct_writes"] and result["accepted_publication_id"] is None
    else:
        assert result["status"] == "accepted", result
        assert len(result["change"]["commands"]) == len(request["change"]["commands"])
        for actual, sent in zip(result["change"]["commands"], request["change"]["commands"]):
            # SDK records additional version/authorship metadata; every caller field stays exact.
            for key, item in sent.items():
                if key == "expect":
                    assert all(actual["expect"].get(path) == state for path, state in item.items()), (actual, sent)
                else:
                    assert actual.get(key) == item, (actual, sent)
    replay = service.commit(request, port)
    assert replay == result, "exact request replay changed the receipt"
    replays.append(replay == result)
    if result["status"] == "accepted":
        assert len(port.accepts) == 1
        assert port.accepts[0]["evidence"]["direct_writes"] == result["change"]["direct_writes"]
        document = copy.deepcopy(result["canonical_document"])
    results.append(result)
    accept_counts.append(len(port.accepts))
if mode == "positive" and len(results) > 1:
    assert results[1]["canonical_document"] == before, "Undo did not restore the entire authored document"
if mode == "positive" and len(results) > 2:
    assert results[2]["canonical_document"] == results[0]["canonical_document"], "Redo changed authored content"
print(json.dumps(dict(before=before, results=results, result=results[-1], replay=replays,
                     accept_counts=accept_counts, source=str(sdk), requests=value["requests"])))
