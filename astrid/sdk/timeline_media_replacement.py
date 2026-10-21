"""Selected-media adapter for the existing Runtime commit door."""
from __future__ import annotations

import copy
import re
from collections.abc import Mapping

from .contracts import DomainResult, ErrorObject


def replace_selected_media(timelines, project, ref, *, occurrence_id, clip_id, source_object_id,
                           expected_head, expected_publication, old_media, media, idempotency_key):
    from .timeline.commands import CommandError, validate_command

    try:
        if (not all(isinstance(value, str) and value.strip() for value in (
                project, expected_head, expected_publication))
                or not isinstance(clip_id, str) or not re.fullmatch(r'(?!.*::)[^/]+', clip_id)
                or (occurrence_id is not None and (not isinstance(occurrence_id, str)
                    or not re.fullmatch(r'(?!.*::)[^/]+', occurrence_id)))
                or not isinstance(old_media, Mapping) or not isinstance(media, Mapping)
                or source_object_id != media.get('object_id')):
            raise CommandError('native replacement requires exact selections, raw identity and base head pair')
        owner = 'parent' if occurrence_id is None else 'occurrence:' + occurrence_id
        command = {'schema_version': 1, 'version': '1',
                   'op': 'clip.swap-media' if owner == 'parent' else 'occurrence.swap-media',
                   'select': owner + '/clip:' + clip_id,
                   'args': {'old_media': copy.deepcopy(dict(old_media)), 'media': copy.deepcopy(dict(media))},
                   'intent': {'ownership': 'parent' if owner == 'parent' else 'occurrence'}}
        validate_command(command)
    except CommandError as exc:
        return DomainResult.failure(ErrorObject('validation_error', str(exc), {}),
                                    idempotency_key=idempotency_key)
    resolved = timelines._resolve_timeline(project, ref)
    if not resolved.ok:
        return resolved
    scope = resolved.data
    body = {'api_version': 1, 'project_id': scope['project_id'], 'timeline_id': scope['timeline_id'],
            'base_revision_id': expected_head, 'base_publication_id': expected_publication,
            'commands': [command], 'source': {'via': 'python'}}
    return timelines.commit(project, ref, body, idempotency_key=idempotency_key)
