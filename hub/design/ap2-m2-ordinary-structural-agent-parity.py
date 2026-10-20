from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

from astrid.sdk.timeline._clip_commands import capture_clip_add
from astrid.sdk.timeline.capture import capture_clip_delete, capture_track_create
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.rebase import replay

fixture = json.loads(Path(sys.argv[1]).read_text())
document = next(item['document'] for item in fixture['cases'] if item['name'] == 'parent-only')
bundle = bundle_from_document(document)
track = capture_track_create(bundle, 'parent', {
    'id': 'ordinary-track', 'kind': 'visual', 'role': 'output', 'opaque': {'keep': [None, False]},
})
after_track = execute(bundle, [track]).bundle
row = {
    'id': 'ordinary-clip', 'clipType': 'text', 'track': 'ordinary-track', 'at': 1.25, 'hold': 2.5,
    'params': {'text': 'Ordinary'}, 'app': {'opaque': {'keep': [None, False]}}, 'nullable': None,
}
add = capture_clip_add(after_track, 'parent', row)
added_plan = execute(bundle, [track, add])
delete = capture_clip_delete(added_plan.bundle, 'parent/clip:ordinary-clip')
delete_plan = execute(added_plan.bundle, [delete])
replayed = replay(added_plan, bundle)
delete_replayed = replay(delete_plan, added_plan.bundle)
json.dump({
    'add': {'commands': added_plan.commands, 'records': added_plan.records, 'bundle': added_plan.bundle},
    'delete': {'commands': delete_plan.commands, 'records': delete_plan.records, 'bundle': delete_plan.bundle},
    'replay': {'records': replayed.records, 'bundle': replayed.bundle},
    'deleteReplay': {'records': delete_replayed.records, 'bundle': delete_replayed.bundle},
}, sys.stdout, separators=(',', ':'))
