"""Recorded App defaults on the Runtime's pristine empty publication."""
from __future__ import annotations

from ._command_state import ABSENT, CommandError, equal

_EMPTY_STRUCTURAL_PATHS = (
    ('tracks',), ('clips',), ('occurrences',), ('placements',), ('shots',),
    ('groups',), ('pinnedShotGroups',), ('media',), ('references',),
    ('reference',), ('assets',), ('registry', 'assets'),
)


def _at_path(value, path):
    for token in path:
        if not isinstance(value, dict) or token not in value:
            return ABSENT
        value = value[token]
    return value


def _require_empty_structure(config, record):
    if record['created']:
        raise CommandError('raw initialization cannot create structural entities', kind='unrecorded_birth')
    for path in _EMPTY_STRUCTURAL_PATHS:
        value = _at_path(config, path)
        if value != ABSENT and value not in ([], {}):
            raise CommandError(
                'nonempty raw initialization structure requires recorded creation facts',
                kind='unrecorded_birth', path=path,
            )


def initialize(ctx, command):
    bundle = ctx.state.bundle
    parent = ctx.read('parent')
    if (ctx.record['ordinal'] != 0
            or not equal(parent, {'config': {'clips': [], 'tracks': []}, 'registry': {}, 'clips': []})
            or bundle['placements'] or bundle['shots']):
        raise CommandError('initialization requires the pristine empty timeline', kind='not_pristine')
    if command['version'] == '2':
        args = command['args']
        ctx.read('parent', ['config'])
        for path in (['name'], ['slug']):
            ctx.read('parent', path)
            if ctx.state.get('parent', path) != ABSENT:
                raise CommandError('initialization field is already authored', kind='not_pristine')
        _require_empty_structure(args['config'], ctx.record)
        ctx.write('parent', ['config'], args['config'])
        ctx.write('parent', ['name'], args['name'])
        ctx.write('parent', ['slug'], args['slug'])
        return
    for path in (['config', 'output'], ['name'], ['slug'], ['registry', 'assets']):
        ctx.read('parent', path)
        if ctx.state.get('parent', path) != ABSENT:
            raise CommandError('initialization field is already authored', kind='not_pristine')
    args = command['args']
    ctx.write('parent', ['config', 'output'], args['output'])
    ctx.write('parent', ['name'], args['name'])
    ctx.write('parent', ['slug'], args['slug'])
    ctx.write('parent', ['registry', 'assets'], {})


def capture_initialize_raw(bundle, *, name, slug, config):
    """Capture authored raw config on the authenticated pristine publication."""
    from .commands import execute

    command = {'schema_version': 1, 'op': 'timeline.init', 'version': '2',
               'select': 'parent',
               'args': {'name': name, 'slug': slug, 'config': config}}
    return execute(bundle, [command]).commands[0]


def capture_initialize(bundle, *, name, slug, output):
    """Capture raw defaults; publication-history authority stays in the provider.

    Append full V1 then A1 track.create captures over each preceding local result.
    Persist the resulting batch and its original base pair before sending it.
    """
    from .commands import execute

    command = {'schema_version': 1, 'op': 'timeline.init', 'version': '1',
               'select': 'parent', 'args': {'name': name, 'slug': slug, 'output': output}}
    return execute(bundle, [command]).commands[0]
