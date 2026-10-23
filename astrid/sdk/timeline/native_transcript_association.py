"""Associate an authenticated project transcript and reconcile its legacy references."""
from __future__ import annotations

import copy
import json
from urllib.parse import quote

from ._command_state import ABSENT, CommandError, equal
from ._common import TimelineEditError
from .native_source_inputs import _canonical_digest, _validate_transcript_v1

OP = 'transcript.associate'
SCHEMA = 'astrid.transcript_segment/v1'
REFERENCES = 'media.transcript.references/v1'
EXTENSION = 'haus.astrid.transcript-lane'
CONTRIBUTION = 'transcript-caption-foundry'
TRACK = CONTRIBUTION + '-track'
PIN = {'type': 'object', 'additionalProperties': False,
       'required': ['document_id', 'version', 'content_digest'], 'properties': {
           'document_id': {'type': 'string', 'pattern': '^transcript:'},
           'version': {'type': 'integer', 'minimum': 1, 'maximum': 9007199254740991},
           'content_digest': {'type': 'string', 'pattern': '^sha256:[0-9a-f]{64}$'}}}
PARAMETERS = {'type': 'object', 'additionalProperties': False,
              'required': ['asset_id', 'media_id', 'source_id', 'document',
                           'previous_document', 'source_schema_ref'], 'properties': {
                  **{key: {'type': 'string', 'minLength': 1}
                     for key in ('asset_id', 'media_id', 'source_id')},
                  'document': PIN, 'previous_document': {'anyOf': [PIN, {'type': 'null'}]},
                  'source_schema_ref': {'const': SCHEMA}}}


def fail(message, kind='unsupported_shape'):
    raise CommandError(message, kind=kind)


def obj(value, label):
    if not isinstance(value, dict):
        fail(label + ' must be an object')
    return value


def encode(value):
    return quote(value, safe="~()*!.'-_")


def prefixes(asset, source):
    return (f'transcript-source:{encode(source)}:segment:',
            f'transcript-source:{encode(asset)}:source:{encode(source)}:segment:')


def caption_id(value):
    # The persisted host IDs use FNV-1a over the JSON string, including quotes.
    result = 0xcbf29ce484222325
    for byte in json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode():
        result = ((result ^ byte) * 0x100000001b3) & 0xffffffffffffffff
    return f'transcript-caption-{result:016x}'


def resolve_transcripts(port, resolver):
    """Capture exact bytes through the request-private port at each command input."""
    def resolve(ctx):
        inputs = resolver(ctx)
        command = ctx.record['command']
        if command['op'] != OP:
            return inputs
        from .commit import _document_pin

        captures = []
        for value in (command['args']['document'], command['args']['previous_document']):
            if value is None:
                continue
            pin = _document_pin(value)
            captured = port.transcript_source(copy.deepcopy(pin))
            document = obj(captured.get('document'), 'verified transcript document')
            if (captured.get('pin') != pin or document.get('project_id') != ctx.state.bundle['project_id']
                    or document.get('document_id') != pin['document_id']
                    or type(document.get('version')) is not int or document['version'] != pin['version']
                    or _canonical_digest(document.get('content')) != pin['content_digest']):
                fail('transcript source does not match its exact scoped pin', 'invalid_source')
            try:
                _validate_transcript_v1(ctx.state.bundle['project_id'], pin, document)
            except TimelineEditError as exc:
                raise CommandError(str(exc), kind='invalid_source') from exc
            content = document['content']
            segments = content['segments']
            if (not 1 <= len(segments) <= 100000 or len(content['source_id']) > 1024
                    or any(len(segment['id']) > 1024 or len(segment['text']) > 100000
                           or isinstance(segment.get('speaker'), str) and len(segment['speaker']) > 1024
                           or len(segment.get('words', [])) > 100000
                           or any(len(word['id']) > 1024 or len(word['text']) > 100000
                                  for word in segment.get('words', [])) for segment in segments)):
                fail('transcript content is outside the project transcript limits', 'invalid_source')
            captures.append(copy.deepcopy(captured))
        ctx.transcript_inputs = captures
        return inputs
    return resolve


