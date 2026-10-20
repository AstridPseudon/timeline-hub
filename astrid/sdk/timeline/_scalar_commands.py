"""Scoped literal scalar edits, using the native recorder for every write."""
from __future__ import annotations

import copy
import re

from jsonschema import Draft202012Validator
from referencing import Registry
from referencing.exceptions import Unresolvable

from ._command_state import CommandError


def _target(ctx, command, kind):
    ref = command['select']
    if not isinstance(ref, str) or not re.fullmatch(
            rf'(?:parent|occurrence:[^/]+)/{kind}:[^/]+', ref) or '::' in ref:
        raise CommandError(f"{command['op']} requires a parent or occurrence {kind} identity")
    owner = ref.rsplit('/', 1)[0]
    if ctx.read(ref, ['id']) is None:
        raise CommandError('scalar target disappeared', kind='identity_conflict', ref=ref)
    pin = {'parent': copy.deepcopy(ctx.state.bundle.get('base_parent', {}))}
    if owner != 'parent':
        ctx.read(owner, ['occurrence_id'])
        ctx.read(owner + '/shot', ['shot_id'])
        shot = ctx.state.occurrence(owner)['shot_id']
        pin['source'] = copy.deepcopy(ctx.state.bundle['source_mapping']['shots'][shot])
        ctx.bind('scalar.owner', owner)
    ctx.dependency('scalar.images', 'entity', pin)
    ctx.bind('scalar.target', ref, dependencies=['scalar.images'])
    return ref


def _changes(command):
    values, clear = command['args']['values'], command['args']['clear']
    if any(not isinstance(key, str) for key in values):
        raise CommandError('parameter keys must be JSON strings')
    if set(values).intersection(clear):
        raise CommandError('a scalar key cannot be both set and cleared')
    return values, clear


def track_set(ctx, command):
    ref = _target(ctx, command, 'track')
    values, clear = _changes(command)
    for key in sorted(values):
        ctx.write(ref, [key], values[key])
    for key in sorted(clear):
        ctx.clear(ref, [key])


def clip_set_params(ctx, command):
    from astrid.sdk.timeline_address import element_schema

    ref = _target(ctx, command, 'clip')
    values, clear = _changes(command)
    identity = {key: ctx.read(ref, [key]) for key in (
        'clipType', 'clip_type', 'asset', 'asset_id', 'media_id', 'object_id',
        'elementRef', 'element_ref')}
    # A type/asset label can stay fixed while its exact element or media changes.
    # Match main's selector precedence; retain literal tagged reads, not a digest
    # of the entire registry (unrelated assets can still change independently).
    selector = next((key for key in ('asset', 'asset_id', 'media_id', 'object_id')
                     if key in ctx.state.entity(ref)), None)
    if selector in ('asset', 'asset_id') and isinstance(identity[selector], str):
        registry_ref = ref.rsplit('/', 1)[0] + '/registry'
        for key in ('media_id', 'object_id', 'digest', 'content_digest'):
            ctx.read(registry_ref, ['assets', identity[selector], key])
    element = identity['clipType'] or identity['clip_type'] or 'media'
    if not isinstance(element, str):
        raise CommandError('clip type must be a string', ref=ref)
    # These are stored JSON values, not human expressions or canvas-unit input.
    # Reuse the element's declared value schemas without parsing or coercion.
    _validate_param_values(ref, values, element_schema(element))
    ctx.object(ref, ['params'])
    for key in sorted(values):
        ctx.write(ref, ['params', key], values[key])
    for key in sorted(clear):
        ctx.clear(ref, ['params', key])


def _validate_param_values(ref, values, schema):
    """Check only changed known properties, preserving literal opaque values."""
    properties = schema.get('properties', {})
    validator = Draft202012Validator(schema, registry=Registry())
    for key, value in values.items():
        if key in properties:
            try:
                errors = list(validator.evolve(schema=properties[key]).iter_errors(value))
            except Unresolvable as exc:
                raise CommandError('parameter schema reference is unavailable', ref=ref,
                                   path=['params', key]) from exc
            if errors:
                raise CommandError(errors[0].message, ref=ref, path=['params', key])


def capture_track_set(bundle, select, *, values=None, clear=()):
    return _capture(bundle, 'track.set', select, values, clear)


def capture_clip_set_params(bundle, select, *, values=None, clear=()):
    return _capture(bundle, 'clip.set-params', select, values, clear)


def _capture(bundle, op, select, values, clear):
    from .commands import execute

    return execute(bundle, [{'schema_version': 1, 'op': op, 'version': '1',
                             'select': select, 'args': {'values': copy.deepcopy({} if values is None else values),
                                                       'clear': list(clear)}}]).commands[0]
