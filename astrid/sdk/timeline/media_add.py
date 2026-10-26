"""One parent media birth using managed import and the registered SDK recipes."""
from __future__ import annotations

import copy
import hashlib
import uuid
from collections.abc import Mapping
from pathlib import Path

from ._command_state import State
from ._common import TimelineEditError
from .capture import number
from .outbox import request_bytes


def _selection(session, bundle, source):
    from astrid.sdk.authoring_media import _metadata
    from astrid.sdk.media_handles import resolve_media_handle
    from astrid.sdk.pagination import paged_rows
    from astrid.sdk.timeline_media_replacement import _plain, _verified

    transport, project = session.client._remote._transport, session.project_id
    if isinstance(source, Mapping):
        return _verified(transport, project, source)
    path = Path(source).expanduser()
    if path.is_file():
        metadata = _metadata(path)
        if metadata['media_type'].split('/')[0] not in ('image', 'video'):
            raise TimelineEditError('media layers require an image or video file')
        payload = path.read_bytes()
        if 'sha256:' + hashlib.sha256(payload).hexdigest() != metadata['digest']:
            raise TimelineEditError('local media changed during import; retry after the file is saved')
        imported = _plain(transport.import_project_media(
            project, payload, media_type=metadata['media_type'], filename=metadata['filename'],
            expected_digest=metadata['digest'],
            idempotency_key='timeline-media-' + hashlib.sha256(request_bytes(metadata)).hexdigest(),
            **{key: metadata[key] for key in ('width', 'height', 'duration_seconds') if key in metadata},
        ))
        selectors = {'asset': imported['variant_id'], 'generation_id': imported['generation_id'],
                     'variant_id': imported['variant_id']}
    else:
        entry = State(bundle).registry('parent').get('assets', {}).get(source)
        if isinstance(entry, Mapping) and entry.get('generationId') and entry.get('variantId'):
            selectors = {'asset': source, 'generation_id': entry['generationId'],
                         'variant_id': entry['variantId']}
        else:
            descriptor, _ = resolve_media_handle(session.client, project, source)
            matches = []
            for generation in paged_rows(transport.list_generations, project) or []:
                for variant in paged_rows(transport.list_variants, generation['generation_id']) or []:
                    if variant.get('object_id') == descriptor['digest']:
                        matches.append({'asset': variant['variant_id'],
                                        'generation_id': generation['generation_id'],
                                        'variant_id': variant['variant_id']})
            if len(matches) != 1:
                raise TimelineEditError('media handle needs one exact catalog variant; use a local file '
                                        'or an existing timeline asset key')
            selectors = matches[0]
    pin = _plain(transport.get_project_media_selection(project, selectors))
    return _verified(transport, project, pin)


def add_media(session, source, *, on, duration, track, clip_id, values,
              idempotency_key, dry_run, via):
    """Capture once, including IDs/import selection, then retry the original request.

    The editor's empty drop authors a parent clip, not a synthetic shot. A missing
    visual track and the clip are one commit_many batch. Catalog import is the
    existing independent managed-media operation, never a timeline publication.
    """
    on, duration = number(on, 'on'), number(duration, 'duration', positive=True)
    if on < 0:
        raise TimelineEditError('on must not be negative')
    if idempotency_key is not None and (not isinstance(idempotency_key, str) or not idempotency_key.strip()):
        raise TimelineEditError('idempotency key must be nonempty')
    if not isinstance(track, str) or not track.strip():
        raise TimelineEditError('media add needs a visual track; use --track V1')
    if {'id', 'clipType', 'track', 'asset', 'at', 'hold', 'from', 'to', 'speed'}.intersection(values or {}):
        raise TimelineEditError('media identity and timing must use the add_media arguments')
    intent = {'source': dict(source) if isinstance(source, Mapping) else str(source),
              'on': on, 'duration': duration, 'track': track,
              'clip_id': clip_id, 'values': dict(values or {})}
    with session.outbox.locked():
        state = session._state()
    previous = state.get('acknowledged', {}).get(idempotency_key)
    if previous is not None:
        return session.retry(idempotency_key, matches=lambda _: previous.get('media_input') == intent,
                             dry_run=dry_run, via=via)
    if state['pending'] or state['flight'] is not None:
        if state.get('media_input') != intent:
            raise TimelineEditError('pending intent differs; retry the original edit and key first')
        return session.flush(idempotency_key=idempotency_key, dry_run=dry_run, via=via)

    bundle = session._bundle(state)
    lane = State(bundle).entity('parent/track:' + track, optional=True)
    if lane is not None and (lane.get('kind') != 'visual' or lane.get('role', 'output') != 'output'):
        raise TimelineEditError(f'track {track!r} is not a visual output track; use --track V1')
    pin, verified = _selection(session, bundle, source)
    row = {'id': clip_id or 'clip-' + uuid.uuid4().hex, 'clipType': 'media', 'track': track,
           'asset': pin['asset'], 'at': on, 'hold': duration, **dict(values or {})}
    if verified['media_type'].startswith('video/'):
        row.update({'from': 0, 'to': duration, 'speed': 1})
    commands = []
    if lane is None:
        commands.append({'schema_version': 1, 'op': 'track.create', 'version': '1',
                         'select': 'parent', 'args': {'row': {'id': track, 'kind': 'visual'}}})
    commands.append({'schema_version': 1, 'op': 'clip.add-media', 'version': '1',
                     'select': 'parent', 'args': {'row': row, 'media': pin}})
    # Capture/validate the entire batch before persisting its input descriptor.
    from .commands import execute

    commands = execute(bundle, commands, verified_media=[verified]).commands
    with session.outbox.locked():
        if session._state() != state:
            raise TimelineEditError('outbox changed during capture; retry the original edit first')
        state['media_input'] = copy.deepcopy(intent)
        session.outbox.write(state)
    return session.commit_many(commands, idempotency_key=idempotency_key, dry_run=dry_run,
                               via=via, verified_media=[verified], label='Add media')
