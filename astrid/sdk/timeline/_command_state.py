"""Canonical addresses and tagged authored state for the command recorder."""
from __future__ import annotations

import copy
import json
import re

from ._common import TimelineEditError

ABSENT = {"state": "absent"}


class CommandError(TimelineEditError):
    def __init__(self, message, *, kind="invalid_edit_command", ref="parent", path=(),
                 base=None, theirs=None, ours=None):
        super().__init__(message)
        self.kind, self.ref, self.path = kind, ref, list(path)
        self.base = copy.deepcopy(base or ABSENT)
        self.theirs = copy.deepcopy(theirs or ABSENT)
        self.ours = copy.deepcopy(ours or ABSENT)

    def to_json(self):
        return {"kind": self.kind, "ref": self.ref, "path": self.path,
                "base": self.base, "theirs": self.theirs, "ours": self.ours, "choices": []}


def present(value):
    return {"state": "present", "value": copy.deepcopy(value)}


def equal(a, b):
    """JSON equality, with numeric equivalence but no bool/number coercion."""
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def tokens(path):
    """Parse the legacy property spelling once; quoted punctuation is data."""
    if not isinstance(path, str):
        raise CommandError("property path must be a string")
    result, pos = [], 0
    while pos < len(path):
        if path[pos] == '[':
            if path[pos + 1:pos + 2] == '"':
                try:
                    value, end = json.JSONDecoder().raw_decode(path, pos + 1)
                except ValueError as exc:
                    raise CommandError("invalid quoted property token") from exc
                if end >= len(path) or path[end] != ']':
                    raise CommandError("missing property bracket")
                pos = end + 1
            else:
                match = re.match(r'\[(0|[1-9][0-9]*)\]', path[pos:])
                if not match:
                    raise CommandError("invalid numeric property token")
                value, pos = match[1], pos + match.end()
        else:
            match = re.match(r'[A-Za-z_][\w-]*', path[pos:])
            if not match:
                raise CommandError("invalid property token")
            value, pos = match[0], pos + match.end()
        result.append(value)
        if pos < len(path) and path[pos] == '.':
            pos += 1
            if pos == len(path) or path[pos] == '[':
                raise CommandError("invalid property separator")
        elif pos < len(path) and path[pos] != '[':
            raise CommandError("invalid property separator")
    return tuple(result)


def spelling(path):
    return ''.join((('.' if i else '') + token if re.fullmatch(r'[A-Za-z_][\w-]*', token)
                    else '[' + json.dumps(token, ensure_ascii=False) + ']')
                   for i, token in enumerate(path))


def address(key, resolved):
    # The entity delimiter is outside any quoted JSON property atom.
    quoted, escaped, split = False, False, []
    for i, char in enumerate(key):
        if escaped:
            escaped = False
        elif quoted and char == '\\':
            escaped = True
        elif char == '"':
            quoted = not quoted
        elif not quoted and key[i:i + 2] == '::':
            split.append(i)
    if len(split) > 1:
        raise CommandError("ambiguous entity/property delimiter")
    if split:
        i = split[0]
        return key[:i], tokens(key[i + 2:])
    if len(resolved) != 1:
        raise CommandError("bare property guard needs exactly one target")
    return resolved[0], tokens(key)


def overlaps(a, b):
    return (a == ("timeline", ()) or b == ("timeline", ())
            or (a[0] == b[0] and a[1][:len(b[1])] == b[1][:len(a[1])]))


def one(rows, key, identity, *, optional=False):
    if not isinstance(rows, list):
        raise CommandError("entity collection must be an array")
    matches = [row for row in rows if isinstance(row, dict) and row.get(key) == identity]
    if len(matches) != 1:
        if optional and not matches:
            return None
        raise CommandError(f"missing or ambiguous identity {identity!r}", kind="identity_conflict")
    return matches[0]


