"""Real R4 execution plus a deliberately small future-guard/outbox adapter.

Only the command runner, recorder, compiler, rebase and inverse checks are product
code. Publication storage, retry and the JSON-file outbox are protocol models.
"""
# The frozen checkout must precede main on the import path.
# ruff: noqa: E402
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT))

from astrid.sdk import timeline_intent as intent
from astrid.sdk.timeline import commands, inverse
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
from astrid.sdk.timeline.identity import retain_cut_reservations
from astrid.sdk.timeline.rebase import rebase
from astrid.version import __version__

SID = "occurrence:occ-A/clip:a-rocket"


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def tiny():
    raw = json.loads((ROOT / "tests/fixtures/timeline_editing/tiny_publishable.json").read_text())
    # The stock four-second shot cannot contain the mandated moves to 5 and 7.
    raw["placements"][0]["duration_ms"] = 20000
    raw["placements"][1]["placement"]["start_ms"] = 20000
    raw["shots"]["A"]["internal_timeline"]["clips"][0]["hold"] = 20
    return retain_cut_reservations(Checkout(raw).document())


def apply(document, call):
    return RuntimeCommitService._apply(copy.deepcopy(document), [call])[:2]


def r4_call(wire):
    return commands.EditCommand.coerce({k: v for k, v in wire.items()
                                       if k not in {"schema_version", "reads", "selections"}})


def read_basis(document, call):
    if call.op not in {"clip.on", "clip.nudge"}:
        return [], []
    tl = Checkout(copy.deepcopy(document))
    states = commands.entity_states(tl)
    sid = call.select
    paths = ["id", "track", "intent.on"]
    if commands.state_at(states, sid, "intent.on")["state"] == "absent":
        paths.append("at")  # Created clips can have a fixed at without intent.on.
    reads = [{"ref": sid, "path": path.split("."), "state": commands.state_at(states, sid, path)}
             for path in paths]
    # Fixture selector: choose a clip from this track's ordered membership, then
    # freeze that selection. R4 has no selection recorder; this query is the
    # explicit future-policy adapter, not an inferred before/after diff.
    clip = tl.clip(sid)
    owner = sid.split("/clip:")[0]
    members = [commands.scoped_clip(tl, item) for item in tl.clips()
               if commands.scoped_clip(tl, item).startswith(owner + "/clip:")
               and item.data.get("track") == clip.data.get("track")]
    selection = {"key": "move.track-members", "query_version": 1,
                 "owner": owner + "/track:" + clip.data["track"],
                 "members": sorted(members), "order": members,
                 "boundaries": members[:1] + members[-1:] if members else [],
                 "policy": "guard-membership"}
    return reads, [selection]


def record(document, op, args, sid=SID):
    after, plan = apply(document, {"op": op, "select": sid, "args": args})
    wire = plan.calls[0].to_json()
    if op in {"clip.on", "clip.nudge"}:
        # R4's recorder emits a local selector alongside the scoped resolved ID.
        wire["select"] = wire["resolved"][0]
    if op == "clip.nudge":
        # R4 converts nudge into clip.on. Preserve the original relative intent
        # at the adapter boundary; use R4's captured guards and resolved IDs.
        assert wire["op"] in {"clip.on", "clip.nudge"}
    if op in {"clip.on", "clip.nudge"}:
        wire.update(op=op, args=copy.deepcopy(args))
    if op == "timeline.add":
        # The initial R4 add record can omit destination/occurrence guards that
        # replay requires. Capture them ONCE on the original authoring document,
        # using the real destination guard builder and the allocated clip ID.
        guarded, _ = commands.guard_add_destination(
            Checkout(copy.deepcopy(document)), commands.EditCommand.coerce(wire))
        wire = guarded.to_json()
    wire["schema_version"] = 1
    wire["reads"], wire["selections"] = read_basis(document, r4_call(wire))
    return after, wire


