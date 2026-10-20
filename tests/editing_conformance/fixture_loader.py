"""Load compact conformance fixtures without changing their test-facing shape."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


def load_fixture(path: str | Path) -> Any:
    """Load a fixture and restore only the compact forms used by M2 recipes."""
    path = Path(path)
    fixture = json.loads(path.read_text(encoding='utf-8'))
    _restore_record_fields(fixture)

    if path.name == 'recipe_m2_placement.json':
        shared_input = fixture.pop('input', None)
        if shared_input is not None:
            for case in fixture['cases']:
                case['input'] = copy.deepcopy(shared_input)
    elif path.name == 'recipe_m2_occurrence_media.json':
        shared_input = fixture.pop('input', None)
        shared_verified_media = fixture.pop('verified_media', None)
        for operation in fixture.values():
            if shared_input is not None:
                operation['input'] = copy.deepcopy(shared_input)
            if shared_verified_media is not None:
                operation['verified_media'] = copy.deepcopy(shared_verified_media)
    elif path.name == 'recipe_m2_placement_create_unplace.json':
        if 'input' not in fixture['unplace']:
            fixture['unplace']['input'] = copy.deepcopy(fixture['create']['output'])

    return fixture


def _restore_record_fields(value: Any) -> None:
    if isinstance(value, dict):
        records = value.get('records')
        if isinstance(records, list):
            for record in records:
                if not isinstance(record, dict) or not isinstance(record.get('command'), dict):
                    continue
                command = record['command']
                for key in ('created', 'reads', 'selections'):
                    if key not in record and key in command:
                        record[key] = copy.deepcopy(command[key])
        for child in value.values():
            _restore_record_fields(child)
    elif isinstance(value, list):
        for child in value:
            _restore_record_fields(child)
