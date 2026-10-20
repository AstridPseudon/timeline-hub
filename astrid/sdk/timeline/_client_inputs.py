"""Bounded public Runtime reads for native capture, outside the pure recipes."""
from __future__ import annotations

import base64
import copy

from ._command_state import CommandError, equal
from .commit import _digest, _document_pin, _schema_resolver


class CaptureInputs:
    def __init__(self, client, project_id, realm_id):
        self.transport = client._remote._transport
        self.project_id, self.realm_id = project_id, realm_id
        self.media, self.schemas = [], []
        self.schema_resolver = _schema_resolver(self, self.schemas, ())

    def document_object(self, pin, object_id):
        verified = next(row for row, _ in self.schemas if equal(row['pin'], pin))
        descriptors = [a['snapshot_object'] for a in verified['document']['content']['admissions']
                       if a.get('snapshot_object', {}).get('object_id') == object_id]
        if not descriptors or any(not equal(row, descriptors[0]) for row in descriptors):
            raise CommandError('selected pack snapshot descriptor unavailable')
        data = self.transport.get_object(object_id)['data']
        return {**copy.deepcopy(descriptors[0]), 'bytes_base64': base64.b64encode(data).decode('ascii')}

    def resolve(self, ctx):
        args = ctx.record['command']['args']
        for key in ('old_media', 'media'):
            pin = args.get(key)
            if pin is not None and not any(equal(row['selection'], pin) for row in self.media):
                value = self.transport.get_project_verified_media(self.project_id, copy.deepcopy(pin))
                if not equal(value.get('selection'), pin):
                    raise CommandError('Runtime returned a different media selection')
                self.media.append(value)
        ctx.verified_media = self.media
        pin = args.get('schema_source')
        if pin is not None and not any(equal(row['pin'], pin) for row, _ in self.schemas):
            pin = _document_pin(pin)
            row = self.transport.get_document(self.project_id, pin['document_id'])
            # Public Document reads expose the current version only. An older
            # pin must refuse here, never fall forward to its replacement schema.
            if (row.get('project_id') != self.project_id or row.get('kind') != 'astrid.project-pack'
                    or not equal(row.get('version'), pin['version'])
                    or row.get('document_id') != pin['document_id']
                    or _digest(row.get('content')) != pin['content_digest']):
                raise CommandError('exact selected pack document version unavailable')
            self.schemas.append(({'pin': copy.deepcopy(pin), 'document': row}, {}))
        return self.schema_resolver(ctx)

    def execute(self, bundle, commands):
        from .commands import execute

        return execute(bundle, commands, realm_id=self.realm_id, resolve_inputs=self.resolve)
