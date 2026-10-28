"""Best-effort publication of the local skills inventory to Runtime app-state."""

from __future__ import annotations

import hashlib
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from astrid.core.foundation.paths import REPO_ROOT

APP_STATE_LIMIT = 15 * 1024
PUBLISH_TIMEOUT = 8.0
APP_STATE_PREFIX = "astrid.skills."


def app_state_key(package_root: str | Path = REPO_ROOT) -> str:
    """Return the app-state key bound to this real package installation."""
    root = str(Path(package_root).resolve())
    install_id = hashlib.sha256(root.encode("utf-8")).hexdigest()[:12]
    return APP_STATE_PREFIX + install_id


def _value(resource: Any, name: str) -> Any:
    if isinstance(resource, Mapping):
        return resource.get(name)
    return getattr(resource, name, None)


def _pending(reason: str) -> dict[str, str]:
    return {"status": "pending", "reason": reason}


def _error_status(exc: Exception) -> str:
    code = str(getattr(exc, "code", ""))
    status = getattr(exc, "status", None)
    if code == "protocol_error" or code in {"invalid_response", "not_ready"}:
        return "protocol_error"
    if status == 409 or code in {"version_conflict", "conflict"}:
        return "version_conflict"
    return "unavailable"


def publish(
    *,
    package_root: str | Path = REPO_ROOT,
    state_file: str | Path | None = None,
    client_factory: Any | None = None,
    timeout: float = PUBLISH_TIMEOUT,
) -> dict[str, str]:
    """Publish the local inventory without changing command success or local state."""
    from .state import state_path

    root = Path(package_root).resolve()
    local_state_path = Path(state_file) if state_file is not None else state_path()
    try:
        local_state = json.loads(local_state_path.read_text(encoding="utf-8"))
        harnesses = local_state["skills"]
        if not isinstance(harnesses, dict):
            raise ValueError("skills inventory must be an object")
    except (OSError, ValueError, KeyError, TypeError):
        return _pending("unavailable")

    key = app_state_key(root)
    content = {
        "format": "astrid.skills.v1",
        "install": {
            "id": key.removeprefix(APP_STATE_PREFIX),
            "package_root": str(root),
            "state_path": str(local_state_path),
        },
        "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "harnesses": harnesses,
    }
    encoded = json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if len(encoded) > APP_STATE_LIMIT:
        return {"status": "too_large"}

    if client_factory is None:
        from astrid.sdk import AstridClient

        client_factory = AstridClient.open_existing_from_launcher

    outcome: list[dict[str, str]] = []

    def perform() -> None:
        try:
            with client_factory() as client:
                transport = client._remote._transport
                current = transport.get_user_app_state(key)
                version = _value(current, "version")
                if type(version) is not int or version < 0:
                    outcome.append(_pending("protocol_error"))
                    return
                idempotency_key = hashlib.sha256(encoded + str(version).encode("ascii")).hexdigest()
                transport.update_user_app_state(
                    key,
                    content,
                    expected_version=version,
                    idempotency_key=idempotency_key,
                )
            outcome.append({"status": "published"})
        except Exception as exc:  # noqa: BLE001 - publication never changes the local command result
            outcome.append(_pending(_error_status(exc)))

    worker = threading.Thread(target=perform, name="astrid-skills-publish", daemon=True)
    worker.start()
    worker.join(timeout=max(0.0, timeout))
    if worker.is_alive():
        return _pending("timeout")
    return outcome[0] if outcome else _pending("unavailable")


__all__ = ["APP_STATE_LIMIT", "APP_STATE_PREFIX", "PUBLISH_TIMEOUT", "app_state_key", "publish"]