def source_item(row):
    row = obj(row, 'transcript source item')
    owner = obj(row.get('sourceArtifactRef'), 'transcript source owner')
    payload = obj(row.get('payload'), 'transcript source payload')
    provenance = obj(row.get('provenance'), 'transcript source provenance')
    if (row.get('schemaRef') != SCHEMA or not isinstance(row.get('id'), str) or not row['id']
            or any(not isinstance(value, str) or not value for value in
                   (owner.get('assetId'), payload.get('sourceId')))
            or payload.get('segmentId') != row['id']
            or any(not isinstance(provenance.get(key), str) for key in ('adapterId', 'adapterVersion'))):
        fail('unsupported transcript source-item envelope')
    return row


def project(source, asset):
    pin, content = source['pin'], source['document']['content']
    return [{'id': segment['id'], 'shape': 'interval', 'domain': 'source_seconds',
             'extent': {'start': segment['start'], 'end': segment['end']}, 'schemaRef': SCHEMA,
             'sourceArtifactRef': {'assetId': asset},
             'provenance': {'adapterId': 'astrid.projectTranscript', 'adapterVersion': '1'},
             'payload': {'sourceId': content['source_id'], 'segmentId': segment['id'],
                         **{key: copy.deepcopy(segment[key]) for key in ('text', 'speaker', 'words')
                            if key in segment},
                         'documentId': pin['document_id'], 'documentVersion': pin['version']}}
            for segment in content['segments']]


def reconcile(config, previous, incoming, asset, source):
    legacy, canonical = prefixes(asset, source)
    prior = {row['id'] for row in previous if row['sourceArtifactRef']['assetId'] == asset
             and row['payload']['sourceId'] == source}
    mapping = {legacy + row['id'][len(canonical):]: row['id'] for row in incoming
               if row['id'].startswith(canonical) and legacy + row['id'][len(canonical):] in prior}
    if not mapping:
        return config
    clips = config.get('clips')
    if not isinstance(clips, list):
        fail('transcript reconciliation clips must be an array')
    owners: dict[str, set[tuple[str, str]]] = {}
    for row in previous:
        owner = (row['sourceArtifactRef']['assetId'], row['payload']['sourceId'])
        old, new = prefixes(*owner)
        aliases = [row['id']]
        if row['id'].startswith(new):
            aliases.append(old + row['id'][len(new):])
        for alias in aliases:
            owners.setdefault(alias, set()).add(owner)
    suffixes = list(dict.fromkeys(suffix for clip in clips if isinstance(clip, dict)
                                and clip.get('asset') == asset and isinstance(clip.get('id'), str)
                                for suffix in ('@' + clip['id'], '@' + encode(clip['id']))))
    occupied = {clip['id'] for clip in clips if isinstance(clip, dict) and isinstance(clip.get('id'), str)}
    result = copy.deepcopy(config)
    for index, clip in enumerate(clips):
        if not isinstance(clip, dict):
            continue
        app = clip.get('app')
        generated = app.get('__generated__') if isinstance(app, dict) else None
        provenance = generated.get('provenance') if isinstance(generated, dict) else None
        if (clip.get('track') != TRACK or not isinstance(generated, dict)
                or generated.get('extensionId') != EXTENSION or generated.get('contributionId') != CONTRIBUTION
                or not isinstance(provenance, dict) or provenance.get('sourceSchemaRef') != SCHEMA
                or type(provenance.get('contractVersion')) is not int or provenance['contractVersion'] != 1):
            continue
        old = provenance.get('sourceItemId')
        if not isinstance(old, str) or old not in mapping:
            continue
        ownership = len(owners.get(old, set()))
        candidates = suffixes + (['', '@source', '@timeline'] if ownership == 1 else [])
        matches = [suffix for suffix in candidates if caption_id(old + suffix) == clip.get('id')]
        if len(matches) > 1 or not matches and ownership > 1 and caption_id(old) == clip.get('id'):
            fail('ambiguous transcript caption ownership', 'identity_conflict')
        if not matches:
            continue
        identity = caption_id(mapping[old] + matches[0])
        if identity in occupied:
            fail('transcript caption destination is occupied', 'identity_conflict')
        occupied.add(identity)
        updated = result['clips'][index]
        updated['id'] = identity
        updated['app']['__generated__']['provenance']['sourceItemId'] = mapping[old]
    app = config.get('app')
    extension = app.get(EXTENSION) if isinstance(app, dict) else None
    if isinstance(extension, dict):
        updated = result['app'][EXTENSION]
        for old, new in mapping.items():
            old_key, new_key = ('transcript-source-review:' + encode(identity) for identity in (old, new))
            review = extension.get(old_key)
            if (not isinstance(review, dict) or type(review.get('schemaVersion')) is not int
                    or review['schemaVersion'] != 1 or review.get('sourceSchemaRef') != SCHEMA
                    or review.get('sourceItemId') != old):
                continue
            if len(owners.get(old, set())) > 1:
                fail('ambiguous transcript review ownership', 'identity_conflict')
            if len(owners.get(old, set())) != 1:
                continue
            if new_key in updated:
                fail('transcript review destination is occupied', 'identity_conflict')
            del updated[old_key]
            updated[new_key] = {**copy.deepcopy(review), 'sourceItemId': new}
    return result


