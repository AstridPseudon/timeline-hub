"""Validate detached commit values against the installed contract artifacts."""

from __future__ import annotations

import copy
import hashlib
import json
import math
from functools import cache
from importlib.resources import files

from .errors import ValidationError
from .util import canonical_json


def finite_json(value) -> None:
    active = set()
    pending = [(value, False)]
    while pending:
        item, leaving = pending.pop()
        if leaving:
            active.remove(id(item))
            continue
        kind = type(item)
        if item is None or kind in (str, bool, int):
            continue
        if kind is float and math.isfinite(item):
            continue
        if kind not in (dict, list):
            raise ValidationError("commit value must contain only finite JSON")
        if id(item) in active:
            raise ValidationError("commit value must not contain cycles")
        if kind is dict and any(type(key) is not str for key in item):
            raise ValidationError("commit JSON object keys must be strings")
        active.add(id(item))
        pending.append((item, True))
        pending.extend(
            (child, False) for child in (item.values() if kind is dict else item)
        )


def detached(value):
    finite_json(value)
    return copy.deepcopy(value)


def digest(value):
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()


@cache
def _schema_resources():
    from referencing import Registry, Resource
    from referencing.exceptions import NoSuchResource
    from referencing.jsonschema import DRAFT202012

    def unavailable(uri):
        raise NoSuchResource(ref=uri)

    bundle = json.loads(
        files("runtime_protocol")
        .joinpath("schemas/timeline-commit-bundle.json")
        .read_text(encoding="utf-8")
    )
    registry = Registry(retrieve=unavailable)
    for uri, schema in bundle["resources"].items():
        resource = Resource.from_contents(schema, default_specification=DRAFT202012)
        registry = registry.with_resource(uri, resource)
        if resource.id() is not None:
            registry = registry.with_resource(resource.id(), resource)
    return bundle, registry


@cache
def _validator(definition: str):
    from jsonschema import Draft202012Validator

    bundle, registry = _schema_resources()
    if definition not in bundle["resources"][bundle["root"]]["$defs"]:
        raise ValidationError("unknown commit schema definition")
    return Draft202012Validator(
        {"$ref": bundle["root"] + "#/$defs/" + definition}, registry=registry
    )


def validate_commit_value(value, definition: str) -> None:
    """Raise Runtime ValidationError without changing the submitted JSON value.

    Schema dependencies are loaded only when validation is requested; importing
    this module or the provider ABI requires only the standard library.
    """
    finite_json(value)
    from jsonschema.exceptions import ValidationError as SchemaValidationError
    from referencing.exceptions import Unresolvable

    try:
        _validator(definition).validate(value)
    except SchemaValidationError as exc:
        raise ValidationError(f"invalid {definition}: {exc.message}") from exc
    except (Unresolvable, RecursionError) as exc:
        raise ValidationError(
            f"cannot validate {definition} against the installed contract"
        ) from exc
