"""Two disposable agents, actual saved commands/encoder/provider, no live Runtime."""
from __future__ import annotations

import copy
import json
from types import SimpleNamespace

import pytest

from astrid.core.cli.domain_output import DomainResult
from astrid.packs.timeline import cli
from astrid.sdk.timeline import journal, saved_publish, store
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.revisions import RuntimeRevisions
from astrid.sdk.timeline.saved_intent import SavedIntentError, read_saved_calls
from astrid.sdk.timeline.sync import status_fields
from tests.sdk.test_timeline_saved_publish import (
    RuntimeFixture,
    edit,
    synthetic_scene_answers,  # noqa: F401
)

pytestmark = pytest.mark.usefixtures('synthetic_scene_answers')


class SharedRuntime(RuntimeFixture):
    def __init__(self):
        super().__init__()
        self.history[0][0].update(is_current_head=True, previous_revision_id=None, previous_publication_id=None)
        self.head_reads = 0
        self.history_reads = 0
        self.after_accept = None

    def port(self, body):
        port = super().port(body)
        accept = port.accept
        def wrapped(prepared):
            previous, previous_pub = self.current, self.publication()
            value = accept(prepared)
            result = value['stored_result']
            if result['status'] == 'accepted':
                self.event(self.current, result['accepted_publication_id'], previous, previous_pub,
                           result['provenance'])
                if self.after_accept:
                    callback, self.after_accept = self.after_accept, None
                    callback()
            return value
        port.accept = wrapped
        port.head = lambda: dict(revision_id=self.current, publication_id=self.publication(), updated_at='fixture')
        return port

    def publication(self):
        return next(r['publication_id'] for r in self.history[0] if r['is_current_head'])

    def event(self, revision, publication, previous, previous_pub, provenance=None):
        for row in self.history[0]:
            row['is_current_head'] = False
        self.history[0].insert(0, dict(revision_id=revision, publication_id=publication,
            previous_revision_id=previous, previous_publication_id=previous_pub,
            is_current_head=True, provenance=provenance))
        self.current = revision

    def facade(self):
        runtime = self
        class Timelines:
            def head_canonical(self, project, timeline):
                assert (project, timeline) == ('p', 't')
                runtime.head_reads += 1
                return DomainResult.success(dict(revision_id=runtime.current,
                    publication_id=None, updated_at=None))

            def resolve_scope(self, *args):
                return DomainResult.success(dict(project_id='p', timeline_id='t'))

            def list_parent_composition_revisions(self, *args, **kwargs):
                runtime.history_reads += 1
                return DomainResult.success(dict(items=copy.deepcopy(runtime.history[0]), next_cursor=None))
        return SimpleNamespace(_transport=self.client(), timelines=Timelines())


@pytest.fixture
def agents(tmp_path, monkeypatch):
    monkeypatch.setenv('BANODOCO_LOCAL_DATA_ROOT', str(tmp_path / 'data'))
    monkeypatch.setattr(Checkout, 'SAY_SAVED', False)
    runtime = SharedRuntime()
    client = runtime.facade()
    monkeypatch.setattr(store, 'resolve_ids', lambda *a, **kw: ('p', 't', runtime.current))
    monkeypatch.setattr(store, 'fetch_bundle', lambda *a, revision_id=None, **kw:
        saved_publish._exact(client._transport, dict(project_id='p', timeline_id='t'), revision_id or runtime.current))
    return Checkout.draft('p', 't', 'alice'), Checkout.draft('p', 't', 'bob'), runtime, client


def fields(draft, runtime, client):
    adapter = RuntimeRevisions(client.timelines)
    return status_fields(draft, adapter.head_state('p', 't'),
                         revisions=adapter.list('p', 't'), client=client)


def bytes_now(draft):
    return draft.path.read_bytes(), journal.journal_path('p', 't').read_bytes()


