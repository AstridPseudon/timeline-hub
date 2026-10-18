"""Both schema entry points and the distribution derive from one input."""
import copy
import json
import unittest
from pathlib import Path

import jsonschema
from banodoco_timeline_schema import load_schema, validate_timeline
from banodoco_timeline_schema.generated import TimelineClip, AuthoredClipAudio, AudioEnvelope

PKG = Path(__file__).resolve().parents[1]


class AuthoredAudioContract(unittest.TestCase):
    def test_root_standalone_generated_types_and_distribution(self):
        schema = load_schema()
        clip = {"id": "bed", "at": 1, "track": "music", "audio": {"envelope": {
            "keyframes": [{"at": 0.123456789, "value": 2}],
            "multiply": [{"keyframes": [{"at": 0, "value": 0.8}]}],
            "minimum": [{"keyframes": [{"at": 0, "value": 0.25}]}], "duck": True}}}
        config = {"clips": [clip], "tracks": []}
        standalone = {"$ref": "#/definitions/TimelineClip", "definitions": schema["definitions"]}
        distributed = json.loads((PKG / "typescript/dist/timeline.schema.json").read_text())
        jsonschema.Draft7Validator.check_schema(schema)
        validate_timeline(config, strict=True)
        jsonschema.validate(clip, standalone)
        jsonschema.validate(config, distributed)
        self.assertEqual(distributed["definitions"]["TimelineClip"], schema["definitions"]["TimelineClip"])
        self.assertEqual(distributed["definitions"]["TimelineConfig"], {k: v for k, v in schema.items() if k not in {"definitions", "$schema"}})
        for name, definition in schema["definitions"].items():
            self.assertEqual(distributed["definitions"][name], definition)
        self.assertIn("audio", TimelineClip.__annotations__)
        self.assertIn("envelope", AuthoredClipAudio.__annotations__)
        self.assertIn("keyframes", AudioEnvelope.__annotations__)
        for audio in (None, {}, {"envelope": None}, {"envelope": {"keyframes": []}},
                      {"envelope": {"keyframes": [{"at": 0, "value": True}]}},
                      {"envelope": {"keyframes": [{"at": 0, "value": -1}]}},
                      {"envelope": {"keyframes": [{"at": 0, "value": 1}], "duck": 1}},
                      {"envelope": {"keyframes": [{"at": 0, "value": 1, "curve": "nope"}]}},
                      {"envelope": clip["audio"]["envelope"], "render_source": {"file": "https://forged"}}):
            bad = copy.deepcopy(clip)
            bad["audio"] = audio
            with self.subTest(audio=audio):
                for value, entry in ((bad, standalone), ({**config, "clips": [bad]}, schema), ({**config, "clips": [bad]}, distributed)):
                    with self.assertRaises(jsonschema.ValidationError):
                        jsonschema.validate(value, entry)
