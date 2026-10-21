"""Occurrence-owned immutable UTF-8 text bindings; live heads belong to Runtime."""
from __future__ import annotations

import copy
import hashlib
import re

from ._command_state import ABSENT, CommandError, equal

TEXT_INTENT = {'ownership': 'occurrence'}
TEXT_MEDIA_TYPE = 'text/plain; charset=utf-8'
LEGACY_INLINE_SOURCE = 'main-inline-voiceover-v1'
DERIVED_FIELDS = {'binding_id', 'project_id', 'shot_id', 'head', 'event_stream_id',
                  'created_at', 'updated_at', 'text'}


def _legacy_inline_voiceover(row):
    return (isinstance(row, dict) and row.get('slot') == 'voiceover'
            and 'kind' not in row and isinstance(row.get('text'), str))


def binding_key(row):
    if _legacy_inline_voiceover(row):
        return 'voiceover_script'
    kind, slot = row.get('kind'), row.get('slot')
    if (kind not in ('prompt', 'voiceover_script', 'transcript')
            or (slot is not None and (kind != 'prompt' or not isinstance(slot, str)
                                     or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', slot)))):
        raise CommandError('unsupported text binding identity', kind='unsupported_shape')
    return kind + (':' + slot if slot is not None else '')


def binding_rows(state, owner):
    shot = state.occurrence(owner)['shot_id']
    rows = state.bundle['shots'][shot]['payload'].get('text_bindings', [])
    if not isinstance(rows, list) or any(
            not isinstance(row, dict)
            or (not _legacy_inline_voiceover(row) and not {
                'kind', 'slot', 'media_id', 'content_hash', 'byte_size', 'mime_type'} <= row.keys())
            for row in rows):
        raise CommandError('text bindings require immutable descriptors', kind='unsupported_shape')
    keys = [binding_key(row) for row in rows]
    if len(keys) != len(set(keys)):
        raise CommandError('ambiguous text binding identity', kind='identity_conflict')
    return rows


def text_binding_set(ctx, command):
    owner, args = command['select'], command['args']
    if not isinstance(owner, str) or not re.fullmatch(r'occurrence:(?!.*::)[^/]+', owner):
        raise CommandError('text binding requires explicit occurrence ownership')
    ctx.read(owner, ['occurrence_id'])
    ctx.read(owner + '/shot', ['shot_id'])
    if ctx.select('text-binding.owners', owner) != [owner]:
        raise CommandError('text binding requires an exclusive occurrence', kind='unsupported_ownership')
    ref = owner + '/text-binding:' + binding_key(args['binding'])
    old = ctx.read(ref)
    legacy_source = args.get('legacy_source')
    if legacy_source is None and _legacy_inline_voiceover(old):
        raise CommandError('legacy inline text binding is not a registered binding',
                           kind='unsupported_shape', ref=ref)
    if legacy_source is not None:
        if (legacy_source != LEGACY_INLINE_SOURCE
                or set(args) != {'binding', 'text', 'legacy_source'}
                or args['binding'] != {'kind': 'voiceover_script', 'slot': None}
                or not _legacy_inline_voiceover(old)):
            raise CommandError('legacy inline migration requires its exact voiceover row',
                               kind='unsupported_shape', ref=ref)
        try:
            encoded = old['text'].encode('utf-8', 'strict')
        except (UnicodeEncodeError, UnicodeDecodeError) as exc:
            raise CommandError('legacy inline text is not strict UTF-8',
                               kind='unsupported_shape', ref=ref) from exc
        digest = 'sha256:' + hashlib.sha256(encoded).hexdigest()
        expected = {'object_id': digest, 'digest': digest, 'size': len(encoded),
                    'media_type': TEXT_MEDIA_TYPE}
        pin = args['text']
        if not equal(pin, expected):
            raise CommandError('legacy inline bytes do not match text descriptor',
                               kind='dependency_changed', ref=ref)
        if not any(equal(value, {**pin, 'utf8': True}) for value in ctx.verified_media):
            raise CommandError('text binding requires exact Runtime-verified UTF-8 input',
                               kind='dependency_changed')
        ctx.select('collection.text-bindings', owner)
    if 'clear' in args:
        if ctx.state.get(ref, []) == ABSENT:
            raise CommandError('cannot clear an absent text binding', kind='absent_binding', ref=ref)
        ctx.select('collection.text-bindings', owner)
        ctx.clear(ref, [])
        return
    pin = args['text']
    if pin['object_id'] != pin['digest']:
        raise CommandError('text object id must equal its content digest', ref=ref)
    if not any(equal(value, {**pin, 'utf8': True}) for value in ctx.verified_media):
        raise CommandError('text binding requires exact Runtime-verified UTF-8 input', kind='dependency_changed')
    if old is None:
        path = ['payload', 'text_bindings']
        if ctx.state.get(owner + '/shot', path) == ABSENT:
            ctx.read(owner + '/shot', path)
            ctx.write(owner + '/shot', path, [])
        ctx.select('collection.text-bindings.append', owner)
    ctx.dependency('text:' + pin['digest'], 'media', pin)
    row = {key: copy.deepcopy(value) for key, value in (old or {}).items() if key not in DERIVED_FIELDS}
    row.update(args['binding'], media_id=pin['object_id'], content_hash=pin['digest'],
               byte_size=pin['size'], mime_type=pin['media_type'])
    ctx.write(ref, [], row)


def capture_text_binding_set(bundle, owner, binding, *, text=None, clear=False, verified_text=(),
                             legacy_source=None):
    from .commands import execute

    args = {'binding': copy.deepcopy(binding)}
    if text is not None:
        args['text'] = copy.deepcopy(text)
    if clear:
        args['clear'] = True
    if legacy_source is not None:
        args['legacy_source'] = legacy_source
    return execute(bundle, [{'schema_version': 1, 'op': 'text-binding.set', 'version': '1',
                             'select': owner, 'args': args, 'intent': TEXT_INTENT}],
                   verified_media=verified_text).commands[0]
