"""The three declared timeline file routes that can run without Runtime.

Classify parsed operations, not CLI spellings. Unclassified edit-command,
contribution and media paths retain ordinary authenticated acquisition.
"""
from pathlib import Path
import json


def _script_is_local(parsed):
    from astrid.sdk.timeline._timing_evaluators import script_take_folders

    path = Path(parsed.from_script).expanduser()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("a narration script must be an object")
    if "version" in data and "lines" in data:
        return False  # managed take verification/preparation is never offline
    segments = data.get("segments") or []
    if not isinstance(segments, list) or any(not isinstance(item, dict) for item in segments):
        raise ValueError("script segments must be an array of objects")
    folders = script_take_folders(path, parsed.takes)
    # A selected WAV is imported into managed media by apply_script. Even an
    # unchanged take conservatively keeps that operation on authenticated Runtime.
    return not any((folder / f"{item['id']}.wav").is_file()
                   for item in segments if item.get("id")
                   for folder in folders)


def edit_is_local(parsed):
    if any(getattr(parsed, name, None) is not None for name in (
        "command", "add_component", "shape_from", "swap_asset", "replace_asset",
        "add_media", "trim_in", "trim_out", "slip",
    )) or parsed.verify:
        return False
    if parsed.from_script:
        # This edit adapter prepares/generates managed takes without --takes.
        if not parsed.takes or not _script_is_local(parsed):
            return False
    if parsed.beats and parsed.beats.strip().lower() != "keep" and not Path(parsed.beats).expanduser().is_file():
        return False
    media = [value for value in (parsed.take, parsed.picture) if value]
    if media:
        from astrid.sdk.timeline.checkout import Checkout
        tl = Checkout.load(parsed.file)
        keys = {key for sid in tl._shot_ids() for key in tl._registry(sid)}
        if any(value not in keys for value in media):
            return False  # local paths import; handles resolve managed objects
    return True


def lines_is_local(parsed):
    validate_lines_file(parsed)
    return not parsed.from_script or _script_is_local(parsed)


def validate_lines_file(parsed):
    if not getattr(parsed, "file", None):
        return
    if parsed.published or parsed.draft or parsed.ref:
        raise ValueError("lines --file cannot be combined with a timeline, --published or --draft")
    if parsed.from_script:
        data = json.loads(Path(parsed.from_script).expanduser().read_text(encoding="utf-8"))
        if isinstance(data, dict) and "version" in data and "lines" in data:
            raise ValueError("lines --file does not prepare or verify managed takes; use timelines edit --from-script")


def adopt_is_local(parsed):
    return parsed.kind == "music-bed"