def test_two_agents_visibility_refresh_order_exact_receipts_and_identity(agents, capsys):
    alice, bob, runtime, client = agents
    runtime.principal = 'agent:alice'
    edit(alice, x=90)
    edit(bob, y=100)
    edit(bob, y=180)
    original = read_saved_calls(bob)
    accepted_a = alice.publish('Alice x', client=client)
    state = fields(bob, runtime, client)
    assert state['unimported_external_revisions'][0]['revision_id'] == accepted_a['accepted_revision_id']
    assert state['conflicts'] == [] and state['accepted_state'] == 'absent'
    result = bob.refresh(client=client)
    assert result['status'] == 'refreshed' and bob.clip('c1.rocket').params == dict(x=15, y=30)
    replay = read_saved_calls(Checkout.load(bob.path))
    assert [c['args'] for c in replay] == [c['args'] for c in original]
    runtime.principal = 'agent:bob'
    accepted_b = bob.publish('Bob y', client=client)
    assert accepted_a['accepted_revision_id'] != accepted_b['accepted_revision_id']
    assert alice.base_revision == accepted_a['accepted_revision_id']
    state = fields(alice, runtime, client)
    assert state['accepted_revision'] == accepted_a['accepted_revision_id']
    assert state['observed_head'] == accepted_b['accepted_revision_id']
    assert alice.refresh(client=client)['status'] == 'refreshed'
    assert alice.clip('c1.rocket').params == dict(x=15, y=30)
    assert read_saved_calls(alice) == ()
    # History and log use accepted identity, independent of local environment.
    parser = cli.build_parser(client)
    args = parser.parse_args(['history', 't', '--project', 'p'])
    assert args.handler(args) == 0
    text = capsys.readouterr().out
    assert 'agent:alice' in text and 'agent:bob' in text
    args.json = False
    assert args.handler(args) == 0
    assert {'agent:alice', 'agent:bob'} <= set(capsys.readouterr().out.split())
    args = parser.parse_args(['log', 't', '--project', 'p'])
    assert args.handler(args) == 0
    text = capsys.readouterr().out
    assert 'agent:alice' in text and 'agent:bob' in text


