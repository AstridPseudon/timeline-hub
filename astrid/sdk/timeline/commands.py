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
from ._recording import Recording, guard, selection, selection_matches

_SCHEMA = json.loads((Path(__file__).parents[2] / 'core/timeline/schema/edit-command.schema.json').read_text())
_VALIDATOR = Draft202012Validator(_SCHEMA)
TRACK_CREATE_PARAMETERS = _SCHEMA['$defs']['TrackCreateArgs']


@dataclass(frozen=True)
class Operation:
    parameters: dict
    handler: Callable[[Recording, dict], None]
    intent: dict
    singleton: bool = False
    versioned_parameters: dict[str, dict] = dataclass_field(default_factory=dict)

    def parameters_for(self, version):
        return self.versioned_parameters.get(version, self.parameters)


def operations():
    """Native recipe entries; the full extensible registry belongs to M2."""
    from ._clip_commands import clip_add
    from ._clip_scalar_commands import clip_set, clip_set_element
    from ._delete_commands import delete
    from ._move_set import move_set
    from ._project_data_commands import PROJECT_DATA_INTENT, project_data_write
    from ._scalar_commands import clip_set_params, track_set
    from ._shot_commands import SHOT_INTENT, shot_set
    from ._split_commands import clip_split
    from ._track_commands import track_reorder
    from ._trim_commands import clip_trim
    from .capture import MOVE_INTENT, move, track_create
    from .native_initialize import initialize
    from .native_occurrence_create import occurrence_create
    from .native_occurrence_delete import occurrence_delete
    from .native_occurrence_duplicate import OCCURRENCE_INTENT, occurrence_duplicate
    from .native_occurrence_media_commands import (
        MEDIA_INTENT,
        add_media,
        parent_swap_media,
        swap_media,
    )
    from .native_occurrence_resize import OCCURRENCE_RESIZE_INTENT, occurrence_resize
    from .native_parent_media_commands import add_media as parent_add_media
    from .native_parent_media_commands import assembled_target
    from .native_parent_reference_commands import timeline_reference
    from .native_placement_commands import (
        PLACEMENT_INTENT,
        placement_create,
        placement_move,
        placement_unplace,
    )
    from .native_shot_pool_commands import POOL_INTENT, shot_pool
    from .native_text_binding import TEXT_INTENT, text_binding_set
    from .native_transcript_association import associate as transcript_associate
    from .native_word_anchor import declare
    from .new_group_commands import migrate_groups
    from .occurrence_commands import OCCURRENCE_MOVE_INTENT, occurrence_move
    from .producer import producer_guard
    return {'timeline.migrate-groups': Operation(_SCHEMA['$defs']['MigrateGroupsArgs'], migrate_groups, {}),
            'occurrence.move': Operation(_SCHEMA['$defs']['OccurrenceMoveArgs'], occurrence_move,
                                         OCCURRENCE_MOVE_INTENT, True),
            'text-binding.set': Operation(_SCHEMA['$defs']['TextBindingSetArgs'], text_binding_set, TEXT_INTENT, True),
            'transcript.associate': Operation(_SCHEMA['$defs']['TranscriptAssociateArgs'], transcript_associate,
                                              {'ownership': 'parent'}, True),
            'timeline.init': Operation(
                _SCHEMA['$defs']['TimelineInitArgs'], initialize, {},
                versioned_parameters={'2': _SCHEMA['$defs']['TimelineInitRawArgs']}),
            'clip.anchor': Operation(_SCHEMA['$defs']['ClipAnchorArgs'], declare, {'anchor': 'follow'}, True),
            'occurrence.create': Operation(_SCHEMA['$defs']['OccurrenceCreateArgs'], occurrence_create,
                                          OCCURRENCE_INTENT),
            'clip.move': Operation(_SCHEMA['$defs']['ClipMoveArgs'], move, MOVE_INTENT, True),
            'clip.move-set': Operation(_SCHEMA['$defs']['ClipMoveSetArgs'], move_set, MOVE_INTENT),
            'placement.move': Operation(_SCHEMA['$defs']['ClipMoveArgs'], placement_move, MOVE_INTENT, True),
            'occurrence.delete': Operation(_SCHEMA['$defs']['OccurrenceDeleteArgs'], occurrence_delete, OCCURRENCE_INTENT, True),
            'placement.create': Operation(_SCHEMA['$defs']['PlacementCreateArgs'], placement_create,
                                          PLACEMENT_INTENT, True),
            'placement.unplace': Operation(_SCHEMA['$defs']['PlacementUnplaceArgs'], placement_unplace,
                                           PLACEMENT_INTENT, True),
            'shot.pool': Operation(_SCHEMA['$defs']['ShotPoolArgs'], shot_pool, POOL_INTENT, True),
            'occurrence.duplicate': Operation(_SCHEMA['$defs']['OccurrenceDuplicateArgs'], occurrence_duplicate,
                                              OCCURRENCE_INTENT, True),
            'occurrence.resize': Operation(_SCHEMA['$defs']['OccurrenceResizeArgs'], occurrence_resize,
                                           OCCURRENCE_RESIZE_INTENT, True),
            'clip.delete': Operation(_SCHEMA['$defs']['ClipDeleteArgs'], delete, {}, True),
            'occurrence.add-media': Operation(_SCHEMA['$defs']['OccurrenceAddMediaArgs'], add_media, MEDIA_INTENT, True),
            'occurrence.swap-media': Operation(_SCHEMA['$defs']['OccurrenceSwapMediaArgs'], swap_media, MEDIA_INTENT, True),
            'clip.swap-media': Operation(_SCHEMA['$defs']['OccurrenceSwapMediaArgs'], parent_swap_media,
                                         {'ownership': 'parent'}, True),
            'track.create': Operation(TRACK_CREATE_PARAMETERS, track_create, {}),
            'clip.set': Operation(_SCHEMA['$defs']['ClipSetArgs'], clip_set, {}, True),
            'clip.set-element': Operation(_SCHEMA['$defs']['ClipSetElementArgs'], clip_set_element, {}, True),
            'clip.add': Operation(_SCHEMA['$defs']['ClipAddArgs'], clip_add, {}),
            'clip.trim': Operation(_SCHEMA['$defs']['ClipTrimArgs'], clip_trim, {}, True),
            'clip.split': Operation(_SCHEMA['$defs']['ClipSplitArgs'], clip_split, {}, True),
            'track.set': Operation(_SCHEMA['$defs']['TrackSetArgs'], track_set, {}, True),
            'track.reorder': Operation(_SCHEMA['$defs']['TrackReorderArgs'], track_reorder, {}),
            'shot.set': Operation(_SCHEMA['$defs']['ShotSetArgs'], shot_set, SHOT_INTENT, True),
            'clip.set-params': Operation(_SCHEMA['$defs']['ClipSetParamsArgs'], clip_set_params, {}, True),
            'timeline.assembled-target': Operation(_SCHEMA['$defs']['AssembledTargetArgs'], assembled_target, {}),
            'timeline.reference': Operation(_SCHEMA['$defs']['TimelineReferenceArgs'], timeline_reference, {}),
            'clip.add-media': Operation(_SCHEMA['$defs']['ClipAddMediaArgs'], parent_add_media, {}),
            'producer.guard': Operation(_SCHEMA['$defs']['ProducerGuardArgs'], producer_guard, {}),
            'project-data.write': Operation(_SCHEMA['$defs']['ProjectDataWriteArgs'], project_data_write,
                                            PROJECT_DATA_INTENT)}


