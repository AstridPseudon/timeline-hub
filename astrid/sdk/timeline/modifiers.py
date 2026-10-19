"""Instance-addressed clip fields consumed by the existing setters and runner.

Wire clips retain their ordered list. Semantic paths use modifiers["instance"]
and modifiers.order; numeric array positions are deliberately not accepted.
"""
from __future__ import annotations

import copy
import json
import math
import re

import jsonschema

from astrid.sdk.timeline._common import TimelineEditError

_INSTANCE = re.compile(r'^modifiers\[("(?:[^"\\]|\\.)*")\](.*)$')


def handles(path):
    return path == 'modifiers' or path.startswith(('modifiers.', 'modifiers['))


def address(path):
    match = _INSTANCE.fullmatch(path)
    if not match or not json.loads(match[1]):
        raise TimelineEditError('use modifiers["instance-id"] or modifiers.order; array position is not identity')
    suffix = match[2]
    if suffix and not re.fullmatch(r'\.params(?:\.[A-Za-z_][\w-]*|\[\d+\])*', suffix):
        raise TimelineEditError('a modifier edit addresses its instance or params property path')
    return json.loads(match[1]), suffix


def parameter_address(mid, leaf):
    return 'modifiers[' + json.dumps(mid) + '].params.' + leaf


def keyframe_address(path):
    """Only the reserved stable-ID domain; all legacy parameter names are opaque."""
    if not handles(path):
        return None
    try:
        mid, suffix = address(path)
    except (ValueError, TypeError) as exc:
        raise TimelineEditError(f'invalid modifier keyframe address: {path}') from exc
    if (not re.fullmatch(r'\.params\.[A-Za-z_][\w-]*', suffix)
            or not mid.strip() or parameter_address(mid, suffix[8:]) != path):
        raise TimelineEditError(f'noncanonical modifier parameter address: {path}')
    return mid, suffix[8:]


def _binding(row):
    if not row['element'].startswith('timeline.component/'):
        raise TimelineEditError('animated modifier requires an admitted timeline.component descriptor')
    from astrid.core.pack.components import component_reference_binding
    return component_reference_binding(row)


def _numeric_leaf(schema, leaf):
    allowed = {'type', 'properties', 'required', 'additionalProperties', '$schema', '$id',
               'title', 'description', 'default', 'examples'}
    if (not isinstance(schema, dict) or schema.get('type') != 'object'
            or not isinstance(schema.get('properties'), dict) or set(schema) - allowed
            or ('additionalProperties' in schema and not isinstance(schema['additionalProperties'], bool))):
        raise TimelineEditError('animated modifier requires an independently constrained object descriptor')
    definition = schema['properties'].get(leaf)
    if definition is None:
        raise TimelineEditError(f'undeclared modifier parameter: {leaf}')
    number_keys = {'type', 'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum',
                   'title', 'description', 'default', 'examples'}
    if (not isinstance(definition, dict) or definition.get('type') != 'number' or set(definition) - number_keys):
        raise TimelineEditError(f'unsupported animated modifier parameter: {leaf}')


def validate_keyframes(data, keyframes):
    """Admit reserved channels; no sampling or legacy filtering lives in Python."""
    if not isinstance(keyframes, dict):
        return {}  # historical absent/null maps remain restorable by inverse
    by_id = None
    dependencies = {}
    bindings = {}
    for path, keys in keyframes.items():
        parsed = keyframe_address(path)
        if parsed is None:
            continue
        mid, leaf = parsed
        if by_id is None:
            by_id = instances(data)
        if mid not in by_id:
            raise TimelineEditError(f'unknown modifier instance: {mid}')
        row = by_id[mid]
        if row['element'] not in bindings:
            bindings[row['element']] = _binding(row)
        binding = bindings[row['element']]
        schema = binding['descriptor']['params']
        _numeric_leaf(schema, leaf)
        validator = jsonschema.Draft202012Validator(schema)
        try:
            validator.validate(row['params'])
        except jsonschema.ValidationError as exc:
            raise TimelineEditError(f'invalid static modifier params: {exc.message}') from None
        if not isinstance(keys, list):
            raise TimelineEditError(f'modifier keyframe channel must be an array: {path}')
        from astrid.core.timeline.motion_curves import motion_curve_name
        for key in keys:
            if (not isinstance(key, dict) or type(key.get('time')) not in {int, float}
                    or not math.isfinite(key['time']) or type(key.get('value')) not in {int, float}
                    or not math.isfinite(key['value']) or key.get('interpolation') not in {'linear', 'hold'}
                    or ('easing' in key and not isinstance(key['easing'], str))):
                raise TimelineEditError(f'malformed numeric modifier keyframe: {path}')
            if 'easing' in key:
                motion_curve_name(key['easing'])
            try:
                validator.validate({**row['params'], leaf: key['value']})
            except jsonschema.ValidationError as exc:
                raise TimelineEditError(f'invalid modifier key value: {exc.message}') from None
        dependencies['modifiers[' + json.dumps(mid) + ']'] = copy.deepcopy(row)
        dependencies['modifierDeclarations[' + json.dumps(row['element']) + ']'] = binding
    return dependencies