def test_apply_file_batch_sync_conflict_and_publication_undo_journey(agents, tmp_path, capsys, monkeypatch):
    from astrid.packs.timeline import cli_sync

    alice, bob, runtime, client = agents
    overlapping = Checkout.draft('p', 't', name='overlapping')
    base = alice.document()
    assert runtime.current == 'rev-0'
    assert {draft.base_revision for draft in (alice, bob, overlapping)} == {'rev-0'}
    assert all(draft.document() == base for draft in (bob, overlapping))

    parser = cli.build_parser(client)

    def apply_jsonl(draft, commands):
        path = tmp_path / f'{draft.draft_name}.jsonl'
        path.write_text(''.join(json.dumps(command) + '\n' for command in commands), encoding='utf-8')
        args = parser.parse_args(['apply', 't', '--project', 'p', '--draft', draft.draft_name, str(path)])
        assert args.handler(args) == 0
        assert capsys.readouterr().out == 'applied file\n'
        return Checkout.load(draft.path)

    batch = [
        {'op': 'clip.set', 'select': 'c1.rocket', 'args': {'y': 100}},
        {'op': 'clip.set', 'select': 'c1.rocket', 'args': {'y': 180}},
    ]
    before_batch_records = journal.read(journal.journal_path('p', 't'))
    before_batch_steps = set(store._history_dir(bob.path).glob('*.json'))
    bob = apply_jsonl(bob, batch)
    original_calls = read_saved_calls(bob)
    after_batch_records = journal.read(journal.journal_path('p', 't'))
    added_records = [row for row in after_batch_records
                     if row.id not in {old.id for old in before_batch_records} and row.draft == bob.path.stem]
    after_batch_steps = set(store._history_dir(bob.path).glob('*.json'))
    sid = 'occurrence:occ-A/clip:a-rocket'
    assert len(original_calls) == 2
    assert [call['args'] for call in original_calls] == [command['args'] for command in batch]
    assert [call['resolved'] for call in original_calls] == [[sid], [sid]]
    assert len(added_records) == 1 and len(added_records[0].calls) == 2
    assert len(after_batch_steps - before_batch_steps) == 1

    overlap_batch = [
        {'op': 'clip.set', 'select': 'c1.rocket', 'args': {'x': 120}},
        {'op': 'clip.set', 'select': 'c1.rocket', 'args': {'x': 240}},
    ]
    overlapping = apply_jsonl(overlapping, overlap_batch)

    runtime.principal = 'agent:alice'
    edit(alice, x=90)
    accepted_a = alice.publish('Alice changes x', client=client)
    revision_a = accepted_a['accepted_revision_id']
    assert accepted_a['status'] == 'accepted' and runtime.current == revision_a

    ticks = iter([0.0, 1.0])
    watch = parser.parse_args(['status', 't', '--project', 'p', '--draft', 'bob', '--watch',
                               '--poll-seconds', '1', '--timeout-seconds', '1'])
    with monkeypatch.context() as watch_patch:
        watch_patch.setattr(cli_sync.time, 'monotonic', lambda: next(ticks))
        assert watch.handler(watch) == 0
    watch_data = json.loads(capsys.readouterr().out)['data']
    assert watch_data['current_head'] == watch_data['observed_head'] == revision_a

    refresh = parser.parse_args(['checkout', 't', '--project', 'p', '--draft', 'bob', '--refresh', '--json'])
    assert refresh.handler(refresh) == 0
    refreshed = json.loads(capsys.readouterr().out)['data']
    assert refreshed['status'] == 'refreshed' and refreshed['observed_head'] == revision_a
    bob = Checkout.load(bob.path)
    rebased_calls = read_saved_calls(bob)
    assert [call['args'] for call in rebased_calls] == [command['args'] for command in batch]
    assert [call['resolved'] for call in rebased_calls] == [[sid], [sid]]
    assert bob.base_revision == revision_a

    before_conflict = bytes_now(overlapping), overlapping.document()
    history_before_conflict = copy.deepcopy(runtime.history[0])
    conflict_refresh = parser.parse_args(['checkout', 't', '--project', 'p', '--draft', 'overlapping',
                                          '--refresh', '--json'])
    assert conflict_refresh.handler(conflict_refresh) == 1
    conflict_data = json.loads(capsys.readouterr().out)['data']
    assert conflict_data['status'] == 'conflict'
    assert conflict_data['conflicts'] == [{
        'kind': 'same-property', 'id': sid, 'path': 'params.x',
        'base': {'state': 'present', 'value': 10},
        'theirs': {'state': 'present', 'value': 15},
        'ours': {'x': 120},
    }]
    assert conflict_data['choices'] == [
        'Inspect base, theirs and ours for the named property; choose a value and record a new command on this head.'
    ]
    assert (bytes_now(overlapping), overlapping.document()) == before_conflict
    assert runtime.current == revision_a and runtime.history[0] == history_before_conflict

    runtime.principal = 'agent:bob'
    accepted_b = bob.publish('Bob applies the disjoint batch', client=client)
    revision_b = accepted_b['accepted_revision_id']
    assert accepted_b['status'] == 'accepted' and bob.base_revision == revision_b
    assert [call['args'] for call in accepted_b['change']['commands']] == [command['args'] for command in batch]
    assert [call['resolved'] for call in accepted_b['change']['commands']] == [[sid], [sid]]

    exact_a = Checkout(store.fetch_bundle('p', 't', revision_id=revision_a, client=client))
    assert (exact_a.clip('c1.rocket').get('x'), exact_a.clip('c1.rocket').get('y')) == (90, None)
    assert alice.base_revision == revision_a
    alice_state = fields(alice, runtime, client)
    assert (alice_state['accepted_revision'], alice_state['observed_head']) == (revision_a, revision_b)

    undo_labels = bob.undo(client=client)
    assert len(undo_labels) == 1 and undo_labels[0].startswith('Undo publication ')
    accepted_undo = bob.publish('Undo Bob batch', client=client)
    if accepted_undo['status'] != 'accepted':
        pytest.fail(json.dumps({key: accepted_undo.get(key) for key in (
            'status', 'error', 'conflicts', 'choices', 'previous_revision_id', 'base_revision_id'
        )}, sort_keys=True))
    revision_undo = accepted_undo['accepted_revision_id']
    assert accepted_undo['previous_revision_id'] == revision_b
    assert runtime.current == revision_undo
    head_event = runtime.history[0][0]
    assert head_event['revision_id'] == revision_undo
    assert head_event['publication_id'] == accepted_undo['accepted_publication_id']
    assert head_event['previous_revision_id'] == revision_b
    assert sum(row['is_current_head'] for row in runtime.history[0]) == 1
    exact_undo = Checkout(store.fetch_bundle('p', 't', revision_id=revision_undo, client=client))
    assert exact_undo.clip('c1.rocket').data == exact_a.clip('c1.rocket').data

    assert alice.refresh(client=client)['status'] == 'refreshed'
    edit(alice, x=110)
    runtime.principal = 'agent:alice'
    accepted_a_later = alice.publish('Alice changes x again', client=client)
    revision_a_later = accepted_a_later['accepted_revision_id']
    bob_state = fields(bob, runtime, client)
    assert (bob_state['accepted_revision'], bob_state['observed_head']) == (revision_undo, revision_a_later)
    exact_b = Checkout(store.fetch_bundle('p', 't', revision_id=revision_b, client=client))
    assert (exact_b.clip('c1.rocket').get('x'), exact_b.clip('c1.rocket').get('y')) == (90, 180)
    exact_head = Checkout(store.fetch_bundle('p', 't', revision_id=revision_a_later, client=client))
    assert exact_head.clip('c1.rocket').data == alice.clip('c1.rocket').data
    assert runtime.history[0][0]['revision_id'] == revision_a_later
    assert runtime.history[0][0]['previous_revision_id'] == revision_undo

    bodies = [(json.loads(raw), headers) for raw, headers in runtime.calls]
    assert len(bodies) == 4
    returned = (accepted_a, accepted_b, accepted_undo, accepted_a_later)
    bases = (('rev-0', 'pub-0'), (revision_a, accepted_a['accepted_publication_id']),
             (revision_b, accepted_b['accepted_publication_id']),
             (revision_undo, accepted_undo['accepted_publication_id']))
    for (body, headers), receipt, (base_revision, base_publication) in zip(bodies, returned, bases):
        assert (body['base_revision_id'], body['base_publication_id']) == (base_revision, base_publication)
        assert headers['Idempotency-Key'] == body['request_id']
        stored_result = runtime.saved[body['request_id']]['result']
        assert receipt['request_id'] == body['request_id']
        assert stored_result['accepted_revision_id'] == receipt['accepted_revision_id']
        assert receipt['accepted_publication_id'] == stored_result['accepted_publication_id']


