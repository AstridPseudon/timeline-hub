import copy

import pytest

from astrid.sdk.timeline.commit import _digest
from tests.helpers.runtime import use_runtime
from tests.sdk import test_timeline_arrange_commit as arrange
from tests.sdk.test_timeline_arrange_commit import arranged_session  # noqa: F401
from tests.sdk.test_timeline_commit_provider_document import _manifest, document_fixture


def empty_document():
    """An empty timeline, as Runtime's create_empty leaves it (the acceptance starting point)."""
    document = document_fixture(shared=False)
    parent = document['parent_revision']['payload']
    parent['occurrences'] = []
    parent['clips'] = []
    parent['config']['clips'] = []
    parent['registry'] = {'assets': {}}
    document['parent_revision']['content_digest'] = _digest(parent)
    document['shot_revisions'] = []
    document['internal_timeline_revisions'] = []
    document['dependency_manifest'] = _manifest([], [], [], [])
    return document


@pytest.fixture(autouse=True)
def empty_start(monkeypatch):
    use_runtime()
    monkeypatch.setattr(arrange, 'twenty_document', empty_document)


@pytest.mark.parametrize('shape', ['single', 'per_id', 'two_halves'])
def test_explore(arranged_session, monkeypatch, shape):  # noqa: F811
    tl, realm, calls = arranged_session
    from astrid.sdk.timeline import inverse as inv
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create

    from_bundle = copy.deepcopy(tl.bundle)
    births = []
    for index in range(20):
        command = capture_occurrence_create(
            from_bundle, f'new-occ-{index:02d}', f'new-shot-{index:02d}',
            name=f'New shot {index:02d}', track='picture', on=index * 3, duration=2)
        births.append(command)
        from_bundle = execute(from_bundle, [command]).bundle
    tl.commit(births, label='Create twenty occurrences')
    order = [f'new-occ-{index:02d}' for index in reversed(range(20))]
    if shape == 'single':
        def fn(t):
            t.arrange(order, at=100, gap=0)
    elif shape == 'per_id':
        def fn(t):
            for i, identity in enumerate(order):
                t.arrange([identity], at=100 + i * 2)
    else:
        def fn(t):
            t.arrange(order[:10], at=100, gap=0)
            t.arrange(order[10:], at=200, gap=0)
    arranged = tl.commit(fn, label='Arrange occurrences')
    print('SHAPE', shape)
    real_guard = inv.guard

    def logging_guard(state, ref, path, expected, *, kind='dependency_changed'):
        try:
            real_guard(state, ref, path, expected, kind=kind)
        except Exception as exc:
            print('GUARD FAIL', ref, path, 'expected', str(expected)[:300], 'actual', str(state.get(ref, path))[:300])
            raise
    monkeypatch.setattr(inv, 'guard', logging_guard)
    try:
        tl.undo(publications=[arranged['receipt']['receipt_id']])
        print('UNDO OK')
    except Exception as exc:
        print('UNDO EXC', type(exc).__name__, exc, getattr(exc, 'kind', None))
