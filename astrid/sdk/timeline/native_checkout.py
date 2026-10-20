"""Bounded ordinary clip verbs over the existing durable command session."""
from __future__ import annotations

import copy
import re

from astrid.core.timeline import clip_fields
from astrid.sdk import timeline_intent as intent

from ._command_state import State, equal
from ._common import AUDIO_KINDS, TIME_RE, TimelineEditError, _length_seconds, _r
from .capture import move_intent, number, occurrence_start, rate
from .checkout import Checkout
from .commands import execute
from .model import Clip, _is_formula_or_moment
from .selection import Selection
from .units import from_canvas


def _held(*args, **kwargs):
    raise TimelineEditError('this verb is held for attached checkouts; use bounded clip verbs and flush()')


def _seconds(value):
    if isinstance(value, str):
        match = TIME_RE.fullmatch(value.strip())
        if match:
            return int(match.group(1) or 0) * 60 + float(match.group(2))
    return number(value, 'literal timeline seconds')


def _publishable_parent_command(command):
    if (not isinstance(command, dict) or not isinstance(command.get('select'), str)
            or re.fullmatch(r'parent/clip:[^/]+', command['select']) is None):
        return False
    if command.get('op') == 'clip.move':
        return True
    args = command.get('args')
    if (command.get('op') == 'clip.trim' and isinstance(args, dict)
            and set(args) == {'in_s', 'out_s'}):
        return True
    if command.get('op') == 'clip.delete' and args == {}:
        return True
    if (command.get('op') == 'clip.split' and isinstance(args, dict)
            and set(args) == {'on', 'right_id'}):
        return True
    values = args.get('values') if isinstance(args, dict) else None
    return (command.get('op') == 'clip.set' and isinstance(args, dict)
            and ((args.get('clear') == [] and isinstance(values, dict)
                  and set(values) == {'hold'} and values['hold'] is not None)
                 or (args.get('values') == {} and args.get('clear') == ['asset'])))


class AttachedCheckout(Checkout):
    """A raw scoped preview, never flattened or published as a candidate."""

    def __init__(self, session):
        super().__init__({})
        self.session = session
        self._read_pending()

    def _read_pending(self):
        with self.session.outbox.locked():
            state = self.session._state()
        self.bundle = self.session._bundle(state)
        self._basis = copy.deepcopy(state['base'])
        self._pending = copy.deepcopy(state['pending'])
        self._preview = copy.deepcopy(self.bundle)
        self.fps = float(rate(self.bundle['parent'].get('config', {}).get('output', {}).get('fps')))
        self._mcache = None

    def _unchanged_preview(self):
        if not equal(self.bundle, self._preview):
            raise TimelineEditError('unqueued local changes in attached checkout; reattach before editing')
        with self.session.outbox.locked():
            self._unchanged_basis(self.session._state())

    def _unchanged_basis(self, state):
        if not equal(state['base'], self._basis) or not equal(state['pending'], self._pending):
            raise TimelineEditError('attached checkout basis changed; reattach before editing')

    def _queue(self, command):
        self._unchanged_preview()
        plans = []

        def capture(state):
            self._unchanged_basis(state)
            bundle = self.session._bundle(state)
            if not equal(bundle, self._preview):
                raise TimelineEditError('attached checkout basis changed; reattach before editing')
            plan = execute(bundle, [command])
            plans.append(plan)
            return plan.commands

        self.session._stage(capture)
        # Only expose the candidate after the existing outbox's atomic write.
        self._pending.extend(copy.deepcopy(plans[0].commands))
        self.bundle = plans[0].bundle
        self._preview = copy.deepcopy(self.bundle)
        self._mcache = None

    @property
    def clips(self):
        state = State(self.bundle)
        owners = ['parent', *('occurrence:' + row['occurrence_id'] for row in self.bundle['placements'])]
        pool = [AttachedClip(self, owner, row['id']) for owner in owners
                for row in state.collection(owner, 'clip')]
        return Selection(sorted(pool, key=lambda clip: (clip.start, clip.id)), kind='clip', tl=self)

    def clip(self, query, *, cut=None, near=None):
        if cut is not None or near is not None:
            _held()
        # A raw scope ref is also accepted, but never inferred from a display ID.
        matches = [clip for clip in self.clips if query in (clip.id, clip._ref)]
        if len(matches) != 1:
            raise TimelineEditError('attached checkout needs one exact clip ID or raw scoped clip reference')
        return matches[0]

    def flush(self, **options):
        self._unchanged_preview()
        result = self.session.flush(**options)
        self._read_pending()
        return result

    def publish(self, message='', *, idempotency_key=None, client=None, force=False, restructure=False):
        """Publish one captured parent move, hold set, trim, delete, or split from an explicitly selected outbox.

        The outbox path is this draft's recovery identity. Reattach that same
        session after a restart; detached checkouts never discover its intent.
        Other attached verbs continue to use ``flush()``. A hold remains a
        source-unit scalar, trim keeps the original registry/source reads,
        delete keeps its full dependency guards, and split retains its
        caller-allocated right identity; all are captured through the native
        command operations.
        """
        if (not getattr(self.session, '_explicit_outbox', False) or force or restructure
                or (client is not None and client is not self.session.client)):
            _held()
        self._unchanged_preview()

        def prepare(state):
            self._unchanged_basis(state)
            commands = state['pending']
            if len(commands) != 1 or not _publishable_parent_command(commands[0]):
                _held()
            # Rationale and request are sealed in one existing outbox write.
            # A retry may omit the message, but cannot replace the original.
            rationale = state.get('rationale', '')
            if state['flight'] is not None:
                if message and message != rationale:
                    raise TimelineEditError('in-flight publish rationale is immutable; retry its original message')
            elif message:
                state['rationale'] = message

        result = self.session._flush(idempotency_key=idempotency_key, prepare=prepare)
        self._read_pending()
        data = result['data']
        return {'old_head': data['previous_revision_id'], 'new_head': data['accepted_revision_id'],
                'structure': 'changed', 'receipt': result['receipt'],
                'idempotency_key': result['receipt']['idempotency_key'],
                'narration_pinned': [], 'transcripts': [], 'message': data.get('rationale', '')}

    def undo(self, publications, **options):
        """Reverse accepted publications through the session's guarded inverse."""
        self._unchanged_preview()
        result = self.session.undo(publications, **options)
        self._read_pending()
        return result

    save = edit = step = redo = discard = adopt = _held
    cut = cut_picture = voice = sequence = pin_narration = _held
    add = add_cut = set_cut_note = ripple_delete = close_gap = insert_time = _held
    insert_line = remove_line = apply_script = fill_slot = fill_standins = _held
    declare_gaps = reflow = retime = resolve = film_end = replace_asset = _held

    @property
    def cuts(self):
        _held()