def schema():
    # Extend the ACTUAL frozen envelope, retaining its tagged-state/ScopedId
    # validation. These two future record leaves are test-only recipe adapters.
    value = json.loads((ROOT / "schemas/change-contract/opcall.schema.json").read_text())
    state = value["properties"]["expect"]["additionalProperties"]
    value["required"] += ["schema_version", "version", "resolved", "expect", "bindings",
                          "created", "authorship", "reads", "selections"]
    value["properties"].update({
        "schema_version": {"const": 1},
        "version": {"const": __version__},
        "reads": {"type": "array", "items": {
            "type": "object", "required": ["ref", "path", "state"],
            "additionalProperties": False, "properties": {
                "ref": {"$ref": "#/$defs/scopedId"},
                "path": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                "state": state}}},
        "selections": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["key", "query_version", "owner", "members", "order",
                         "boundaries", "policy"],
            "properties": {
                "key": {"const": "move.track-members"}, "query_version": {"const": 1},
                "owner": {"$ref": "#/$defs/scopedId"},
                **{key: {"type": "array", "items": {"$ref": "#/$defs/scopedId"}}
                   for key in ("members", "order", "boundaries")},
                "policy": {"const": "guard-membership"}}}},
    })
    Draft202012Validator.check_schema(value)
    return Draft202012Validator(value)


VALIDATOR = schema()


class Refused(ValueError):
    pass


class Provider:
    def __init__(self):
        self.phases = []

    def verify(self, document, wire, phase):
        VALIDATOR.validate(wire)
        call = r4_call(wire)
        # Verify ORIGINAL claims before executing/recording. No setdefault or
        # replacement with guards sampled from the accepted base is permitted.
        try:
            commands.check_expectations(Checkout(copy.deepcopy(document)), call, call.resolved)
            reads, selections = read_basis(document, call)
        except commands.TimelineEditError as exc:
            raise Refused("original guards: " + str(exc)) from exc
        if wire["reads"] != reads or wire["selections"] != selections:
            raise Refused("original read/selection guards differ")
        self.phases.append(phase)
        result = rebase([call], document)
        if result.conflicts:
            raise Refused("original guards: " + str(result.conflicts))
        # R4 checks direct-path completeness against actual handler execution.
        # Also reject omitted/extra recorded expectations, not just bad values.
        actual = result.plan.calls[0].to_json()
        for key in ("expect", "bindings", "created", "authorship", "resolved"):
            observed, original = actual[key], wire[key]
            if phase == "head" and key == "authorship":
                # Compiler consequences can differ on a newer head. Only the
                # handler's direct write declaration is an original claim.
                observed = {k: v for k, v in observed.items() if v == "direct"}
                original = {k: v for k, v in original.items() if v == "direct"}
            if observed != original:
                raise Refused(f"incomplete original record: {key}: {wire[key]!r} -> {actual[key]!r}")
        return result.document

    def commit(self, base, head, wire):
        original = encoded(wire)
        after = self.verify(base, wire, "base")
        if head != base:
            after = self.verify(head, wire, "head")
        assert encoded(wire) == original
        return after


class Server:
    """Publication/idempotency model around the real semantic execution path."""

    def __init__(self):
        self.entries = {"H0": tiny()}
        self.head = "H0"
        self.keys = {}
        self.provider = Provider()

    @staticmethod
    def revision(document):
        return "sha256:" + hashlib.sha256(encoded(document).encode()).hexdigest()

    def request(self, base, command):
        return {"api_version": 1, "project_id": "p", "timeline_id": "t",
                "base_revision_id": self.revision(self.entries[base]),
                "base_publication_id": base, "commands": [copy.deepcopy(command)]}

    def publish(self, document):
        self.head = "H" + str(len(self.entries))
        self.entries[self.head] = copy.deepcopy(document)

    def commit(self, key, body):
        if set(body) != {"api_version", "project_id", "timeline_id", "base_revision_id",
                         "base_publication_id", "commands"}:
            raise Refused("closed commit envelope")
        assert (body["api_version"], body["project_id"], body["timeline_id"]) == (1, "p", "t")
        if key in self.keys:
            previous, response = self.keys[key]
            if previous != encoded(body):
                raise Refused("idempotency mismatch")
            return copy.deepcopy(response)
        base = self.entries[body["base_publication_id"]]
        if self.revision(base) != body["base_revision_id"]:
            raise Refused("base pair mismatch")
        assert len(body["commands"]) == 1
        result = self.provider.commit(base, self.entries[self.head], body["commands"][0])
        self.publish(result)
        response = {"receipt": {"receipt_id": self.head},
                    "data": {"accepted_revision_id": self.revision(result),
                             "canonical_document": result}}
        self.keys[key] = [encoded(body), copy.deepcopy(response)]
        return copy.deepcopy(response)

    def external(self, change, sid=SID, *, args=None):
        document = copy.deepcopy(self.entries[self.head])
        tl = Checkout(document)
        if change == "disjoint":
            # A real R4 command and compiler, on a property B did not read.
            document, _ = apply(document, {"op": "clip.set", "select": sid,
                                          "args": args or {"x": 120}})
        elif change == "read_conflict":
            tl.clip(sid).data["track"] = "type"
        elif change == "selection_conflict":
            neighbor = copy.deepcopy(tl.clip(sid).data)
            neighbor["id"] = "external-neighbor"
            intent.set_layer(neighbor, "external-neighbor")
            tl._internal("A")["clips"].append(neighbor)
        elif change == "replacement":
            tl.clip(sid).data["id"] = "replacement"
        else:
            raise AssertionError(change)
        # Structural fixtures stand in for a validated other writer; only the
        # disjoint edit above uses the actual command runner.
        self.publish(document)