@dataclass
class Plan:
    bundle: dict
    records: list[dict]
    semantic_events: list[dict] = dataclass_field(default_factory=list)
    id_map: dict[str, str] = dataclass_field(default_factory=dict)

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
    from ._materialization import SOURCE_BOUND_OPERATIONS

    source_bound = command['version'] == '2' and command['op'] in SOURCE_BOUND_OPERATIONS
    raw_old_swap = ((command['op'], command['version']) in {
        ('clip.swap-media', '2'), ('occurrence.swap-media', '3')})
    raw_initialize = command['op'] == 'timeline.init' and command['version'] == '2'
    if command['version'] != '1' and not (source_bound or raw_old_swap or raw_initialize):
        raise CommandError("unsupported operation version", kind='unsupported_version')
    if command['op'] not in (*operations(), 'timeline.inverse', 'timeline.restore'):
        raise CommandError(f"unsupported operation {command['op']!r}", kind='unsupported_operation')
    operation = operations().get(command['op'])
    if operation is not None:
        parameters = (_SCHEMA['$defs']['RawOldSwapMediaArgs']
                      if raw_old_swap else operation.parameters_for(command['version']))
        errors = list(_VALIDATOR.evolve(schema=parameters).iter_errors(command['args']))
        if errors:
            raise CommandError(errors[0].message)
    if command['op'] == 'track.create':
        if command['select'] != 'parent' and not (
                isinstance(command['select'], str) and command['select'].startswith('occurrence:')
                and '/' not in command['select']):
            raise CommandError("track.create requires parent or occurrence owner")
        if command.get('intent', {}) != {}:
            raise CommandError("track.create has no intention overrides")

    if command['op'] == 'producer.guard':
        pin = command['args']['pin']
        if any(type(pin[key]) is not int for key in ('fence', 'runtime_epoch')):
            raise CommandError('producer fence and epoch must be positive integers')


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


