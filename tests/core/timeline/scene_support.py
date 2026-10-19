"""Legacy behavior assertions through real native host queries, never private math."""
from unittest.mock import patch

from astrid.core.theme import builtin_theme
from astrid.core.timeline import scene_answers, scene_roles
from astrid.core.timeline.duration import timeline_duration_frames
from astrid.packs.rendering.actions.timeline_visualize.overlays.labels import labels_for


def visible_at(config, frame, fps, canvas, elements):
    with patch.object(scene_roles, "element_coverage", return_value=elements):
        return labels_for(config, frame, fps, canvas, assets={"assets": {}}, theme=builtin_theme())


def coverage(config, fps, canvas, elements, *, start_frame=0, end_frame=None):
    with patch.object(scene_roles, "element_coverage", return_value=elements):
        return scene_answers.coverage({"timeline": config, "assets": {"assets": {}}, "theme": builtin_theme()},
                                      {**canvas, "fps": fps}, start_frame=start_frame,
                                      end_frame=end_frame if end_frame is not None else timeline_duration_frames(config, fps))

# Retained instrumentation in the old complexity regression targets these names.
from astrid.core.timeline.duration import clip_end_frame, clip_start_frame  # noqa: E402, F401