def test_refresh_same_property_returns_real_choices_and_never_mutates(agents):
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    edit(bob, x=180)
    alice.publish(client=client)
    before = bytes_now(bob), bob.document()
    state = fields(bob, runtime, client)
    assert state['conflicts'][0]['kind'] == 'same-property' and state['choices']
    result = bob.refresh(client=client)
    assert result['status'] == 'conflict' and result['choices']
    assert result['conflicts'][0]['path'] == 'params.x'
    assert (bytes_now(bob), bob.document()) == before


def test_acceptance_followed_by_same_content_republication_verifies_resets_exact_r1(agents, monkeypatch):
    alice, _bob, runtime, client = agents
    edit(alice, x=90)
    runtime.principal = 'agent:alice'
    def republish():
        old, old_pub = runtime.current, runtime.publication()
        runtime.parents['R2'] = {**copy.deepcopy(runtime.parents[old]), 'revision_id': 'R2'}
        runtime.event('R2', 'pub-R2', old, old_pub)
    runtime.after_accept = republish
    accepted = alice.publish(client=client)
    assert runtime.current == 'R2'
    assert alice.base_revision == accepted['accepted_revision_id'] == 'accepted-1'
    assert not any('/composition-revisions/R2' in read for read in runtime.reads)
    state = fields(alice, runtime, client)
    assert (state['accepted_revision'], state['observed_head']) == ('accepted-1', 'R2')
    assert state['unimported_external_revisions'][0]['revision_id'] == 'R2'
    # Existing pixel-verification producer selects the pinned accepted revision.
    from astrid.packs.rendering.actions.timeline_visualize.fast_lane import _base_revision
    assert _base_revision(alice) == 'accepted-1'
    before = len(runtime.calls)
    runtime.reads.clear()
    replayed = Checkout.load(alice.path).publish(client=client)
    assert replayed['accepted_revision_id'] == 'accepted-1' and len(runtime.calls) == before
    assert Checkout.load(alice.path).base_revision == 'accepted-1'
    assert not any('/composition-revisions/R2' in read for read in runtime.reads)


@pytest.mark.parametrize('damage', ['unknown-links', 'duplicate-base', 'missing-journal', 'manual-edit', 'pending'])
def test_refresh_refuses_ambiguous_or_unrecorded_inputs_without_mutation(agents, damage):
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    edit(bob, y=180)
    if damage == 'pending':
        runtime.lose = True
        with pytest.raises(Exception, match='timed out'):
            bob.publish(client=client)
    else:
        alice.publish(client=client)
    if damage == 'unknown-links':
        runtime.history[0][0]['previous_publication_id'] = None
    elif damage == 'duplicate-base':
        runtime.history[0].append({**runtime.history[0][-1], 'publication_id': 'pub-other'})
    elif damage == 'missing-journal':
        journal.journal_path('p', 't').write_text('')
    elif damage == 'manual-edit':
        bob.path.write_text(bob.path.read_text() + ' ')
    before = bytes_now(bob)
    with pytest.raises(SavedIntentError):
        bob.refresh(client=client)
    assert bytes_now(bob) == before


