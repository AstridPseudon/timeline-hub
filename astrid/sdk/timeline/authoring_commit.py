"""Translate a detached authoring candidate onto its authenticated commit base."""
from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from astrid.core.timeline.authoring_bundle import (
    AuthoringBundleError,
    CandidateCompilation,
    compile_authoring_candidate,
)


def response_data(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise AuthoringBundleError('Runtime response must be an object')
    value = value.get('data', value)
    if not isinstance(value, Mapping):
        raise AuthoringBundleError('Runtime response data must be an object')
    return copy.deepcopy(dict(value))


def _read_base(writer: Any, candidate: Mapping[str, Any]) -> dict[str, Any]:
    from .commit import (
        INTERNAL_IMAGE_FIELDS,
        PARENT_IMAGE_FIELDS,
        SHOT_IMAGE_FIELDS,
        bundle_from_document,
    )

    project, timeline = candidate['project_id'], candidate['timeline_id']
    pin = candidate['base_parent']
    cursor = None
    seen: set[str] = set()
    matches: list[dict[str, Any]] = []
    while True:
        page = response_data(writer.list_timeline_commits(project, timeline, cursor=cursor, limit=100))
        matches.extend(row for row in page['items'] if row['revision_id'] == pin['revision_id']
                       and ('publication_id' not in pin or row['publication_id'] == pin['publication_id']))
        cursor = page.get('next_cursor')
        if cursor is None:
            break
        if cursor in seen:
            raise AuthoringBundleError('Runtime history cursor repeated')
        seen.add(cursor)
    if len(matches) != 1:
        raise AuthoringBundleError('candidate requires one exact original revision/publication pair')
    entry = matches[0]
    if entry['receipt']['receipt_id'] != entry['publication_id']:
        raise AuthoringBundleError('Runtime history receipt differs from the original publication')
    parent = response_data(writer.get_project_parent_composition_revision(project, timeline, pin['revision_id']))
    if (parent.get('project_id'), parent.get('timeline_id'), parent.get('revision_id'), parent.get('content_digest')) != (
            project, timeline, pin['revision_id'], pin['content_digest']):
        raise AuthoringBundleError('Runtime parent differs from the candidate scope or pin')
    manifest = parent['dependency_manifest']
    shots, internals = {}, {}
    owners = {row['revision_id']: row['timeline_id'] for row in manifest['internal_timelines']}
    for occurrence in parent['payload']['occurrences']:
        revision = occurrence['shot_revision_id']
        shot = response_data(writer.get_project_shot_revision(project, occurrence['shot_id'], revision))
        if (shot.get('project_id'), shot.get('shot_id'), shot.get('revision_id')) != (project, occurrence['shot_id'], revision):
            raise AuthoringBundleError('Runtime shot differs from its exact scope or pin')
        shots[revision] = {key: shot[key] for key in SHOT_IMAGE_FIELDS}
        revision = shot['internal_timeline_revision_id']
        owner = owners[revision]
        internal = response_data(writer.get_project_timeline_revision(project, owner, revision))
        if (internal.get('project_id'), internal.get('timeline_id'), internal.get('revision_id')) != (project, owner, revision):
            raise AuthoringBundleError('Runtime internal timeline differs from its exact owner or pin')
        internals[revision] = {key: internal[key] for key in INTERNAL_IMAGE_FIELDS}
    document = {'schema_version': 1, 'project_id': project, 'timeline_id': timeline,
        'parent_revision': {key: parent[key] for key in PARENT_IMAGE_FIELDS},
        'shot_revisions': sorted(shots.values(), key=lambda row: (row['shot_id'], row['revision_id'])),
        'internal_timeline_revisions': sorted(internals.values(), key=lambda row: (row['timeline_id'], row['revision_id'])),
        'dependency_manifest': manifest}
    recorded = entry['receipt']['result'].get('canonical_document')
    if recorded is not None and recorded != document:
        raise AuthoringBundleError('Runtime receipt differs from the immutable closure')
    base = bundle_from_document(document)
    base['base_parent']['publication_id'] = entry['publication_id']
    return base


def authoring_commit_request(
    candidate: Mapping[str, Any], writer: Any, *, compilation: CandidateCompilation | None = None,
) -> dict[str, Any]:
    from ._command_state import equal
    from .emitter import _diff, emit_document_commands
    from .native_media_admission import registry_selections
    from .native_occurrence_delete import capture_occurrence_delete

    if compilation is None:
        compilation = compile_authoring_candidate(candidate)
    base = _read_base(writer, candidate)
    work = copy.deepcopy(dict(candidate))
    # These two missing transport pins may be hydrated only from Runtime. All
    # supplied baseline/provenance fields remain checked by the normal emitter.
    work['base_parent'].setdefault('publication_id', base['base_parent']['publication_id'])
    work['source_mapping'].setdefault('_runtime_document', copy.deepcopy(base['source_mapping']['_runtime_document']))
    placements = work['placements']
    original = {row['occurrence_id']: row for row in base['placements']}
    if any(row['occurrence_id'] not in original
           or row['shot_id'] != original[row['occurrence_id']]['shot_id'] for row in placements):
        raise AuthoringBundleError('closure membership edits require registered semantic commands')
    retained = {row['occurrence_id'] for row in placements}
    placed_shots = {row['shot_id'] for row in placements}
    removed = [row for row in base['placements'] if row['occurrence_id'] not in retained]
    # Detached local copies are not publication roots. Restore only omitted
    # removal baselines from the authenticated closure; supplied pins still
    # pass through the emitter's exact provenance checks.
    unplaced = set(work['shots']) - set(base['shots']) - placed_shots
    for local in unplaced:
        work['shots'].pop(local)
        work['source_mapping']['shots'].pop(local, None)
    for identity, row in list(work['source_mapping']['placements'].items()):
        if identity not in original and row['shot_id'] in unplaced:
            work['source_mapping']['placements'].pop(identity)
    for row in removed:
        identity, local = row['occurrence_id'], row['shot_id']
        work['source_mapping']['placements'].setdefault(identity, copy.deepcopy(base['source_mapping']['placements'][identity]))
        if local not in placed_shots:
            work['shots'].setdefault(local, copy.deepcopy(base['shots'][local]))
            work['source_mapping']['shots'].setdefault(local, copy.deepcopy(base['source_mapping']['shots'][local]))
    placement_changes: list[dict[str, Any]] = []
    # Move complete physical occurrence rows before applying keyed field edits.
    # Runtime's list.move checks both the previous item and collection order.
    source_rows = base['source_mapping']['_runtime_document']['parent_revision']['payload']['occurrences']
    ordered = list(source_rows)
    target_order = [row['occurrence_id'] for row in placements] + [row['occurrence_id'] for row in removed]
    for index, identity in enumerate(target_order):
        ids = [row['occurrence_id'] for row in ordered]
        if ids[index] != identity:
            item = ordered.pop(ids.index(identity))
            placement_changes.append({'op': 'list.move', 'ref': 'parent', 'path': ['occurrences'],
                'id': identity, 'before': {'state': 'present', 'value': copy.deepcopy(item)},
                'order_before': ids, 'after_id': target_order[index - 1] if index else None})
            ordered.insert(index, item)
    for row in placements:
        old = original[row['occurrence_id']]
        _diff(old, row, 'parent', ('occurrences', 'occurrence_id:' + row['occurrence_id']), placement_changes)
    work['placements'] = copy.deepcopy(base['placements'])
    commands = emit_document_commands(base, work)
    if placement_changes:
        commands.append({'schema_version': 1, 'op': 'doc.patch', 'version': '1', 'select': None,
                         'args': {'changes': placement_changes}})
    for row in removed:
        commands.append(capture_occurrence_delete(base, 'occurrence:' + row['occurrence_id']))
    if not commands:
        # Republishing an unchanged checkout still needs Runtime's replay/CAS
        # boundary. A guarded equal-value set preserves the authored config
        # without replacing the closure or manufacturing an edit.
        config = copy.deepcopy(base['parent']['config'])
        commands.append({'schema_version': 1, 'op': 'doc.patch', 'version': '1', 'select': None,
            'args': {'changes': [{'op': 'set', 'ref': 'parent', 'path': ['config'],
                'before': {'state': 'present', 'value': config}, 'value': copy.deepcopy(config)}]}})
    source = base['source_mapping']['_runtime_document']
    inputs = [{'pin': copy.deepcopy(pin)} for pin in compilation.publication['dependency_manifest']['media']
              if pin not in source['dependency_manifest']['media']]
    old_selections = list(registry_selections(base))
    selected_work = {**work, 'shots': {key: value for key, value in work['shots'].items() if key in placed_shots}}
    for association in registry_selections(selected_work):
        if association in old_selections:
            continue
        selected = response_data(writer.get_project_media_selection(candidate['project_id'],
            {key: association[key] for key in ('asset', 'generation_id', 'variant_id')}))
        if not equal({key: selected.get(key) for key in association}, association):
            raise AuthoringBundleError('Runtime catalog association differs from the candidate media')
        pin = {'media_id': selected['object_id'], 'content_digest': selected['object_id']}
        value = {'pin': pin, 'selection': selected}
        inputs = [row for row in inputs if row != {'pin': pin}]
        if value not in inputs:
            inputs.append(value)
    steps = [{'id': 'authoring', 'label': 'Publish authoring candidate', 'intent': '', 'tags': [],
        'command_ordinals': list(range(len(commands))),
        'patch': [copy.deepcopy(change) for call in commands if call['op'] == 'doc.patch'
                  for change in call['args']['changes']]}]
    if inputs:
        # Runtime captures all inputs before execution. Record consumption at
        # the final boundary, where these pins are in the resulting closure.
        steps.append({'id': 'media', 'label': 'Capture authoring media', 'intent': '', 'tags': [],
                      'command_ordinals': [len(commands)], 'patch': []})
        commands.append({'schema_version': 1, 'op': 'media.admit', 'version': '1',
                         'select': None, 'args': {'inputs': inputs}})
    return {'api_version': 1, 'project_id': candidate['project_id'], 'timeline_id': candidate['timeline_id'],
        'base_revision_id': base['base_parent']['revision_id'],
        'base_publication_id': base['base_parent']['publication_id'], 'commands': commands,
        'label': 'Publish authoring candidate', 'steps': steps, 'merge': 'atomic', 'source': {'via': 'python'},
        'rationale': 'Publish authoring candidate ' + compilation.candidate_digest}