def _project_data_container_claim(ctx, command, ref, path, expected):
    """Allow a recorded namespace birth to merge through a disjoint key.

    The property guards for the requested leaf remain authoritative.  A
    missing/null config, app map, or extension namespace is only setup for
    that leaf, so an ordinary replay may reuse a concurrently created object
    while preserving its other members.  Malformed shapes still fail visibly
    instead of being overwritten.
    """
    if not _is_project_data_container_path(command, ref, path):
        return False
    if expected["state"] == "present" and expected.get("value") is not None:
        return False
    actual = ctx.state.get(ref, path)
    if actual["state"] == "absent" or (
        actual["state"] == "present"
        and (actual.get("value") is None or isinstance(actual.get("value"), dict))
    ):
        return True
    raise CommandError(
        "project-data namespace shape changed",
        kind="dependency_changed",
        ref=ref,
        path=path,
        base=expected,
        theirs=actual,
    )


def _is_project_data_container_path(command, ref, path):
    if command.get("op") != "project-data.write" or ref != "parent":
        return False
    target = command["args"]["target"]
    return tuple(path) in (("config",), ("config", "app"), ("config", "app", target))


def _verify_claims(ctx, command):
    for ref in command.get('created', []):
        if ctx.state.entity(ref, optional=True) is not None:
            raise CommandError('created identity is occupied', kind='identity_collision', ref=ref)
    for key, expected in command.get('expect', {}).items():
        ref, path = address(key, command.get('resolved', []))
        if _project_data_container_claim(ctx, command, ref, path, expected):
            continue
        guard(ctx.state, ref, path, expected)
    for read in command.get('reads', []):
        if _project_data_container_claim(ctx, command, read['ref'], read['path'], read['state']):
            continue
        guard(ctx.state, read['ref'], read['path'], read['state'])
    for selected in command.get('selections', []):
        actual = selection(ctx.state, selected['key'], selected['owner'], selected['members'])
        if not selection_matches(selected, actual):
            raise CommandError("original selection membership/order changed", kind='selection_changed', ref=selected['owner'])