def test_duplicate_publication_of_exact_base_is_external_activity(agents):
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    alice.publish(client=client)
    rid, pid = runtime.current, runtime.publication()
    runtime.event(rid, 'republished-same-revision', rid, pid)
    state = fields(alice, runtime, client)
    assert state['accepted_revision'] == rid and len(state['unimported_external_revisions']) == 1
    assert state['unimported_external_revisions'][0]['publication_id'] == 'republished-same-revision'
    assert fields(bob, runtime, client)['external_state'] == 'known'
    assert alice.refresh(client=client)['status'] == 'refreshed'
    assert fields(alice, runtime, client)['unimported_external_revisions'] == []
    assert read_saved_calls(alice) == ()


def test_refresh_keeps_explicit_clear_and_opaque_upstream_fields_and_undo(agents):
    alice, bob, runtime, client = agents
    edit(bob, x={'op': 'clear'})
    # Publish an opaque authored object through the existing command path.
    edit(alice, **{'opaque': {'nested': None, 'looks_like': {'op': 'clear'}}, '_allow_new': True})
    alice.publish(client=client)
    before = bob.document()
    assert bob.refresh(client=client)['status'] == 'refreshed'
    params = bob.clip('c1.rocket').params
    assert 'x' not in params and params['opaque'] == {'nested': None, 'looks_like': {'op': 'clear'}}
    assert read_saved_calls(bob)[0]['args']['x'] == {'op': 'clear'}
    bob.undo(client=client)
    from astrid.sdk.timeline.identity import retain_cut_reservations
    assert bob.document() == retain_cut_reservations(before, bob.document())
    bob.redo()
    assert 'x' not in bob.clip('c1.rocket').params


@pytest.mark.parametrize('flags', [[], ['--json'], ['--text'], ['--human'], ['--text', '--all'], ['--text', '--render']])
def test_status_all_presentations_expose_sync_fields(agents, flags, monkeypatch, capsys):
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    alice.publish(client=client)
    monkeypatch.setattr('astrid.packs.timeline.cli_common.render_line', lambda *a: 'latest render: fixture')
    args = cli.build_parser(client).parse_args(['status', 't', '--project', 'p', '--draft', 'bob', *flags])
    assert args.handler(args) == 0
    text = capsys.readouterr().out
    if '--text' in flags or '--human' in flags:
        for label in ('checkout base:', 'observed head:', 'accepted revision: absent', 'unimported external revisions:', 'conflicts: []'):
            assert label in text
    else:
        data = json.loads(text)['data']
        assert data['base_revision'] == 'rev-0' and data['observed_head'] == 'accepted-1'
        assert data['accepted_state'] == 'absent' and data['conflicts'] == []


@pytest.mark.parametrize('text', [False, True])
def test_watch_one_compact_call_per_tick_and_no_closure_or_history(agents, monkeypatch, capsys, text):
    alice, bob, runtime, client = agents
    from astrid.packs.timeline import cli_sync
    tick = [0.0]
    monkeypatch.setattr(cli_sync.time, 'monotonic', lambda: tick[0])
    def sleep(seconds):
        tick[0] += seconds
        runtime.event('new-observed-head', 'new-pub', 'rev-0', 'pub-0')
    monkeypatch.setattr(cli_sync.time, 'sleep', sleep)
    before = bytes_now(bob)
    runtime.reads.clear()
    def no_lock(*a, **kw):
        pytest.fail('read-only watch must not create or rewrite lock files')
    monkeypatch.setattr(store, '_file_lock', no_lock)
    monkeypatch.setattr(journal, '_locked', no_lock)
    args = cli.build_parser(client).parse_args(['status', 't', '--project', 'p', '--draft', 'bob',
        '--watch', '--poll-seconds', '1', '--timeout-seconds', '2', *(['--text'] if text else [])])
    assert args.handler(args) == 0
    assert runtime.head_reads == 2 and runtime.history_reads == 0 and runtime.reads == []
    assert bytes_now(bob) == before
    output = capsys.readouterr().out
    if text:
        assert 'observed head: new-observed-head' in output
    else:
        rows = [json.loads(line)['data'] for line in output.splitlines()]
        assert [r['observed_head'] for r in rows] == ['rev-0', 'new-observed-head']
        assert all(r['external_state'] == r['conflict_state'] == 'unknown' for r in rows)


