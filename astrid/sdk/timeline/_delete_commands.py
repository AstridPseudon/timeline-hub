"""Bounded parent clip removal; semantic dependency resolution is a later slice."""
from __future__ import annotations

import re

from ._command_state import CommandError

# Declared main intent only (astrid_ns / timeline_intent / reflow); never scan
# arbitrary strings or opaque extension JSON for possible references.
RELATIONS = ('on', 'until', 'until_film_end', 'cut', 'formulas', 'sequence', 'sequence_index',
             'sequence_fit', 'sequence_shape_from', 'segment', 'words', 'beats',
             'slot', 'replaces', 'standin', 'standin_for', 'intended', 'group', 'duck')


def _unrelated(ctx, ref, prefixes, keys):
    for prefix in prefixes:
        for key in keys:
            value = ctx.read(ref, [*prefix, key])
            if value is not None and value != '' and value != {} and value != []:
                raise CommandError('clip.delete cannot prove declared semantic dependencies safe',
                                   kind='unsupported_dependency', ref=ref, path=[*prefix, key])


def removable(ctx, ref):
    """Guard that one parent clip can be removed; reads only, so a caller may then create and clear."""
    if not isinstance(ref, str) or re.fullmatch(r'parent/clip:(?!.*::)[^/]+', ref) is None:
        raise CommandError('clip.delete v1 requires one parent clip identity', kind='unsupported_ownership')
    members = ctx.select('collection.clips', 'parent')
    if ref not in members:
        raise CommandError('delete target disappeared', kind='identity_conflict', ref=ref)
    # Removing the complete authored row consumes every source/opaque field;
    # this explicit read is also the original-state guard for portable capture.
    row = ctx.read(ref)
    if row.get('clipType') == 'shot' or row.get('clip_type') == 'shot':
        raise CommandError('clip.delete cannot remove legacy shot ownership', kind='unsupported_ownership', ref=ref)
    if any(row.get(key) is not None for key in ('clips', 'children')):
        raise CommandError('clip.delete cannot remove nested clip ownership', kind='unsupported_ownership', ref=ref)
    owners = ['parent', *ctx.select('collection.occurrences', 'parent')]
    for owner in owners:
        config_ref, prefix = ('parent', ['config']) if owner == 'parent' else (owner + '/source', [])
        _unrelated(ctx, config_ref, [prefix], ('pinnedShotGroups',))
        _unrelated(ctx, config_ref, [prefix, [*prefix, 'app'], [*prefix, 'app', 'astrid']],
                   ('sequences', 'formulas', 'slots'))
        for member in ctx.select('collection.clips', owner):
            _unrelated(ctx, member, [[]], ('transition',))
            _unrelated(ctx, member, [['app'], ['app', 'astrid']], RELATIONS)
    return row


def delete(ctx, command):
    ref = command['select']
    removable(ctx, ref)
    ctx.clear(ref, [])