class Outbox:
    """JSON persistence model; reload discards all Python objects and callables."""

    def __init__(self, server, mode, created=False):
        base = server.entries["H0"]
        if created:
            optimistic, prefix = record(base, "timeline.add", {
                "element": "am-sprite", "at": 5, "hold": 1, "layer": "suffix-created"}, None)
            sid = prefix["created"][0]
        else:
            optimistic, prefix = record(base, "clip.on", {"moment": 5})
            sid = SID
        assert Checkout(optimistic).clip(sid).start == 5
        op, args = (("clip.on", {"moment": 7}) if mode == "absolute"
                    else ("clip.nudge", {"seconds": 2}))
        _, suffix = record(optimistic, op, args, sid)
        self.data = {"inflight": {"key": "request-A", "body": server.request("H0", prefix)},
                     "suffix": {"status": "UNSENT", "commands": [suffix],
                                "refs": suffix["resolved"],
                                "created_dependencies": prefix["created"],
                                "predecessor": "request-A", "request": None, "key": None}}

    def ack(self, server, response):
        assert self.data["suffix"]["status"] == "UNSENT"
        prefix_key = self.data["inflight"]["key"]
        suffix = self.data["suffix"]
        suffix["request"] = server.request(response["receipt"]["receipt_id"], suffix["commands"][0])
        suffix["key"] = "request-B"
        assert suffix["key"] != prefix_key
        suffix["status"] = "INFLIGHT"
        self.data["inflight"] = None

    def reject(self):
        self.data["suffix"]["status"] = "CONFLICT"


def reload_data(server, outbox):
    path = Path("process-data.json")
    path.write_text(encoded({"entries": server.entries, "head": server.head,
                             "keys": server.keys, "outbox": outbox.data}))
    saved = json.loads(path.read_text())
    other = Server()
    other.entries, other.head, other.keys = saved["entries"], saved["head"], saved["keys"]
    box = object.__new__(Outbox)
    box.data = saved["outbox"]
    path.unlink()
    return other, box