class State:
    def __init__(self, bundle, *, closures=None):
        self.bundle = bundle
        self.closures = closures or {}

    def occurrence(self, owner):
        return one(self.bundle["placements"], "occurrence_id", owner.removeprefix("occurrence:"))

    def config(self, owner):
        if owner == "parent":
            return self.bundle["parent"].get("config", {})
        row = self.occurrence(owner)
        return self.bundle["shots"][row["shot_id"]]["internal_timeline"]

    def collection(self, owner, kind):
        config = self.config(owner)
        if owner == "parent" and kind == "clip":
            parent = self.bundle["parent"]
            return parent.get("clips") or config.get("clips", parent.get("clips", []))
        return config.get(kind + "s", [])

    def entity(self, ref, *, optional=False):
        if '/clip:' in ref or '/track:' in ref:
            owner, entity = ref.rsplit('/', 1)
            kind, identity = entity.split(':', 1)
            return one(self.collection(owner, kind), "id", identity, optional=optional)
        if ref == "parent":
            return self.bundle["parent"]
        if ref.endswith('/registry'):
            owner = ref.removesuffix('/registry')
            if owner == "parent":
                from astrid.core.timeline.parent_registry import effective_parent_registry
                return effective_parent_registry(self.bundle["parent"])
            return self.config(owner).get("registry", {})
        if ref.endswith('/source'):
            return self.config(ref.removesuffix('/source'))
        if ref.endswith('/shot'):
            owner = ref.removesuffix('/shot')
            row = self.occurrence(owner)
            source = self.bundle['source_mapping']['shots'][row['shot_id']]['shot_id']
            from astrid.core.timeline.authoring_bundle import _authoring_shot_id
            identity = _authoring_shot_id(
                self.bundle['project_id'], self.bundle['timeline_id'], row['occurrence_id'],
                source, shared=True)
            if row['shot_id'] not in (source, identity):
                raise CommandError('occurrence authoring owner changed', kind='identity_conflict',
                                   ref=owner, path=['shot_id'])
            return {"shot_id": source}
        if ref.startswith("occurrence:") and '/' not in ref:
            return self.occurrence(ref)
        raise CommandError(f"unsupported entity reference {ref!r}")

    def get(self, ref, path):
        if ref == "timeline":
            if path:
                raise CommandError("timeline replacement requires the whole closure")
            from .commit import document_from_bundle
            image = document_from_bundle(self.bundle)['parent_revision']
            return present({key: image[key] for key in ('revision_id', 'content_digest')})
        value = self.entity(ref, optional=True)
        if value is None:
            return copy.deepcopy(ABSENT)
        for key in path:
            if isinstance(value, dict) and key in value:
                value = value[key]
            elif isinstance(value, list) and key.isdecimal() and int(key) < len(value):
                value = value[int(key)]
            else:
                return copy.deepcopy(ABSENT)
        return present(value)

    def matches(self, ref, path, expected):
        actual = self.get(ref, path)
        if equal(actual, expected):
            return True
        if (ref.endswith('/shot') and list(path) == ['shot_id']
                and expected['state'] == actual['state'] == 'present'
                and isinstance(expected.get('value'), str)):
            from astrid.core.timeline.authoring_bundle import _authoring_shot_id
            # The only admitted source change is this occurrence's exact main
            # materialization of the original source, never a prefix heuristic.
            occurrence = self.occurrence(ref.removesuffix('/shot'))
            def materialized(source):
                return _authoring_shot_id(self.bundle['project_id'], self.bundle['timeline_id'],
                                          occurrence['occurrence_id'], source, shared=True)
            return (actual['value'] == materialized(expected['value'])
                    or expected['value'] == occurrence['shot_id'] == materialized(actual['value']))
        return False

    def set(self, ref, path, state):
        if ref == "timeline":
            pin = state.get('value', {})
            target = self.closures.get(pin.get('revision_id'))
            if path or state.get('state') != 'present' or target is None:
                raise CommandError("timeline replacement requires a verified historical closure",
                                   kind='history_unavailable', ref=ref)
            image = target['source_mapping']['_runtime_document']['parent_revision']
            if pin != {key: image[key] for key in ('revision_id', 'content_digest')}:
                raise CommandError("historical closure pin mismatch", ref=ref)
            replacement = copy.deepcopy(target)
            self.bundle.clear()
            self.bundle.update(replacement)
            return
        if not path:
            owner, entity = ref.rsplit('/', 1)
            kind, identity = entity.split(':', 1)
            rows = self.collection(owner, kind)
            existing = self.entity(ref, optional=True)
            if existing is not None:
                index = rows.index(existing)
                if state["state"] == "absent":
                    rows.pop(index)
                else:
                    rows[index] = copy.deepcopy(state["value"])
            elif state["state"] == "present":
                rows.append(copy.deepcopy(state["value"]))
            return
        value = self.entity(ref)
        for key in path[:-1]:
            if not isinstance(value, dict) or key not in value or not isinstance(value[key], dict):
                raise CommandError("write requires recorded container creation", ref=ref, path=path)
            value = value[key]
        if not isinstance(value, dict):
            raise CommandError("property parent must be an object", ref=ref, path=path)
        if state["state"] == "absent":
            value.pop(path[-1], None)
        else:
            value[path[-1]] = copy.deepcopy(state["value"])
