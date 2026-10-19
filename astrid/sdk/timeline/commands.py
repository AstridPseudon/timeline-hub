"""Small native EditCommand engine over main's lossless authoring bundle."""
from __future__ import annotations

import copy
import json
from collections.abc import Callable
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from pathlib import Path

from jsonschema import Draft202012Validator

from ._command_state import CommandError, address, equal, spelling
from ._recording import Recording, guard, selection

_SCHEMA = json.loads((Path(__file__).parents[2] / 'core/timeline/schema/edit-command.schema.json').read_text())
_VALIDATOR = Draft202012Validator(_SCHEMA)
TRACK_CREATE_PARAMETERS = {
    'type': 'object', 'required': ['row'], 'additionalProperties': False,
    'properties': {'row': {'type': 'object', 'required': ['id', 'kind'],
                           'properties': {'id': {'type': 'string', 'pattern': '^(?!.*::)[^/]+$'},
                                          'kind': {'type': 'string', 'minLength': 1}}}},
}


@dataclass(frozen=True)
class Operation:
    parameters: dict
    handler: Callable[[Recording, dict], None]
    intent: dict
    singleton: bool = False


def operations():
    """M1 native recipe entries; the full extensible registry belongs to M2."""
    from .capture import MOVE_INTENT, move, track_create
    return {'clip.move': Operation(_SCHEMA['$defs']['ClipMoveArgs'], move, MOVE_INTENT, True),
            'track.create': Operation(TRACK_CREATE_PARAMETERS, track_create, {})}


@dataclass
class Plan:
    bundle: dict
    records: list[dict]
    semantic_events: list[dict] = dataclass_field(default_factory=list)

    @property
    def commands(self):
        return [copy.deepcopy(record['command']) for record in self.records]


def validate_command(command):
    try:
        json.dumps(command, allow_nan=False)
    except (ValueError, TypeError) as exc:
        raise CommandError("command must be finite JSON") from exc
    errors = sorted(_VALIDATOR.iter_errors(command), key=lambda e: str(e.path))
    if errors:
        raise CommandError(errors[0].message)
    if command['version'] != '1':
        raise CommandError("unsupported operation version", kind='unsupported_version')
    if command['op'] not in ('clip.move', 'track.create', 'timeline.inverse'):
        raise CommandError(f"unsupported operation {command['op']!r}", kind='unsupported_operation')
    operation = operations().get(command['op'])
    if operation is not None:
        errors = list(Draft202012Validator(operation.parameters).iter_errors(command['args']))
        if errors:
            raise CommandError(errors[0].message)
    if command['op'] == 'track.create':
        if command['select'] != 'parent' and not (
                isinstance(command['select'], str) and command['select'].startswith('occurrence:')
                and '/' not in command['select']):
            raise CommandError("track.create requires parent or occurrence owner")
        if command.get('intent', {}) != {}:
            raise CommandError("track.create has no intention overrides")


def _normalize(command):
    command = copy.deepcopy(command)
    validate_command(command)
    resolved = command.get('resolved', [command['select']] if command['op'] == 'clip.move' else [])
    for field in ('expect', 'authorship'):
        if field not in command:
            continue
        normalized = {}
        for key, value in command[field].items():
            ref, path = address(key, resolved)
            canonical = ref + '::' + spelling(path)
            if canonical in normalized and not equal(normalized[canonical], value):
                raise CommandError("inconsistent equivalent property guards", ref=ref, path=path)
            normalized[canonical] = value
        command[field] = normalized
    return command


def _verify_claims(ctx, command):
    for ref in command.get('created', []):
        if ctx.state.entity(ref, optional=True) is not None:
            raise CommandError('created identity is occupied', kind='identity_collision', ref=ref)
    for key, expected in command.get('expect', {}).items():
        ref, path = address(key, command.get('resolved', []))
        guard(ctx.state, ref, path, expected)
    for read in command.get('reads', []):
        guard(ctx.state, read['ref'], read['path'], read['state'])
    for selected in command.get('selections', []):
        actual = selection(ctx.state, selected['key'], selected['owner'], selected['members'])
        if not equal(actual, selected):
            raise CommandError("original selection membership/order changed", kind='selection_changed', ref=selected['owner'])


def execute(bundle, commands, *, inverse_records=(), intervening_records=(), id_map=None):
    """Execute atomically. History inputs must already be authenticated by provider.

    Empty intervening_records means proven empty ancestry, never unavailable
    history. Incoming recorder fields are checked claims; generated records are
    the authority. No persistence, mutable reads or renderer lives here.
    """
    from .inverse import apply_inverse

    if not commands:
        raise CommandError("command batch must not be empty")
    if id_map and any(key != value for key, value in id_map.items()):
        raise CommandError("id_map must contain identity pairs only", kind='identity_collision')
    candidate, records, events = copy.deepcopy(bundle), [], []
    for ordinal, supplied in enumerate(commands):
        command = _normalize(supplied)
        ctx = Recording(candidate, command, ordinal)
        _verify_claims(ctx, command)
        operation = operations().get(command['op'])
        if operation is not None:
            supplied_intent = {**operation.intent, **command.get('intent', {})}
            if supplied_intent != operation.intent:
                raise CommandError("unsupported operation intention policy")
            ctx.record['command']['intent'] = dict(operation.intent)
            operation.handler(ctx, command)
            ctx.record['command']['resolved'] = [command['select']] if operation.singleton else []
        else:
            apply_inverse(ctx, inverse_records, intervening_records)
            ctx.record['command']['intent'] = {}
            ctx.record['command']['resolved'] = []
        record = ctx.finish(capture=True)
        for field in ('resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'):
            if field in command and not equal(command[field], record['command'][field]):
                raise CommandError(f"submitted {field} does not match authoritative capture", kind='capture_mismatch')
        # Keep original claims and metadata after they have been verified.
        record['command'].update({k: v for k, v in command.items() if k != 'intent'})
        records.append(record)
        try:
            events.extend(_events(record, ctx.state))
        except ValueError as exc:
            if isinstance(exc, CommandError):
                raise
            raise CommandError(str(exc)) from exc
    return Plan(candidate, records, events)


def _events(record, state):
    from astrid.core.timeline.events.schema.payloads.clip import ClipRetimedPayload
    from astrid.core.timeline.events.schema.payloads.track import (
        TrackAddedPayload,
        TrackRemovedPayload,
    )

    from .capture import _duration

    events, emitted = [], set()
    for write in record['writes']:
        ref = write['ref']
        if ref in emitted:
            continue
        emitted.add(ref)
        entity = state.entity(ref, optional=True)
        if '/clip:' in ref and entity is not None:
            clip = dict(entity, at=entity.get('at', entity.get('at_ms', 0) / 1000))
            payload = ClipRetimedPayload(clip['id'], clip['at'], _duration(clip))
            kind = 'clip.retimed'
        elif '/track:' in ref and not write['path']:
            if entity is None:
                payload = TrackRemovedPayload(ref.rsplit('/track:', 1)[1])
                kind = 'track.removed'
            else:
                payload = TrackAddedPayload(entity['id'], entity['kind'], entity.get('label', entity['id']))
                kind = 'track.added'
        else:
            continue
        events.append({'command_ordinal': record['ordinal'], 'kind': kind, 'subject_ref': ref,
                       'payload': payload.to_json_obj()})
    return events
