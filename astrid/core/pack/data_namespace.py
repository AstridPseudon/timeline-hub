"""Lossless detached owner-data codec; never a timeline persistence path.

Callers must adopt results through admitted semantic EditCommands. This codec
cannot grant a generic owner property command the right to alter transcript,
Astrid semantics, tracks, identity, or derived timing.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping

import jsonschema

from .canonical import _freeze
from .document_access import canonical, check_document_source, owner_namespace, plain


class OwnerData:
    def __init__(self, entry):
        check_document_source(entry)
        self._entry = entry
        self._declaration = entry.definition.extensions.get("data_namespace")
        if self._declaration is None:
            raise ValueError("owner namespace is undeclared")
        if self.owner != self._declaration["owner"]:
            raise ValueError("owner namespace differs from admitted manifest identity")

    @property
    def owner(self):
        return owner_namespace(self._entry.id)

    def read(self, carrier):
        """Immutable opaque read. Foreign/malformed data is never normalized."""
        app = carrier.get("app") if isinstance(carrier, Mapping) else None
        return _freeze(copy.deepcopy(app.get(self.owner))) if isinstance(app, Mapping) else None

    def _change(self, carrier, namespace, key, value, *, clear):
        check_document_source(self._entry)
        ns = self._declaration
        if namespace != self.owner or key not in ns["writable"]:
            raise ValueError("write is outside declared owner properties")
        if ns["version"] != 1:
            raise ValueError("unsupported owner namespace version")
        if not isinstance(carrier, dict):
            raise ValueError("malformed carrier")
        if "app" in carrier and not isinstance(carrier["app"], dict):
            raise ValueError("malformed app carrier is opaque")
        app = carrier.get("app", {})
        if clear and self.owner not in app:
            return copy.deepcopy(carrier)
        current = app.get(self.owner, {"v": ns["version"]})
        if (
            not isinstance(current, dict)
            or type(current.get("v")) is not int
            or current["v"] != ns["version"]
        ):
            raise ValueError("malformed or unsupported owner namespace is opaque")
        # Presence-aware whole-property edits make arrays atomic. No index intent.
        next_value = copy.deepcopy(current)
        if clear:
            next_value.pop(key, None)
        else:
            next_value[key] = copy.deepcopy(value)
        canonical(next_value)
        schema = plain(ns["schema"])
        # Validate declared properties without interpreting foreign/unknown keys.
        # The owner schema must explicitly allow those opaque keys.
        jsonschema.Draft202012Validator(schema).validate(next_value)
        result = copy.deepcopy(carrier)
        result.setdefault("app", {})[self.owner] = next_value
        return result

    def set(self, carrier, namespace, key, value):
        return self._change(carrier, namespace, key, value, clear=False)

    def clear(self, carrier, namespace, key):
        """Remove presence; None and clear-shaped objects remain literal values."""
        return self._change(carrier, namespace, key, None, clear=True)
