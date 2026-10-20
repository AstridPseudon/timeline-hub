"""The public element helper against the actual retained-schema Runtime provider."""
from __future__ import annotations

import copy
import shutil
from types import SimpleNamespace

import pytest
import yaml

from astrid.core.element import project_packs as packs
from astrid.core.receipts.contract import CommandReceipt
from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline import commands, commit
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline._scalar_commands import capture_track_set
from astrid.sdk.timeline_elements import update_parent_element
from tests.helpers.runtime import use_runtime, vendored_runtime_commit
from tests.sdk import test_timeline_selected_schema_runtime as selected_schema

REF = selected_schema.REF
inverse = selected_schema.inverse
configured_project_pack = selected_schema.configured_project_pack
retained_pack = selected_schema.retained_pack

pytestmark = pytest.mark.integration
use_runtime(commit=vendored_runtime_commit())


def owner_for(case, monkeypatch):
    class Documents:
        def _identity(self):
            return {'realm_id': 'realm'}

        def show(self, document, *, project):
            return DomainResult.success(case.service.get_document(project, document))

    monkeypatch.setattr('astrid.sdk.timeline_elements.Documents', lambda client: Documents())

    def opened(project, timeline):
        head = case.head()
        return DomainResult.success({'project_id': project, 'timeline_id': timeline,
            'bundle': case.bundle(), 'revision_id': head['revision_id'],
            'head_revision_id': head['revision_id']})

    requests = []

    def submit(project, timeline, body, *, idempotency_key):
        requests.append(copy.deepcopy(body))
        result = case.submit(body, idempotency_key)
        return DomainResult.success(result['data'], receipt=CommandReceipt.from_dict(result['receipt']),
                                    idempotency_key=idempotency_key)

    owner = SimpleNamespace(_client=None, open_bundle=opened,
        history=lambda *args, **kwargs: DomainResult.success({'head': case.head()}), commit=submit)
    return owner, requests


@pytest.mark.parametrize('same_revision', [False, True])
def test_native_element_update_reload_guarded_inverse_and_exact_retry(retained_pack, monkeypatch,
                                                                     same_revision):
    from runtime_protocol.errors import RuntimeErrorBase
    from runtime_protocol.service import RuntimeService

    case = retained_pack
    original = copy.deepcopy(case.bundle()['source_mapping']['_runtime_document'])
    before = copy.deepcopy(State(case.bundle()).entity(REF))
    selected = case.selected
    if not same_revision:
        case.definition['schema']['properties']['seed']['maximum'] = 20
        case.path.write_text(yaml.safe_dump(case.definition))
        admitted = packs.admit_project_pack('realm', case.project)
        selected = {key: admitted['elements'][0]['descriptor'][key]
                    for key in ('id', 'kind', 'packId', 'revision')}
        assert selected['revision'] != before['elementRef']['revision']
    # Source and build-cache availability never establish save-time authority.
    shutil.rmtree(case.source_root)
    shutil.rmtree(case.artifact_root)

    def forbidden(*args, **kwargs):
        raise AssertionError('element save used launcher, local source, cache, or renderer')

    monkeypatch.setattr(packs, '_open_client', forbidden)
    monkeypatch.setattr(packs, 'resolve_admitted_element', forbidden)
    monkeypatch.setattr(packs, 'artifact_root', forbidden)
    monkeypatch.setattr(packs, 'authoring_root', forbidden)
    owner, requests = owner_for(case, monkeypatch)
    result = update_parent_element(owner, case.project, 'film', realm='realm', clip_id='effect',
        element=selected, expected_head=case.head()['revision_id'], duration=6,
        params={'seed': 8 if same_revision else 16, 'opaque': {'keep': [None, False, {}]}},
        idempotency_key='native-element-update')
    assert result.ok, result.error
    accepted = case.submit(requests[0], 'native-element-update')
    document = accepted['data']['canonical_document']
    row = State(commit.bundle_from_document(document)).entity(REF)
    assert result.data['new_head'] == accepted['data']['accepted_revision_id']
    assert result.receipt.as_dict() == accepted['receipt']
    assert result.data['before'] == {'element': before['elementRef'], 'duration': before['hold'],
                                     'params': before['params']}
    assert row['elementRef'] == selected and row['hold'] == 6
    assert row['params'] == {**before['params'], **result.data['params']}
    assert row['params']['future'] == before['params']['future']
    assert document['shot_revisions'] == original['shot_revisions']
    assert document['internal_timeline_revisions'] == original['internal_timeline_revisions']
    case.service.close()
    case.service = RuntimeService(case.root)
    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    assert case.bundle()['source_mapping']['_runtime_document'] == document
    with monkeypatch.context() as retry:
        retry.setattr(commands, 'execute', forbidden)
        assert case.submit(requests[0], 'native-element-update') == accepted
    undone = case.submit(case.request([inverse(result.receipt.receipt_id)]), 'undo-element-update')
    restored = undone['data']['canonical_document']
    assert restored['parent_revision']['payload'] == original['parent_revision']['payload']
    assert restored['shot_revisions'] == original['shot_revisions']
    assert restored['internal_timeline_revisions'] == original['internal_timeline_revisions']
    # The native provider retains immutable schema provenance for redo.
    assert restored['dependency_manifest'] == {
        **original['dependency_manifest'],
        'documents': document['dependency_manifest']['documents']}
    redone = case.submit(case.request([inverse(undone['receipt']['receipt_id'])]), 'redo-element-update')
    assert redone['data']['canonical_document'] == document
    # A newer disjoint label survives the guarded inverse.
    case.submit(case.request([capture_track_set(case.bundle(), 'parent/track:picture',
                                               values={'label': 'Newer'})]), 'newer-label')
    disjoint = case.submit(case.request([inverse(redone['receipt']['receipt_id'])]), 'undo-after-label')
    restored_state = State(commit.bundle_from_document(disjoint['data']['canonical_document']))
    assert restored_state.entity(REF) == before
    assert restored_state.entity('parent/track:picture')['label'] == 'Newer'
    # The redo wrote the same element again; its history edge guards old undo.
    head = case.head()
    with pytest.raises(RuntimeErrorBase) as error:
        case.submit(case.request([inverse(result.receipt.receipt_id)]), 'refuse-element-aba')
    assert error.value.details['reason'] == 'intervening_write'
    assert case.head() == head


@pytest.mark.parametrize('damage', ['params', 'revision'])
def test_native_element_batch_refusal_is_atomic(retained_pack, monkeypatch, damage):
    from runtime_protocol.errors import RuntimeErrorBase

    case = retained_pack
    owner, requests = owner_for(case, monkeypatch)
    original, head = copy.deepcopy(case.bundle()), case.head()
    selected = case.selected if damage == 'params' else {
        **case.selected, 'revision': 'sha256:' + '0' * 64}
    with pytest.raises(RuntimeErrorBase):
        update_parent_element(owner, case.project, 'film', realm='realm', clip_id='effect',
            element=selected, expected_head=head['revision_id'], duration=6,
            params={'seed': 11 if damage == 'params' else 8}, idempotency_key='refused-element')
    assert len(requests) == 1
    assert case.head() == head and case.bundle() == original
