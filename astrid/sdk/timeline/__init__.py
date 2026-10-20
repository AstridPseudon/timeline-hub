"""Modular API over the timeline working-copy implementation."""
__all__ = ["Checkout", "Clip", "Cut", "Word", "Voice", "TimelineEditError", "EDITABLE_NOTE",
           "draft_path", "drafts_root", "find_draft", "resolve_ids",
           "capture_assembled_media", "capture_clip_add_media", "capture_clip_replace_media",
           "capture_parent_completion"]


def __getattr__(name):
    if name in ('capture_assembled_media', 'capture_clip_add_media', 'capture_clip_replace_media',
                'capture_parent_completion'):
        from . import native_parent_media_commands
        return getattr(native_parent_media_commands, name)
    from astrid.sdk import timeline_checkout as legacy
    if name in __all__:
        return getattr(legacy, name)
    raise AttributeError(name)
