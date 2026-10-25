"""Validate detached commit values against the installed contract artifacts."""

from __future__ import annotations

import copy
import hashlib
import json
import math
from collections import OrderedDict
from functools import cache, lru_cache
from importlib.resources import files
from threading import RLock
from typing import Protocol, cast

from .errors import ValidationError
from .util import canonical_json


def finite_json(value) -> None:
    active = set()
    parents = []
    children = iter((value,))
    while True:
        for item in children:
            kind = type(item)
            if kind is str or kind is int or kind is bool or item is None:
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
            # Keep only container frames; scalar children need no pending tuples.
            parents.append((item, children))
            # Capture sibling references when entering a container, matching
            # the eager pending stack without allocating one tuple per child.
            children = reversed(tuple(item.values() if kind is dict else item))
            break
        else:
            if not parents:
                return
            parent, children = parents.pop()
            active.remove(id(parent))


def detached(value):
    finite_json(value)
    return copy.deepcopy(value)


def digest(value):
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()


class _ValidatorWithResolver(Protocol):
    _resolver: object


def _validator_resolver(validator):
    return cast(_ValidatorWithResolver, validator)._resolver


@cache
def _load_schema_resources():
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
        resource = Resource.from_contents(
            copy.deepcopy(schema), default_specification=DRAFT202012
        )
        registry = registry.with_resource(uri, resource)
        if resource.id() is not None:
            registry = registry.with_resource(resource.id(), resource)
    return bundle, registry


_schema_source_digest = None


def _schema_resources():
    global _schema_source_digest
    source = (
        files("runtime_protocol")
        .joinpath("schemas/timeline-commit-bundle.json")
        .read_bytes()
    )
    source_digest = hashlib.sha256(source).digest()
    if source_digest != _schema_source_digest:
        _load_schema_resources.cache_clear()
        _schema_source_digest = source_digest
    return _load_schema_resources()


_schema_resources.cache_clear = _load_schema_resources.cache_clear  # type: ignore[attr-defined]


@cache
def _validator_for_bundle(definition: str, bundle_digest: str):
    from jsonschema import Draft202012Validator

    bundle, registry = _schema_resources()
    if definition not in bundle["resources"][bundle["root"]]["$defs"]:
        raise ValidationError("unknown commit schema definition")
    validator = _reuse_schema_validators(Draft202012Validator)(
        {"$ref": bundle["root"] + "#/$defs/" + definition}, registry=registry
    )
    return validator.evolve(
        _resolver=_reuse_schema_resolution(_validator_resolver(validator))
    )


def _active_schema_bundle():
    bundle, registry = _schema_resources()
    return bundle, registry, digest(bundle)


def _validator(definition: str):
    _, _, bundle_digest = _active_schema_bundle()
    return _validator_for_bundle(definition, bundle_digest)


def _reuse_schema_validators(base):
    from threading import RLock

    from jsonschema.validators import extend

    validator = extend(base)
    evolve = validator.evolve
    compiled = OrderedDict()
    lock = RLock()

    def reuse(self, **changes):
        if len(changes) != 2 or "schema" not in changes or "_resolver" not in changes:
            return evolve(self, **changes)
        schema, resolver = changes["schema"], changes["_resolver"]
        key = (id(self), id(schema), id(resolver))
        entry = compiled.get(key)
        if entry is not None:
            return entry[3]
        with lock:
            child = evolve(self, **changes)
            # Retain all identity-keyed objects until eviction. Only schema setup
            # is reused; validation still traverses each instance with fresh errors.
            compiled[key] = (self, schema, resolver, child)
            if len(compiled) > 256:
                compiled.popitem(last=False)
            return child

    validator.evolve = reuse
    return validator


def _reuse_schema_resolution(resolver):
    # Cache only schema lookups, keyed by the identity of the complete resolver
    # state (including registry, base URI and dynamic scope), never by a value.
    @lru_cache(maxsize=256)
    def lookup(state, ref):
        resolved = state.resolver.lookup(ref)
        return type(resolved)(resolved.contents, Resolver(resolved.resolver))

    class Resolver:
        def __init__(self, resolver):
            self.resolver = resolver

        def lookup(self, ref):
            return lookup(self, ref)

        def in_subresource(self, resource):
            child = self.resolver.in_subresource(resource)
            return self if child is self.resolver else Resolver(child)

        def dynamic_scope(self):
            return self.resolver.dynamic_scope()

    return Resolver(resolver)


_VALIDATION_MEMO_MAXSIZE = 256
_validation_memo: OrderedDict[tuple[str, str, str], None] = OrderedDict()
_validation_memo_lock = RLock()


def clear_validation_memo() -> None:
    """Clear process-local validation successes, primarily for lifecycle tests."""
    with _validation_memo_lock:
        _validation_memo.clear()


def validate_commit_value(value, definition: str) -> None:
    """Raise Runtime ValidationError without changing the submitted JSON value.

    Schema dependencies are loaded only when validation is requested; importing
    this module or the provider ABI requires only the standard library.
    """
    finite_json(value)
    snapshot = copy.deepcopy(value)
    finite_json(snapshot)
    _, _, bundle_digest = _active_schema_bundle()
    value_digest = digest(snapshot)
    memo_key = (bundle_digest, definition, value_digest)
    with _validation_memo_lock:
        if memo_key in _validation_memo:
            _validation_memo.move_to_end(memo_key)
            return

        from jsonschema.exceptions import ValidationError as SchemaValidationError
        from referencing.exceptions import Unresolvable

        try:
            _validator(definition).validate(snapshot)
            if digest(snapshot) != value_digest:
                raise ValidationError("commit value changed during validation")
        except SchemaValidationError as exc:
            raise ValidationError(f"invalid {definition}: {exc.message}") from exc
        except (Unresolvable, RecursionError) as exc:
            raise ValidationError(
                f"cannot validate {definition} against the installed contract"
            ) from exc
        _validation_memo[memo_key] = None
        _validation_memo.move_to_end(memo_key)
        while len(_validation_memo) > _VALIDATION_MEMO_MAXSIZE:
            _validation_memo.popitem(last=False)
