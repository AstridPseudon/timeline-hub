from __future__ import annotations

import copy
from collections import Counter
from functools import cache

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012
from test_timeline_commit_sequential_verifier import _verify_packet
from test_timeline_validation_cost import _packet

from runtime_protocol import timeline_commit_validation as validation
from runtime_protocol.errors import ValidationError


@pytest.mark.parametrize("reuse", [False, True])
def test_genuine_capture_reuses_resolution_but_revalidates_every_value(monkeypatch, reuse):
    packet = _packet()
    before = copy.deepcopy(packet)
    bundle, registry = validation._schema_resources()

    @cache
    def original(definition):
        return Draft202012Validator(
            {"$ref": bundle["root"] + "#/$defs/" + definition}, registry=registry
        )

    factory = validation._validator if reuse else original
    finite = validation.finite_json
    counts = Counter()

    def validator(definition):
        counts[definition] += 1
        return factory(definition)

    def finite_json(value):
        counts["finite_json"] += 1
        return finite(value)

    monkeypatch.setattr(validation, "_validator", validator)
    monkeypatch.setattr(validation, "finite_json", finite_json)
    _verify_packet(packet)
    assert counts == {"CanonicalDocument": 54, "Recorder": 2, "finite_json": 56}
    assert packet == before


def _validators(resources, root):
    def unavailable(uri):
        from referencing.exceptions import NoSuchResource

        raise NoSuchResource(ref=uri)

    registry = Registry(retrieve=unavailable).with_resources(
        (uri, Resource.from_contents(schema, default_specification=DRAFT202012))
        for uri, schema in resources.items()
    )
    original = Draft202012Validator({"$ref": root}, registry=registry)
    cached = original.evolve(
        _resolver=validation._reuse_schema_resolution(getattr(original, "_resolver"))
    )
    return original, cached


def _errors(validator, value):
    return [(list(e.path), list(e.schema_path), e.message)
            for e in validator.iter_errors(value)]


def test_resolution_preserves_nested_ids_relative_uris_anchors_and_ref_siblings():
    root = "https://example.invalid/root"
    resources = {root: {
        "$id": root,
        "$defs": {
            "a": {"$id": "a/", "$defs": {
                "target": {"$anchor": "target", "type": "integer"},
                "use": {"$ref": "#target", "minimum": 2},
            }, "$ref": "#/$defs/use"},
            "b": {"$id": "b/", "$defs": {
                "target": {"$anchor": "target", "type": "string"},
                "use": {"$ref": "#target", "minLength": 2},
            }, "$ref": "#/$defs/use"},
        },
        "type": "object",
        "properties": {"a": {"$ref": "a/"}, "b": {"$ref": "b/"}},
        "required": ["a", "b"],
        "additionalProperties": False,
    }}
    original, cached = _validators(resources, root)
    valid = {"a": 2, "b": "ok"}
    for value in (valid, {"a": 1, "b": "ok"}, {"a": 2, "b": "x"},
                  {"a": "ok", "b": 2}, {**valid, "unknown": True}, valid):
        assert _errors(cached, value) == _errors(original, value)
    assert not _errors(cached, valid)
    for value in ({"a": 1, "b": "ok"}, {"a": 2, "b": "x"}):
        assert _errors(cached, value)


def test_dynamic_reference_retains_the_full_scope_on_alternating_calls():
    tree = "https://example.invalid/tree"
    strict = "https://example.invalid/strict"
    loose = "https://example.invalid/loose"
    resources = {
        tree: {"$id": tree, "$dynamicAnchor": "node", "type": "object",
               "properties": {"child": {"$dynamicRef": "#node"}}},
        strict: {"$id": strict, "$dynamicAnchor": "node", "$ref": tree,
                 "required": ["tag"]},
        loose: {"$id": loose, "$dynamicAnchor": "node", "$ref": tree},
    }
    validators = [_validators(resources, root) for root in (strict, loose)]
    for _ in range(2):
        for original, cached in validators:
            for value in ({"tag": 1}, {"tag": 1, "child": {}},
                          {"tag": 1, "child": {"tag": 2}}):
                assert _errors(cached, value) == _errors(original, value)
    assert _errors(validators[0][1], {"tag": 1, "child": {}})
    assert not _errors(validators[1][1], {"tag": 1, "child": {}})


@pytest.mark.parametrize("ref", [
    "https://example.invalid/missing", "file:///unpackaged.json",
    "#missing", "#/$defs/missing",
])
def test_unknown_references_fail_identically_after_a_successful_lookup(ref, monkeypatch):
    root = "https://example.invalid/root"
    resources = {root: {"$id": root, "$defs": {"ok": {"type": "integer"}},
                        "properties": {"ok": {"$ref": "#/$defs/ok"},
                                       "bad": {"$ref": ref}}}}
    original, cached = _validators(resources, root)
    for validator in (original, cached):
        validator.validate({"ok": 1})
        for _ in range(2):
            with pytest.raises(Unresolvable):
                validator.validate({"ok": 1, "bad": 1})
        monkeypatch.setattr(validation, "_validator", lambda _definition, v=validator: v)
        with pytest.raises(ValidationError, match="cannot validate CommitRequest"):
            validation.validate_commit_value({"ok": 1, "bad": 1}, "CommitRequest")


def test_resolution_cache_evicts_without_retaining_values_or_losing_constraints():
    root = "https://example.invalid/root"
    resources = {root: {"$id": root,
                        "$defs": {str(i): {"const": i} for i in range(300)},
                        "properties": {str(i): {"$ref": f"#/$defs/{i}"}
                                       for i in range(300)}}}
    original, cached = _validators(resources, root)
    value = {str(i): i for i in range(300)}
    for validator in (original, cached):
        validator.validate(value)
    value["0"] = -1
    assert _errors(cached, value) == _errors(original, value)
    assert _errors(cached, value)