def test_watch_ctrl_c_and_invalid_intervals(agents, monkeypatch):
    from astrid.packs.timeline import cli_sync
    _alice, _bob, runtime, client = agents
    def interrupt(seconds):
        raise KeyboardInterrupt
    monkeypatch.setattr(cli_sync.time, 'sleep', interrupt)
    parser = cli.build_parser(client)
    args = parser.parse_args(['status', 't', '--project', 'p', '--watch'])
    assert args.handler(args) == 130 and runtime.head_reads == 1
    for value in ('0', '-1', 'nan', 'inf'):
        with pytest.raises(SystemExit):
            parser.parse_args(['status', 't', '--watch', '--poll-seconds', value])


@pytest.mark.parametrize('verb', ['refresh', 'watch', 'review'])
def test_removed_verb_spellings_remain_unparsed(verb):
    with pytest.raises(SystemExit):
        cli.build_parser(object()).parse_args([verb, 't'])


def test_compact_api_refuses_closure_fallback_and_empty_unknown_identity():
    class NoCompact:
        def open_composition(self, *a, **kw):
            pytest.fail('must not fetch a closure')
    with pytest.raises(Exception, match='compact head'):
        RuntimeRevisions(NoCompact()).head_state('p', 't')
    empty = SimpleNamespace(head=lambda *a: DomainResult.success(dict(revision_id=None)))
    assert RuntimeRevisions(empty).head_state('p', 't')['revision_id'] is None
    invalid = SimpleNamespace(head=lambda *a: DomainResult.success({}))
    with pytest.raises(Exception, match='omitted'):
        RuntimeRevisions(invalid).head_state('p', 't')


@pytest.mark.parametrize('flags', [[], ['--json'], ['--text'], ['--human'], ['--text', '--all'], ['--text', '--render']])
@pytest.mark.parametrize('state', ['absent', 'unknown'])
def test_status_absent_and_unknown_are_distinct_in_every_format(agents, flags, state, monkeypatch, capsys):
    _alice, bob, runtime, client = agents
    if state == 'absent':
        bob.path.unlink()
    else:
        journal.journal_path('p', 't').write_text('damaged journal\n')
    monkeypatch.setattr('astrid.packs.timeline.cli_common.render_line', lambda *a: 'latest render: fixture')
    args = cli.build_parser(client).parse_args(['status', 't', '--project', 'p', '--draft', 'bob', *flags])
    assert args.handler(args) == 0
    output = capsys.readouterr().out
    if '--text' in flags or '--human' in flags:
        assert f'accepted revision: {state}' in output
        assert f'unimported external revisions: {state}' in output
        assert f'conflicts: {state}' in output
    else:
        value = json.loads(output)['data']
        assert value['accepted_state'] == value['external_state'] == value['conflict_state'] == state
        assert value['accepted_revision'] is value['conflicts'] is value['unimported_external_revisions'] is None


def test_refresh_observed_head_can_advance_during_exact_fetch_without_substitution(agents, monkeypatch):
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    edit(bob, y=180)
    accepted = alice.publish(client=client)
    original = saved_publish._exact
    def fetch(workspace, body, revision):
        if revision == accepted['accepted_revision_id']:
            runtime.parents['R2'] = {**copy.deepcopy(runtime.parents[revision]), 'revision_id': 'R2'}
            if runtime.current != 'R2':
                runtime.event('R2', 'pub-R2', runtime.current, runtime.publication())
        return original(workspace, body, revision)
    monkeypatch.setattr(saved_publish, '_exact', fetch)
    result = bob.refresh(client=client)
    assert result['observed_head'] == bob.base_revision == 'accepted-1'
    assert runtime.current == 'R2' and read_saved_calls(bob)
    assert fields(bob, runtime, client)['observed_head'] == 'R2'


def test_refresh_concurrent_local_save_and_new_publish_are_refused(agents, monkeypatch):
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    edit(bob, y=180)
    alice.publish(client=client)
    original = saved_publish._exact
    changed = []
    def fetch(workspace, body, revision):
        if not changed:
            handle = Checkout.load(bob.path)
            edit(handle, y=240)
            changed.append(bytes_now(handle))
        return original(workspace, body, revision)
    monkeypatch.setattr(saved_publish, '_exact', fetch)
    with pytest.raises(SavedIntentError, match='changed|stale'):
        bob.refresh(client=client)
    assert bytes_now(bob) == changed[-1]


