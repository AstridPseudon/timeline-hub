from __future__ import annotations

import copy
from collections import Counter
from functools import cache

import pytest
from jsonschema import Draft202012Validator
from test_timeline_commit_sequential_verifier import (
    test_moved_history_replays_authenticated_original_and_landing as _verify_history,
)
from test_timeline_validation_cost import _packet

from runtime_protocol import timeline_commit_validation as validation


@pytest.mark.parametrize("reuse", [False, True])
def test_retained_history_revalidates_every_value_on_each_read(monkeypatch, reuse):
    packet = _packet()
    before = copy.deepcopy(packet)
    bundle, registry = validation._schema_resources()

    @cache
    def native(definition):
        return Draft202012Validator(
            {"$ref": bundle["root"] + "#/$defs/" + definition}, registry=registry
        )

    factory = validation._validator if reuse else native
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
    for reads in (1, 2):
        with monkeypatch.context() as history_patches:
            # The existing control constructs only the enclosing receipt/event;
            # its original/landing documents and intervening history are genuine.
            _verify_history(packet, history_patches)
        assert counts == {
            "CanonicalDocument": 54 * reads,
            "Recorder": 2 * reads,
            "CommitContext": reads,
            "PreparedCommit": reads,
            "finite_json": 58 * reads,
        }
        assert packet == before
