"""Content identity for asset registry entries.

Two registry entries describe the same media when they name the same content,
whatever else each carries.  Identity is ``media_id``, else ``content_sha256``
(an optional ``sha256:`` prefix is dropped so bare and prefixed digests agree),
else ``file`` for legacy entries.  Decoration such as ``thumbnailUrl``, ``url``,
``url_expires_at``, ``etag``, ``handle``, ``source``, ``pixel_provenance`` or
filenames never makes two entries different.  An entry with no identity at all
can only be compared by full equality.

Render, inspection and (in a later wave) publish share this one rule.
"""

from __future__ import annotations

from collections.abc import Mapping

_SHA_PREFIX = "sha256:"


def _text(value):
    return value.strip() if isinstance(value, str) and value.strip() else None


def asset_identity(entry):
    """Return the ``(kind, value)`` identity of a registry entry, or None."""
    if not isinstance(entry, Mapping):
        return None
    media_id = _text(entry.get("media_id"))
    if media_id:
        return ("media_id", media_id)
    digest = _text(entry.get("content_sha256"))
    if digest:
        if digest.lower().startswith(_SHA_PREFIX):
            digest = digest[len(_SHA_PREFIX):]
        return ("content_sha256", digest.lower())
    file = _text(entry.get("file"))
    if file:
        return ("file", file)
    return None


def same_asset_identity(a, b):
    """Return True when two registry entries name the same media."""
    identity_a, identity_b = asset_identity(a), asset_identity(b)
    if identity_a is None and identity_b is None:
        return a == b
    return identity_a == identity_b