def associate(ctx, command):
    args, target = command['args'], command['select']
    if target != 'parent/asset:' + args['asset_id'] or '/' in args['asset_id'] or '::' in args['asset_id']:
        fail('transcript association requires its exact parent asset owner', 'identity_conflict')
    captures = getattr(ctx, 'transcript_inputs', None)
    if not captures:
        fail('association requires Runtime-authenticated transcript input', 'dependency_changed')
    source = captures[0]
    previous = captures[1] if len(captures) == 2 else None
    if source['pin'] != args['document'] or (previous['pin'] if previous else None) != args['previous_document']:
        fail('transcript source does not match command pins', 'capture_mismatch')
    asset = ctx.read(target)
    media = asset.get('media_id', asset.get('content_sha256'))
    content = source['document']['content']
    if (media != args['media_id'] or media != content['media_id'] or args['source_id'] != content['source_id']
            or previous and previous['document']['content']['media_id'] != media):
        fail('transcript source owner differs from command', 'invalid_source')
    initial = ctx.state.bundle['source_mapping']['_runtime_document']
    if media not in {pin['media_id'] for pin in initial['dependency_manifest']['media']}:
        fail('transcript media is outside the authenticated input closure', 'invalid_source')
    parent = ctx.state.bundle['parent']
    config = obj(ctx.read('parent', ['config']), 'parent config')
    for carrier in (parent, config, parent.get('bundle', {})):
        if isinstance(carrier, dict) and any(key in carrier for key in ('transcriptReferences', 'sourceItemsBySchemaRef')):
            fail('transcript source planes must use parent.config.bundle')
    carrier = obj(config.get('bundle', {}), 'parent.config.bundle')
    if 'sourceItemsBySchemaRef' in carrier:
        fail('transcript source items must use persisted itemsBySchemaRef')
    refs_path = ['config', 'bundle', 'transcriptReferences']
    items_path = ['config', 'bundle', 'itemsBySchemaRef']
    refs_value = ctx.read('parent', refs_path)
    refs = ({'schema': REFERENCES, 'associations': []} if ctx.state.get('parent', refs_path) == ABSENT
            else obj(refs_value, 'transcript references'))
    associations = refs.get('associations')
    if refs.get('schema') != REFERENCES or not isinstance(associations, list):
        fail('transcript reference plane is unsupported')
    if (any(not isinstance(row, dict) or not isinstance(row.get('assetId'), str)
            or not isinstance(row.get('documentId'), str) for row in associations)
            or len({row['assetId'] for row in associations}) != len(associations)):
        fail('ambiguous transcript association ownership', 'identity_conflict')
    existing = next((row for row in associations if row['assetId'] == args['asset_id']), None)
    if (existing is None and previous is not None or existing is not None
            and (previous is None or existing['documentId'] != previous['pin']['document_id'])):
        fail('exact prior DocumentPin is required for replacement', 'history_unavailable')
    items_value = ctx.read('parent', items_path)
    items = {} if ctx.state.get('parent', items_path) == ABSENT else obj(items_value, 'transcript source items')
    rows = items.get(SCHEMA, [])
    if not isinstance(rows, list):
        fail('transcript source item collection must be an array')
    rows = [source_item(row) for row in rows]
    keys = [(row['sourceArtifactRef']['assetId'], row['payload']['sourceId'], row['id']) for row in rows]
    if len(set(keys)) != len(keys):
        fail('ambiguous existing transcript source-item identity', 'identity_conflict')
    if previous:
        prior_pin = previous['pin']
        manifest = ctx.state.bundle['source_mapping'].get('_copy_manifest', initial['dependency_manifest'])
        retained = [pin for pin in manifest['documents']
                    if pin['document_id'] == prior_pin['document_id']]
        scoped = [row['payload'] for row in rows if row['sourceArtifactRef']['assetId'] == args['asset_id']
                  and row['payload'].get('documentId') == prior_pin['document_id']]
        if (retained and prior_pin not in retained or any(
                payload.get('documentVersion') != prior_pin['version'] for payload in scoped)):
            fail('prior transcript pin differs from the input association', 'history_unavailable')
    projected = project(source, args['asset_id'])
    reconciled = reconcile(config, rows, projected, args['asset_id'], args['source_id'])
    # Everything that can refuse above runs before the first authored write.
    ctx.bind('transcript.owner', target)
    for row in projected:
        ctx.bind('transcript.segment:' + row['id'], target)
        for word in row['payload'].get('words', []):
            ctx.bind('transcript.word:' + word['id'], target)
    ctx.dependency('transcript.document', 'transcript', source['pin'])
    if previous:
        ctx.dependency('transcript.previous', 'transcript', previous['pin'])
    retained_rows = [row for row in rows if row['sourceArtifactRef']['assetId'] != args['asset_id']
                     or row['provenance']['adapterId'] != 'astrid.projectTranscript'
                     and row['payload']['sourceId'] != args['source_id']]
    next_refs = {**copy.deepcopy(refs), 'associations': [copy.deepcopy(row) for row in associations
                 if row['assetId'] != args['asset_id']] + [
                     {'assetId': args['asset_id'], 'documentId': source['pin']['document_id']}]}
    ctx.object('parent', ['config', 'bundle'])
    ctx.write('parent', refs_path, next_refs)
    ctx.write('parent', items_path, {**copy.deepcopy(items), SCHEMA: retained_rows + projected})
    if not equal(config.get('clips'), reconciled.get('clips')):
        ctx.read('parent', ['clips'])
        ctx.write('parent', ctx.state.parent_clip_path, reconciled['clips'])
    if not equal(config.get('app'), reconciled.get('app')):
        ctx.write('parent', ['config', 'app', EXTENSION], reconciled['app'][EXTENSION])
    mapping = ctx.state.bundle['source_mapping']
    manifest = mapping.setdefault('_copy_manifest', copy.deepcopy(initial['dependency_manifest']))
    for capture in captures:
        if capture['pin'] not in manifest['documents']:
            manifest['documents'].append(copy.deepcopy(capture['pin']))
        if capture not in mapping.setdefault('pinned_documents', []):
            mapping['pinned_documents'].append(copy.deepcopy(capture))