def run(scenario, mode, recovery, stage):
    server = Server()
    outbox = Outbox(server, mode, created=scenario in {"created", "basis_conflict"})
    original = encoded(outbox.data["suffix"])
    a = copy.deepcopy(outbox.data["inflight"])
    # Durable UNSENT intent is recoverable before A's first send.
    server, outbox = reload_data(server, outbox)
    assert encoded(outbox.data["suffix"]) == original
    if scenario == "rejected":
        server.external("replacement")
        with pytest.raises(Refused):
            server.commit(a["key"], a["body"])
        outbox.reject()
        server, outbox = reload_data(server, outbox)
        assert outbox.data["suffix"]["status"] == "CONFLICT"
        retained = copy.deepcopy(outbox.data["suffix"])
        retained["status"] = "UNSENT"
        assert encoded(retained) == original
        assert not server.keys
        return
    # Disjoint C can precede A's acceptance too: A is genuinely server-rebased.
    if scenario == "disjoint":
        server.external("disjoint", "occurrence:occ-A/clip:a-plate", args={"zoom": 2})
    if scenario == "basis_conflict":
        # A creates a pinned clip; B selects its track's members. C changes
        # that selection before A accepts, without invalidating A's add guards.
        server.external("selection_conflict")
    if scenario == "created":
        server.external("disjoint")
    accepted = server.commit(a["key"], a["body"])
    ha = accepted["receipt"]["receipt_id"]
    sid = outbox.data["suffix"]["refs"][0]
    if stage == "before_ack" and scenario in {"read_conflict", "selection_conflict"}:
        server.external(scenario, sid)
    if scenario in {"aba", "same_value"}:
        identical = copy.deepcopy(server.entries[server.head])
        if scenario == "aba":
            server.external("read_conflict", sid)
        server.publish(identical)
    if recovery == "reload":
        server, outbox = reload_data(server, outbox)
    if recovery in {"retry", "reload"}:
        count = len(server.entries)
        # Retry bypasses even semantic validation and returns the old result,
        # despite a later head. No original-result reconstruction is present.
        assert not server.provider.phases or recovery == "retry"
        before = list(server.provider.phases)
        assert server.commit(a["key"], a["body"]) == accepted
        assert server.provider.phases == before
        assert len(server.entries) == count
    assert encoded(outbox.data["suffix"]) == original
    outbox.ack(server, accepted)
    server.provider.phases.clear()
    b = outbox.data["suffix"]
    assert b["request"]["base_publication_id"] == ha
    assert b["request"]["base_revision_id"] == accepted["data"]["accepted_revision_id"]
    assert b["request"]["commands"] == json.loads(original)["commands"]
    if stage == "after_ack" and scenario in {"disjoint", "read_conflict", "selection_conflict"}:
        server.external(scenario, sid)
    if recovery == "reload":
        before = encoded(b)
        server, outbox = reload_data(server, outbox)
        b = outbox.data["suffix"]
        assert encoded(b) == before
    if scenario in {"read_conflict", "selection_conflict", "basis_conflict"}:
        count = len(server.entries)
        with pytest.raises(Refused, match="original read/selection"):
            server.commit(b["key"], b["request"])
        assert server.provider.phases == ([] if scenario == "basis_conflict" else ["base"])
        assert len(server.entries) == count and b["key"] not in server.keys
        return
    if scenario == "guards":
        guard_cases(server, b)
        return
    if scenario == "schema":
        schema_cases(b["request"]["commands"][0])
        with pytest.raises(Refused, match="closed commit envelope"):
            server.commit("extra-basis", {**b["request"], "base_view": "original-result"})
        return
    if scenario == "retry_identity":
        with pytest.raises(Refused, match="idempotency mismatch"):
            server.commit(a["key"], b["request"])
    before = encoded(b["request"])
    result = server.commit(b["key"], b["request"])
    if scenario == "retry_identity":
        changed = copy.deepcopy(b["request"])
        changed["commands"][0]["args"] = ({"moment": 8} if mode == "absolute" else {"seconds": 3})
        with pytest.raises(Refused, match="idempotency mismatch"):
            server.commit(b["key"], changed)
    final = Checkout(result["data"]["canonical_document"])
    assert final.clip(sid).start == 7
    assert encoded(b["request"]) == before
    command = b["commands"][0]
    assert command["args"] == ({"moment": 7} if mode == "absolute" else {"seconds": 2})
    assert command["op"] == ("clip.on" if mode == "absolute" else "clip.nudge")
    assert Checkout(server.entries[ha]).clip(sid).start == 5
    assert next(r["state"] for r in command["reads"] if r["path"] == ["intent", "on"]) == (
        commands.state_at(commands.entity_states(Checkout(server.entries[ha])), sid, "intent.on"))
    if any(r["path"] == ["at"] for r in command["reads"]):
        assert next(r["state"] for r in command["reads"] if r["path"] == ["at"]) == {
            "state": "present", "value": 5}
    if scenario == "disjoint":
        assert final.clip(sid).get("x") == 120
        assert final.clip("occurrence:occ-A/clip:a-plate").get("zoom") == 2
        assert server.provider.phases[-2:] == ["base", "head"] or stage == "before_ack"
    if scenario == "created":
        assert b["created_dependencies"] == [sid]
        assert sid in commands.entity_states(final)
        assert b["commands"][0]["resolved"] == [sid]
    count = len(server.entries)
    server, outbox = reload_data(server, outbox)
    assert server.commit(b["key"], b["request"]) == result
    assert len(server.entries) == count


