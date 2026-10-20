"""The one-time guarded initialization of a pristine empty parent."""
from __future__ import annotations

import copy

from ._command_state import CommandError, equal

# The Runtime bootstrap publishes exactly this (occurrences open as bundle placements);
# anything else is authored.
_EMPTY = {'config': {'clips': [], 'tracks': []}, 'registry': {}, 'clips': []}
_READS = (['config'], ['registry'], ['clips'], ['name'], ['slug'])


def timeline_init(ctx, command):
    bundle = ctx.state.bundle
    if not equal(bundle['parent'], _EMPTY) or bundle['placements'] or bundle['shots']:
        raise CommandError('timeline.init requires the pristine empty bootstrap',
                           kind='not_pristine', ref='parent')
    for path in _READS:
        ctx.read('parent', path)
    args = command['args']
    ctx.write('parent', ['config', 'output'], args['output'])
    ctx.write('parent', ['name'], args['name'])
    ctx.write('parent', ['slug'], args['slug'])
    ctx.write('parent', ['registry'], {'assets': {}})


def capture_timeline_init(bundle, *, name, slug, output):
    from .commands import execute

    return execute(bundle, [{
        'schema_version': 1,
        'op': 'timeline.init',
        'version': '1',
        'select': 'parent',
        'args': copy.deepcopy({'name': name, 'slug': slug, 'output': output}),
    }]).commands[0]