def execute(bundle, commands, *, inverse_records=(), intervening_records=(), id_map=None,
            closures=None, materializations=(), verified_media=(), schema_inputs=(), realm_id=None, resolve_inputs=None,
            verified_producer=None):
    """Execute atomically. History inputs must already be authenticated by provider.

    Empty intervening_records means proven empty ancestry, never unavailable
    history. Incoming recorder fields are checked claims; generated records are
    the authority. No persistence, mutable reads or renderer lives here.
    """
    from ._materialization import SOURCE_BOUND_OPERATIONS
    from .inverse import apply_inverse

    if not commands:
        raise CommandError("command batch must not be empty")
    from .producer import guard_pin
    guard_pin(commands)
    config = bundle['parent'].get('config')
    if isinstance(config, dict) and 'pinnedShotGroups' in config:
        migration = len(commands) == 1 and commands[0].get('op') == 'timeline.migrate-groups'
        reversing = len(commands) == 1 and commands[0].get('op') == 'timeline.inverse' and any(
            write['ref'] == 'parent' and write['path'] == ['config', 'pinnedShotGroups']
            for record in inverse_records for write in record['writes'])
        if not migration and not reversing:
            raise CommandError('legacy groups require the sole recorded migration command',
                               kind='unsupported_dependency')
    if any(call.get('op') == 'timeline.restore' for call in commands) and len(commands) != 1:
        raise CommandError("restore must be the sole command", kind='invalid_commands')
    candidate, records = copy.deepcopy(bundle), []
    for ordinal, supplied in enumerate(commands):
        command = _normalize(supplied)
        if command['version'] == '2' and command['op'] in SOURCE_BOUND_OPERATIONS:
            if '_source_closure' not in candidate['source_mapping']:
                raise CommandError('source-bound v2 requires the verified original closure', kind='capture_mismatch')
            fields = {'resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'}
            if fields.intersection(command) and not fields.issubset(command):
                raise CommandError('incomplete v2 capture; keep the draft and explicitly re-author it',
                                   kind='capture_mismatch')
        if command['op'] == 'timeline.inverse':
            from ._materialization import consume
            candidate = consume(candidate, inverse_records, closures=closures)
        ctx = Recording(candidate, command, ordinal, closures=closures, verified_media=verified_media,
                        schema_inputs=schema_inputs, realm_id=realm_id,
                        verified_producer=verified_producer)
        ctx.prior_records = records
        _verify_claims(ctx, command)
        if resolve_inputs is not None:
            ctx.prior_records = records
            ctx.schema_inputs = resolve_inputs(ctx)
        operation = operations().get(command['op'])
        if operation is not None:
            from .native_word_anchor import guard_basis

            guard_basis(ctx, command)
            from .capture import move_intent
            intent = move_intent(command['select']) if command['op'] in ('clip.move', 'placement.move') else operation.intent
            supplied_intent = {**intent, **command.get('intent', {})}
            if supplied_intent != intent:
                raise CommandError("unsupported operation intention policy")
            ctx.record['command']['intent'] = dict(intent)
            operation.handler(ctx, command)
            ctx.record['command']['resolved'] = (
                [member['clip'] for member in command['args']['members']]
                if command['op'] == 'clip.move-set'
                else [command['select']] if operation.singleton else [])
        elif command['op'] == 'timeline.restore':
            ctx.read('timeline')
            ctx.write('timeline', [], command['args'])
            ctx.record['command']['intent'] = {}
            ctx.record['command']['resolved'] = []
        else:
            apply_inverse(ctx, inverse_records, intervening_records, staged_records=records)
            ctx.record['command']['intent'] = {}
            ctx.record['command']['resolved'] = []
        if ordinal == len(commands) - 1:
            ctx.compile_inputs()
            from .native_word_anchor import compile_recorded

            compile_recorded(ctx, inverse_records=inverse_records)
        ctx.compile_mirrors()
        from ._materialization import capture, verify_sources
        # Complete public S2 v1 captures retain their original record format.
        # Inverses carry original facts from authenticated accepted history.
        if (command['version'] == '2' and command['op'] in SOURCE_BOUND_OPERATIONS
                or command['op'] == 'timeline.inverse'):
            capture(ctx, inverse_records if command['op'] == 'timeline.inverse' else materializations)
        verify_sources(ctx.state, [ctx.record])
        record = ctx.finish(capture=True)
        for field in ('resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'):
            if field not in command:
                continue
            matches = equal(command[field], record['command'][field])
            if field == 'selections':
                matches = len(command[field]) == len(record['command'][field]) and all(
                    selection_matches(claimed, actual)
                    for claimed, actual in zip(command[field], record['command'][field]))
            if field == 'expect':
                authoritative = record['command'][field]
                matches = set(authoritative).issubset(command[field]) and all(
                    ctx.command_input.matches(
                        *address(key, command.get('resolved', [])), authoritative[key]
                    )
                    for key in authoritative
                )
                matches = matches and all(
                    _project_data_container_claim(
                        ctx, command, *address(key, command.get('resolved', [])), expected
                    )
                    for key, expected in command[field].items()
                    if key not in authoritative
                )
            if field == 'authorship':
                authoritative = record['command'][field]
                matches = set(authoritative).issubset(command[field]) and all(
                    command[field][key] == authoritative[key] for key in authoritative
                )
                matches = matches and all(
                    _is_project_data_container_path(
                        command, *address(key, command.get('resolved', []))
                    )
                    and value == 'direct'
                    for key, value in command[field].items()
                    if key not in authoritative
                )
            if field == 'reads':
                supplied = [
                    read for read in command[field]
                    if not _is_project_data_container_path(command, read['ref'], read['path'])
                ]
                authoritative = record['command']['reads']
                matches = len(supplied) == len(authoritative) and all(
                    claimed['ref'] == read['ref']
                    and claimed['path'] == read['path']
                    and (
                        equal(claimed['state'], read['state'])
                        or ctx.command_input.matches(read['ref'], read['path'], claimed['state'])
                    )
                    for claimed, read in zip(supplied, authoritative)
                )
                matches = matches and all(
                    _project_data_container_claim(ctx, command, read['ref'], read['path'], read['state'])
                    for read in command[field]
                    if _is_project_data_container_path(command, read['ref'], read['path'])
                )
            if not matches:
                raise CommandError(
                    f"submitted {field} does not match authoritative v{command['version']} capture; "
                    "keep the draft and explicitly re-author it against the current timeline",
                    kind='capture_mismatch')
        # Keep original claims and metadata after they have been verified.
        record['command'].update({k: v for k, v in command.items() if k != 'intent'})
        records.append(record)
    from ._materialization import id_map as allocation_map
    mapping = allocation_map(records)
    if id_map is not None:
        if any(not isinstance(key, str) or not key or not isinstance(value, str) or not value
               for key, value in id_map.items()) or {
                key: value for key, value in id_map.items() if key != value} != mapping:
            raise CommandError('id_map requires identity pairs or verified allocations', kind='identity_collision')
        mapping = {**id_map, **mapping}
    return Plan(candidate, records, id_map=mapping)
