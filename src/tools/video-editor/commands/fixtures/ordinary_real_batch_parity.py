"""Compare the exported real ordinary App batch with native Agent capture.

Run ordinaryRealBatch.test.ts with ORDINARY_CAPTURE_OUTPUT=/absolute/output.json,
then run this file with that output argument and the exact Agent on PYTHONPATH.
No Runtime, renderer, browser or socket is started.
"""
import copy
import json
import sys
from pathlib import Path

from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document

data = json.loads(Path(sys.argv[1]).read_text())
original = data['original']
document = original['source_mapping']['_runtime_document']
assert bundle_from_document(document) == original, 'App/SDK opening differs'
before = copy.deepcopy(original)
claims = {'resolved', 'expect', 'authorship', 'reads', 'selections', 'bindings', 'created'}
bare = [{key: value for key, value in command.items() if key not in claims}
        for command in data['commands']]
native = execute(original, bare)
assert len(native.records) == len(data['commands']) == 10
for ordinal, (command, record) in enumerate(zip(data['commands'], native.records)):
    assert command == record['command'], (ordinal, command['select'], 'command')
    assert data['records'][ordinal] == record, (ordinal, command['select'], 'record')
assert data['bundle'] == native.bundle, 'final authored bundle'
verified = execute(original, data['commands'])
assert verified.records == native.records
assert original == before, 'atomic execution mutated its input'
print('10/10 exact native commands and records; opening, final bundle, original basis verified')
