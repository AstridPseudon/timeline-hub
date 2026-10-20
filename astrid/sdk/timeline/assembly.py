"""Requester-owned reads for the registered two-child assembler admission."""
from __future__ import annotations

import copy
import json

from ._command_state import State, equal
from ._common import TimelineEditError
from .capture import number


def capture_assembly(session, state, child_outputs, *, replace_clips):
    """Read exact original inputs once; never select a mutable primary or head."""
    bundle = session._bundle(state)
    authored = State(bundle)
    replace_clips = list(replace_clips)
    if bundle['placements'] or replace_clips != [
            'parent/clip:' + row['id'] for row in authored.collection('parent', 'clip')]:
        raise TimelineEditError('assembly requires explicit original flat parent clip membership')
    child_outputs = copy.deepcopy(list(child_outputs))
    if len(child_outputs) != 2:
        raise TimelineEditError('assembly requires two ordered exact child output selectors')
    transport = session.client._remote._transport
    children = []
    for ordinal, selector in enumerate(child_outputs):
        if (not isinstance(selector, dict) or set(selector) != {'association_id', 'object_id', 'version'}
                or type(selector['version']) is not int or selector['version'] < 1):
            raise TimelineEditError('assembly requires exact association/object/version selectors')
        association = transport.get_managed_output(selector['association_id'])
        if (association['project_id'] != session.project_id
                or association['object_id'] != selector['object_id']
                or association['lifecycle']['version'] != selector['version']
                or association['durability'] != 'durable'
                or association['lifecycle']['state'] not in ('available', 'promoted')
                or association['role'] not in ('primary', 'primary_visual')
                or not association['media_type'].startswith('video/')):
            raise TimelineEditError('assembly child is not the exact eligible project visual output')
        media = transport.get_project_media_selection(session.project_id, selector)
        verified = transport.get_project_verified_media(session.project_id, media)
        if (media['object_id'] != selector['object_id'] or not equal(verified['selection'], media)
                or verified['media_type'] != association['media_type']
                or type(verified['size']) is not int or verified['size'] <= 0
                or verified['size'] != association['size']):
            raise TimelineEditError('verified media differs from the exact child association')
        number(verified.get('duration_seconds'), 'child intrinsic duration', positive=True)
        children.append({'ordinal': ordinal, 'task_id': association['task_id'],
                         'association': selector, 'media': media, 'verified_media': verified})
    target = {'project_id': session.project_id, 'timeline_id': session.timeline_id,
              'base_revision_id': state['base']['revision_id'],
              'base_publication_id': state['base']['publication_id']}
    # Plain task data carries neither the client nor credentials to the worker.
    return json.loads(json.dumps({'admitted_target': target, 'bundle': bundle,
                                 'replace_clips': replace_clips, 'children': children}, allow_nan=False))
