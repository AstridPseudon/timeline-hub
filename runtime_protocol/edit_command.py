"""Generated from Astrid OpCall; no timing or edit execution."""
from typing import Any, Mapping
OPCALL_SCHEMA = {'$schema': 'https://json-schema.org/draft/2020-12/schema', '$id': 'https://astrid.local/schemas/change-contract/opcall.schema.json', 'title': 'OpCall', 'description': 'Candidate single EditCommand envelope (SDK executable name: EditCommand). D RUNNER emits canonical OpCalls in Plan.calls and journal calls. Handler ids remain open. This increment is not a schema freeze.', 'type': 'object', 'required': ['op', 'select', 'args'], 'additionalProperties': False, '$defs': {'scopedId': {'type': 'string', 'description': 'Current ScopedId vocabulary: parent, shot, or occurrence clip/track ids, plus cut ids.', 'pattern': '^(?:(?:parent|shot:[^/]+|occurrence:[^/]+)/(?:clip|track):[^/]+|cut:[^/:]+)$'}, 'anchorIdentity': {'description': 'Current resolved anchor identities, including scoped entity ids and the documented word, beat, and cut anchors.', 'oneOf': [{'$ref': '#/$defs/scopedId'}, {'type': 'string', 'pattern': '^(?:word:[^:]+:[0-9]+|beat:[0-9]+|cut:[^/:]+:(?:start|end))$'}]}}, 'properties': {'op': {'type': 'string', 'description': 'Qualified operation id, e.g. timeline.opacity or myteam.stagger.', 'pattern': '^[a-z][a-z0-9_-]*(\\.[a-z][a-z0-9_-]*)+$'}, 'select': {'type': ['string', 'null'], 'description': 'Authoring selector; executed calls use the canonical stable selector resolved by the runner. null for timeline-level operations.'}, 'args': {'type': 'object', 'description': 'Opaque finite JSON operation arguments in authoring units. Omitted keys, JSON null, explicit clip.clear keys, and ordinary objects (including {$absent:true} or {op:clear}) remain distinct. Only the selected handler interprets these values.', 'additionalProperties': True}, 'expect': {'type': 'object', 'description': 'Optional prior values keyed by direct-write path. Absence and present JSON values are tagged separately; command-specific requirements remain producer/consumer rules.', 'additionalProperties': {'oneOf': [{'type': 'object', 'required': ['state'], 'properties': {'state': {'const': 'absent'}}, 'additionalProperties': False}, {'type': 'object', 'required': ['state', 'value'], 'properties': {'state': {'const': 'present'}, 'value': {}}, 'additionalProperties': False}]}}, 'bindings': {'type': 'object', 'description': 'Runner-resolved anchor identity keyed by the exact authored TimeRef text.', 'additionalProperties': {'$ref': '#/$defs/anchorIdentity'}}, 'created': {'type': 'array', 'description': 'Scoped IDs allocated by the runner for this call.', 'items': {'$ref': '#/$defs/scopedId'}}, 'authorship': {'type': 'object', 'description': 'Per-write-path authorship classification; it carries no actor or authentication claim.', 'additionalProperties': {'enum': ['direct', 'consequence']}}, 'version': {'type': ['string', 'null'], 'description': 'The tool version when it ran (filled by the runner).'}, 'resolved': {'type': 'array', 'description': 'Runner-populated IDs of the selected targets in the current ScopedId vocabulary.', 'items': {'$ref': '#/$defs/scopedId'}, 'default': []}}}

def validate_edit_command(value: Any) -> Mapping[str, Any]:
    """Validate only the OpCall envelope; return the exact unmodified value."""
    import math
    import re
    def finite_json(item):
        if item is None or isinstance(item, (str, bool, int)):
            return True
        if isinstance(item, float):
            return math.isfinite(item)
        if isinstance(item, list):
            return all(finite_json(v) for v in item)
        if isinstance(item, dict):
            return all(isinstance(k, str) and finite_json(v) for k, v in item.items())
        return False
    if not isinstance(value, dict):
        raise ValueError("OpCall must be an object")
    fields = OPCALL_SCHEMA["properties"]
    if set(value) - set(fields) or not set(OPCALL_SCHEMA["required"]) <= set(value):
        raise ValueError("OpCall missing or unknown field")
    try:
        valid_json = finite_json(value)
    except RecursionError:
        valid_json = False
    if not valid_json:
        raise ValueError("OpCall requires finite JSON values")
    types = {"string": lambda v: isinstance(v, str), "null": lambda v: v is None,
             "object": lambda v: isinstance(v, dict), "array": lambda v: isinstance(v, list)}
    def matches(node, item):
        if "$ref" in node:
            return matches(OPCALL_SCHEMA["$defs"][node["$ref"].rsplit("/", 1)[-1]], item)
        if "oneOf" in node and sum(matches(branch, item) for branch in node["oneOf"]) != 1:
            return False
        if "const" in node and item != node["const"]:
            return False
        if "enum" in node and item not in node["enum"]:
            return False
        if "type" in node:
            kinds = node["type"] if isinstance(node["type"], list) else [node["type"]]
            if not any(types[kind](item) for kind in kinds):
                return False
        if isinstance(item, str) and "pattern" in node and re.search(node["pattern"], item) is None:
            return False
        if isinstance(item, list) and "items" in node and not all(matches(node["items"], v) for v in item):
            return False
        if isinstance(item, dict):
            fields = node.get("properties", {})
            if not set(node.get("required", [])) <= set(item):
                return False
            for key, child in item.items():
                if key in fields:
                    if not matches(fields[key], child):
                        return False
                else:
                    extra = node.get("additionalProperties", True)
                    if extra is False or (isinstance(extra, dict) and not matches(extra, child)):
                        return False
        return True
    if not matches(OPCALL_SCHEMA, value):
        raise ValueError("OpCall invalid envelope")
    return value


def validate_edit_command_bytes(raw: bytes) -> bytes:
    """Validate without reserializing: whitespace, key order and UTF-8 survive."""
    import json
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON field: " + key)
            result[key] = value
        return result
    validate_edit_command(json.loads(raw, object_pairs_hook=unique_object))
    return raw
