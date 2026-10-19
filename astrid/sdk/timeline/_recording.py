"""Instrumented authored-state primitives. Handlers never manufacture records."""
from __future__ import annotations

import copy

from ._command_state import ABSENT, CommandError, State, equal, present, spelling
from ._common import AUDIO_KINDS


def active(row):
    return (row.get('enabled') is not False and row.get('active') is not False
            and not any(row.get(key) is True for key in ('disabled', 'hidden', 'deleted')))


def selection(state, key, owner, members=()):
    if key == "move.target":
        result = [ref for ref in members if state.entity(ref, optional=True) is not None]
    elif key == "track.create":
        result = [owner + '/track:' + row['id'] for row in state.collection(owner, 'track')]
    elif key == "move.blockers":
        origin = state.occurrence(owner)
        lane = (origin.get('placement') or {}).get('track', origin.get('track'))
        track = state.entity('parent/track:' + lane, optional=True) if isinstance(lane, str) else None
        output = track is None or (track.get('kind') not in AUDIO_KINDS
                                   and track.get('role') not in AUDIO_KINDS and active(track))
        result = []
        for row in state.bundle['placements']:
            if output and active(row) and (row.get('placement') or {}).get('track', row.get('track')) == lane:
                result.append('occurrence:' + row['occurrence_id'])
    else:
        raise CommandError(f"unsupported recorded query {key!r}")
    return {"key": key, "query_version": 1, "owner": owner, "members": result,
            "order": list(result), "boundaries": list(result), "policy": "guard-membership"}