def test_refresh_cli_and_incompatible_flags_preserve_draft(agents, capsys):
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    edit(bob, y=180)
    alice.publish(client=client)
    parser = cli.build_parser(client)
    args = parser.parse_args(['checkout', 't', '--project', 'p', '--draft', 'bob', '--refresh'])
    assert args.handler(args) == 0
    assert json.loads(capsys.readouterr().out)['data']['status'] == 'refreshed'
    before = bytes_now(bob)
    args = parser.parse_args(['checkout', 't', '--project', 'p', '--draft', 'bob', '--refresh', '--fresh'])
    with pytest.raises(Exception, match='cannot be combined'):
        args.handler(args)
    assert bytes_now(bob) == before


def test_generated_compact_head_route_is_one_call_with_exact_scope(agents):
    from astrid.sdk.remote import RemoteAstridClient
    _alice, _bob, runtime, _client = agents
    workspace = runtime.client()
    generated = workspace._generated
    original = generated._transport
    calls = []
    def transport(method, path, headers, payload):
        calls.append((method, path))
        assert method == 'GET' and path == '/v1/projects/p/timelines/t'
        return 200, {}, json.dumps(dict(project_id='p', timeline_id='t', head_revision_id='R1')).encode()
    generated._transport = transport
    try:
        remote = RemoteAstridClient(workspace)
        result = RuntimeRevisions(remote.timelines).head_state('p', 't')
    finally:
        generated._transport = original
    assert result == dict(revision_id='R1', publication_id=None, updated_at=None)
    assert len(calls) == 1


def test_accepted_identity_never_uses_asserted_actor():
    from astrid.sdk.timeline.revisions import publisher_identity
    assert publisher_identity(dict(publisher='agent:alice', asserted_actor='agent:fake')) == 'agent:alice'
    assert publisher_identity(dict(asserted_actor='agent:fake')) is None


def test_publish_starting_during_refresh_is_refused_without_replacing_envelope(agents, monkeypatch):
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    edit(bob, y=180)
    alice.publish(client=client)
    original = saved_publish._exact
    changed = []
    def fetch(workspace, body, revision):
        if not changed:
            changed.append(None)
            runtime.lose = True
            with pytest.raises(Exception, match='timed out'):
                Checkout.load(bob.path).publish(client=client)
            changed[0] = bytes_now(bob)
        return original(workspace, body, revision)
    monkeypatch.setattr(saved_publish, '_exact', fetch)
    with pytest.raises(SavedIntentError, match='publish started'):
        bob.refresh(client=client)
    assert bytes_now(bob) == changed[0]


def test_refresh_network_reads_hold_no_local_draft_or_journal_lock(agents, monkeypatch):
    import contextlib
    alice, bob, runtime, client = agents
    edit(alice, x=90)
    edit(bob, y=180)
    alice.publish(client=client)
    held = []
    def tracked(function):
        @contextlib.contextmanager
        def lock(*a, **kw):
            with function(*a, **kw):
                held.append(function)
                try:
                    yield
                finally:
                    held.pop()
        return lock
    monkeypatch.setattr(store, '_file_lock', tracked(store._file_lock))
    monkeypatch.setattr(journal, '_locked', tracked(journal._locked))
    original = saved_publish._exact
    def fetch(*args):
        assert held == []
        return original(*args)
    monkeypatch.setattr(saved_publish, '_exact', fetch)
    assert bob.refresh(client=client)['status'] == 'refreshed'


@pytest.mark.parametrize('published', [False, True])
def test_remote_assessment_failure_does_not_erase_known_receipt_or_known_absence(agents, monkeypatch, published):
    alice, _bob, runtime, client = agents
    if published:
        edit(alice, x=90)
        alice.publish(client=client)
    from astrid.sdk.timeline._common import TimelineEditError
    def unavailable(*a, **kw):
        raise TimelineEditError('exact remote read unavailable')
    monkeypatch.setattr(saved_publish, '_exact', unavailable)
    state = fields(alice, runtime, client)
    assert state['accepted_state'] == ('known' if published else 'absent')
    assert state['accepted_revision'] == ('accepted-1' if published else None)
    assert state['conflict_state'] == 'unknown' and state['conflicts'] is None
