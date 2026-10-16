"""Trusted V3 build inputs for the native Composition consumer.

Like the App build, the operator supplies JSON ASTRID_COMPONENTS (exact identity
and implementation_digest) and ASTRID_COMPONENT_PACK_ROOTS. Timeline/browser
props never supply source paths or executable authority.
"""
from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path

from astrid.core.pack.component_consumer import stage_components
from astrid.sdk.timeline.commands import CommandError


def stage_render_components(timeline, *, output: Path, environment: Mapping[str, str] | None = None):
    env = os.environ if environment is None else environment
    references = {
        row['element']
        for clip in timeline.get('clips', [])
        for row in clip.get('modifiers', [])
        if str(row.get('element', '')).startswith('timeline.component/')
    }
    raw = env.get('ASTRID_COMPONENTS')
    if not raw:
        if references:
            raise CommandError('native export requires explicit component identity/digest selection')
        return None
    requests = json.loads(raw)
    roots = json.loads(env.get('ASTRID_COMPONENT_PACK_ROOTS', '[]'))
    if (not isinstance(requests, list) or not requests
            or any(not isinstance(row, dict) or set(row) != {'identity', 'implementation_digest'}
                   or not isinstance(row['identity'], str)
                   or not isinstance(row['implementation_digest'], str) for row in requests)):
        raise CommandError('native export requires exact component identity/digest requests')
    if (not isinstance(roots, list) or not roots
            or any(not isinstance(root, str) or not Path(root).is_absolute()
                   or not Path(root).is_dir() for root in roots)):
        raise CommandError('native export requires explicit absolute trusted component roots')
    if not references.issubset({row['identity'] for row in requests}):
        raise CommandError('native export component selection does not cover timeline identities')
    # The shared discovery can inspect installed/environment packs too. Only
    # this build's explicitly supplied roots may contribute executable bytes.
    from astrid.core.pack.components import resolve_component
    for request in requests:
        component = resolve_component(request['identity'], extra_pack_roots=tuple(roots))
        if not any(component.pack_root.resolve().is_relative_to(Path(root).resolve()) for root in roots):
            raise CommandError('native export component is outside trusted roots')
    projection = stage_components(requests, trusted_roots=roots, output=output, host='composition')
    return {**projection, 'root': str(output.resolve())}