class AttachedClip(Clip):
    def __init__(self, checkout, owner, identity):
        self._tl, self.shot_id = checkout, owner
        self._ref = owner + '/clip:' + identity

    @property
    def data(self):
        # Handles remain live after preview replacement, including materialization.
        return State(self._tl.bundle).entity(self._ref)

    @property
    def element(self):
        return self.data.get('clipType') or self.data.get('clip_type') or 'media'

    @property
    def at(self):
        return self.data.get('at', self.data.get('at_ms', 0) / 1000)

    @property
    def start(self):
        state = State(self._tl.bundle)
        return self.at + (0 if self.shot_id == 'parent' else occurrence_start(state.occurrence(self.shot_id)))

    @property
    def is_audio(self):
        tracks = State(self._tl.bundle).config(self.shot_id).get('tracks', [])
        return self.track in AUDIO_KINDS or any(
            row['id'] == self.track and row.get('kind') in AUDIO_KINDS for row in tracks)

    def _command(self, op, args):
        command = {'schema_version': 1, 'op': op, 'version': '1', 'select': self._ref, 'args': args}
        if op == 'clip.move':
            command['intent'] = move_intent(self._ref)
        self._tl._queue(command)
        return self

    def on(self, moment):
        if intent.cut_of(self.data):
            _held()
        return self._command('clip.move', {'on': _seconds(moment)})

    def enter_at(self, when, *, offset=0.0, anchor=True):
        return self.on(_seconds(when) + number(offset, 'offset'))

    def nudge(self, seconds=0.0, *, frames=0):
        if intent.on(self.data):
            _held()
        return self.on(self.start + number(seconds, 'seconds') + number(frames, 'frames') / self._tl.fps)

    def trim(self, in_s=None, out_s=None):
        return self._command('clip.trim', {'in_s': in_s, 'out_s': out_s})

    def set_duration(self, seconds):
        # Public duration is playback seconds; the native scalar is source hold.
        speed = self.data.get('speed')
        duration = self._tl.quantize(number(seconds, 'duration', positive=True))
        hold = _r(duration * number(1 if speed is None else speed, 'speed', positive=True))
        if self.data.get('from') is not None or self.data.get('to') is not None:
            if (self.data.get('from') is None or self.data.get('to') is None
                    or 'hold' not in self.data):
                _held()
            return self.trim(out_s=self.data['from'] + hold)
        return self._command('clip.set', {'values': {'hold': hold}, 'clear': []})

    def hold_for(self, seconds):
        return self.set_duration(_length_seconds(seconds, self._tl.fps))

    for_ = hold_for

    def extend(self, seconds=0.0, *, frames=0):
        return self.set_duration(self.duration + number(seconds, 'seconds') + number(frames, 'frames') / self._tl.fps)

    def clear_asset(self):
        return self._command('clip.set', {'values': {}, 'clear': ['asset']})

    def set(self, **params):
        allow_new = params.pop('_allow_new', False)
        selected = self.data.get('elementRef') or self.data.get('element_ref')
        if isinstance(selected, dict) and selected.get('packId'):
            # Session queue currently has no exact selected-schema input reader.
            # Never substitute the locally installed pack or caller-inline schema.
            raise TimelineEditError('selected pack params require exact schema inputs; attached setter is held')
        if any('.' in key or '[' in key or _is_formula_or_moment(value) for key, value in params.items()):
            _held()
        if intent.formulas(self.data):
            _held()
        from astrid.sdk.timeline_address import element_schema

        declared = element_schema(self.element).get('properties', {})
        if any(key not in declared and (key in clip_fields.FIELDS or clip_fields.is_reserved(key))
               for key in params):
            _held()
        if not allow_new:
            self._check_param_keys(list(params))
        if not params:
            return self
        return self._command('clip.set-params', {
            'values': {key: from_canvas(self.element, key, value) for key, value in params.items() if value is not None},
            'clear': [key for key, value in params.items() if value is None],
        })

    def set_param(self, path, value):
        return self.set(**{path: value}, _allow_new=True)

    def remove(self):
        if self.shot_id != 'parent':
            _held()
        return self._command('clip.delete', {})

    def split(self, on, *, id):
        """Split this attached parent media clip at absolute timeline seconds.

        The caller reserves ``id`` once; the native command keeps that identity
        in the durable outbox for retries, reloads, and inverse/redo.
        """
        if self.shot_id != 'parent':
            _held()
        return self._command('clip.split', {'on': on, 'right_id': id})

    until = end_at = slip = keep = remove_layer = _held
    set_look = tag = move_to_cut = set_track = swap_asset = set_beats = keyframe_at = _held