class Recording:
    def __init__(self, bundle, command, ordinal, *, closures=None):
        self.state = State(bundle, closures=closures)
        self.record = {"ordinal": ordinal, "command": copy.deepcopy(command), "writes": [],
                       "reads": [], "selections": [], "bindings": [], "created": [],
                       "dependencies": [], "derived_writes": []}

    def read(self, ref, path=()):
        value = self.state.get(ref, path)
        read = {"ref": ref, "path": list(path), "state": value}
        if not any(equal(read, prior) for prior in self.record['reads']):
            self.record['reads'].append(read)
        return copy.deepcopy(value.get('value'))

    def select(self, key, owner, members=()):
        value = selection(self.state, key, owner, members)
        if value not in self.record['selections']:
            self.record['selections'].append(value)
        return value['members']

    def bind(self, key, ref, *, dependencies=()):
        self.record['bindings'].append({"key": key, "ref": ref, "policy": "fixed",
                                        "dependencies": list(dependencies)})

    def dependency(self, key, kind, pin):
        self.record['dependencies'].append({"key": key, "kind": kind,
                                            "pin": copy.deepcopy(pin), "policy": "exact"})

    def assign(self, ref, path, after):
        before = self.state.get(ref, path)
        self.record['writes'].append({"ref": ref, "path": list(path),
                                       "before": before, "after": copy.deepcopy(after)})
        self.state.set(ref, path, after)

    def write(self, ref, path, value):
        self.assign(ref, path, present(value))

    def clear(self, ref, path):
        self.assign(ref, path, ABSENT)

    def object(self, ref, path):
        value = self.state.get(ref, path)
        if value['state'] == 'present' and isinstance(value['value'], dict):
            return
        self.read(ref, path)
        if value['state'] == 'present' and value['value'] is not None:
            raise CommandError("intent container must be object or null", ref=ref, path=path)
        self.write(ref, path, {})

    def create(self, owner, kind, row):
        if not isinstance(self.state.config(owner).get(kind + 's'), list):
            raise CommandError('structural create requires an authored entity collection', ref=owner)
        if owner != 'parent':
            self.read(owner, ['occurrence_id'])
            self.read(owner + '/shot', ['shot_id'])
            self.bind('create.owner', owner)
        self.select('track.create', owner)
        ref = owner + '/' + kind + ':' + row['id']
        if self.state.get(ref, []) != ABSENT:
            raise CommandError("created identity is occupied", kind="identity_collision", ref=ref)
        self.read(ref)
        self.write(ref, [], row)
        self.record['created'].append({"ref": ref, "kind": kind, "owner": owner})
        return ref

    def create_entity(self, ref, *, kind, owner, value):
        from ._command_state import root_identity

        root = root_identity(ref)
        if (root is None or root[0] != kind
                or owner != (None if kind == 'shot' else 'parent')):
            raise CommandError('invalid created root scope', ref=ref)
        self.state.validate_root(ref, value)
        document = self.state.bundle['source_mapping'].get('_runtime_document', {})
        occupied = (any(row['shot_id'] == root[1] for row in document.get('shot_revisions', []))
                    if kind == 'shot' else any(row['occurrence_id'] == root[1] for row in
                        document.get('parent_revision', {}).get('payload', {}).get('occurrences', [])))
        if not document:
            mapping = self.state.bundle['source_mapping']
            occupied = (any(row['shot_id'] == root[1] for row in mapping['shots'].values())
                        if kind == 'shot' else root[1] in mapping['placements'])
        if occupied or self.state.get(ref, []) != ABSENT or any(
                item['ref'] == ref for item in self.record['created']):
            raise CommandError('created identity is occupied', kind='identity_collision', ref=ref)
        self.read(ref)
        self.write(ref, [], value)
        if kind == 'shot':
            self.state.bundle['shots'][root[1]]['_created'] = True
        self.record['created'].append({'ref': ref, 'kind': kind, 'owner': owner})
        return ref

    def compile_inputs(self):
        # The compiler retains this immutable input closure. These pins do not
        # imply that the move evaluated an anchor or any document settings.
        mapping = self.state.bundle.get('source_mapping', {})
        retained = mapping.get('_runtime_document', {}).get('dependency_manifest', {}).get('documents', [])
        from astrid.core.timeline.authoring_bundle import _digest
        for capture in mapping.get('pinned_documents', []):
            pin = capture['pin']
            if pin in retained:
                kind = 'transcript' if capture['document']['kind'] == 'media.transcript' else 'source'
                self.dependency('compile.document:' + _digest(pin), kind, pin)

    def compile_mirrors(self):
        parent = self.state.bundle['parent']
        config = parent.get('config', {})
        if parent.get('clips') and config.get('clips'):
            before = self.state.get('parent', ['config', 'clips'])
            after = present(parent['clips'])
            if not equal(before, after):
                self.record['derived_writes'].append({
                    "ref": "parent", "path": ['config', 'clips'], "before": before,
                    "after": after, "cause": self.record['ordinal']})
                self.state.set('parent', ['config', 'clips'], after)

    def finish(self, *, capture=False):
        command = self.record['command']
        if capture:
            command['reads'] = copy.deepcopy(self.record['reads'])
            command['selections'] = copy.deepcopy(self.record['selections'])
            command['bindings'] = {b['key']: b['ref'] for b in self.record['bindings']
                                   if '/clip:' in b['ref'] or '/track:' in b['ref']
                                   or (b['ref'].startswith('occurrence:') and '/' not in b['ref'])}
            command['created'] = [item['ref'] for item in self.record['created']]
            command['expect'], command['authorship'] = {}, {}
            for write in self.record['writes']:
                # Whole-closure guards use the schema's general read refs. The
                # legacy authored-property TargetKey cannot spell this scope.
                if write['ref'] == 'timeline':
                    continue
                key = write['ref'] + '::' + spelling(write['path'])
                command['expect'].setdefault(key, copy.deepcopy(write['before']))
                command['authorship'][key] = 'direct'
        return self.record


def guard(state, ref, path, expected, *, kind='dependency_changed'):
    actual = state.get(ref, path)
    if not state.matches(ref, path, expected):
        raise CommandError("original authored guard changed", kind=kind, ref=ref, path=path,
                           base=expected, theirs=actual)
