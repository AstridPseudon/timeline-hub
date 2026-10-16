"""Runtime validates named dormant asset references within atomic acceptance."""
import copy
import json

import pytest
from test_timeline_accept import fixture, acceptance, IDENTITY  # noqa: F401
from test_selected_media_commit import snapshot
from runtime_protocol.errors import ValidationError
from runtime_protocol.shot_groups import _shape
from runtime_protocol.shot_group_schema import SHOT_GROUP_SCHEMA


def prepared_group(service, project):
    value = acceptance(service, project)
    parent = value['publication']['parent_composition']
    parent['clips'] = [dict(id='v',clipType='media',track='V',at=0,hold=1,params={})]
    parent['config']['pinnedShotGroups'] = [dict(shotId='logical-shot',trackId='V',clipIds=['v'],memberSelectors=['parent/clip:v'],mode='video',name='Name',poolGenerationIds=['g'],derivedFrom=None,opaque={'retain':None})]
    return value


@pytest.mark.parametrize('field', ['videoAssetKey', 'assetKey'])
def test_invalid_nested_dependencies_roll_back_every_row(fixture,field):
    s,p=fixture
    value=prepared_group(s,p)
    row=value['publication']['parent_composition']['config']['pinnedShotGroups'][0]
    if field=='videoAssetKey':row[field]='missing'
    else:row['imageClipSnapshot']=[dict(assetKey='missing')]
    before=snapshot(s)
    with pytest.raises(ValidationError,match='missing assetKey/videoAssetKey'):
        s.accept(value,identity=IDENTITY)
    assert snapshot(s)==before


def test_valid_dormant_only_media_retained_in_immutable_dependency_rows(fixture):
    s,p=fixture
    media=s.ingest(p,b'dormant-fixture',media_type='image/png',original_name='image.png',idempotency_key='image')['data']['object_id']
    value=prepared_group(s,p)
    parent=value['publication']['parent_composition']
    parent['registry']={'assets':{'image':{'media_id':media}}}
    parent['config']['pinnedShotGroups'][0]['imageClipSnapshot']=[dict(assetKey='image')]
    result=s.accept(value,identity=IDENTITY)['stored_result']
    refs=s.store.conn.execute("SELECT dependency_id FROM composition_revision_dependencies WHERE parent_revision_id=? AND dependency_kind='media'",(result['accepted_revision_id'],)).fetchall()
    assert media in {row[0] for row in refs}
    assert s.accept(value,identity=IDENTITY)['stored_result']==result


@pytest.mark.parametrize('mutate', [lambda r:r.update(clipIds=['v','v']),lambda r:r.update(name=None),lambda r:r.update(memberSelectors=['bare']),lambda r:r.update(mode='arbitrary'),lambda r:r.update(poolGenerationIds='g'),lambda r:r.update(imageClipSnapshot=[{'authoring':{'selector':'x','clip':{},'order':[]}}])])
def test_stored_schema_shape_parity_and_atomic_rejection(fixture,mutate):
    import jsonschema
    s,p=fixture
    value=prepared_group(s,p)
    row=value['publication']['parent_composition']['config']['pinnedShotGroups'][0]
    mutate(row)
    assert not _shape(row,SHOT_GROUP_SCHEMA)
    assert list(jsonschema.Draft202012Validator(SHOT_GROUP_SCHEMA).iter_errors(row))
    before=snapshot(s)
    with pytest.raises(ValidationError):s.accept(value,identity=IDENTITY)
    assert snapshot(s)==before


def test_valid_unknown_fields_and_duplicate_group_key_validation(fixture):
    s,p=fixture
    value=prepared_group(s,p)
    row=value['publication']['parent_composition']['config']['pinnedShotGroups'][0]
    assert _shape(row,SHOT_GROUP_SCHEMA)
    value['publication']['parent_composition']['config']['pinnedShotGroups'].append(copy.deepcopy(row))
    before=snapshot(s)
    with pytest.raises(ValidationError,match='duplicate'):s.accept(value,identity=IDENTITY)
    assert snapshot(s)==before
