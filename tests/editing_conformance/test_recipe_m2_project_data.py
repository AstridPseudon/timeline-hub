"""Private candidate contract for authored extension project-data replacement."""

from __future__ import annotations

import copy
import json

import pytest
from jsonschema import Draft202012Validator

from astrid.sdk.timeline._command_state import CommandError, State
from astrid.sdk.timeline.commands import _SCHEMA, execute, operations, validate_command
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import bundle, inverse

TARGET = "com.example.compiler-canary"


def command(key, value, *, target=TARGET, select="parent"):
    return {
        "schema_version": 1,
        "op": "project-data.write",
        "version": "1",
        "select": select,
        "args": {"target": target, "key": key, "value": value, "mode": "replace"},
    }


def project_data(value):
    return State(value).config("parent").get("app", {})


def test_compiler_canary_source_and_source_map_are_one_ordered_native_batch():
    original = bundle()
    source = command("__dsl__:dsl://com.example.compiler-canary/main.json", {"version": 1})
    source_map = command("__dsl_sm__:sm-1", {"id": "sm-1", "sourceLine": 3})

    plan = execute(original, [source, source_map])

    assert [record["ordinal"] for record in plan.records] == [0, 1]
    assert list(project_data(plan.bundle)[TARGET]) == [
        "__dsl__:dsl://com.example.compiler-canary/main.json",
        "__dsl_sm__:sm-1",
    ]
    assert plan.bundle["parent"]["clips"] == original["parent"]["clips"]
    assert plan.bundle["placements"] == original["placements"]
    assert plan.bundle["shots"] == original["shots"]
    assert original["parent"]["config"].get("app") is None


def test_batch_refusal_does_not_leave_a_supported_project_data_member_applied():
    original = bundle()
    before = copy.deepcopy(original)
    with pytest.raises(CommandError):
        execute(
            original,
            [
                command("source", {"version": 1}),
                {
                    "schema_version": 1,
                    "op": "project-data.delete",
                    "version": "1",
                    "select": "parent",
                    "args": {},
                },
            ],
        )
    assert original == before


@pytest.mark.parametrize(
    "prior",
    [
        {},
        {"keep": {"opaque": True}, "slot": None},
    ],
)
def test_replace_preserves_namespace_and_restores_absent_null_and_opaque_values(prior):
    original = bundle()
    original["parent"]["config"]["app"] = {TARGET: copy.deepcopy(prior)}
    before = copy.deepcopy(original)
    value = {"__proto__": {"safe": True}, "constructor": None, "prototype": [1, 2]}
    plan = execute(original, [command("source", value)])

    assert (
        project_data(plan.bundle)[TARGET]["keep"] == prior.get("keep") if "keep" in prior else True
    )
    assert project_data(plan.bundle)[TARGET]["source"] == value
    assert original == before
    validate_command(plan.commands[0])
    assert plan.records[0]["command"]["expect"][f'parent::config.app["{TARGET}"].source'] == {
        "state": "absent"
    }

    undone = inverse(plan.bundle, plan.records)
    assert undone.bundle == before
    redone = inverse(undone.bundle, undone.records)
    assert redone.bundle == plan.bundle


def test_null_prior_value_is_distinct_from_absence():
    original = bundle()
    original["parent"]["config"]["app"] = {TARGET: {"source": None}}
    plan = execute(original, [command("source", "next")])
    assert plan.records[0]["command"]["expect"][f'parent::config.app["{TARGET}"].source'] == {
        "state": "present",
        "value": None,
    }
    assert inverse(plan.bundle, plan.records).bundle == original


def test_disjoint_keys_rebase_and_same_key_aba_refuses():
    original = bundle()
    original["parent"]["config"]["app"] = {TARGET: {"existing": True}}
    first = execute(original, [command("source", "A")])
    other = execute(original, [command("source-map", {"id": "B"})])
    rebased = replay(first, other.bundle, intervening_records=other.records)
    assert project_data(rebased.bundle)[TARGET] == {
        "existing": True,
        "source-map": {"id": "B"},
        "source": "A",
    }

    away = execute(first.bundle, [command("source", "B")])
    back = execute(away.bundle, [command("source", "A")])
    with pytest.raises(CommandError) as error:
        execute(
            back.bundle,
            [inverse(first.bundle, first.records).commands[0]],
            inverse_records=first.records,
            intervening_records=[*away.records, *back.records],
        )
    assert error.value.kind == "intervening_write"


@pytest.mark.parametrize(
    "bad",
    [
        command("", 1),
        command("key", 1, target="not valid"),
        command("key", float("nan")),
        command("key", 1, select="occurrence:occ-1"),
    ],
)
def test_replace_contract_refuses_invalid_input_without_mutation(bad):
    original = bundle()
    before = copy.deepcopy(original)
    with pytest.raises((CommandError, ValueError)):
        execute(original, [bad])
    assert original == before


def test_private_schema_and_registry_are_closed():
    assert "project-data.write" in operations()
    assert operations()["project-data.write"].parameters == _SCHEMA["$defs"]["ProjectDataWriteArgs"]
    validator = Draft202012Validator(_SCHEMA)
    validator.validate(command("source", {"value": 1}))
    with pytest.raises(Exception):
        validator.validate(
            {**command("source", 1), "args": {**command("source", 1)["args"], "extra": True}}
        )
    assert json.loads(json.dumps(command("source", {"__proto__": 1}), allow_nan=False))