def declaration_state(data, path):
    match = re.fullmatch(r'modifierDeclarations\[("(?:[^"\\]|\\.)*")\]', path)
    if not match:
        return None
    from astrid.core.pack.components import component_declaration_binding
    return dict(state='present', value=component_declaration_binding(json.loads(match[1])))


def instances(data):
    rows = data.get('modifiers', [])
    if not isinstance(rows, list):
        raise TimelineEditError('modifiers must be an ordered list')
    result = {}
    for row in rows:
        if (not isinstance(row, dict) or set(row) != {'id', 'element', 'params'}
                or not isinstance(row['id'], str) or not row['id'].strip()
                or not isinstance(row['element'], str) or not isinstance(row['params'], dict)):
            raise TimelineEditError('a modifier requires exactly id, element and object params')
        if row['id'] in result:
            raise TimelineEditError(f'duplicate modifier instance {row["id"]!r}')
        result[row['id']] = row
    return result


def validate(row):
    if row['element'].startswith('timeline.component/'):
        from astrid.core.pack.components import validate_component_reference
        validate_component_reference(row)
        return
    # Read declarations through the existing catalog. No component code or I/O
    # implementation is loaded. Unknown/unavailable declarations fail closed.
    from astrid.core.element.catalog import read_element_meta, read_element_schema
    from astrid.core.pack import qualified_id_pack_id
    try:
        qualified_id_pack_id(row['element'])
        schema = read_element_schema(row['element'], kind='components')
        meta = read_element_meta(row['element'], kind='components')
        # Same declaration fields as I's admitted ModifierDeclaration; the
        # catalog supplies data only, never a second renderer/implementation.
        if meta.get('kind') != 'modifier' or meta.get('element') != row['element']:
            raise ValueError('modifier declaration identity/subtype mismatch')
        if any(meta.get(field) != 'preserve' for field in ('bounds', 'alpha', 'support')):
            raise ValueError('modifier declaration must preserve bounds, alpha and support')
        if not isinstance(meta.get('hosts'), list) or not meta['hosts']:
            raise ValueError('modifier declaration must name its supported hosts')
        jsonschema.Draft202012Validator(schema).validate(row['params'])
    except (KeyError, ValueError, jsonschema.ValidationError) as exc:
        raise TimelineEditError(f'{row["element"]}: invalid modifier: {exc}') from None


def set_value(clip, path, value):
    from astrid.sdk.timeline.commands import _path_state
    from astrid.sdk.timeline.doc import _set_path
    if clip.is_audio:
        raise TimelineEditError('modifiers require a clip visual subtree')
    rows = copy.deepcopy(clip.data.get('modifiers', []))
    by_id = instances({'modifiers': rows})
    if path == 'modifiers.order':
        if (not isinstance(value, list) or any(not isinstance(x, str) for x in value)
                or len(value) != len(by_id) or set(value) != set(by_id)):
            raise TimelineEditError('modifier order must contain each existing instance ID exactly once')
        rows = [by_id[key] for key in value]
    else:
        mid, suffix = address(path)
        if not suffix:
            row = copy.deepcopy(value)
            instances({'modifiers': [row]})
            if row['id'] != mid:
                raise TimelineEditError('modifier path and instance ID must agree')
            if mid in by_id:
                rows[rows.index(by_id[mid])] = row
            else:
                rows.append(row)
        else:
            if mid not in by_id:
                raise TimelineEditError(f'missing modifier instance {mid!r}')
            row = by_id[mid]
            # Validate the complete result; nested values never bypass schema.
            _path_state(row, suffix[1:])  # grammar validation before mutation
            try:
                _set_path(row, suffix[1:], copy.deepcopy(value))
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                raise TimelineEditError(f'invalid modifier property path: {exc}') from None
        validate(row)
    try:
        validate_keyframes({**clip.data, 'modifiers': rows}, clip.data.get('keyframes'))
    except TimelineEditError as exc:
        raise TimelineEditError(f'{exc}; clear incompatible curves with the clip.set keyframes/keyframeOrigin pair before replacing the modifier') from None
    clip.data['modifiers'] = rows
    return clip


def clear_value(clip, path):
    mid, suffix = address(path)
    if suffix:
        raise TimelineEditError('clear a modifier by its instance ID')
    by_id = instances(clip.data)
    if mid in by_id:
        keys = clip.data.get('keyframes')
        if isinstance(keys, dict):
            clip.data['keyframes'] = {key: value for key, value in keys.items()
                                      if (keyframe_address(key) or (None,))[0] != mid}
        clip.data['modifiers'] = [row for row in clip.data['modifiers'] if row['id'] != mid]
    return clip


def paths(before, after):
    """Diff list contents by ID; order is an independent authored property."""
    left, right = instances({'modifiers': before}), instances({'modifiers': after})
    yield 'modifiers.order', list(left), list(right)
    for mid in sorted(set(left) | set(right)):
        yield 'modifiers[' + json.dumps(mid) + ']', left.get(mid), right.get(mid)
