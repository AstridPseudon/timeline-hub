"""Typed pinned-group retention/dependencies inside composition acceptance."""
from __future__ import annotations

import json
import re

from .shot_group_schema import SHOT_GROUP_SCHEMA

from .errors import ValidationError

def _shape(value, schema):
    """Enforce the small closed schema subset used by this stored row."""
    kind = schema.get("type")
    matches = {"object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str)}
    if kind is not None and not matches.get(kind, False):
        return False
    if "enum" in schema and value not in schema["enum"]:
        return False
    if isinstance(value, str) and (len(value) < schema.get("minLength", 0) or
            "pattern" in schema and re.search(schema["pattern"], value) is None):
        return False
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            return False
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            return False
        if "items" in schema and not all(_shape(v, schema["items"]) for v in value):
            return False
    if isinstance(value, dict):
        if not set(schema.get("required", [])) <= set(value):
            return False
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and set(value) - set(properties):
            return False
        if any(not _shape(v, properties[k]) for k, v in value.items() if k in properties):
            return False
    return True


def validate_groups(parent, occurrences, shots, internal):
    """Return exact media dependencies, including dormant snapshot references.

    Asset namespaces come from the captured member owner, never a union of
    sibling registries. Legacy groups without selectors must prove one owner.
    """
    schema = SHOT_GROUP_SCHEMA
    rows = parent.get('config', {}).get('pinnedShotGroups', [])
    if not isinstance(rows, list):
        raise ValidationError('pinnedShotGroups must be an array')
    seen, dependencies = set(), set()
    for row in rows:
        if not _shape(row, schema):
            raise ValidationError('invalid typed pinned shot group')
        key = (row['shotId'], row['trackId'])
        if key in seen:
            raise ValidationError('duplicate pinned shot group key')
        seen.add(key)
        selectors = row.get('memberSelectors', [])
        scopes = {s.split('/clip:', 1)[0] for s in selectors}
        if not selectors:
            # Legacy rows: only unambiguous authored membership grants scope.
            candidates = []
            if all(any(c.get('id') == local for c in parent.get('clips', [])) for local in row['clipIds']):
                candidates.append('parent')
            for occurrence in occurrences:
                if row['shotId'] not in {occurrence['shot_id'], occurrence['occurrence_id']}:
                    continue
                shot = shots[(occurrence['shot_id'], occurrence['shot_revision_id'])]
                child = next(v['payload'] for v in internal.values() if v['revision_id'] == shot['internal_timeline_revision_id'])
                if all(any(c.get('id') == local for c in child.get('clips', [])) for local in row['clipIds']):
                    candidates.append('occurrence:' + occurrence['occurrence_id'])
            scopes = set(candidates)
        if len(scopes) != 1:
            raise ValidationError('pinned shot group has missing or ambiguous member owner')
        scope = next(iter(scopes))
        owner = parent
        if scope != 'parent':
            matches = [o for o in occurrences if 'occurrence:' + o['occurrence_id'] == scope]
            if len(matches) != 1 or (row.get('ownerOccurrenceId') != matches[0]['occurrence_id'] and row['shotId'] not in {matches[0]['shot_id'], matches[0]['occurrence_id']}):
                raise ValidationError('pinned shot group owner does not match shot')
            shot = shots[(matches[0]['shot_id'], matches[0]['shot_revision_id'])]
            owner = next(v['payload'] for v in internal.values() if v['revision_id'] == shot['internal_timeline_revision_id'])
        clips = owner.get('clips', [])
        selected = []
        for local in row['clipIds']:
            matches = [c for c in clips if c.get('id') == local]
            if len(matches) != 1:
                raise ValidationError('pinned shot group member missing or ambiguous')
            selected.append(matches[0])
        if selectors and selectors != [scope + '/clip:' + c['id'] for c in selected]:
            raise ValidationError('pinned shot group scoped membership mismatch')
        if any(c.get('track') != row['trackId'] for c in selected):
            raise ValidationError('pinned shot group track mismatch')
        registry = owner.get('registry', owner.get('config', {}).get('registry', {}))
        parent_registry = parent.get('registry', parent.get('config', {}).get('registry', {}))
        assets = {**parent_registry.get('assets', {}), **registry.get('assets', {})}
        def asset(key):
            if not isinstance(key, str) or key not in assets or not isinstance(assets[key], dict):
                raise ValidationError('pinned shot group references missing assetKey/videoAssetKey')
            entry = assets[key]
            media = entry.get('media_id', entry.get('object_id'))
            if not isinstance(media, str):
                raise ValidationError('pinned shot group asset has no canonical media identity')
            import re
            if not re.fullmatch(r'(?:sha256:)?[a-f0-9]{64}', media):
                raise ValidationError('pinned shot group asset has invalid media identity')
            dependencies.add('sha256:' + media.removeprefix('sha256:'))
        if 'videoAssetKey' in row:
            asset(row['videoAssetKey'])
        dormant = set()
        for snapshot in row.get('imageClipSnapshot', []):
            if 'assetKey' in snapshot:
                asset(snapshot['assetKey'])
            authored = snapshot.get('authoring')
            if authored is None:
                continue  # retained compatibility snapshot; asset dependency still checked
            selector = authored['selector']
            clip = authored['clip']
            if selector != scope + '/clip:' + clip.get('id', '') or selector in dormant:
                raise ValidationError('invalid dormant snapshot identity')
            dormant.add(selector)
            if clip.get('asset') != snapshot.get('assetKey'):
                raise ValidationError('snapshot assetKey disagrees with retained clip')
            if row.get('mode') == 'video' and any(c.get('id') == clip['id'] for c in clips):
                raise ValidationError('dormant snapshot ID collides with active clip')
    return dependencies