def guard_cases(server, suffix):
    original = encoded(suffix["request"])
    for field in ("expect", "reads", "selections", "resolved", "authorship"):
        forged = copy.deepcopy(suffix["request"])
        forged["commands"][0][field] = [] if field in {"reads", "selections", "resolved"} else {}
        with pytest.raises((Refused, commands.TimelineEditError)):
            server.commit("forged-" + field, forged)
    forged = copy.deepcopy(suffix["request"])
    forged["commands"][0]["reads"][0]["state"]["value"] = "forged-id"
    with pytest.raises(Refused, match="original read/selection"):
        server.commit("forged-id", forged)
    forged = copy.deepcopy(suffix["request"])
    forged["commands"][0]["selections"][0]["order"] = []
    with pytest.raises(Refused, match="original read/selection"):
        server.commit("forged-order", forged)
    # A real changed dependency on the submitted HA cannot be hidden by
    # recording on that base first: original claims must be checked first.
    wire = suffix["request"]["commands"][0]
    changed = copy.deepcopy(server.entries[server.head])
    Checkout(changed).clip(wire["select"]).data["track"] = "type"
    provider = Provider()
    with pytest.raises(Refused, match="original read/selection"):
        provider.commit(changed, changed, wire)
    assert provider.phases == []
    # The client retains original claims; only an explicit new user edit may
    # capture a different basis. The wire cannot attest what a client once saw.
    assert encoded(suffix["request"]) == original


def schema_cases(wire):
    VALIDATOR.validate(wire)
    assert r4_call(wire).to_json()["expect"] == wire["expect"]
    mutations = [
        ("schema_version", 2), ("version", "unsupported"),
        ("reads", [{"ref": SID, "path": ["track"], "state": {"state": "absent", "value": 1}}]),
        ("expect", {"intent.on": {"state": "present"}}),
        ("resolved", ["array-index:0"]), ("created", ["not-an-id"]),
        ("base_view", "original-result"), ("authority", "admin"),
    ]
    for key, value in mutations:
        bad = {**copy.deepcopy(wire), key: value}
        with pytest.raises(ValidationError):
            VALIDATOR.validate(bad)
    for field in ("expect", "reads", "selections", "created", "resolved", "bindings"):
        bad = copy.deepcopy(wire)
        bad.pop(field)
        with pytest.raises(ValidationError):
            VALIDATOR.validate(bad)


def inverse_history():
    base = tiny()
    first, plan = apply(base, {"op": "clip.set", "select": SID, "args": {"x": 120}})
    undo = inverse.inverse_command(plan.calls, base, first, "pub-original")
    for value in (120, 180):
        intervening, _ = apply(first, {"op": "clip.set", "select": SID, "args": {"x": value}})
        aba, returned = apply(intervening, {"op": "clip.set", "select": SID, "args": {"x": 120}})
        evidence = {"commands": [c.to_json() for c in returned.calls],
                    "direct_writes": list(returned.direct_writes)}
        row = {"publication_id": "pub-later", "revision_id": "rev-later",
               "previous_publication_id": "pub-original", "previous_revision_id": "rev-original",
               "evidence_digest": _digest(evidence), "label": "another writer"}
        port = SimpleNamespace(revisions=lambda options: [row], evidence=lambda _: evidence)
        failure = RuntimeCommitService._inverse_history(
            port, {"project_id": "p", "timeline_id": "t"}, [commands.EditCommand.coerce(undo)],
            {"publication_id": "pub-later"}, aba, {"status": None, "conflicts": [], "choices": []})
        assert failure and failure["conflicts"][0]["kind"] == "same-property"


if __name__ == "__main__":
    scenario, mode, recovery, stage = sys.argv[2:]
    if scenario == "inverse_history":
        inverse_history()
    else:
        run(scenario, mode, recovery, stage)
    print(f"PASS {scenario} {mode} {recovery} {stage}")
