from __future__ import annotations

import copy
import json
from pathlib import Path

from tests.editing_conformance.fixture_loader import load_fixture


FIXTURES = Path(__file__).parent / 'fixtures'


def test_record_restoration_does_not_rewrite_opaque_input_payload(tmp_path):
    source = json.loads((FIXTURES / 'recipe_m2_clip_add.json').read_text())
    opaque = {
        'records': [{
            'command': {'created': ['authored'], 'reads': ['authored']},
            'reads': ['authored'],
        }],
    }
    source['input']['parent_revision']['payload']['opaque'] = copy.deepcopy(opaque)
    fixture = tmp_path / 'recipe_m2_clip_add.json'
    fixture.write_text(json.dumps(source))

    loaded = load_fixture(fixture)

    assert loaded['input']['parent_revision']['payload']['opaque'] == opaque
