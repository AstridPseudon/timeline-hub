#!/usr/bin/env python3
"""Small external consumer probe for the normal private 357/613 client.

This loads generated files by path and deliberately checks the published
surface separately from the internal source-bound DTO module.  It does not
start a provider or write candidate artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import sys
import types
import typing
from pathlib import Path
from types import ModuleType
from typing import Any, Literal, get_args, get_origin, get_type_hints


SOURCE_COMMIT = "357230816c86da65d5f8cc92b10a3a90d29874e0"
SOURCE_SCHEMA_SHA256 = "613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3"
EXPECTED_SOURCE_DEFS = 55
EXPECTED_OLD_PUBLIC_FLOORS = {
    "runtime-0.2.2.json": "460e61c70702f1f6bfa5cd033c8da859c913c3c8839f2a5b928df7691e08a388",
    "runtime-0.2.3.json": "472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9",
    "runtime-0.2.10.json": "472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9",
}
NEW_PUBLIC_ARGS = {
    "AssembledTargetArgs",
    "ClipAddMediaArgs",
    "ClipAnchorArgs",
    "OccurrenceCreateArgs",
    "TextBindingSetArgs",
    "TimelineInitArgs",
    "WordAnchor",
}
OPEN_AUTHORED_DEFS = {
    "ParentComposition",
    "ShotPayload",
    "TimelineConfig",
    "RawTimelinePayload",
    "Document",
}


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load generated module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def source_schema(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == SOURCE_SCHEMA_SHA256, (
        f"source schema is not Agent {SOURCE_COMMIT}: {digest}"
    )
    value = json.loads(raw)
    defs = value.get("$defs")
    assert isinstance(defs, dict) and len(defs) == EXPECTED_SOURCE_DEFS
    return value, defs


def resolve(annotation: Any, module: ModuleType) -> Any:
    """Resolve generated ForwardRefs in the generated module namespace."""

    return typing._eval_type(annotation, vars(module), vars(module), set())


def leaves(annotation: Any, module: ModuleType) -> list[Any]:
    annotation = resolve(annotation, module)
    origin = get_origin(annotation)
    if origin in (typing.Union, types.UnionType):
        result: list[Any] = []
        for member in get_args(annotation):
            result.extend(leaves(member, module))
        return result
    return [annotation]


def literal_value(annotation: Any) -> Any:
    if get_origin(annotation) is Literal:
        values = get_args(annotation)
        assert len(values) == 1, f"expected one discriminant value: {annotation!r}"
        return values[0]
    return None


def assert_closed_command_union(module: ModuleType) -> None:
    pairs: set[tuple[Any, Any]] = set()
    for leaf in leaves(module.EditCommand, module):
        leaf_hints = get_type_hints(leaf, vars(module))
        op = literal_value(leaf_hints.get("op"))
        version = literal_value(leaf_hints.get("version"))
        if op is not None and version is not None:
            pairs.add((op, version))

    assert len(pairs) > 1, (
        "EditCommand is still an open op string rather than a closed union"
    )
    assert ("clip.move", "2") in pairs, "clip.move v2 is missing"
    assert ("clip.move", "3") not in pairs, "unsupported clip.move version is typed"
    assert ("producer.guard", "2") not in pairs, "producer.guard v2 is typed"
    assert ("producer.guard", "1") in pairs, "producer.guard v1 disappeared"


def assert_source_definitions(module: ModuleType, defs: dict[str, Any]) -> None:
    missing = sorted(name for name in defs if not hasattr(module, name))
    assert not missing, f"generated Python DTOs omit source definitions: {missing}"

    # These are authored payloads whose schemas intentionally preserve unknown
    # JSON.  Their Any is not a failed closed-field generation.
    for name in OPEN_AUTHORED_DEFS:
        annotation = getattr(module, name)
        assert get_origin(annotation) is dict
        assert get_args(annotation)[1] is Any, f"{name} stopped being open JSON"

    # Check representative closed fields without rejecting the legitimate open
    # payloads above (or MutationReceipt.result, which is also opaque data).
    assert get_type_hints(module.ClipMoveArgs, vars(module))["on"] is float
    assert get_type_hints(module.WordAnchor, vars(module))["source"] is str
    assert get_args(get_type_hints(module.AgentRead, vars(module))["path"]) == (str,)
    assert get_type_hints(module.ProducerGuardArgs, vars(module))["pin"] is module.ProducerAttemptPin


def empty_intent_pairs(schema: dict[str, Any]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for clause in schema["$defs"]["EditCommand"]["allOf"]:
        op = clause["if"]["properties"]["op"]["const"]
        for branch in clause["then"].get("anyOf", [clause["then"]]):
            intent = branch.get("properties", {}).get("intent")
            if isinstance(intent, dict) and intent.get("type") == "object" and not intent.get("properties"):
                version = branch.get("properties", {}).get("version", {}).get("const")
                if isinstance(version, str):
                    pairs.add((op, version))
    return pairs


def assert_empty_intents_are_closed(module: ModuleType, schema: dict[str, Any]) -> None:
    failures: list[str] = []
    expected = empty_intent_pairs(schema)
    for leaf in leaves(module.EditCommand, module):
        hints = get_type_hints(leaf, vars(module))
        pair = (literal_value(hints.get("op")), literal_value(hints.get("version")))
        if pair not in expected:
            continue
        intent = hints.get("intent")
        if not isinstance(intent, type) or getattr(intent, "__annotations__", None) != {}:
            failures.append(f"{pair[0]} v{pair[1]}")
    assert not failures, "closed empty operation intents became open dict[str, Any]: " + ", ".join(failures)


def assert_public_exports(package: ModuleType) -> None:
    missing = sorted(name for name in NEW_PUBLIC_ARGS if not hasattr(package, name))
    assert not missing, f"Python package root omits new public exports: {missing}"
    exported = set(getattr(package, "__all__", ()))
    assert NEW_PUBLIC_ARGS <= exported, "new public exports are not in __all__"


def assert_receipt_alias(candidate: ModuleType, main: ModuleType) -> None:
    assert candidate.MutationReceipt.__annotations__ == main.MutationReceipt.__annotations__
    sequence = get_type_hints(candidate.MutationReceipt, vars(candidate))["project_seq"]
    assert get_origin(sequence) is list and get_args(sequence) == (int,), (
        f"MutationReceipt.project_seq no longer matches Main list[int]: {sequence!r}"
    )


def assert_old_public_provenance(root: Path) -> None:
    for filename, expected in EXPECTED_OLD_PUBLIC_FLOORS.items():
        path = root / "tests/fixtures/published-command-schemas" / filename
        assert path.is_file(), f"old public v1 schema floor missing: {path}"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == expected, f"old public v1 floor changed: {filename}"
    openapi = (root / "contract/openapi/workspace-v1.yaml").read_text()
    assert "project_seq: { type: array, minItems: 2, maxItems: 2" in openapi
    timeline = json.loads((root / "contract/schemas/timeline-commit.json").read_text())
    assert timeline["$defs"]["MutationReceipt"]["$ref"].endswith(
        "CommittedMutation/properties/receipt"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("source_schema", type=Path)
    args = parser.parse_args()
    schema, defs = source_schema(args.source_schema)
    generated = load_module(
        args.candidate / "packages/python/astrid_runtime_client/timeline_commit_types.py",
        "private613_generated_types",
    )
    main_types = load_module(
        args.candidate / "runtime_protocol/timeline_commit_types.py",
        "private613_main_types",
    )
    sys.path.insert(0, str(args.candidate / "packages/python"))
    package = importlib.import_module("astrid_runtime_client")

    checks = [
        ("closed command discriminants", lambda: assert_closed_command_union(generated)),
        ("55 source definitions and closed fields", lambda: assert_source_definitions(generated, defs)),
        ("public Args and WordAnchor exports", lambda: assert_public_exports(package)),
        ("Main MutationReceipt alias and list sequence", lambda: assert_receipt_alias(generated, main_types)),
        ("closed empty operation intents", lambda: assert_empty_intents_are_closed(generated, schema)),
        ("old public provenance", lambda: assert_old_public_provenance(args.candidate)),
    ]
    failures = []
    for name, check in checks:
        try:
            check()
        except AssertionError as error:
            failures.append((name, str(error)))
            print(f"FAIL [{name}]: {error}")
        else:
            print(f"PASS [{name}]")
    if failures:
        raise SystemExit(1)
    print("private 357/613 corrected Python consumer probe: PASS")


if __name__ == "__main__":
    main()
