"""Instrumented authored-state primitives. Handlers never manufacture records."""
from __future__ import annotations

import copy

from ._collections import KINDS, order, rows
from ._command_state import ABSENT, CommandError, State, equal, present, spelling
from ._common import AUDIO_KINDS


def active(row):
    return (row.get('enabled') is not False and row.get('active') is not False
            and not any(row.get(key) is True for key in ('disabled', 'hidden', 'deleted')))


def selection(state, key, owner, members=()):
    boundaries = None
    if key == "move.target":
        result = [ref for ref in members if state.entity(ref, optional=True) is not None]
    elif key in KINDS:
        result = ([] if owner != 'parent' and state.entity(owner, optional=True) is None
                  else order(state, owner, KINDS[key]))
    elif key == 'placement.owners':
        shot = state.occurrence(owner)['shot_id']
        result = ['occurrence:' + row['occurrence_id'] for row in state.bundle['placements']
                  if row['shot_id'] == shot]
        boundaries = ['shot:' + shot]
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
            "order": list(result), "boundaries": list(result) if boundaries is None else boundaries,
            "policy": "guard-membership"}


class Recording:
    def __init__(self, bundle, command, ordinal, *, closures=None, verified_media=()):
        self.state = State(bundle, closures=closures)
        self.verified_media = copy.deepcopy(verified_media)
        self.input_state = None
        self.command_input = State(copy.deepcopy(bundle), closures=closures)
        parent = bundle['parent']
        config = parent.get('config')
        self.mirrored_clips = (isinstance(parent.get('clips'), list)
                               and isinstance(config, dict) and isinstance(config.get('clips'), list)
                               and equal(parent['clips'], config['clips']))
        self.record = {"ordinal": ordinal, "command": copy.deepcopy(command), "writes": [],
                       "reads": [], "selections": [], "bindings": [], "created": [],
                       "dependencies": [], "derived_writes": []}

    def capture_input(self):
        """Keep inverse claims on its immutable head, separate from reverse stages."""
        self.input_state = State(copy.deepcopy(self.state.bundle), closures=self.state.closures)

    def read(self, ref, path=()):
        value = self.state.get(ref, path)
        captured = self.input_state.get(ref, path) if self.input_state is not None else value
        read = {"ref": ref, "path": list(path), "state": captured}
        if not any(equal(read, prior) for prior in self.record['reads']):
            self.record['reads'].append(read)
        return copy.deepcopy(value.get('value'))

    def select(self, key, owner, members=()):
        value = selection(self.input_state or self.state, key, owner, members)
        if value not in self.record['selections']:
            if key.startswith('collection.'):
                self.read(owner + '/collection:' + KINDS[key])
                if owner != 'parent':
                    self.read(owner, ['occurrence_id'])
                    self.read(owner + '/shot', ['shot_id'])
                    self.bind('collection.owner:' + key, owner)
            self.record['selections'].append(value)
        return value['members']

    def bind(self, key, ref, *, dependencies=()):
        self.record['bindings'].append({"key": key, "ref": ref, "policy": "fixed",
                                        "dependencies": list(dependencies)})

    def dependency(self, key, kind, pin):
        self.record['dependencies'].append({"key": key, "kind": kind,
                                            "pin": copy.deepcopy(pin), "policy": "exact"})

    def assign(self, ref, path, after):
        if after['state'] == 'absent':
            for end in range(1, len(path)):
                ancestor = self.state.get(ref, path[:end])
                if ancestor == ABSENT or ancestor == present(None):
                    # A missing leaf must not erase its ancestor's tagged presence.
                    self.read(ref, path[:end])
                    break
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

    def create(self, owner, kind, row, *, restoring=False):
        rows(self.state, owner, kind, check_mirrors=not restoring)
        if owner != 'parent':
            self.read(owner, ['occurrence_id'])
            self.read(owner + '/shot', ['shot_id'])
            self.bind('create.owner', owner)
        if not restoring:
            self.select('track.create' if kind == 'track' else 'collection.' + kind + 's', owner)
        ref = owner + '/' + kind + ':' + row['id']
        if self.state.get(ref, []) != ABSENT:
            raise CommandError("created identity is occupied", kind="identity_collision", ref=ref)
        self.read(ref)
        self.write(ref, [], row)
        self.record['created'].append({"ref": ref, "kind": kind, "owner": owner})
        return ref

    def create_entity(self, ref, *, kind, owner, value, restoring=False):
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
        if (occupied and not restoring) or self.state.get(ref, []) != ABSENT or any(
                item['ref'] == ref for item in self.record['created']):
            raise CommandError('created identity is occupied', kind='identity_collision', ref=ref)
        self.read(ref)
        self.write(ref, [], value)
        if kind == 'shot' and root[1] not in self.state.bundle['source_mapping']['shots']:
            self.state.bundle['shots'][root[1]]['_created'] = True
        self.record['created'].append({'ref': ref, 'kind': kind, 'owner': owner})
        return ref

    def create_asset(self, owner, identity, value):
        ref = owner + '/asset:' + identity
        if owner != 'parent':
            self.read(owner, ['occurrence_id'])
            self.read(owner + '/shot', ['shot_id'])
        if self.state.get(ref, []) != ABSENT:
            raise CommandError('created identity is occupied', kind='identity_collision', ref=ref)
        self.read(ref)
        self.write(ref, [], value)
        self.record['created'].append({'ref': ref, 'kind': 'asset', 'owner': owner})
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
        if self.mirrored_clips:
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
            # Public replay guards describe the input; the record retains actual
            # observations made between the deterministic recipe's own writes.
            command['reads'], command['selections'] = [], []
            for read in self.record['reads']:
                claim = {**read, 'state': self.command_input.get(read['ref'], read['path'])}
                if not any(equal(claim, prior) for prior in command['reads']):
                    command['reads'].append(claim)
            for selected in self.record['selections']:
                claim = selection(self.command_input, selected['key'], selected['owner'], selected['members'])
                if claim not in command['selections']:
                    command['selections'].append(claim)
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
                before = self.command_input.get(write['ref'], write['path'])
                command['expect'].setdefault(key, copy.deepcopy(before))
                command['authorship'][key] = 'direct'
        return self.record


def guard(state, ref, path, expected, *, kind='dependency_changed'):
    actual = state.get(ref, path)
    if not state.matches(ref, path, expected):
        raise CommandError("original authored guard changed", kind=kind, ref=ref, path=path,
                           base=expected, theirs=actual)
