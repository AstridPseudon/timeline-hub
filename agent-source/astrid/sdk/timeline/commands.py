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
TRACK_CREATE_PARAMETERS = _SCHEMA['$defs']['TrackCreateArgs']


@dataclass(frozen=True)
class Operation:
    parameters: dict
    handler: Callable[[Recording, dict], None]
    intent: dict
    singleton: bool = False


def operations():
    """Native recipe entries; the full extensible registry belongs to M2."""
    from ._clip_commands import clip_add
    from ._clip_scalar_commands import clip_set, clip_set_element
    from ._delete_commands import delete
    from ._scalar_commands import clip_set_params, track_set
    from ._shot_commands import SHOT_INTENT, shot_set
    from ._split_commands import clip_split
    from ._trim_commands import clip_trim
    from .capture import MOVE_INTENT, move, track_create
    from .native_occurrence_delete import occurrence_delete
    from .native_occurrence_duplicate import OCCURRENCE_INTENT, occurrence_duplicate
    from .native_occurrence_media_commands import MEDIA_INTENT, add_media, swap_media
    from .native_placement_commands import (
        PLACEMENT_INTENT,
        placement_create,
        placement_move,
        placement_unplace,
    )
    from .native_shot_pool_commands import POOL_INTENT, shot_pool
    return {'clip.move': Operation(_SCHEMA['$defs']['ClipMoveArgs'], move, MOVE_INTENT, True),
            'placement.move': Operation(_SCHEMA['$defs']['ClipMoveArgs'], placement_move, MOVE_INTENT, True),
            'occurrence.delete': Operation(_SCHEMA['$defs']['OccurrenceDeleteArgs'], occurrence_delete, OCCURRENCE_INTENT, True),
            'placement.create': Operation(_SCHEMA['$defs']['PlacementCreateArgs'], placement_create,
                                          PLACEMENT_INTENT, True),
            'placement.unplace': Operation(_SCHEMA['$defs']['PlacementUnplaceArgs'], placement_unplace,
                                           PLACEMENT_INTENT, True),
            'shot.pool': Operation(_SCHEMA['$defs']['ShotPoolArgs'], shot_pool, POOL_INTENT, True),
            'occurrence.duplicate': Operation(_SCHEMA['$defs']['OccurrenceDuplicateArgs'], occurrence_duplicate,
                                              OCCURRENCE_INTENT, True),
            'clip.delete': Operation(_SCHEMA['$defs']['ClipDeleteArgs'], delete, {}, True),
            'occurrence.add-media': Operation(_SCHEMA['$defs']['OccurrenceAddMediaArgs'], add_media, MEDIA_INTENT, True),
            'occurrence.swap-media': Operation(_SCHEMA['$defs']['OccurrenceSwapMediaArgs'], swap_media, MEDIA_INTENT, True),
            'track.create': Operation(TRACK_CREATE_PARAMETERS, track_create, {}),
            'clip.set': Operation(_SCHEMA['$defs']['ClipSetArgs'], clip_set, {}, True),
            'clip.set-element': Operation(_SCHEMA['$defs']['ClipSetElementArgs'], clip_set_element, {}, True),
            'clip.add': Operation(_SCHEMA['$defs']['ClipAddArgs'], clip_add, {}),
            'clip.trim': Operation(_SCHEMA['$defs']['ClipTrimArgs'], clip_trim, {}, True),
            'clip.split': Operation(_SCHEMA['$defs']['ClipSplitArgs'], clip_split, {}, True),
            'track.set': Operation(_SCHEMA['$defs']['TrackSetArgs'], track_set, {}, True),
            'shot.set': Operation(_SCHEMA['$defs']['ShotSetArgs'], shot_set, SHOT_INTENT, True),
            'clip.set-params': Operation(_SCHEMA['$defs']['ClipSetParamsArgs'], clip_set_params, {}, True)}


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
    if command['op'] not in (*operations(), 'timeline.inverse', 'timeline.restore'):
        raise CommandError(f"unsupported operation {command['op']!r}", kind='unsupported_operation')
    operation = operations().get(command['op'])
    if operation is not None:
        errors = list(_VALIDATOR.evolve(schema=operation.parameters).iter_errors(command['args']))
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
    operation = operations().get(command['op'])
    resolved = command.get('resolved', [command['select']] if operation and operation.singleton else [])
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


def execute(bundle, commands, *, inverse_records=(), intervening_records=(), id_map=None,
            closures=None, verified_media=(), schema_inputs=(), realm_id=None, resolve_inputs=None):
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
    if any(call.get('op') == 'timeline.restore' for call in commands) and len(commands) != 1:
        raise CommandError("restore must be the sole command", kind='invalid_commands')
    candidate, records = copy.deepcopy(bundle), []
    for ordinal, supplied in enumerate(commands):
        command = _normalize(supplied)
        ctx = Recording(candidate, command, ordinal, closures=closures, verified_media=verified_media,
                        schema_inputs=schema_inputs, realm_id=realm_id)
        _verify_claims(ctx, command)
        if resolve_inputs is not None:
            ctx.schema_inputs = resolve_inputs(ctx)
        operation = operations().get(command['op'])
        if operation is not None:
            from .capture import move_intent
            intent = move_intent(command['select']) if command['op'] in ('clip.move', 'placement.move') else operation.intent
            supplied_intent = {**intent, **command.get('intent', {})}
            if supplied_intent != intent:
                raise CommandError("unsupported operation intention policy")
            ctx.record['command']['intent'] = dict(intent)
            operation.handler(ctx, command)
            ctx.record['command']['resolved'] = [command['select']] if operation.singleton else []
        elif command['op'] == 'timeline.restore':
            ctx.read('timeline')
            ctx.write('timeline', [], command['args'])
            ctx.record['command']['intent'] = {}
            ctx.record['command']['resolved'] = []
        else:
            apply_inverse(ctx, inverse_records, intervening_records)
            ctx.record['command']['intent'] = {}
            ctx.record['command']['resolved'] = []
        if ordinal == len(commands) - 1:
            ctx.compile_inputs()
        ctx.compile_mirrors()
        record = ctx.finish(capture=True)
        for field in ('resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'):
            if field not in command:
                continue
            matches = equal(command[field], record['command'][field])
            if field == 'reads':
                actual = record['command']['reads']
                matches = len(command[field]) == len(actual) and all(
                    claimed['ref'] == read['ref'] and claimed['path'] == read['path']
                    and (equal(claimed['state'], read['state'])
                         or ctx.command_input.matches(read['ref'], read['path'], claimed['state']))
                    for claimed, read in zip(command[field], actual))
            if field == 'expect' and command[field].keys() == record['command'][field].keys():
                matches = all(ctx.command_input.matches(*address(key, command.get('resolved', [])), expected)
                              for key, expected in command[field].items())
            if not matches:
                raise CommandError(f"submitted {field} does not match authoritative capture", kind='capture_mismatch')
        # Keep original claims and metadata after they have been verified.
        record['command'].update({k: v for k, v in command.items() if k != 'intent'})
        records.append(record)
    return Plan(candidate, records)
