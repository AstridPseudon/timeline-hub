import json

from astrid.core.timeline.banodoco_composer import Timeline
from astrid.core.timeline.duration import clip_start_frame

raw = {
    'tracks': [{'id': 'A1', 'kind': 'audio', 'label': 'Audio'}],
    'clips': [{'id': 'phase', 'track': 'A1', 'asset': 'sound', 'at': 0.016682,
               'from': 0.051, 'to': 3.051, 'speed': 1.5,
               'params': {'fadeIn': 0.2, 'fadeInCurve': 'equal-power'}}],
}
rendered = Timeline.from_json_data(raw).for_render().to_json_data()
fps = 30000 / 1001
print(json.dumps({'original_at': raw['clips'][0]['at'], 'rendered_at': rendered['clips'][0]['at'],
                  'original_start_frame': clip_start_frame(raw['clips'][0], fps),
                  'rendered_start_frame': clip_start_frame(rendered['clips'][0], fps)}, indent=2))
assert clip_start_frame(rendered['clips'][0], fps) == clip_start_frame(raw['clips'][0], fps)
